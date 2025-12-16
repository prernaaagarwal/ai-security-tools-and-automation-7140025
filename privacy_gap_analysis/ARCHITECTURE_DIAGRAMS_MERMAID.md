# Privacy Gap Analysis System - Mermaid Diagrams

**Renderable in GitHub, VS Code, and diagram tools**

---

## Diagram 1: High-Level System Flow

```mermaid
graph TD
    A[Company URL Input] --> B[Privacy Policy Scraper<br/>Playwright]
    B --> C[PDF Download<br/>company_privacy_policy.pdf]
    C --> D[Text Extraction<br/>PyPDF2]
    D --> E[Text Chunking]

    F[CCPA Framework CSV<br/>35 Requirements] --> G[Vector Database<br/>vectordb_ccpa]
    E --> H[Vector Database<br/>vectordb_privacy_policies]

    G --> I[RAG Retrieval<br/>Semantic Search]
    H --> I

    I --> J[GPT-4o Analysis<br/>Temperature: 0.3]
    J --> K[Gap Detection<br/>Recommendations]

    K --> L[MCP Tracking<br/>Audit Trail]
    K --> M[Report Generation<br/>Markdown + Word]

    M --> N[Final Output<br/>Gap Analysis Report]

    style A fill:#e1f5ff
    style N fill:#d4edda
    style J fill:#fff3cd
    style L fill:#f8d7da
```

---

## Diagram 2: RAG Architecture Detail

```mermaid
graph LR
    subgraph "Knowledge Bases"
        A1[CCPA Framework<br/>CSV File]
        A2[Privacy Policy<br/>PDF File]
    end

    subgraph "Embedding Pipeline"
        B1[Text → Chunks]
        B2[HuggingFace Embeddings<br/>all-MiniLM-L12-v2]
        B3[384-dim Vectors]
    end

    subgraph "Vector Storage"
        C1[ChromaDB<br/>vectordb_ccpa]
        C2[ChromaDB<br/>vectordb_privacy]
    end

    subgraph "RAG Retrieval"
        D1[Query: CCPA Requirements]
        D2[Semantic Search<br/>Cosine Similarity]
        D3[Top-k Results<br/>k=35 for CCPA<br/>k=50 for Policy]
    end

    subgraph "LLM Processing"
        E1[Context Building<br/>8000+ tokens]
        E2[GPT-4o API<br/>temp=0.3]
        E3[Gap Analysis Output]
    end

    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    B3 --> C2

    C1 --> D1
    C2 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> E1
    E1 --> E2
    E2 --> E3

    style E2 fill:#fff3cd
    style C1 fill:#e1f5ff
    style C2 fill:#e1f5ff
```

---

## Diagram 3: MCP Server Architecture

```mermaid
graph TD
    subgraph "MCP Server (Port 8080)"
        A[FastAPI Application]

        A --> B[JSON-RPC Endpoint<br/>POST /mcp]
        A --> C[Health Check<br/>GET /health]
        A --> D[Debug Endpoints<br/>GET /debug/*]

        B --> E1[insert_memory]
        B --> E2[insert_token_usage]
        B --> E3[insert_gap_analysis]
        B --> E4[insert_confidence]
        B --> E5[fetch_memory]

        E1 --> F1[(Memory Store<br/>Sessions)]
        E2 --> F2[(Token Store<br/>Usage Tracking)]
        E3 --> F3[(Gap Store<br/>Analysis Results)]
        E4 --> F4[(Confidence Store<br/>Scores)]
    end

    subgraph "Client (privacy_rag_mcp.py)"
        G[Gap Analysis Process]
        G --> H1[Log Session Start]
        G --> H2[Track Tokens]
        G --> H3[Store Gaps]
        G --> H4[Record Confidence]

        H1 -.HTTP POST.-> E1
        H2 -.HTTP POST.-> E2
        H3 -.HTTP POST.-> E3
        H4 -.HTTP POST.-> E4
    end

    style A fill:#d4edda
    style F1 fill:#f8d7da
    style F2 fill:#f8d7da
    style F3 fill:#f8d7da
    style F4 fill:#f8d7da
```

---

## Diagram 4: End-to-End Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant S as Scraper
    participant R as RAG System
    participant M as MCP Server
    participant G as GPT-4o API
    participant O as Output

    U->>S: python run_privacy_analysis.py https://stripe.com
    S->>S: Find privacy policy link
    S->>S: Download as PDF (Playwright)
    S->>R: stripe.com_privacy_policy.pdf

    R->>R: Extract text (PyPDF2)
    R->>R: Chunk text (127 chunks)
    R->>R: Load CCPA framework (35 docs)
    R->>R: Create embeddings (all-MiniLM)
    R->>R: Store in ChromaDB

    R->>M: POST /mcp (insert_memory)
    M-->>R: Session logged

    R->>R: Retrieve CCPA requirements (k=35)
    R->>R: Retrieve policy chunks (k=50)
    R->>R: Build context (8245 tokens)

    R->>G: POST /chat/completions
    Note over G: Temperature: 0.3<br/>Max tokens: 2000
    G-->>R: Gap analysis (23 gaps)

    R->>M: POST /mcp (insert_token_usage)
    M-->>R: Tokens logged (6234)

    R->>M: POST /mcp (insert_gap_analysis)
    M-->>R: Gaps stored

    R->>O: Generate markdown report
    R->>O: Convert to Word DOCX

    O->>U: Stripe_CCPA_Gap_Analysis.md
    O->>U: Stripe_CCPA_Gap_Analysis.docx
    U->>M: GET /debug/gaps (verify)
```

---

## Diagram 5: Component Dependencies

```mermaid
graph TD
    subgraph "Main Orchestrator"
        A[run_privacy_analysis.py]
    end

    subgraph "Core Modules"
        B[privacy_policy_scraper.py]
        C[privacy_rag_mcp.py]
        D[privacy_mcp_server.py]
        E[markdown_to_docx.py]
    end

    subgraph "External Services"
        F[OpenAI API<br/>gpt-4o]
        G[Playwright Browser<br/>Chromium]
    end

    subgraph "Storage"
        H[(ChromaDB<br/>vectordb_ccpa)]
        I[(ChromaDB<br/>vectordb_privacy)]
        J[(MCP Stores<br/>In-Memory)]
    end

    subgraph "Data Files"
        K[CCPA_CPRA_Framework.csv]
        L[.env<br/>API Keys]
        M[requirements.txt]
    end

    A -->|imports| B
    A -->|imports| C
    A -->|imports| E

    B -->|uses| G
    B -->|writes| N[*.pdf files]

    C -->|uses| F
    C -->|reads| K
    C -->|writes| H
    C -->|writes| I
    C -->|calls| D
    C -->|uses| E

    D -->|stores| J

    C -.reads.-> L
    D -.reads.-> L

    style A fill:#d4edda
    style F fill:#fff3cd
    style D fill:#f8d7da
```

---

## Diagram 6: Data Flow Timeline

```mermaid
gantt
    title Privacy Gap Analysis Timeline
    dateFormat ss
    axisFormat %S sec

    section Scraping
    Find privacy link    :a1, 00, 5s
    Download PDF         :a2, after a1, 8s

    section Extraction
    Parse PDF            :b1, after a2, 3s
    Chunk text           :b2, after b1, 1s

    section Vector DB
    Load CCPA framework  :c1, after b2, 2s
    Embed policy chunks  :c2, after c1, 5s

    section RAG
    Retrieve CCPA        :d1, after c2, 1s
    Retrieve policy      :d2, after d1, 1s
    Build context        :d3, after d2, 1s

    section AI Analysis
    GPT-4o API call      :e1, after d3, 15s
    Parse response       :e2, after e1, 1s

    section MCP Tracking
    Log session          :f1, after e2, 1s
    Log tokens           :f2, after f1, 1s
    Log gaps             :f3, after f2, 1s

    section Report
    Generate markdown    :g1, after f3, 2s
    Convert to Word      :g2, after g1, 3s
```

---

## Diagram 7: Security Architecture

```mermaid
graph TD
    subgraph "External Inputs (Untrusted)"
        A[User URL Input]
        B[Company Website]
        C[Privacy Policy PDF]
    end

    subgraph "Input Validation Layer"
        D[URL Validation<br/>- Scheme check: http/https<br/>- Domain validation<br/>- No javascript: schemes]
        E[PDF Validation<br/>- File type check<br/>- Size limits<br/>- Malware scan option]
    end

    subgraph "Processing Layer"
        F[Sandboxed Browser<br/>Playwright Chromium<br/>- No extensions<br/>- Isolated context]
        G[Text Extraction<br/>PyPDF2<br/>- Limited memory<br/>- Timeout controls]
    end

    subgraph "AI Safety Layer"
        H[Prompt Injection Defense<br/>- Strong system prompt<br/>- Temperature: 0.3<br/>- Output validation]
        I[RAG Grounding<br/>- Only cite retrieved docs<br/>- No hallucinations<br/>- Verify CCPA sections]
    end

    subgraph "API Security"
        J[API Key Management<br/>- .env files<br/>- Never committed<br/>- Environment vars]
        K[Rate Limiting<br/>- Max requests/min<br/>- Budget caps<br/>- Cost tracking MCP]
    end

    subgraph "Audit & Compliance"
        L[MCP Audit Trail<br/>- All actions logged<br/>- Timestamps<br/>- Session IDs<br/>- Token usage]
        M[Access Control<br/>- API key auth<br/>- Endpoint protection<br/>- RBAC optional]
    end

    A --> D
    B --> D
    C --> E

    D --> F
    E --> G

    F --> H
    G --> H
    H --> I

    I --> J
    J --> K

    K --> L
    L --> M

    style A fill:#f8d7da
    style B fill:#f8d7da
    style C fill:#f8d7da
    style H fill:#fff3cd
    style I fill:#fff3cd
    style L fill:#d4edda
```

---

## How to Use These Diagrams

### Rendering Options:

1. **GitHub** - Mermaid renders automatically in `.md` files
2. **VS Code** - Install "Markdown Preview Mermaid Support" extension
3. **Mermaid Live Editor** - https://mermaid.live/
4. **Export to PNG/SVG** - Use mermaid-cli or online editor
5. **PowerPoint** - Screenshot or use mermaid-to-pptx tools

### For LinkedIn Learning Slides:

1. Copy diagram code to Mermaid Live Editor
2. Adjust theme/colors as needed
3. Export as PNG (high resolution)
4. Import into PowerPoint slide
5. Add annotations and labels

### Recommended Diagrams per Chapter:

| Chapter | Primary Diagram | Secondary Diagram |
|---------|-----------------|-------------------|
| **0: Intro** | Diagram 1 (High-Level Flow) | Diagram 4 (Sequence) |
| **1: AI Security** | Diagram 1 + Stats | Diagram 7 (Security) |
| **2: RAG Basics** | Diagram 2 (RAG Architecture) | Diagram 5 (Dependencies) |
| **2: MCP** | Diagram 3 (MCP Server) | Diagram 4 (Sequence) |
| **3: Gap Analysis** | Diagram 4 (Sequence) | Diagram 6 (Timeline) |
| **5: System Design** | Diagram 5 (Dependencies) | Diagram 7 (Security) |

---

**Repository:** https://github.com/Blodgic/CADDIE_RAG_MPC
