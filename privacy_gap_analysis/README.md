# Privacy Policy Gap Analysis Tool

AI-powered privacy compliance tool that analyzes company privacy policies against CCPA/CPRA requirements. Uses RAG (Retrieval-Augmented Generation) with GPT-4 to identify compliance gaps, classify them by priority, and generate professional audit reports.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/AI-GPT--4-green.svg)](https://openai.com/)

---

##  Overview

This tool automates privacy policy compliance analysis by:
- Scraping privacy policies from company websites
- Comparing them against CCPA/CPRA regulatory requirements
- Using RAG (Retrieval-Augmented Generation) for semantic analysis
- Identifying compliance gaps with specific CCPA section references
- Generating professional audit reports in multiple formats
- Tracking all analyses with complete audit trails
- Collecting human feedback for continuous improvement

**Powered by:** OpenAI GPT-4, LangChain, ChromaDB, FastAPI

---

##  Key Features

###  Automated Compliance Analysis
- **Web Scraping**: Automatically downloads privacy policies and terms from websites
- **CCPA/CPRA Framework**: Built-in database of 102+ California privacy law requirements
- **RAG System**: Semantic search using vector embeddings (all-MiniLM-L12-v2)
- **GPT-4 Analysis**: Advanced AI-powered gap identification with confidence scoring
- **Priority Classification**: Gaps ranked as Critical, High, Medium, or Low

###  Professional Report Generation
- **Multiple Formats**: Markdown, Word (.docx), and PDF
- **Template-Based**: Uses Audit Caddie professional template styling
- **Audit Caddie Branding**: Color-coded priorities, structured sections
- **Auto-Generated**: Complete reports with executive summaries and recommendations

###  Enterprise Audit Trails
- **MCP Server**: Model Context Protocol for structured logging
- **Session Tracking**: Unique session IDs for every analysis
- **Token Usage**: Complete GPT-4 API consumption tracking
- **Gap Analysis Store**: Structured compliance data storage
- **Confidence Scoring**: Automatic quality assessment

###  Human Feedback Reinforcement Learning (HFRL)
- **Automatic Confidence Scoring**: Multi-factor quality assessment
- **Interactive User Feedback**: 1-5 rating scale with comments
- **Structured Gap Parsing**: Automated data extraction
- **Feedback Dashboard**: Visual analytics and trends
- **Continuous Improvement**: Data for model fine-tuning

---

##  Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- LibreOffice (optional, for PDF generation)

### Installation

```bash
# Clone the repository
git clone https://github.com/Blodgic/privacy_analysis.git
cd privacy_analysis

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Basic Usage

```bash
# 1. Start the MCP server (in one terminal)
cd scripts
python privacy_mcp_server.py

# 2. Run analysis (in another terminal)
python run_privacy_analysis.py https://example.com "Example Company"
```

**Output:**
- `Example_Company_CCPA_Gap_Analysis_YYYYMMDD.md` - Markdown report
- `Example_Company_CCPA_Gap_Analysis_YYYYMMDD.docx` - Professional Word document
- `Example_Company_CCPA_Gap_Analysis_YYYYMMDD.pdf` - PDF (if LibreOffice installed)

---

##  Documentation

### Complete Guides
- **[TEMPLATE_USAGE_GUIDE.md](TEMPLATE_USAGE_GUIDE.md)** - Report generation and templates
- **[HUMAN_FEEDBACK_GUIDE.md](HUMAN_FEEDBACK_GUIDE.md)** - HFRL system documentation
- **[CHAPTER2_SCREENCAP_GUIDE.md](CHAPTER2_SCREENCAP_GUIDE.md)** - RAG demonstration guide

### LinkedIn Learning Course Materials
- **[CHAPTER2_LESSON02_SCRIPT.md](CHAPTER2_LESSON02_SCRIPT.md)** - MCP Server narration
- **[CHAPTER2_LESSON03_SCRIPT.md](CHAPTER2_LESSON03_SCRIPT.md)** - GRC Classification narration

---

##  Architecture

### System Components

```

                    Privacy Analysis Tool                     

                              
        
                                                  
                                                  
      
   Web Scraper       RAG System         MCP Server   
                                                     
 • Selenium        • ChromaDB           • FastAPI    
 • BeautifulSoup   • LangChain          • JSON-RPC   
 • PDF Extract     • HuggingFace        • Audit Log  
      
                              
                              
                    
                       GPT-4 Engine   
                                      
                     • Gap Analysis   
                     • CCPA Matching  
                     • Confidence     
                    
                              
                              
                    
                     Report Generator 
                                      
                     • Markdown       
                     • Word (python-docx)
                     • PDF (LibreOffice)
                    
```

### Data Flow

1. **Input**: Company URL → Web scraper downloads privacy policy
2. **Extraction**: PDF text extraction → Policy content
3. **Indexing**: CCPA framework + policy → ChromaDB vector embeddings
4. **Retrieval**: Semantic search → Top 35 relevant CCPA requirements
5. **Analysis**: GPT-4 → Gap identification with priorities
6. **Logging**: MCP server → Session tracking, tokens, gaps, feedback
7. **Generation**: Template system → Professional reports (MD/DOCX/PDF)
8. **Feedback**: Human reviewer → Quality ratings and comments

---

##  Usage Examples

### Example 1: Complete Analysis Workflow

```bash
# Start MCP server
python scripts/privacy_mcp_server.py

# Run analysis
python scripts/run_privacy_analysis.py https://auditcaddie.com "Audit Caddie"

# Provide feedback when prompted
Rating (1-5): 4
Comments: Comprehensive analysis, very thorough

# View results in MCP dashboard
python scripts/view_feedback.py
```

### Example 2: Generate Report from Existing Markdown

```bash
cd scripts
python generate_compliance_report.py \
  --markdown ../reports/Company_Analysis.md \
  --company "Acme Corp" \
  --output-dir ../reports
```

### Example 3: Manual Feedback Entry

```bash
# Add feedback for a previous analysis
python scripts/add_feedback.py \
  privacy_analysis_Company_20251227_143521 \
  excellent \
  "Identified all critical gaps"
```

### Example 4: View Feedback Dashboard

```bash
# Interactive dashboard
python scripts/view_feedback.py

# Export data
python scripts/view_feedback.py --export
```

---

##  Educational Demos

### Demo Scripts for Training

The repository includes educational demo scripts perfect for learning and teaching:

```bash
# RAG (Retrieval-Augmented Generation) Demo
python scripts/02_01_demo_retrieval_terminal.py    # Terminal REPL simulation
python scripts/02_01_demo_rag_retrieval.py          # Full RAG walkthrough

# MCP (Model Context Protocol) Demo
python scripts/02_02_demo_mcp_server.py             # Audit trail demonstration

# GRC (Data Classification) Demo
python scripts/demo_grc_classification.py           # Classification framework
```

Each demo includes:
- Interactive mode (with pauses for explanation)
- Quick mode (auto-run for recording)
- Visual output with ASCII tables
- Educational explanations

---

##  Data Classification & Security

### GRC Data Types

| Data Type | Classification | AI Deployment | Used in Tool |
|-----------|---------------|---------------|--------------|
| Regulatory Frameworks (CCPA, GDPR) | Public |  Cloud AI Safe |  Yes |
| Public Privacy Policies | Public |  Cloud AI Safe |  Yes |
| Internal Policies | Confidential |  On-Prem Only |  No |
| Control Implementations | Confidential |  On-Prem Only |  No |
| Audit Evidence | Restricted |  Extreme Caution |  No |

### Deployment Options

**Current**: Cloud AI (OpenAI GPT-4) - Suitable for public data only

**For Confidential Data**:
- **Local LLM**: Llama 3, Mistral (on-premises)
- **Enterprise Cloud**: Azure OpenAI, AWS Bedrock (with DPAs)
- **Hybrid**: Public data → Cloud, Confidential → On-prem

---

##  Example Output

### Gap Analysis Report Structure

```markdown
# CCPA/CPRA Gap Analysis Report

**Company:** BLodgic
**Analysis Date:** 2025-12-27
**Session ID:** privacy_analysis_BLodgic_20251227_115333

## Gap Analysis

**Gap 1: Right to Delete Disclosure**
- **Missing:** Information on consumers' right to request deletion
- **Reference:** CCPA Section 1798.105
- **Priority:** Critical

**Gap 2: Do Not Sell Link**
- **Missing:** "Do Not Sell or Share My Personal Information" link
- **Reference:** CCPA Section 1798.135
- **Priority:** Critical

## Recommendations

1. Add Right to Delete section to privacy policy
2. Implement "Do Not Sell" link on homepage
3. Define specific data retention periods

## Metadata

- **Model Used:** GPT-4
- **Tokens Consumed:** 4,236
- **Confidence Score:** 0.95
```

---

##  Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
MCP_SERVER_URL=http://localhost:8080
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com
LOCAL_MODEL_PATH=/models/llama3-8b
```

### MCP Server Configuration

Default configuration in `scripts/privacy_mcp_server.py`:
- **Port**: 8080
- **Host**: 0.0.0.0
- **Protocol**: JSON-RPC 2.0

**Endpoints**:
- `/health` - Server health check
- `/mcp` - JSON-RPC endpoint
- `/debug/memory` - Session logs
- `/debug/confidence` - Confidence scores
- `/debug/feedback` - User feedback
- `/debug/tokens` - Token usage
- `/debug/gaps` - Gap analysis data

---

##  Contributing

Contributions are welcome! This is an educational tool for LinkedIn Learning courses.

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest tests/
```

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions
- Comment complex logic

---

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

---

##  Acknowledgments

- **OpenAI** - GPT-4 API
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **FastAPI** - MCP server
- **python-docx** - Word document generation
- **LibreOffice** - PDF conversion

---

##  Support

For questions, issues, or contributions:
- **GitHub Issues**: https://github.com/Blodgic/privacy_analysis/issues
- **Documentation**: See individual guide files in repository
- **LinkedIn Learning**: Course materials included in repository

---

##  Roadmap

### Current Features (v1.0)
-  Automated web scraping
-  RAG-based compliance analysis
-  Multi-format report generation
-  MCP audit trail server
-  Human feedback system
-  Professional templates

### Planned Features (v2.0)
-  Support for GDPR, SOC 2, ISO 27001
-  Multi-language policy analysis
-  Persistent MCP database (PostgreSQL)
-  Web dashboard for results
-  Batch analysis mode
-  Custom compliance frameworks
-  API endpoints for integration
-  Model fine-tuning with feedback data

---

##  Version History

**v1.0.0** (December 2025)
- Initial release
- CCPA/CPRA compliance analysis
- RAG system with ChromaDB
- MCP server for audit trails
- Human feedback reinforcement learning
- Professional report templates
- Educational demo scripts

---

##  Legal Notice

This tool is for educational and compliance assistance purposes only. It does not constitute legal advice. Always consult with qualified legal counsel for compliance matters.

---

**Built with  for privacy compliance professionals**
