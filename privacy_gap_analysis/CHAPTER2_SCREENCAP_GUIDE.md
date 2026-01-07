# Chapter 2 Screencap Guide - RAG Demonstration

##  Overview

This guide helps you record the RAG (Retrieval-Augmented Generation) demonstration for LinkedIn Learning Chapter 2.

You have **two demo scripts** available:

1. **`demo_retrieval_terminal.py`** - Simulates Python REPL (matches your outline)
2. **`demo_rag_retrieval.py`** - Full interactive demo with 3 phases

---

##  Pre-Screencap Checklist

### Terminal Setup

```bash
# 1. Navigate to project
cd privacy_gap_analysis/scripts

# 2. Ensure MCP server is NOT running (to avoid conflicts)
# Kill if running: Ctrl+C or pkill -f privacy_mcp_server

# 3. Clear terminal for clean recording
clear

# 4. Test demo scripts once before recording
python demo_retrieval_terminal.py
python demo_rag_retrieval.py --quick
```

### Screen Layout

**Recommended:**
- **Left**: Code editor showing `privacy_rag_mcp.py`
- **Right**: Terminal for running demos

**OR:**

- **Full screen**: Terminal only, switch to code with screen share

---

##  Option 1: Terminal REPL Demo (Recommended)

**Best for:** Showing the exact Python commands from your course outline

### Recording Steps

1. **Show the code first:**
   - Open `privacy_rag_mcp.py` in your editor
   - Highlight lines 49-73 (indexing)
   - Highlight lines 469-474 (retrieval)
   - Highlight lines 479-518 (generation)

2. **Switch to terminal:**
   ```bash
   clear
   python demo_retrieval_terminal.py
   ```

3. **What the audience sees:**
   ```
   >>> from privacy_rag_mcp import load_ccpa_framework
    Imported load_ccpa_framework

   >>> vectordb = load_ccpa_framework()
    Vector database loaded

   >>> retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    Retriever created (will return top 3 results)

   >>> results = retriever.invoke("right to delete personal information")
    Retrieved 3 documents

   >>> for doc in results:
   ...     print(doc.page_content[:200])

   [Document 1]
   Category: Consumer Rights
   Requirement: Right to Delete
   Consumers have the right to request deletion of their personal information...
   ```

4. **Narration while recording:**
   - "Let's see this in action..."
   - "First, we import the function to load our CCPA framework"
   - "This loads all 34 CCPA requirements into a vector database"
   - "Now we create a retriever that will find the top 3 most relevant items"
   - "Let's search for 'right to delete personal information'"
   - "Notice it found exactly the CCPA sections about deletion rights"
   - "This is semantic search - it understood the MEANING, not just keywords"

**Runtime:** ~1 minute

**Output:** Clean, formatted, matches your course outline exactly

---

##  Option 2: Full Interactive Demo

**Best for:** Showing all 3 RAG phases step-by-step

### Recording Steps

1. **Run interactive mode:**
   ```bash
   clear
   python demo_rag_retrieval.py
   ```

2. **What happens:**
   - Shows intro screen
   - Prompts you to press Enter between phases
   - Phase 1: INDEXING (loads vector DB)
   - Phase 2: RETRIEVAL (shows 3 search examples)
   - Phase 3: GENERATION (shows GPT-4 context)

3. **Narration during pauses:**
   - **Phase 1:** "First, we need to index our CCPA requirements..."
   - **Phase 2:** "Now let's retrieve relevant requirements for different queries..."
   - **Phase 3:** "Finally, this context gets sent to GPT-4 for analysis..."

4. **Edit video:** Cut out the "Press Enter" pauses in post-production

**Runtime:** ~3-4 minutes (can trim to 2 minutes)

**Output:** Comprehensive, shows full workflow

---

##  Option 3: Quick Non-Interactive Demo

**Best for:** Screen recording without pauses

### Recording Steps

```bash
clear
python demo_rag_retrieval.py --quick
```

**Runtime:** ~1.5 minutes

**Output:** Runs through all 3 phases automatically, no pauses

**Narration:** Do voice-over in post-production

---

##  Suggested Script for Narration

### Introduction
> "Now let's see how RAG works in our privacy compliance tool. RAG stands for Retrieval-Augmented Generation, and it's the technique that lets us combine a knowledge base with GPT-4's reasoning."

### Phase 1: Indexing
> "First, we load our CCPA requirements into a vector database. We're using ChromaDB and the all-MiniLM-L12-v2 embedding model. This converts each requirement into a mathematical representation that captures its meaning."

### Phase 2: Retrieval
> "Now when we query for 'right to delete personal information,' the system doesn't just look for those exact words. It performs semantic search - finding requirements that MEAN the same thing, even if worded differently. Look how it retrieved the exact CCPA Section 1798.105 about deletion rights."

### Phase 3: Generation
> "Finally, this retrieved context gets sent to GPT-4 along with the company's privacy policy. GPT-4 uses both pieces of information to perform an accurate gap analysis. This is the power of RAG - combining retrieval precision with GPT-4's analytical abilities."

---

##  Code Sections to Highlight

### In `privacy_rag_mcp.py`:

**1. INDEXING (Lines 49-79):**
```python
def load_ccpa_framework():
    ccpa_df = pd.read_csv("CCPA_CPRA_Framework.csv")

    documents_ccpa = DataFrameLoader(ccpa_df, page_content_column='Body').load()

    vectordb_ccpa = Chroma.from_documents(
        documents=documents_ccpa,
        embedding=embedding_model,  # all-MiniLM-L12-v2
        persist_directory=ccpa_dir,
    )
```

**Highlight:**
- Line 63: Reading CSV
- Line 71: Converting to LangChain documents
- Lines 73-77: Creating vector database

**2. RETRIEVAL (Lines 469-474):**
```python
ccpa_retriever = vectordb_ccpa.as_retriever(search_kwargs={"k": 35})
ccpa_requirements = ccpa_retriever.invoke("CCPA CPRA requirements")
```

**Highlight:**
- Line 469: Creating retriever with k=35
- Line 470: Invoking retrieval

**3. GENERATION (Lines 479-518):**
```python
analysis_query = f"""
CCPA/CPRA REQUIREMENTS:
{ccpa_context}

COMPANY PRIVACY POLICY:
{policy_context}

Perform a comprehensive gap analysis...
"""

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.3,
)
```

**Highlight:**
- Lines 479-492: Building prompt with retrieved context
- Lines 511-517: Calling GPT-4

---

##  Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
cd privacy_gap_analysis/scripts
python demo_retrieval_terminal.py
```
(Must be in the scripts directory)

### Issue: "CCPA_CPRA_Framework.csv not found"
**Solution:**
Check that file is in `data/frameworks/CCPA_CPRA_Framework.csv`

### Issue: Demo runs too slow
**Solution:**
Use `--quick` mode:
```bash
python demo_rag_retrieval.py --quick
```

### Issue: Output too verbose
**Solution:**
Redirect stderr to hide deprecation warnings:
```bash
python demo_retrieval_terminal.py 2>/dev/null
```

---

##  Recommended Recording Flow

### 5-Minute Segment:

1. **Intro (30 seconds)**
   - Explain what RAG is
   - Show the 3 phases diagram

2. **Code Walkthrough (1.5 minutes)**
   - Show indexing code
   - Show retrieval code
   - Show generation code

3. **Live Demo (2 minutes)**
   - Run `demo_retrieval_terminal.py`
   - Explain output as it appears

4. **Wrap-up (1 minute)**
   - Recap the 3 phases
   - Explain why RAG is powerful
   - Preview next chapter

---

##  Post-Production Tips

1. **Add annotations:**
   - Arrow pointing to "k=3" → "Retrieves top 3 results"
   - Highlight retrieved CCPA sections
   - Circle similarity scores if visible

2. **Speed up:**
   - 1.5x speed during vector DB loading
   - Normal speed for retrieval results

3. **Add B-roll:**
   - Diagram of RAG workflow
   - Vector embedding visualization

---

##  Quick Reference Commands

```bash
# Terminal REPL demo (recommended)
python demo_retrieval_terminal.py

# Full interactive demo
python demo_rag_retrieval.py

# Quick auto-run demo
python demo_rag_retrieval.py --quick

# Help
python demo_rag_retrieval.py --help
```

---

##  Expected Output Summary

**Indexing:**
-  "Vector database created!"
-  "All CCPA requirements indexed"
-  "102 requirements stored"

**Retrieval:**
-  "Query: right to delete personal information"
-  "Found 3 relevant requirements"
-  Shows CCPA Section 1798.105 (Right to Delete)

**Generation:**
-  "Context prepared (916 characters)"
-  Shows prompt structure
-  Demonstrates what GPT-4 receives

---

**Good luck with your recording! **
