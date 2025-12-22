# Privacy Gap Analysis System - Architecture Diagrams

Based on: https://github.com/Blodgic/CADDIE_RAG_MPC

---

## DIAGRAM 1: High-Level System Overview (For Intro/Chapter 1)

**Use Case:** Executive summary slide showing what the system does

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PRIVACY GAP ANALYSIS SYSTEM                      │
│                  AI-Powered CCPA Compliance Automation              │
└─────────────────────────────────────────────────────────────────────┘

                              INPUT
                                │
                    ┌───────────▼───────────┐
                    │  Company Website URL  │
                    │  (e.g., stripe.com)   │
                    └───────────┬───────────┘
                                │
                    ╔═══════════▼═══════════╗
                    ║   AUTOMATED SCRAPER   ║
                    ║   (Playwright)        ║
                    ║   • Finds privacy     ║
                    ║     policy link       ║
                    ║   • Downloads PDF     ║
                    ╚═══════════╤═══════════╝
                                │
                                │ PDF
                                │
                    ╔═══════════▼═══════════╗
                    ║  TEXT EXTRACTION      ║
                    ║  (PyPDF2)             ║
                    ║  • Parse PDF          ║
                    ║  • Chunk text         ║
                    ╚═══════════╤═══════════╝
                                │
                                │ Text Chunks
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼────────┐     ┌────────▼────────┐    ┌───────▼────────┐
│  CCPA FRAMEWORK│     │  COMPANY POLICY │    │  MCP SERVER    │
│  Knowledge Base│     │  Vector Store   │    │  (Tracking)    │
│  (35 Sections) │     │  (ChromaDB)     │    │                │
└───────┬────────┘     └────────┬────────┘    └───────┬────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                    ╔═══════════▼═══════════╗
                    ║   RAG RETRIEVAL       ║
                    ║   • Semantic search   ║
                    ║   • Find relevant     ║
                    ║     CCPA sections     ║
                    ║   • Context building  ║
                    ╚═══════════╤═══════════╝
                                │
                                │ Context
                                │
                    ╔═══════════▼═══════════╗
                    ║   GPT-4 ANALYSIS      ║
                    ║   (OpenAI API)        ║
                    ║   • Gap detection     ║
                    ║   • Recommendations   ║
                    ║   • Prioritization    ║
                    ╚═══════════╤═══════════╝
                                │
                                │ Analysis
                                │
                    ╔═══════════▼═══════════╗
                    ║   REPORT GENERATION   ║
                    ║   • Markdown          ║
                    ║   • Word (docx)       ║
                    ║   • Audit trail       ║
                    ╚═══════════╤═══════════╝
                                │
                                ▼
                           OUTPUT

                    📄 Gap Analysis Report
                    ├─ 23 Compliance Gaps
                    ├─ CCPA References
                    ├─ Recommendations
                    ├─ Priority Levels
                    └─ Session Audit Trail

┌────────────────────────────────────────────────────────────┐
│  METRICS:                                                  │
│  ⏱️  Time: 2 minutes (vs 3-5 hours manual)                │
│  💰 Cost: $0.50 (vs $5,000 attorney)                      │
│  🎯 Accuracy: 100% coverage of 35 CCPA requirements       │
│  📊 Audit: Full MCP tracking (tokens, sessions, gaps)     │
└────────────────────────────────────────────────────────────┘
```

**Key Selling Points:**
- **90x faster** than manual review
- **99% cost reduction**
- **Consistent** analysis every time
- **Auditable** with full MCP tracking

---

## DIAGRAM 2: Technical Architecture (For Chapter 2 - RAG Deep Dive)

**Use Case:** Explaining how RAG and MCP work together

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    TECHNICAL ARCHITECTURE DIAGRAM                         │
│              RAG (Retrieval-Augmented Generation) + MCP                   │
└──────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  KNOWLEDGE BASES    │
└─────────────────────┘
           │
           ├─────► ┌──────────────────────────────────────┐
           │       │  CCPA_CPRA_Framework.csv             │
           │       │  • 35 CCPA requirements              │
           │       │  • Category, Requirement, Body       │
           │       │  • CCPA Section References           │
           │       └──────────────┬───────────────────────┘
           │                      │
           │              ┌───────▼────────┐
           │              │  CSV → pandas  │
           │              │  DataFrame     │
           │              └───────┬────────┘
           │                      │
           │       ┌──────────────▼──────────────────────┐
           │       │  LangChain DataFrameLoader          │
           │       │  Convert rows → Document objects    │
           │       └──────────────┬──────────────────────┘
           │                      │
           │       ┌──────────────▼──────────────────────┐
           │       │  HuggingFace Embeddings             │
           │       │  Model: all-MiniLM-L12-v2           │
           │       │  Text → 384-dim vectors             │
           │       └──────────────┬──────────────────────┘
           │                      │
           │       ┌──────────────▼──────────────────────┐
           │       │  ChromaDB - vectordb_ccpa/          │
           │       │  • Persistent vector database       │
           │       │  • Semantic similarity search       │
           │       └──────────────┬──────────────────────┘
           │                      │
           │                      ├─────► CCPA Retriever
           │                      │       (k=35 documents)
           │                      │
           └─────► ┌──────────────▼───────────────────────┐
                   │  Company Privacy Policy (PDF)        │
                   │  • Scraped from website              │
                   │  • Extracted text (PyPDF2)           │
                   │  • Chunked by paragraphs             │
                   └──────────────┬───────────────────────┘
                                  │
                   ┌──────────────▼──────────────────────┐
                   │  HuggingFace Embeddings             │
                   │  (same model as CCPA)               │
                   └──────────────┬──────────────────────┘
                                  │
                   ┌──────────────▼──────────────────────┐
                   │  ChromaDB - vectordb_privacy/       │
                   │  • Separate DB per company          │
                   │  • Metadata: company, source        │
                   └──────────────┬──────────────────────┘
                                  │
                                  ├─────► Policy Retriever
                                  │       (k=50 chunks)

┌────────────────────────────────────────────────────────────────┐
│                        RAG QUERY FLOW                          │
└────────────────────────────────────────────────────────────────┘

   User Query: "Analyze company X for CCPA compliance"
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌───────────────────┐                 ┌───────────────────┐
│ CCPA Retriever    │                 │ Policy Retriever  │
│ Query: "CCPA"     │                 │ Query: "policy"   │
│ Returns: 35 docs  │                 │ Returns: 50 docs  │
└─────────┬─────────┘                 └─────────┬─────────┘
          │                                     │
          │         ┌───────────────────────────┘
          │         │
          ▼         ▼
    ┌─────────────────────────────────┐
    │   CONTEXT AGGREGATION           │
    │   • CCPA requirements (35)      │
    │   • Policy sections (50)        │
    │   • Combined prompt context     │
    └─────────────┬───────────────────┘
                  │
                  │ Context (8,000+ tokens)
                  │
        ┌─────────▼──────────┐
        │   GPT-4o API       │
        │   (OpenAI)         │
        │                    │
        │   System Prompt:   │
        │   "You are a       │
        │    Privacy         │
        │    Compliance      │
        │    Officer..."     │
        │                    │
        │   Temperature: 0.3 │
        │   Max Tokens: 2000 │
        └─────────┬──────────┘
                  │
                  │ Analysis Result
                  │
        ┌─────────▼──────────┐
        │  Gap Analysis      │
        │  • 23 gaps found   │
        │  • CCPA references │
        │  • Recommendations │
        │  • Priority levels │
        └─────────┬──────────┘
                  │
                  ├────────────────────────────┐
                  │                            │
                  ▼                            ▼
        ┌──────────────────┐         ┌────────────────┐
        │  Report Output   │         │  MCP Tracking  │
        │  • Markdown      │         │  (see below)   │
        │  • Word DOCX     │         └────────────────┘
        └──────────────────┘


┌────────────────────────────────────────────────────────────────┐
│                    MCP SERVER ARCHITECTURE                     │
│                  (Model Context Protocol)                      │
└────────────────────────────────────────────────────────────────┘

                        ┌──────────────────┐
                        │  FastAPI Server  │
                        │  Port: 8080      │
                        └────────┬─────────┘
                                 │
                    ┌────────────┼────────────┐
                    │    JSON-RPC Endpoint    │
                    │    POST /mcp            │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ Memory Store  │      │ Token Store   │      │ Gap Store     │
│               │      │               │      │               │
│ • Session ID  │      │ • Timestamp   │      │ • Company     │
│ • Text log    │      │ • Model       │      │ • Gaps list   │
│ • Timestamp   │      │ • Tokens used │      │ • Priority    │
│               │      │ • Cost ($)    │      │ • Session ID  │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Debug Endpoints    │
                    ├─────────────────────┤
                    │ GET /debug/memory   │
                    │ GET /debug/tokens   │
                    │ GET /debug/gaps     │
                    │ GET /health         │
                    └─────────────────────┘


┌────────────────────────────────────────────────────────────────┐
│                       KEY COMPONENTS                           │
└────────────────────────────────────────────────────────────────┘

EMBEDDING MODEL:
┌──────────────────────────────────────┐
│  sentence-transformers/              │
│  all-MiniLM-L12-v2                   │
│  • 384 dimensions                    │
│  • Semantic similarity               │
│  • Fast inference (~5ms/text)        │
│  • Runs locally (no API calls)      │
└──────────────────────────────────────┘

VECTOR DATABASE:
┌──────────────────────────────────────┐
│  ChromaDB                            │
│  • Persistent storage                │
│  • Cosine similarity search          │
│  • Metadata filtering                │
│  • Separate collections per dataset  │
└──────────────────────────────────────┘

LLM:
┌──────────────────────────────────────┐
│  GPT-4o (OpenAI)                     │
│  • Temperature: 0.3 (consistency)    │
│  • Max tokens: 2000 (output)         │
│  • Context window: 128K tokens       │
│  • Cost: ~$0.005/1K tokens           │
└──────────────────────────────────────┘
```

---

## DIAGRAM 3: Data Flow Sequence (For Chapter 3 - Gap Analysis)

**Use Case:** Show step-by-step what happens during analysis

```
┌──────────────────────────────────────────────────────────────────┐
│           DATA FLOW: PRIVACY GAP ANALYSIS WORKFLOW               │
│                    End-to-End Sequence                           │
└──────────────────────────────────────────────────────────────────┘


STEP 1: SCRAPING
────────────────

User Input: "https://stripe.com"
     │
     ▼
privacy_policy_scraper.py
     │
     ├──► [Find Privacy Link]
     │    • Scan homepage HTML
     │    • Look for "privacy" keywords
     │    • Found: https://stripe.com/privacy
     │
     ├──► [Download as PDF]
     │    • Launch Playwright browser
     │    • Navigate to privacy URL
     │    • Print to PDF
     │    • Save: stripe.com_privacy_policy.pdf
     │
     └──► Output: stripe.com_privacy_policy.pdf (1.1 MB)


STEP 2: EXTRACTION
──────────────────

Input: stripe.com_privacy_policy.pdf
     │
     ▼
PyPDF2.PdfReader()
     │
     ├──► [Parse PDF Pages]
     │    • Extract text from each page
     │    • Total pages: 24
     │    • Total characters: 87,543
     │
     ├──► [Text Chunking]
     │    • Split by double newlines (\n\n)
     │    • Filter empty chunks
     │    • Total chunks: 127
     │
     └──► Output: 127 text chunks


STEP 3: VECTOR DATABASE LOADING
────────────────────────────────

┌─────────────────────────────────────────────────────────┐
│  PARALLEL LOADING (2 Vector Databases)                  │
└─────────────────────────────────────────────────────────┘

[Database 1: CCPA Framework]          [Database 2: Policy Chunks]

Input: CCPA_CPRA_Framework.csv        Input: 127 text chunks
     │                                      │
     ▼                                      ▼
pandas.read_csv()                     Document objects
     │                                      │
     ▼                                      ▼
LangChain DataFrameLoader             LangChain Documents
     │                                      │
     ├─► 35 CCPA documents                 ├─► 127 policy documents
     │                                      │
     ▼                                      ▼
HuggingFace Embeddings                HuggingFace Embeddings
(all-MiniLM-L12-v2)                   (all-MiniLM-L12-v2)
     │                                      │
     ├─► 35 x 384-dim vectors              ├─► 127 x 384-dim vectors
     │                                      │
     ▼                                      ▼
ChromaDB                              ChromaDB
./vectordb_ccpa/                      ./vectordb_privacy_policies/
     │                                      │
     └──────────────┬───────────────────────┘
                    │
                    ▼
         [Both Databases Ready]


STEP 4: RAG RETRIEVAL
─────────────────────

Query: "Analyze Stripe for CCPA compliance"
     │
     ├──────────────────┬──────────────────┐
     │                  │                  │
     ▼                  ▼                  ▼
[Retrieve CCPA]   [Retrieve Policy]   [Build Context]
     │                  │                  │
     │                  │                  │
k=35 documents     k=50 chunks        Combined prompt:
     │                  │                  │
     ├─► Section 1798.100  ├─► "Stripe collects..."   ├─► 8,245 tokens
     ├─► Section 1798.105  ├─► "You have the right"   │
     ├─► Section 1798.110  ├─► "We share data with"   │
     │   ...                │   ...                    │
     └─► [35 sections]      └─► [50 chunks]            │
                                                        │
                                                        ▼
                                            Context sent to GPT-4


STEP 5: GPT-4 ANALYSIS
──────────────────────

Input: Combined Context (8,245 tokens)
     │
     ▼
┌────────────────────────────────────────────┐
│  OpenAI API Call                           │
│                                            │
│  Model: gpt-4o                             │
│  Temperature: 0.3                          │
│  Max Tokens: 2000                          │
│                                            │
│  System Prompt:                            │
│  "You are a Privacy Compliance Officer    │
│   specializing in CCPA/CPRA. Analyze      │
│   the following privacy policy against    │
│   CCPA requirements and identify gaps..." │
│                                            │
│  User Prompt:                              │
│  "CCPA REQUIREMENTS: [35 sections]        │
│   COMPANY POLICY: [50 chunks]             │
│   Perform comprehensive gap analysis..."   │
└────────────────┬───────────────────────────┘
                 │
                 │ [Processing: ~15 seconds]
                 │
                 ▼
┌────────────────────────────────────────────┐
│  GPT-4 Output                              │
│                                            │
│  Gap Analysis Report:                      │
│                                            │
│  1. Missing: Right to Limit Sensitive PI   │
│     CCPA: Section 1798.121                 │
│     Priority: HIGH                         │
│     Recommendation: Add disclosure...      │
│                                            │
│  2. Inadequate: Data Retention Policy      │
│     CCPA: Section 1798.105                 │
│     Priority: MEDIUM                       │
│     Recommendation: Specify retention...   │
│                                            │
│  [... 21 more gaps]                        │
│                                            │
│  Total Gaps: 23                            │
│  Tokens Used: 6,234                        │
│  Cost: $0.62                               │
└────────────────┬───────────────────────────┘
                 │
                 ▼
        [Analysis Complete]


STEP 6: MCP TRACKING
────────────────────

Analysis Result
     │
     ├──────────────────┬──────────────────┬──────────────────┐
     │                  │                  │                  │
     ▼                  ▼                  ▼                  ▼
[insert_memory]   [insert_token]   [insert_gap]    [insert_confidence]
     │                  │                  │                  │
Session:          Tokens:           Gaps:            Score:
"privacy_         Prompt: 6,034    Count: 23        0.87 (high)
analysis_         Completion: 200  Priority:        Reliable
Stripe_           Total: 6,234     12 High          analysis
20251202"         Cost: $0.62      8 Medium
                                   3 Low
     │                  │                  │                  │
     └──────────────────┴──────────────────┴──────────────────┘
                               │
                               ▼
                    [MCP Server Storage]
                    http://localhost:8080


STEP 7: REPORT GENERATION
─────────────────────────

GPT-4 Output + MCP Metadata
     │
     ▼
markdown_template.format()
     │
     ├──► [Executive Summary]
     │    • Company: Stripe
     │    • Gaps: 23 identified
     │    • Priority: 12 High, 8 Medium, 3 Low
     │
     ├──► [Detailed Gap Analysis]
     │    For each gap:
     │    • Description
     │    • CCPA Reference
     │    • Recommendation
     │    • Priority Level
     │
     ├──► [Metadata]
     │    • Tokens: 6,234
     │    • Model: gpt-4o
     │    • Session: privacy_analysis_Stripe_20251202
     │    • Timestamp: 2025-12-02T18:55:05
     │
     └──► Output: Stripe_CCPA_Gap_Analysis_20251202_185505.md

     │
     ▼
markdown_to_docx.convert()
     │
     └──► Output: Stripe_CCPA_Gap_Analysis_20251202_185505.docx


FINAL OUTPUT
────────────

📄 Stripe_CCPA_Gap_Analysis_20251202_185505.md (5 KB)
📄 Stripe_CCPA_Gap_Analysis_20251202_185505.docx (38 KB)

✅ Analysis Complete
⏱️  Total Time: 118 seconds
💰 Total Cost: $0.62
🎯 Gaps Found: 23
📊 MCP Session: Logged at http://localhost:8080/debug/gaps
```

---

## DIAGRAM 4: MCP Protocol Detail (For Chapter 2 - MCP Explained)

**Use Case:** Understanding how MCP tracks the workflow

```
┌──────────────────────────────────────────────────────────────────┐
│              MCP (MODEL CONTEXT PROTOCOL) DETAILED               │
│                  Workflow Tracking & Audit Trail                 │
└──────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│  MCP SERVER COMPONENTS                                          │
└─────────────────────────────────────────────────────────────────┘

                     ┌──────────────────────┐
                     │   FastAPI Server     │
                     │   Port: 8080         │
                     │   Python 3.9+        │
                     └──────────┬───────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │  HTTP API  │  │  JSON-RPC  │  │   Debug    │
        │            │  │  Endpoint  │  │  Endpoints │
        │ GET /health│  │ POST /mcp  │  │ GET /debug/*│
        └────────────┘  └──────┬─────┘  └────────────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
              ┌─────▼─────┐ ┌──▼────┐ ┌──▼────┐
              │  Memory   │ │ Token │ │  Gap  │
              │  Store    │ │ Store │ │ Store │
              └───────────┘ └───────┘ └───────┘


┌─────────────────────────────────────────────────────────────────┐
│  JSON-RPC METHODS (7 Methods)                                   │
└─────────────────────────────────────────────────────────────────┘

1. search_documents (query, k)
   └─► Search vector databases for documents

2. insert_memory (session_id, text)
   └─► Log conversation/analysis text

3. fetch_memory (session_id)
   └─► Retrieve analysis history

4. insert_confidence (query, response, score)
   └─► Log AI confidence levels

5. insert_feedback (session_id, rating)
   └─► Record user feedback (thumbs up/down)

6. insert_token_usage (query, model, tokens)
   └─► Track API consumption & costs

7. insert_gap_analysis (company, gaps, priority)
   └─► Store detailed gap findings


┌─────────────────────────────────────────────────────────────────┐
│  DATA FLOW: CLIENT → MCP SERVER                                 │
└─────────────────────────────────────────────────────────────────┘

privacy_rag_mcp.py (Client)
        │
        │ 1. Start Analysis
        │
        ├──► Session ID: privacy_analysis_Stripe_20251202_185505
        │
        │ 2. Insert Memory (Analysis Start)
        │
        ▼
┌───────────────────────────────────────────┐
│  POST http://localhost:8080/mcp           │
│                                           │
│  {                                        │
│    "jsonrpc": "2.0",                      │
│    "method": "insert_memory",             │
│    "params": {                            │
│      "session_id": "privacy_analysis...", │
│      "text": "Starting analysis: Stripe"  │
│    },                                     │
│    "id": 1                                │
│  }                                        │
└───────────────────────────────────────────┘
        │
        │ 3. MCP Response
        │
        ▼
┌───────────────────────────────────────────┐
│  {                                        │
│    "jsonrpc": "2.0",                      │
│    "result": "Memory inserted",           │
│    "id": 1                                │
│  }                                        │
└───────────────────────────────────────────┘
        │
        │ 4. Continue Analysis...
        │ 5. GPT-4 Call Complete
        │
        │ 6. Insert Token Usage
        │
        ▼
┌───────────────────────────────────────────┐
│  POST http://localhost:8080/mcp           │
│                                           │
│  {                                        │
│    "method": "insert_token_usage",        │
│    "params": {                            │
│      "query": "Gap analysis: Stripe",     │
│      "model_used": "gpt-4o",              │
│      "tokens_prompt": 6034,               │
│      "tokens_completion": 200,            │
│      "tokens_total": 6234                 │
│    }                                      │
│  }                                        │
└───────────────────────────────────────────┘
        │
        │ 7. Insert Gap Analysis Results
        │
        ▼
┌───────────────────────────────────────────┐
│  POST http://localhost:8080/mcp           │
│                                           │
│  {                                        │
│    "method": "insert_gap_analysis",       │
│    "params": {                            │
│      "company": "Stripe",                 │
│      "gaps": [                            │
│        {                                  │
│          "description": "Missing Right...",│
│          "ccpa_ref": "Section 1798.121", │
│          "priority": "HIGH"               │
│        },                                 │
│        ...                                │
│      ],                                   │
│      "session_id": "privacy_analysis..."  │
│    }                                      │
│  }                                        │
└───────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│  STORED DATA STRUCTURES                                         │
└─────────────────────────────────────────────────────────────────┘

memory_store = {
  "privacy_analysis_Stripe_20251202_185505": [
    {
      "id": "uuid-1",
      "text": "Starting analysis: Stripe",
      "timestamp": "2025-12-02T18:55:05"
    },
    {
      "id": "uuid-2",
      "text": "Gap Analysis Complete\n\n23 gaps found...",
      "timestamp": "2025-12-02T18:57:03"
    }
  ]
}

token_usage_store = [
  {
    "timestamp": "2025-12-02T18:56:45",
    "query": "Gap analysis: Stripe",
    "model_used": "gpt-4o",
    "tokens_prompt": 6034,
    "tokens_completion": 200,
    "tokens_total": 6234
  }
]

gap_analysis_store = [
  {
    "timestamp": "2025-12-02T18:57:03",
    "company": "Stripe",
    "gaps": [
      {
        "description": "Missing: Right to Limit Sensitive PI",
        "ccpa_reference": "Section 1798.121",
        "priority": "HIGH",
        "recommendation": "Add disclosure stating..."
      },
      ...
    ],
    "session_id": "privacy_analysis_Stripe_20251202_185505"
  }
]


┌─────────────────────────────────────────────────────────────────┐
│  DEBUG ENDPOINTS - AUDIT TRAIL QUERY                            │
└─────────────────────────────────────────────────────────────────┘

GET http://localhost:8080/debug/memory
└─► Returns all conversation logs (by session)

GET http://localhost:8080/debug/tokens
└─► Returns token usage & cost tracking
    Example output:
    {
      "total_tokens_today": 24,847,
      "total_cost_today": "$2.48",
      "analyses_run": 4
    }

GET http://localhost:8080/debug/gaps
└─► Returns all gap analyses performed
    Example output:
    {
      "total_analyses": 4,
      "companies": ["Stripe", "Yahoo", "Audit Caddie", "Acme Corp"],
      "total_gaps_found": 87,
      "avg_gaps_per_company": 21.75
    }

GET http://localhost:8080/health
└─► Server health check
    {
      "status": "healthy",
      "service": "Privacy MCP Server",
      "uptime": "3h 45m"
    }


┌─────────────────────────────────────────────────────────────────┐
│  WHY MCP MATTERS FOR COMPLIANCE                                 │
└─────────────────────────────────────────────────────────────────┘

✅ AUDIT TRAIL
   Every analysis is logged with:
   • Who: Session ID
   • When: Timestamp
   • What: Analysis text, gaps found
   • How: Model used, tokens consumed
   • Cost: API spend tracking

✅ REPRODUCIBILITY
   Can retrieve full analysis context:
   • Input data (company, policy URL)
   • Processing steps
   • Output (gaps, recommendations)
   • Confidence scores

✅ COST TRACKING
   Monitor API spend:
   • Per analysis
   • Per day/month
   • Budget alerts
   • Cost allocation

✅ COMPLIANCE DOCUMENTATION
   Required for regulated industries:
   • SOC 2 audits
   • ISO 27001
   • Internal compliance reviews

✅ QUALITY MONITORING
   Track system performance:
   • Gap detection rates
   • False positive trends
   • Model accuracy over time
```

---

## DIAGRAM 5: Component Interaction (For Chapter 5 - System Design)

**Use Case:** Understanding how all files work together

```
┌──────────────────────────────────────────────────────────────────┐
│                  FILE/MODULE INTERACTION DIAGRAM                  │
│                  How Python Files Work Together                  │
└──────────────────────────────────────────────────────────────────┘


[USER INTERACTION]
        │
        │ $ python run_privacy_analysis.py https://stripe.com
        │
        ▼
┌─────────────────────────────────────────┐
│  run_privacy_analysis.py                │
│  (Main Orchestrator)                    │
│                                         │
│  def run_complete_privacy_analysis():   │
│      1. Parse URL                       │
│      2. Call scraper                    │
│      3. Call RAG/MCP analyzer           │
│      4. Display results                 │
└────────────┬────────────────────────────┘
             │
             │ imports & calls
             │
             ├────────────────────┬────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
┌──────────────────────┐  ┌──────────────────┐  ┌────────────────┐
│ privacy_policy_      │  │ privacy_rag_     │  │ markdown_to_   │
│ scraper.py           │  │ mcp.py           │  │ docx.py        │
│                      │  │                  │  │                │
│ Functions:           │  │ Functions:       │  │ Function:      │
│ • find_privacy_link()│  │ • load_ccpa_     │  │ • convert()    │
│ • download_as_pdf()  │  │   framework()    │  │                │
│ • scrape_privacy_    │  │ • load_policy()  │  │ Converts:      │
│   policy()           │  │ • perform_gap_   │  │ MD → DOCX      │
│                      │  │   analysis()     │  │                │
│ Dependencies:        │  │ • generate_      │  │ Dependencies:  │
│ • BeautifulSoup      │  │   report()       │  │ • python-docx  │
│ • Playwright         │  │                  │  │ • markdown     │
│ • requests           │  │ Dependencies:    │  └────────────────┘
│                      │  │ • LangChain      │
│ Returns:             │  │ • ChromaDB       │
│ PDF file path        │  │ • OpenAI         │
└──────────┬───────────┘  │ • HuggingFace    │
           │              │ • PyPDF2         │
           │              │                  │
           │              │ Returns:         │
           │              │ Analysis results │
           │              └────────┬─────────┘
           │                       │
           │                       │ makes API calls to
           │                       │
           │                       ▼
           │              ┌─────────────────────────┐
           │              │ privacy_mcp_server.py   │
           │              │ (Separate Process)      │
           │              │                         │
           │              │ FastAPI App:            │
           │              │ • POST /mcp             │
           │              │ • GET /debug/*          │
           │              │ • GET /health           │
           │              │                         │
           │              │ Stores:                 │
           │              │ • memory_store {}       │
           │              │ • token_usage_store []  │
           │              │ • gap_analysis_store [] │
           │              │                         │
           │              │ Dependencies:           │
           │              │ • FastAPI               │
           │              │ • Uvicorn               │
           │              │ • Pydantic              │
           │              └─────────────────────────┘
           │
           │
           ▼
[DATA FILES]

┌─────────────────────────────────────────────────────────────────┐
│  CONFIGURATION & DATA FILES                                     │
└─────────────────────────────────────────────────────────────────┘

.env
├─ OPENAI_API_KEY=sk-...
└─ MCP_API_KEY=secret-key

CCPA_CPRA_Framework.csv
├─ 35 rows of CCPA requirements
├─ Columns: Category, Requirement, Body, Reference
└─ Used by: privacy_rag_mcp.py → load_ccpa_framework()

requirements.txt
├─ langchain==0.1.0
├─ chromadb==0.4.18
├─ openai==1.3.0
├─ sentence-transformers==2.2.2
├─ playwright==1.40.0
├─ beautifulsoup4==4.12.2
├─ python-docx==1.1.0
└─ ... (14 total dependencies)


┌─────────────────────────────────────────────────────────────────┐
│  GENERATED FILES & DIRECTORIES                                  │
└─────────────────────────────────────────────────────────────────┘

./vectordb_ccpa/
├─ Created by: ChromaDB (persistent)
├─ Contains: Embeddings for 35 CCPA requirements
└─ Size: ~2 MB

./vectordb_privacy_policies/
├─ Created by: ChromaDB (persistent)
├─ Contains: Embeddings for company policy chunks
├─ Cleared between analyses (optional)
└─ Size: ~5-10 MB per company

*.pdf (Downloaded policies)
├─ stripe.com_privacy_policy.pdf (1.1 MB)
├─ yahoo.com_privacy_policy.pdf (23 MB)
└─ auditcaddie.com_privacy_policy.pdf (106 KB)

*_Gap_Analysis_*.md (Reports)
├─ Stripe_CCPA_Gap_Analysis_20251202_185505.md (5 KB)
└─ Audit_Caddie_CCPA_Gap_Analysis_20251202_140343.md (5 KB)

*_Gap_Analysis_*.docx (Word Reports)
├─ Stripe_CCPA_Gap_Analysis_20251202_185505.docx (38 KB)
└─ Audit_Caddie_CCPA_Gap_Analysis_20251202_140343.docx (29 KB)


┌─────────────────────────────────────────────────────────────────┐
│  EXECUTION SEQUENCE                                             │
└─────────────────────────────────────────────────────────────────┘

Terminal 1 (MCP Server):
$ python privacy_mcp_server.py
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://127.0.0.1:8080
✓ Privacy MCP Server ready

Terminal 2 (Analysis):
$ python run_privacy_analysis.py https://stripe.com "Stripe"

[run_privacy_analysis.py]
    │
    ├──► from privacy_policy_scraper import scrape_privacy_policy
    │    scrape_privacy_policy("https://stripe.com")
    │    └──► Returns: "stripe.com_privacy_policy.pdf"
    │
    ├──► from privacy_rag_mcp import analyze_policy_documents
    │    analyze_policy_documents(
    │        privacy_pdf_path="stripe.com_privacy_policy.pdf",
    │        company_name="Stripe"
    │    )
    │    │
    │    ├──► load_ccpa_framework()
    │    │    └──► ChromaDB: vectordb_ccpa/
    │    │
    │    ├──► load_policy_documents()
    │    │    └──► ChromaDB: vectordb_privacy_policies/
    │    │
    │    ├──► perform_gap_analysis()
    │    │    ├──► RAG retrieval (CCPA + Policy)
    │    │    ├──► OpenAI API call (gpt-4o)
    │    │    └──► MCP tracking (HTTP POST to :8080)
    │    │
    │    └──► generate_gap_report()
    │         ├──► Create markdown report
    │         └──► Call markdown_to_docx.convert()
    │
    └──► Display results & exit

Output:
✓ Analysis Complete
📄 Report: Stripe_CCPA_Gap_Analysis_20251202_185505.md
📄 Word: Stripe_CCPA_Gap_Analysis_20251202_185505.docx
🔗 Session: privacy_analysis_Stripe_20251202_185505
💰 Tokens: 6,234 ($0.62)
```

---

## Summary: Which Diagram for Which Chapter

| Chapter | Diagram | Purpose |
|---------|---------|---------|
| **0 (Intro)** | Diagram 1 (High-Level Overview) | Show what the system does |
| **1 (AI in Security)** | Diagram 1 + Real stats | Connect to business value |
| **2 (RAG Basics)** | Diagram 2 (Technical Architecture) | Explain RAG components |
| **2 (MCP Explained)** | Diagram 4 (MCP Protocol) | Explain audit tracking |
| **3 (Gap Analysis)** | Diagram 3 (Data Flow Sequence) | Step-by-step walkthrough |
| **5 (System Design)** | Diagram 5 (Component Interaction) | How files work together |

---

**Files in GitHub Repo:**
- `privacy_policy_scraper.py` - Web scraping (Playwright + BeautifulSoup)
- `privacy_rag_mcp.py` - RAG system (LangChain + ChromaDB + OpenAI)
- `privacy_mcp_server.py` - MCP server (FastAPI + JSON-RPC)
- `run_privacy_analysis.py` - Orchestrator (main entry point)
- `markdown_to_docx.py` - Report converter (python-docx)
- `CCPA_CPRA_Framework.csv` - Knowledge base (35 CCPA requirements)
- `requirements.txt` - Dependencies (14 packages)
- `.env` - API keys (OpenAI + MCP)

**Live Example:** https://github.com/Blodgic/CADDIE_RAG_MPC
