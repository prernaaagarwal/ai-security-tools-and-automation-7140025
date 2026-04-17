# Deploy Guide — Privacy Gap Analysis (for non-technical users)

This guide shows you how to:

- **A.** Run the tool on your own laptop (see it in a browser)
- **B.** Put it on the web for free so you can share a link
- **C.** Understand the costs and limits

You do **not** need to be a programmer. Just follow along.

---

## A. Run it on your laptop

### What you need (one-time setup)

1. **Python 3.9 or newer** — https://www.python.org/downloads/ (pick the "Install now" button, and tick "Add Python to PATH" on Windows)
2. **An OpenAI API key** — https://platform.openai.com/api-keys (you'll need a credit card; each report costs cents, not dollars)
3. **Git** — https://git-scm.com/downloads (only needed to download this repo)

### 5 commands in a terminal

Open Terminal (Mac) / PowerShell (Windows) / a terminal app (Linux) and paste each line one at a time:

```bash
git clone https://github.com/prernaaagarwal/ai-security-tools-and-automation-7140025.git
cd ai-security-tools-and-automation-7140025/privacy_gap_analysis
pip install -r requirements.txt
playwright install chromium
streamlit run streamlit_app.py
```

Your browser should pop open at `http://localhost:8501` showing the app.

### Using the app

The app has three pages, switchable from the left sidebar:

1. **Gap Analysis** (main page)
   - Pick the framework — **CCPA / CPRA** (audits a privacy policy URL) or **NIST CSF 2.0** (audits an uploaded security policy).
   - Paste your OpenAI API key, fill in the inputs, and click **Run analysis**.
   - First run takes ~60–90 seconds to warm up.
   - Preview the report on the page, download Markdown / Word / PDF, then optionally **rate the analysis 1–5 stars**. Ratings feed the audit trail.
2. **Scraper** — just grab the privacy + terms PDFs for a URL without running the full analysis (free, no OpenAI calls).
3. **Audit Trail** — dashboard of every analysis, confidence score, token usage, and rating captured so far. Refreshes on demand and has a "Clear" button.

Audit-trail data lives in `./mcp_store/audit_trail.json` inside the app folder. It persists between runs on your laptop but is **cleared each time Streamlit Cloud restarts** the container (free-tier storage is ephemeral).

To stop the app, close the browser and press `Ctrl + C` in the terminal.

---

## B. Put it on the web (free, shareable link)

You'll host the app for free on **Streamlit Community Cloud**. Anyone you give the link to can open it in a browser — no installation on their side.

### Step 1 — Put the code on your own GitHub

1. Create a free GitHub account at https://github.com (skip if you already have one).
2. Go to this repo's GitHub page and click the **Fork** button (top right). This makes your own copy.

### Step 2 — Sign in to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **Sign in with GitHub** and authorize it.

### Step 3 — Deploy the app

1. Click **New app** (top right).
2. Fill in:
   - **Repository**: pick your fork (e.g. `yourname/ai-security-tools-and-automation-7140025`)
   - **Branch**: `main`
   - **Main file path**: `privacy_gap_analysis/streamlit_app.py`
3. Click **Advanced settings** → **Secrets** and paste:
   ```
   OPENAI_API_KEY = "sk-your-real-key-here"
   ```
4. Click **Deploy**. Wait 3–5 minutes for the first build.

### Step 4 — Share the link

When the build finishes, Streamlit gives you a URL like:

```
https://your-app-name.streamlit.app
```

Send that URL to anyone. They'll see the same app in their browser, using the OpenAI key you pasted in Secrets (so they don't need their own).

> 💡 **Don't want to pay for other people's reports?** Clear the Secrets field — visitors will then have to paste their own OpenAI key in the sidebar.

---

## C. Costs and limits

| | Free tier | |
|---|---|---|
| **OpenAI** | Pay-as-you-go | ~$0.20 – $0.80 per report |
| **Streamlit Cloud** | Free | 1 GB RAM; app sleeps after ~7 days of inactivity and wakes on next visit |
| **GitHub** | Free | Unlimited public repos |

### Troubleshooting

- **App crashes with "out of memory" on Streamlit Cloud.** The vector database is tight on the 1 GB free tier. Contact us / open an issue and we'll document the switch to OpenAI-hosted embeddings, which uses ~0 RAM.
- **"No privacy policy found at that URL."** Try pasting the direct link to the privacy page itself, not just the homepage.
- **"Invalid API key."** Re-check the key on https://platform.openai.com/api-keys. It must start with `sk-`.
- **PDF download button is disabled.** PDF generation needs LibreOffice. Locally: install it from https://www.libreoffice.org/. On Streamlit Cloud it's already listed in `packages.txt` and installs automatically.
- **First run is slow (~90 s).** Normal — it downloads an AI model and builds the vector database. Subsequent runs are faster.

### Questions?

Open an issue on the GitHub repo or edit this file with a PR.
