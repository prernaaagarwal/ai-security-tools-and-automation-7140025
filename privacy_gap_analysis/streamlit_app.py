"""
Streamlit Web UI for the Privacy Policy Gap Analysis Tool.

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
    page_title="Privacy Policy Gap Analysis",
    page_icon="🔐",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
st.sidebar.title("Privacy Gap Analysis")
st.sidebar.caption("CCPA / CPRA compliance audit, powered by GPT-4.")

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
homepage_url = st.sidebar.text_input(
    "Company homepage URL",
    value="",
    placeholder="https://example.com",
)

st.sidebar.info(
    "Each run costs roughly **$0.20 – $0.80** in OpenAI usage. "
    "Your key is used only for this session — it is not saved."
)

run_clicked = st.sidebar.button("Run analysis", type="primary", use_container_width=True)


# ---------------------------------------------------------------------------
# Main area — header
# ---------------------------------------------------------------------------
st.title("🔐 Privacy Policy Gap Analysis")
st.markdown(
    "Paste a company's homepage URL. The tool will scrape its privacy policy, "
    "compare it to **CCPA / CPRA** requirements using retrieval-augmented GPT-4, "
    "and produce a professional audit report you can download."
)

if not run_clicked and "result" not in st.session_state:
    st.info(
        "👈 Fill in the sidebar and click **Run analysis**. "
        "First run takes ~60–90 seconds to warm up."
    )


# ---------------------------------------------------------------------------
# Analysis pipeline
# ---------------------------------------------------------------------------
def _validate_inputs() -> str | None:
    if not api_key.strip():
        return "Please enter your OpenAI API key in the sidebar."
    if not api_key.strip().startswith("sk-"):
        return "That doesn't look like a valid OpenAI key (should start with `sk-`)."
    if not homepage_url.strip():
        return "Please enter the company's homepage URL."
    url = homepage_url.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        return "URL must start with `http://` or `https://`."
    return None


def _disable_mcp_client(module) -> None:
    """The analysis code logs to an MCP server on localhost:8080 that we don't
    run in this deployment. Replace every MCP call with a no-op so the
    pipeline doesn't crash on ConnectionError."""

    def _noop(*_args, **_kwargs):
        return None

    client = getattr(module, "mcp_client", None)
    if client is None:
        return
    for name in (
        "request",
        "insert_memory",
        "fetch_memory",
        "insert_confidence",
        "insert_feedback",
        "insert_token_usage",
    ):
        if hasattr(client, name):
            setattr(client, name, _noop)


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
            from privacy_policy_scraper import scrape_policy_documents  # noqa: E402
            import privacy_rag_mcp  # noqa: E402

            _disable_mcp_client(privacy_rag_mcp)

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

            st.write("📚 Loading CCPA framework and policy into vector DB… (first run is slow)")
            st.write("🤖 Running GPT-4 gap analysis…")
            result = privacy_rag_mcp.analyze_policy_documents(
                privacy_pdf_path=privacy_pdf,
                terms_pdf_path=terms_pdf,
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

            st.session_state["result"] = {
                "company": effective_company,
                "md_path": str(report_md),
                "docx_path": str(report_docx) if report_docx.exists() else None,
                "pdf_path": str(report_pdf) if report_pdf.exists() else None,
                "markdown": report_md.read_text(encoding="utf-8"),
            }
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
    st.success(f"Report generated for **{result['company']}**.")

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
    st.markdown("## Report preview")
    st.markdown(result["markdown"])
