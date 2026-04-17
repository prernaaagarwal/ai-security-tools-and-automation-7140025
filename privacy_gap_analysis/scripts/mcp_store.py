"""SQLite-backed in-process store for MCP audit-trail and feedback data.

Mirrors the storage model of `privacy_mcp_server.py` (memory / confidence /
feedback / token-usage / gap-analysis) but as a plain importable module — no
HTTP server required. Used by the Streamlit web UI so analyses and ratings
are captured without standing up a separate process.

Data lives in a single SQLite file (default: `./mcp_store/audit_trail.sqlite`,
relative to CWD; override with `MCP_STORE_PATH`). SQLite handles concurrent
writes from multiple Streamlit sessions via WAL mode and short transactions.

Note: on Streamlit Community Cloud the filesystem is ephemeral — data is
preserved across reruns and restarts within the same container lifecycle, but
lost when the container is rebuilt. For durable cross-restart storage, point
`MCP_STORE_PATH` at a mounted volume or swap this module for a managed DB.
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

_PROCESS_LOCK = threading.Lock()
_CONN: sqlite3.Connection | None = None
_CONN_PATH: Path | None = None


def _store_path() -> Path:
    env = os.environ.get("MCP_STORE_PATH")
    if env:
        return Path(env)
    return Path.cwd() / "mcp_store" / "audit_trail.sqlite"


def _connect() -> sqlite3.Connection:
    global _CONN, _CONN_PATH
    path = _store_path()
    if _CONN is not None and _CONN_PATH == path:
        return _CONN

    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _init_schema(conn)

    _CONN = conn
    _CONN_PATH = path
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_memory_session ON memory(session_id);

        CREATE TABLE IF NOT EXISTS confidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT,
            response TEXT,
            confidence_score REAL,
            is_high_confidence INTEGER,
            is_low_confidence INTEGER,
            extras TEXT
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT,
            question TEXT,
            rating TEXT,
            numeric_rating REAL,
            comments TEXT,
            company TEXT,
            framework TEXT,
            extras TEXT
        );

        CREATE TABLE IF NOT EXISTS token_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT,
            model_used TEXT,
            tokens_prompt INTEGER,
            tokens_completion INTEGER,
            tokens_total INTEGER,
            extras TEXT
        );

        CREATE TABLE IF NOT EXISTS gap_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT,
            company TEXT,
            priority_level TEXT,
            gaps_json TEXT,
            recommendations_json TEXT,
            extras TEXT
        );
        """
    )


@contextmanager
def _tx():
    with _PROCESS_LOCK:
        conn = _connect()
        try:
            conn.execute("BEGIN")
            yield conn
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _split_extras(known: Iterable[str], kwargs: dict) -> tuple[dict, str]:
    known_set = set(known)
    extras = {k: v for k, v in kwargs.items() if k not in known_set}
    return kwargs, json.dumps(extras, default=str) if extras else "{}"


# ---------------------------------------------------------------------------
# Writers — match the MCPClient signatures used by privacy_rag_mcp.py
# ---------------------------------------------------------------------------
def insert_memory(session_id: str | None = None, text: str | None = None, **kwargs) -> None:
    payload = {"text": text, **kwargs}
    if session_id is not None:
        payload["session_id"] = session_id
    sid = payload.get("session_id") or "unknown"
    with _tx() as conn:
        conn.execute(
            "INSERT INTO memory (session_id, timestamp, payload) VALUES (?, ?, ?)",
            (sid, _now(), json.dumps(payload, default=str)),
        )


def fetch_memory(session_id: str) -> list[dict]:
    conn = _connect()
    rows = conn.execute(
        "SELECT timestamp, payload FROM memory WHERE session_id = ? ORDER BY id",
        (session_id,),
    ).fetchall()
    results = []
    for r in rows:
        try:
            payload = json.loads(r["payload"])
        except Exception:
            payload = {}
        results.append({"timestamp": r["timestamp"], **payload})
    return results


def insert_confidence(query: str = "", response: str = "", score: float = 0.0, **kwargs) -> None:
    _, extras = _split_extras(
        {"query", "response", "score", "is_high_confidence", "is_low_confidence"}, kwargs
    )
    with _tx() as conn:
        conn.execute(
            """
            INSERT INTO confidence
                (timestamp, query, response, confidence_score,
                 is_high_confidence, is_low_confidence, extras)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (_now(), query, response, float(score), int(score > 0.8), int(score < 0.4), extras),
        )


def insert_feedback(
    session_id: str = "",
    question: str = "",
    rating: Any = None,
    **kwargs,
) -> None:
    known = {"session_id", "question", "rating", "numeric_rating", "comments", "company", "framework"}
    _, extras = _split_extras(known, kwargs)
    numeric = kwargs.get("numeric_rating")
    if numeric is None and isinstance(rating, (int, float)):
        numeric = float(rating)
    with _tx() as conn:
        conn.execute(
            """
            INSERT INTO feedback
                (timestamp, session_id, question, rating, numeric_rating,
                 comments, company, framework, extras)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _now(),
                session_id,
                question,
                str(rating) if rating is not None else None,
                float(numeric) if numeric is not None else None,
                kwargs.get("comments"),
                kwargs.get("company"),
                kwargs.get("framework"),
                extras,
            ),
        )


def insert_token_usage(
    query: str = "",
    model: str = "",
    tp: int = 0,
    tc: int = 0,
    total: int = 0,
    **kwargs,
) -> None:
    known = {"query", "model", "model_used", "tp", "tc", "total",
             "tokens_prompt", "tokens_completion", "tokens_total"}
    _, extras = _split_extras(known, kwargs)
    model_used = kwargs.get("model_used", model)
    with _tx() as conn:
        conn.execute(
            """
            INSERT INTO token_usage
                (timestamp, query, model_used, tokens_prompt, tokens_completion,
                 tokens_total, extras)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (_now(), query, model_used, int(tp), int(tc), int(total), extras),
        )


def insert_gap_analysis(
    session_id: str = "",
    company: str = "",
    gaps: list | None = None,
    recommendations: list | None = None,
    priority_level: str = "Medium",
    **kwargs,
) -> None:
    known = {"session_id", "company", "gaps", "recommendations", "priority_level"}
    _, extras = _split_extras(known, kwargs)
    with _tx() as conn:
        conn.execute(
            """
            INSERT INTO gap_analyses
                (timestamp, session_id, company, priority_level,
                 gaps_json, recommendations_json, extras)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _now(),
                session_id,
                company,
                priority_level,
                json.dumps(gaps or [], default=str),
                json.dumps(recommendations or [], default=str),
                extras,
            ),
        )


# ---------------------------------------------------------------------------
# Readers (for dashboards)
# ---------------------------------------------------------------------------
def _rows_to_dicts(rows) -> list[dict]:
    return [dict(r) for r in rows]


def list_gap_analyses() -> list[dict]:
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM gap_analyses ORDER BY id DESC"
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["gaps"] = json.loads(d.pop("gaps_json") or "[]")
        d["recommendations"] = json.loads(d.pop("recommendations_json") or "[]")
        out.append(d)
    return out


def list_feedback() -> list[dict]:
    conn = _connect()
    rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
    return _rows_to_dicts(rows)


def list_confidence() -> list[dict]:
    conn = _connect()
    rows = conn.execute("SELECT * FROM confidence ORDER BY id DESC").fetchall()
    return _rows_to_dicts(rows)


def list_token_usage() -> list[dict]:
    conn = _connect()
    rows = conn.execute("SELECT * FROM token_usage ORDER BY id DESC").fetchall()
    return _rows_to_dicts(rows)


def list_memory_sessions() -> list[str]:
    conn = _connect()
    rows = conn.execute(
        "SELECT DISTINCT session_id FROM memory ORDER BY session_id"
    ).fetchall()
    return [r["session_id"] for r in rows]


def get_stats() -> dict:
    conn = _connect()
    total_sessions = conn.execute(
        "SELECT COUNT(DISTINCT session_id) AS c FROM memory"
    ).fetchone()["c"]
    total_analyses = conn.execute(
        "SELECT COUNT(*) AS c FROM gap_analyses"
    ).fetchone()["c"]
    total_feedback = conn.execute(
        "SELECT COUNT(*) AS c FROM feedback"
    ).fetchone()["c"]
    total_token_logs = conn.execute(
        "SELECT COUNT(*) AS c FROM token_usage"
    ).fetchone()["c"]
    tokens_total = conn.execute(
        "SELECT COALESCE(SUM(tokens_total), 0) AS s FROM token_usage"
    ).fetchone()["s"]
    avg_rating = conn.execute(
        "SELECT AVG(numeric_rating) AS a FROM feedback WHERE numeric_rating IS NOT NULL"
    ).fetchone()["a"]
    avg_confidence = conn.execute(
        "SELECT AVG(confidence_score) AS a FROM confidence"
    ).fetchone()["a"]
    return {
        "total_sessions": int(total_sessions or 0),
        "total_analyses": int(total_analyses or 0),
        "total_feedback": int(total_feedback or 0),
        "total_token_logs": int(total_token_logs or 0),
        "total_tokens_used": int(tokens_total or 0),
        "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
        "avg_confidence": round(avg_confidence, 2) if avg_confidence is not None else None,
        "store_path": str(_store_path()),
    }


def reset() -> None:
    """Delete all stored data (used for tests / dashboard clear button)."""
    with _tx() as conn:
        for table in ("memory", "confidence", "feedback", "token_usage", "gap_analyses"):
            conn.execute(f"DELETE FROM {table}")
