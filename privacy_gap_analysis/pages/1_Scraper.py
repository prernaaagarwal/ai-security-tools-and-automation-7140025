"""Standalone scraper page — download a company's privacy policy and terms
pages as PDFs without running the full gap analysis.

Useful for:
- Previewing what the tool would analyse before spending OpenAI tokens.
- Collecting policy snapshots for your own archive / diffing.
"""

import os
import sys
import traceback
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = APP_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
os.chdir(APP_DIR)


st.set_page_config(page_title="Policy Scraper", page_icon="🌐", layout="wide")

st.title("🌐 Privacy Policy Scraper")
st.markdown(
    "Enter a company's homepage URL. This page will auto-discover the privacy "
    "policy and terms & conditions pages and download each as a PDF. No "
    "OpenAI calls — this is a **free** operation."
)

with st.form("scrape_form"):
    homepage_url = st.text_input(
        "Homepage URL",
        value="",
        placeholder="https://example.com",
    )
    submitted = st.form_submit_button("Scrape", type="primary")


if submitted:
    url = homepage_url.strip()
    if not url:
        st.error("Please enter a URL.")
        st.stop()
    if not (url.startswith("http://") or url.startswith("https://")):
        st.error("URL must start with `http://` or `https://`.")
        st.stop()

    with st.status("Scraping…", expanded=True) as status:
        try:
            st.write(f"🌐 Discovering policy pages on {url}…")
            from privacy_policy_scraper import scrape_policy_documents

            result = scrape_policy_documents(url) or {}
            privacy_pdf = result.get("privacy_policy")
            terms_pdf = result.get("terms_conditions")

            if not privacy_pdf and not terms_pdf:
                status.update(label="Nothing found", state="error")
                st.error(
                    "Couldn't find a privacy policy or terms page at that URL. "
                    "The site may not link to them from the homepage, or the "
                    "scraper couldn't reach them."
                )
                st.stop()

            st.session_state["scrape_result"] = {
                "url": url,
                "privacy_pdf": privacy_pdf,
                "terms_pdf": terms_pdf,
            }
            status.update(label="Done ✅", state="complete")

        except Exception as exc:
            status.update(label="Scrape failed", state="error")
            st.error(f"Scrape failed: {exc}")
            with st.expander("Technical details"):
                st.code(traceback.format_exc())
            st.stop()


scrape_result = st.session_state.get("scrape_result")
if scrape_result:
    st.success(f"Scraped `{scrape_result['url']}`")

    col1, col2 = st.columns(2)
    for col, label, path in (
        (col1, "Privacy Policy", scrape_result["privacy_pdf"]),
        (col2, "Terms & Conditions", scrape_result["terms_pdf"]),
    ):
        with col:
            st.markdown(f"### {label}")
            if not path:
                st.info(f"No {label.lower()} page found.")
                continue
            pdf_path = Path(path)
            if not pdf_path.exists():
                st.warning(f"File missing at {pdf_path}")
                continue
            size_kb = pdf_path.stat().st_size / 1024
            st.caption(f"{pdf_path.name} — {size_kb:.1f} KB")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    f"⬇️ Download {label} PDF",
                    data=f.read(),
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    use_container_width=True,
                )

    st.info(
        "Want to analyse these against CCPA / NIST? Switch to the "
        "**Gap Analysis** page in the sidebar."
    )
