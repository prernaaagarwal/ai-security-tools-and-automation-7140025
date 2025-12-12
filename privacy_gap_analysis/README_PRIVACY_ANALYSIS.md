# Privacy Policy Gap Analysis System
## CCPA/CPRA Compliance with RAG and MCP

**Cardinal Security Privacy Compliance Workflow**

Automated system for evaluating website privacy policies against CCPA/CPRA requirements using Retrieval-Augmented Generation (RAG) and Model Context Protocol (MCP).

---

## Overview

This system provides end-to-end privacy policy compliance analysis:

1. **Scrapes** privacy policies from company websites
2. **Extracts** text content from PDF documents
3. **Loads** content into vector databases
4. **Retrieves** relevant CCPA/CPRA requirements using RAG
5. **Analyzes** gaps using GPT-4.1
6. **Generates** detailed compliance reports with recommendations
7. **Tracks** workflow with MCP (conversation memory, token usage, confidence scores)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: Company URL                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            STEP 1: Privacy Policy Scraper                    │
│  - Scans homepage for privacy policy link                   │
│  - Downloads policy as PDF using Playwright                   │
│  - Output: company_privacy_policy.pdf                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            STEP 2: PDF Text Extraction                       │
│  - Extracts text from PDF (PyPDF2)                          │
│  - Chunks text into semantic sections                        │
│  - Output: Text chunks                                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            STEP 3: Vector Database Loading                   │
│  - Load CCPA/CPRA framework → vectordb_ccpa                 │
│  - Load privacy policy chunks → vectordb_privacy_policies    │
│  - Embedding model: all-MiniLM-L12-v2                       │
│  - Vector store: ChromaDB                                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            STEP 4: RAG Retrieval                             │
│  - Retrieve relevant CCPA requirements                       │
│  - Retrieve relevant policy sections                         │
│  - Combine context for analysis                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            STEP 5: Gap Analysis (GPT-4.1)                    │
│  - System Prompt: Privacy Compliance Officer role           │
│  - Input: CCPA requirements + Policy content                 │
│  - Output: Gap analysis with recommendations                 │
│  - Temperature: 0.3 (consistent analysis)                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            STEP 6: MCP Workflow Tracking                     │
│  - Log conversation memory                                   │
│  - Track token usage                                         │
│  - Store confidence scores                                   │
│  - Record gap analysis results                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            OUTPUT: Compliance Report                         │
│  - Executive summary                                         │
│  - Detailed gaps with CCPA references                        │
│  - Prioritized recommendations                               │
│  - Format: Markdown report                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Files and Components

### Core System Files

| File | Purpose |
|------|---------|
| `CCPA_CPRA_Framework.xlsx` | CCPA/CPRA requirements knowledge base (35+ requirements) |
| `privacy_policy_scraper.py` | Scrapes privacy policies from websites → PDF |
| `privacy_rag_mcp.py` | RAG system for gap analysis with GPT-4.1 |
| `privacy_mcp_server.py` | MCP server for workflow tracking |
| `run_privacy_analysis.py` | End-to-end workflow orchestration |

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `README_PRIVACY_ANALYSIS.md` | This file - system documentation |

### Generated Files/Directories

| Path | Contents |
|------|----------|
| `vectordb_ccpa/` | Vector database for CCPA framework |
| `vectordb_privacy_policies/` | Vector database for scraped policies |
| `*.pdf` | Downloaded privacy policy PDFs |
| `*_CCPA_Gap_Analysis_*.md` | Generated compliance reports |

---

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API Key (for GPT-4.1)
- 8GB+ RAM (for embedding models and vector databases)
- Internet connection (for scraping)

### Step 1: Install Dependencies

```bash
cd "privacy scanner"
pip install -r requirements.txt
```

### Step 2: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 3: Set OpenAI API Key

```bash
# Option 1: Environment variable
export OPENAI_API_KEY="your-api-key-here"

# Option 2: Add to .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### Step 4: Verify CCPA Framework File

Ensure `CCPA_CPRA_Framework.xlsx` is present in the `privacy scanner` directory.

---

## Usage

### Option 1: Complete Workflow (Recommended)

Run the end-to-end analysis:

```bash
# Terminal 1: Start MCP server
python privacy_mcp_server.py

# Terminal 2: Run analysis
python run_privacy_analysis.py https://auditcaddie.com "Audit Caddie"
```

### Option 2: Step-by-Step

#### Step 1: Scrape Privacy Policy

```python
from privacy_policy_scraper import scrape_privacy_policy

pdf_path = scrape_privacy_policy("https://auditcaddie.com")
# Output: auditcaddie.com_privacy_policy.pdf
```

#### Step 2: Analyze with RAG/MCP

```python
from privacy_rag_mcp import analyze_privacy_policy

result = analyze_privacy_policy(
    pdf_path="auditcaddie.com_privacy_policy.pdf",
    company_name="Audit Caddie"
)

print(result['report_path'])
# Output: Audit_Caddie_CCPA_Gap_Analysis_20231201_143022.md
```

### Option 3: Interactive Mode

```bash
python run_privacy_analysis.py

# Follow prompts:
# Enter company homepage URL: https://example.com
# Auto-detect company name? (y/n): y
# MCP server running? Press Enter to continue...
```

---

## Output Report Format

Generated reports include:

### 1. Executive Summary
- Overall compliance status
- Number of gaps identified
- Priority distribution

### 2. Detailed Gap Analysis
For each gap:
- **Gap Description**: What's missing or inadequate
- **CCPA/CPRA Reference**: Specific section (e.g., Section 1798.100)
- **Recommendation**: Specific language or actions to add
- **Priority**: Critical / High / Medium / Low

### 3. Categories Covered
- Consumer Rights (Right to Know, Delete, Opt-Out, Correct, Limit)
- Notice Requirements
- Data Practices
- Security Requirements
- Verification and Response
- Third-Party Requirements
- Special Categories (Children's data)
- Transparency Requirements
- Compliance and Records

### 4. Metadata
- Tokens consumed
- Model used (GPT-4.1)
- Timestamp
- Session ID for MCP tracking

---

## MCP Server Endpoints

The MCP server runs on `http://localhost:8080` and provides:

### Health Check
```
GET http://localhost:8080/health
```

### Debug Endpoints
```
GET http://localhost:8080/debug/memory      # Conversation logs
GET http://localhost:8080/debug/confidence  # Confidence scores
GET http://localhost:8080/debug/feedback    # User feedback
GET http://localhost:8080/debug/tokens      # Token usage stats
GET http://localhost:8080/debug/gaps        # Gap analysis results
```

### JSON-RPC Endpoint
```
POST http://localhost:8080/mcp
```

Supported methods:
- `insert_memory` - Log conversation/analysis
- `fetch_memory` - Retrieve history
- `insert_confidence` - Log confidence scores
- `insert_feedback` - Record feedback
- `insert_token_usage` - Track GPT-4.1 usage
- `insert_gap_analysis` - Store gap results

---

## CCPA/CPRA Framework

The system evaluates policies against 35+ CCPA/CPRA requirements across categories:

1. **Consumer Rights** (5 requirements)
   - Right to Know
   - Right to Delete
   - Right to Opt-Out
   - Right to Correct
   - Right to Limit Use of Sensitive PI

2. **Notice Requirements** (5 requirements)
   - Privacy Policy disclosures
   - Notice at collection
   - Opt-out notice
   - Financial incentives notice

3. **Data Practices** (4 requirements)
   - Data minimization
   - Purpose limitation
   - Storage limitation
   - Sensitive PI handling

4. **Security Requirements** (3 requirements)
   - Reasonable security procedures
   - Service provider obligations
   - Breach notification

5. **Verification and Response** (4 requirements)
   - Identity verification
   - Response timeframes
   - Non-discrimination
   - Authorized agents

6. **Third-Party Requirements** (3 requirements)
   - Service provider contracts
   - Third-party disclosures
   - Sale definition and tracking

7. **Special Categories** (3 requirements)
   - Children under 13
   - Children 13-16
   - Employee/B2B data

8. **Transparency Requirements** (3 requirements)
   - Privacy policy accessibility
   - Request submission methods
   - Do Not Sell link placement

9. **Compliance and Records** (4 requirements)
   - Record keeping
   - Annual metrics reporting
   - Privacy policy updates
   - Training requirements

---

## Cardinal Security Use Case

This system automates the privacy compliance workflow described by Scott Morris of Cardinal Security:

### Current Manual Process
1. Attorney reviews website privacy statement
2. Identifies gaps against state/federal privacy laws
3. Drafts updated privacy policy
4. Delivers fixed-fee compliance package ($5K)

### Automated Workflow
1. **Scale**: Scan multiple websites in parallel
2. **Speed**: Generate gap analysis in minutes vs. hours
3. **Consistency**: Systematic evaluation of all CCPA/CPRA requirements
4. **Documentation**: MCP tracking for audit trails
5. **White-Label**: Cardinal Security branding, tool runs behind the scenes

### Business Impact
- **Efficiency**: Reduce attorney time per assessment
- **Volume**: Process more clients with same resources
- **Quality**: Comprehensive coverage of all requirements
- **Margins**: Maintain pricing while reducing costs

---

## Troubleshooting

### Issue: "No privacy policy link found"
**Solution**: Website may not have a recognizable privacy link. Check:
- Link text contains "privacy"
- Link href contains "privacy", "privacy-policy", etc.
- Policy is not behind authentication

### Issue: "PDF extraction failed"
**Solution**:
- Ensure PyPDF2 is installed
- Some PDFs may be image-based (need OCR)
- Try manual PDF download

### Issue: "MCP connection refused"
**Solution**:
- Start MCP server first: `python privacy_mcp_server.py`
- Check server is running: `curl http://localhost:8080/health`

### Issue: "OpenAI API error"
**Solution**:
- Verify API key is set: `echo $OPENAI_API_KEY`
- Check API key has credits
- Verify model access (gpt-4o)

### Issue: "Vector database not found"
**Solution**:
- First run creates databases automatically
- If corrupted, delete `vectordb_*` directories and re-run

---

## Future Enhancements

- [ ] Add support for additional privacy frameworks (GDPR, PIPEDA, LGPD)
- [ ] Implement automated policy generation based on gaps
- [ ] Add multi-state privacy law comparison
- [ ] Create web UI for non-technical users
- [ ] Implement batch processing for multiple companies
- [ ] Add OCR for image-based PDFs
- [ ] Generate visual compliance dashboards
- [ ] Integrate with Cardinal Security CRM

---

## License

Proprietary -  Audit Caddie

---

## Contact

For questions or support:
- **Audit Caddie**: Brennan Lodge (BLodgic)

---

*System built with Claude Code*
*Powered by OpenAI GPT-4.1, LangChain, ChromaDB, and MCP*
