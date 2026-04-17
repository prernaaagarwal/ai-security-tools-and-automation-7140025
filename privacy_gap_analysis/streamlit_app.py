"""
Streamlit Web UI for the AI Security & Compliance Gap Analysis Tool.

Supports two frameworks:
- **CCPA / CPRA** — scrape a company's privacy policy URL and audit it.
- **NIST CSF 2.0** — paste or upload a security policy and audit it.

Run locally:
    streamlit run streamlit_app.py

Deploy free at https://share.streamlit.io — see DEPLOY.md.
"""

import os
import sys
import traceback
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).parent.resolve()
SCRIPTS_DIR = APP_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Change CWD so the scraper / report generator write into a predictable folder
# and chromadb / downloaded PDFs don't scatter across the filesystem.
os.chdir(APP_DIR)


st.set_page_config(
    page_title="Compliance Gap Analysis",
    page_icon="🔐",
    layout="wide",
)


FRAMEWORK_OPTIONS = {
    "CCPA / CPRA (privacy policy audit)": "CCPA",
    "NIST CSF 2.0 (security policy audit)": "NIST",
}


# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
st.sidebar.title("Gap Analysis")
st.sidebar.caption("AI-powered compliance audit, powered by GPT-4.")

framework_label = st.sidebar.selectbox(
    "Framework",
    list(FRAMEWORK_OPTIONS.keys()),
    index=0,
    help="CCPA/CPRA audits a public privacy policy. NIST CSF 2.0 audits an internal security policy document.",
)
framework_key = FRAMEWORK_OPTIONS[framework_label]

try:
    default_key = st.secrets.get("OPENAI_API_KEY", "")
except Exception:
    default_key = ""
api_key = st.sidebar.text_input(
    "OpenAI API key",
    value=default_key,
    type="password",
    help="Starts with sk-. Not stored. Get one at platform.openai.com.",
)

company_name = st.sidebar.text_input("Company name", value="", placeholder="Acme Corp")

# Framework-specific inputs
homepage_url = ""
policy_text = ""
uploaded_file = None

if framework_key == "CCPA":
    homepage_url = st.sidebar.text_input(
        "Company homepage URL",
        value="",
        placeholder="https://example.com",
        help="The tool will auto-discover the privacy policy and terms pages.",
    )
else:
    uploaded_file = st.sidebar.file_uploader(
        "Security policy document",
        type=["txt", "md"],
        help="Upload a plain-text or Markdown security policy (e.g. an InfoSec Policy).",
    )
    policy_text = st.sidebar.text_area(
        "…or paste the policy here",
        value="",
        height=160,
        help="If you upload a file above, you can skip this.",
    )

st.sidebar.info(
    "Each run costs roughly **$0.20 – $0.80** in OpenAI usage. "
    "Your key is used only for this session — it is not saved."
)

run_clicked = st.sidebar.button("Run analysis", type="primary", use_container_width=True)


# ---------------------------------------------------------------------------
# Main area — header
# ---------------------------------------------------------------------------
st.title("🔐 Compliance Gap Analysis")

if framework_key == "CCPA":
    st.markdown(
        "Paste a company's homepage URL. The tool will scrape its privacy policy, "
        "compare it to **CCPA / CPRA** requirements using retrieval-augmented GPT-4, "
        "and produce a professional audit report you can download."
    )
else:
    st.markdown(
        "Upload or paste an organization's **information security policy**. "
        "The tool compares it to **NIST CSF 2.0** controls using retrieval-augmented "
        "GPT-4 and produces a professional audit report."
    )

if not run_clicked and "result" not in st.session_state:
    st.info(
        "👈 Pick a framework and fill in the sidebar, then click **Run analysis**. "
        "First run takes ~60–90 seconds to warm up."
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _validate_inputs() -> str | None:
    if not api_key.strip():
        return "Please enter your OpenAI API key in the sidebar."
    if not api_key.strip().startswith("sk-"):
        return "That doesn't look like a valid OpenAI key (should start with `sk-`)."

    if framework_key == "CCPA":
        if not homepage_url.strip():
            return "Please enter the company's homepage URL."
        url = homepage_url.strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            return "URL must start with `http://` or `https://`."
    else:
        if not uploaded_file and not policy_text.strip():
            return "Please upload a security policy file or paste the policy text."
    return None


def _wire_mcp_client_to_store(module) -> None:
    """Route the analysis code's MCP calls into the in-process JSON store
    instead of an HTTP server. This gives us an audit trail without having to
    run a separate FastAPI process — important on Streamlit Cloud where we
    can't expose a second port."""
    import mcp_store

    client = getattr(module, "mcp_client", None)
    if client is None:
        return

    client.insert_memory = lambda data: mcp_store.insert_memory(**(data or {}))
    client.fetch_memory = lambda session_id: mcp_store.fetch_memory(session_id)
    client.insert_confidence = mcp_store.insert_confidence
    client.insert_feedback = mcp_store.insert_feedback
    client.insert_token_usage = mcp_store.insert_token_usage

    def _request(method, params):
        fn = {
            "insert_memory": lambda: mcp_store.insert_memory(**(params or {})),
            "insert_confidence": lambda: mcp_store.insert_confidence(**(params or {})),
            "insert_feedback": lambda: mcp_store.insert_feedback(**(params or {})),
            "insert_token_usage": lambda: mcp_store.insert_token_usage(**(params or {})),
            "insert_gap_analysis": lambda: mcp_store.insert_gap_analysis(**(params or {})),
            "fetch_memory": lambda: mcp_store.fetch_memory((params or {}).get("session_id", "")),
        }.get(method)
        return fn() if fn else None

    client.request = _request


def _friendly_error(exc: Exception) -> str:
    try:
        import openai  # lazy
    except Exception:
        openai = None

    if openai is not None:
        if isinstance(exc, getattr(openai, "AuthenticationError", ())):
            return "Invalid OpenAI API key. Double-check the key in the sidebar."
        if isinstance(exc, getattr(openai, "RateLimitError", ())):
            return "OpenAI rate limit or quota exceeded. Try again later or check billing."
        if isinstance(exc, getattr(openai, "APIConnectionError", ())):
            return "Couldn't reach OpenAI. Check your internet connection and try again."

    msg = str(exc) or exc.__class__.__name__
    return f"Something went wrong: {msg}"


def _read_uploaded_text(upload) -> str:
    raw = upload.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")


# ---------------------------------------------------------------------------
# Analysis pipeline
# ---------------------------------------------------------------------------
if run_clicked:
    err = _validate_inputs()
    if err:
        st.error(err)
        st.stop()

    # The RAG module reads OPENAI_API_KEY at import time, so set it BEFORE importing.
    os.environ["OPENAI_API_KEY"] = api_key.strip()

    effective_company = company_name.strip() or "Company"

    with st.status("Running analysis…", expanded=True) as status:
        try:
            st.write("📥 Importing analysis engine…")
            import privacy_rag_mcp  # noqa: E402

            _wire_mcp_client_to_store(privacy_rag_mcp)

            if framework_key == "CCPA":
                from privacy_policy_scraper import scrape_policy_documents  # noqa: E402

                st.write(f"🌐 Scraping policy pages from {homepage_url}…")
                scrape_result = scrape_policy_documents(homepage_url.strip())
                privacy_pdf = scrape_result.get("privacy_policy") if scrape_result else None
                terms_pdf = scrape_result.get("terms_conditions") if scrape_result else None

                if not privacy_pdf and not terms_pdf:
                    status.update(label="No policy found", state="error")
                    st.error(
                        "Couldn't find a privacy policy or terms page at that URL. "
                        "Try a different URL (or link directly to the privacy page)."
                    )
                    st.stop()

                st.write("📚 Loading CCPA/CPRA framework and policy into vector DB… (first run is slow)")
                st.write("🤖 Running GPT-4 gap analysis…")
                result = privacy_rag_mcp.analyze_policy_documents(
                    privacy_pdf_path=privacy_pdf,
                    terms_pdf_path=terms_pdf,
                    company_name=effective_company,
                )
            else:
                # NIST CSF 2.0 flow
                if uploaded_file is not None:
                    resolved_text = _read_uploaded_text(uploaded_file)
                else:
                    resolved_text = policy_text

                st.write(
                    f"📄 Ingesting {len(resolved_text):,} characters of security policy…"
                )
                st.write("📚 Loading NIST CSF 2.0 framework into vector DB… (first run is slow)")
                st.write("🤖 Running GPT-4 gap analysis…")
                result = privacy_rag_mcp.analyze_security_policy_nist(
                    policy_text=resolved_text,
                    company_name=effective_company,
                )

            if not result or not result.get("report_path"):
                status.update(label="Analysis failed", state="error")
                st.error("Analysis completed but no report was produced. Check server logs.")
                st.stop()

            st.write("📝 Generating Markdown, Word, and PDF reports…")
            report_md = Path(result["report_path"]).resolve()
            report_docx = report_md.with_suffix(".docx")
            report_pdf = report_md.with_suffix(".pdf")

            analysis_meta = result.get("analysis") or {}
            st.session_state["result"] = {
                "framework": framework_key,
                "company": effective_company,
                "session_id": analysis_meta.get("session_id"),
                "tokens_used": analysis_meta.get("tokens_used"),
                "md_path": str(report_md),
                "docx_path": str(report_docx) if report_docx.exists() else None,
                "pdf_path": str(report_pdf) if report_pdf.exists() else None,
                "markdown": report_md.read_text(encoding="utf-8"),
            }
            st.session_state.pop("feedback_submitted", None)
            status.update(label="Analysis complete ✅", state="complete")

        except Exception as exc:
            status.update(label="Analysis failed", state="error")
            st.error(_friendly_error(exc))
            with st.expander("Technical details"):
                st.code(traceback.format_exc())
            st.stop()


# ---------------------------------------------------------------------------
# Results — persists across reruns thanks to session_state
# ---------------------------------------------------------------------------
result = st.session_state.get("result")
if result:
    framework_display = "NIST CSF 2.0" if result.get("framework") == "NIST" else "CCPA / CPRA"
    st.success(f"{framework_display} report generated for **{result['company']}**.")

    dl_cols = st.columns(3)
    with dl_cols[0]:
        st.download_button(
            "⬇️ Markdown (.md)",
            data=result["markdown"],
            file_name=Path(result["md_path"]).name,
            mime="text/markdown",
            use_container_width=True,
        )
    with dl_cols[1]:
        if result["docx_path"]:
            with open(result["docx_path"], "rb") as f:
                st.download_button(
                    "⬇️ Word (.docx)",
                    data=f.read(),
                    file_name=Path(result["docx_path"]).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
        else:
            st.button("Word unavailable", disabled=True, use_container_width=True)
    with dl_cols[2]:
        if result["pdf_path"]:
            with open(result["pdf_path"], "rb") as f:
                st.download_button(
                    "⬇️ PDF (.pdf)",
                    data=f.read(),
                    file_name=Path(result["pdf_path"]).name,
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.button("PDF unavailable (install LibreOffice)", disabled=True, use_container_width=True)

    st.divider()

    # -----------------------------------------------------------------------
    # Feedback widget — captured into the MCP store for the Audit Trail page
    # -----------------------------------------------------------------------
    st.markdown("## Rate this analysis")
    if st.session_state.get("feedback_submitted"):
        st.success("Thanks — your feedback has been recorded in the audit trail.")
    else:
        with st.form("feedback_form", clear_on_submit=False):
            rating = st.slider(
                "Overall quality",
                min_value=1,
                max_value=5,
                value=4,
                help="1 = Poor, 3 = Good, 5 = Outstanding",
            )
            comment = st.text_area(
                "Comments (optional)",
                placeholder="What worked well? What was missed?",
                height=80,
            )
            submit_feedback = st.form_submit_button("Submit feedback")

            if submit_feedback:
                import importlib

                importlib.import_module("sys").path.insert(0, str(SCRIPTS_DIR))
                mcp_store = importlib.import_module("mcp_store")
                rating_labels = {1: "poor", 2: "fair", 3: "good", 4: "excellent", 5: "outstanding"}
                mcp_store.insert_feedback(
                    session_id=result.get("session_id") or "unknown",
                    question="Overall analysis quality",
                    rating=rating_labels[rating],
                    numeric_rating=rating,
                    comments=comment.strip(),
                    company=result.get("company"),
                    framework=result.get("framework"),
                )
                st.session_state["feedback_submitted"] = True
                st.rerun()

    st.divider()
    st.markdown("## Report preview")
    st.markdown(result["markdown"])
