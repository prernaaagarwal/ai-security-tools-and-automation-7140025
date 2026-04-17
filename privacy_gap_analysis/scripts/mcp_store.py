"""JSON-persistent in-process store for MCP audit-trail and feedback data.

Mirrors the storage model of `privacy_mcp_server.py` (memory / confidence /
feedback / token-usage / gap-analysis lists) but as a plain importable module —
no HTTP server required. Used by the Streamlit web UI so analyses and ratings
are captured without standing up a separate process.

Data lives in a single JSON file (default: `./mcp_store/audit_trail.json`,
relative to CWD). Writes are serialised with a process-local lock plus a file
lock (fcntl on POSIX) so concurrent Streamlit sessions don't corrupt the file.

Note: on Streamlit Community Cloud the filesystem is ephemeral — data is
preserved across reruns in the same session but lost when the container
restarts. For durable multi-user storage, back this module with SQLite or a
managed DB.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import fcntl  # POSIX only

    _HAS_FCNTL = True
except ImportError:  # pragma: no cover — Windows fallback
    _HAS_FCNTL = False


_DEFAULT_SCHEMA = {
    "memory": {},
    "confidence": [],
    "feedback": [],
    "token_usage": [],
    "gap_analyses": [],
}

_PROCESS_LOCK = threading.Lock()


def _store_path() -> Path:
    env = os.environ.get("MCP_STORE_PATH")
    if env:
        return Path(env)
    return Path.cwd() / "mcp_store" / "audit_trail.json"


def _load() -> dict:
    path = _store_path()
    if not path.exists():
        return json.loads(json.dumps(_DEFAULT_SCHEMA))  # deep copy
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return json.loads(json.dumps(_DEFAULT_SCHEMA))
    # Ensure every key is present for older files
    for key, default in _DEFAULT_SCHEMA.items():
        data.setdefault(key, default if not isinstance(default, (dict, list)) else type(default)())
    return data


def _save(data: dict) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        if _HAS_FCNTL:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(data, f, indent=2, default=str)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def _mutate(fn):
    """Load-modify-save under both a thread lock and a file lock."""
    with _PROCESS_LOCK:
        data = _load()
        result = fn(data)
        _save(data)
        return result


# ---------------------------------------------------------------------------
# Writers — match the MCPClient signatures used by privacy_rag_mcp.py
# ---------------------------------------------------------------------------
def insert_memory(session_id: str | None = None, text: str | None = None, **kwargs) -> None:
    payload = kwargs
    if session_id is not None:
        payload["session_id"] = session_id
    if text is not None:
        payload["text"] = text
    sid = payload.get("session_id") or "unknown"
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        **payload,
    }

    def apply(data):
        data["memory"].setdefault(sid, []).append(entry)

    _mutate(apply)


def fetch_memory(session_id: str) -> list:
    return _load()["memory"].get(session_id, [])


def insert_confidence(
    query: str = "",
    response: str = "",
    score: float = 0.0,
    **kwargs,
) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "response": response,
        "confidence_score": float(score),
        "is_high_confidence": score > 0.8,
        "is_low_confidence": score < 0.4,
        **kwargs,
    }

    def apply(data):
        data["confidence"].append(entry)

    _mutate(apply)


def insert_feedback(
    session_id: str = "",
    question: str = "",
    rating: Any = None,
    **kwargs,
) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "question": question,
        "rating": rating,
        **kwargs,
    }

    def apply(data):
        data["feedback"].append(entry)

    _mutate(apply)


def insert_token_usage(
    query: str = "",
    model: str = "",
    tp: int = 0,
    tc: int = 0,
    total: int = 0,
    **kwargs,
) -> None:
    model_used = kwargs.pop("model_used", model)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "model_used": model_used,
        "tokens_prompt": int(tp),
        "tokens_completion": int(tc),
        "tokens_total": int(total),
        **kwargs,
    }

    def apply(data):
        data["token_usage"].append(entry)

    _mutate(apply)


def insert_gap_analysis(
    session_id: str = "",
    company: str = "",
    gaps: list | None = None,
    recommendations: list | None = None,
    priority_level: str = "Medium",
    **kwargs,
) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "company": company,
        "gaps": gaps or [],
        "recommendations": recommendations or [],
        "priority_level": priority_level,
        **kwargs,
    }

    def apply(data):
        data["gap_analyses"].append(entry)

    _mutate(apply)


# ---------------------------------------------------------------------------
# Readers (for dashboards)
# ---------------------------------------------------------------------------
def list_gap_analyses() -> list:
    return list(_load()["gap_analyses"])


def list_feedback() -> list:
    return list(_load()["feedback"])


def list_confidence() -> list:
    return list(_load()["confidence"])


def list_token_usage() -> list:
    return list(_load()["token_usage"])


def list_memory_sessions() -> list[str]:
    return sorted(_load()["memory"].keys())


def get_stats() -> dict:
    data = _load()
    ratings = [
        float(f.get("numeric_rating") or f.get("rating") or 0)
        for f in data["feedback"]
        if isinstance(f.get("numeric_rating") or f.get("rating"), (int, float))
    ]
    confidences = [float(c.get("confidence_score") or 0) for c in data["confidence"]]
    tokens_total = sum(int(t.get("tokens_total") or 0) for t in data["token_usage"])
    return {
        "total_sessions": len(data["memory"]),
        "total_analyses": len(data["gap_analyses"]),
        "total_feedback": len(data["feedback"]),
        "total_token_logs": len(data["token_usage"]),
        "total_tokens_used": tokens_total,
        "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
        "avg_confidence": round(sum(confidences) / len(confidences), 2) if confidences else None,
        "store_path": str(_store_path()),
    }


def reset() -> None:
    """Delete all stored data (used for testing / dashboard clear button)."""

    def apply(data):
        for key, default in _DEFAULT_SCHEMA.items():
            data[key] = type(default)()

    _mutate(apply)
