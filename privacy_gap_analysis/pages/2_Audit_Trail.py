"""Audit Trail + Feedback dashboard.

Reads the JSON store populated by the Gap Analysis page (via `mcp_store`) and
renders:
- Summary stats
- Table of all analyses (company, framework, session, gaps, tokens)
- Feedback ratings
- Confidence scores per analysis
- Raw token-usage log

This is the "feedback dashboard" equivalent of `scripts/view_feedback.py`,
surfaced in the browser.
"""

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = APP_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import mcp_store  # noqa: E402


st.set_page_config(page_title="Audit Trail", page_icon="📊", layout="wide")

st.title("📊 Audit Trail & Feedback")
st.caption(
    "Every analysis is logged here automatically, along with any star ratings "
    "you leave on the Gap Analysis page."
)


# ---------------------------------------------------------------------------
# Sidebar — controls
# ---------------------------------------------------------------------------
if st.sidebar.button("🔄 Refresh"):
    st.rerun()

with st.sidebar.expander("⚠️ Danger zone"):
    confirm = st.text_input("Type CLEAR to erase all logs")
    if st.button("Clear audit trail", disabled=confirm != "CLEAR"):
        mcp_store.reset()
        st.sidebar.success("Cleared.")
        st.rerun()


# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------
stats = mcp_store.get_stats()

cols = st.columns(5)
cols[0].metric("Sessions", stats["total_sessions"])
cols[1].metric("Analyses", stats["total_analyses"])
cols[2].metric("Feedback entries", stats["total_feedback"])
cols[3].metric(
    "Avg rating",
    f"{stats['avg_rating']:.2f}" if stats["avg_rating"] is not None else "—",
)
cols[4].metric(
    "Tokens used",
    f"{stats['total_tokens_used']:,}" if stats["total_tokens_used"] else "0",
)

st.caption(f"Store file: `{stats['store_path']}`")


analyses = mcp_store.list_gap_analyses()
feedback = mcp_store.list_feedback()
confidence = mcp_store.list_confidence()
token_usage = mcp_store.list_token_usage()


if not (analyses or feedback or confidence or token_usage):
    st.info(
        "No data yet. Go run a **Gap Analysis** and this dashboard will "
        "populate automatically."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Analyses table
# ---------------------------------------------------------------------------
st.markdown("## Analyses")
if analyses:
    analyses_rows = [
        {
            "timestamp": a.get("timestamp"),
            "company": a.get("company"),
            "priority": a.get("priority_level"),
            "gaps_found": len(a.get("gaps") or []),
            "recommendations": len(a.get("recommendations") or []),
            "session_id": a.get("session_id"),
        }
        for a in reversed(analyses)
    ]
    st.dataframe(analyses_rows, use_container_width=True, hide_index=True)
else:
    st.info("No analyses logged yet.")


# ---------------------------------------------------------------------------
# Feedback table
# ---------------------------------------------------------------------------
st.markdown("## Feedback")
if feedback:
    fb_rows = [
        {
            "timestamp": f.get("timestamp"),
            "company": f.get("company"),
            "framework": f.get("framework"),
            "rating": f.get("numeric_rating") or f.get("rating"),
            "comments": (f.get("comments") or "")[:120],
            "session_id": f.get("session_id"),
        }
        for f in reversed(feedback)
    ]
    st.dataframe(fb_rows, use_container_width=True, hide_index=True)
else:
    st.info("No feedback submitted yet. Rate an analysis on the Gap Analysis page.")


# ---------------------------------------------------------------------------
# Confidence scores
# ---------------------------------------------------------------------------
st.markdown("## Confidence scores")
if confidence:
    conf_rows = [
        {
            "timestamp": c.get("timestamp"),
            "query": (c.get("query") or "")[:90],
            "confidence_score": c.get("confidence_score"),
            "band": "high" if c.get("is_high_confidence") else ("low" if c.get("is_low_confidence") else "mid"),
        }
        for c in reversed(confidence)
    ]
    st.dataframe(conf_rows, use_container_width=True, hide_index=True)
else:
    st.info("No confidence scores logged yet.")


# ---------------------------------------------------------------------------
# Token usage
# ---------------------------------------------------------------------------
st.markdown("## Token usage")
if token_usage:
    tu_rows = [
        {
            "timestamp": t.get("timestamp"),
            "query": (t.get("query") or "")[:90],
            "model": t.get("model_used"),
            "prompt": t.get("tokens_prompt"),
            "completion": t.get("tokens_completion"),
            "total": t.get("tokens_total"),
        }
        for t in reversed(token_usage)
    ]
    st.dataframe(tu_rows, use_container_width=True, hide_index=True)
else:
    st.info("No token usage logged yet.")
