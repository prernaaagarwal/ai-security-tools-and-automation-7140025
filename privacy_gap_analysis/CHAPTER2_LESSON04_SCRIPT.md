# Chapter 2, Lesson 04 - Complete Narration Script
## "MCP + RAG Integration: Semantic Search with Audit Trails"

---

## COMPLETE NARRATION SCRIPT

### [INTRO - 30 seconds]

> "In this lesson, we're bringing together the two technologies we've learned about: RAG for semantic search and MCP for audit trails.
>
> We're going to perform a simple query: 'What does CCPA say about consumers' right to delete personal information?' But we're not just getting an answer - we're logging the entire process to create a complete audit trail.
>
> This is the core loop of our privacy gap analysis tool. Let's see it in action."

---

### [SETUP - 20 seconds]

**[SCREEN: Show split terminal - MCP server on left, empty terminal on right]**

> "First, I need to make sure the MCP server is running. I started it in the left terminal - you can see it's listening on port 8080.
>
> On the right, I'll run our demo script that simulates a Python REPL session, showing exactly what you'd type to perform this workflow."

---

### [DEMO PART 1: Verify MCP Server - 30 seconds]

**[SCREEN: Right terminal - Run demo script]**

```bash
python 02_04_demo_mcp_rag_integration.py --quick
```

**[OUTPUT APPEARS]**
```
================================================================================
  MCP + RAG Integration Demo
================================================================================

This demo shows how RAG and MCP work together:

  1. Start MCP server (audit tracking)
  2. Load CCPA framework into vector database (RAG indexing)
  3. Query for specific requirement (RAG retrieval)
  4. Log query to MCP (audit trail)

GOAL: Query 'What does CCPA say about Right to Delete?'
      and track the entire process in the audit trail.

--- STEP 1: Verify MCP Server is Running ---

Checking MCP server at http://localhost:8080...

 MCP Server Status: RUNNING
   Service: Privacy Policy MCP Server
   Total Sessions: 3
   Total Analyses: 2
```

> "Step 1 - verify the MCP server is running. The script checks the health endpoint and confirms the server is ready. Notice it shows existing session count - this is persistent data from previous analyses."

---

### [DEMO PART 2: Load CCPA Framework - 45 seconds]

**[OUTPUT CONTINUES]**
```
--- STEP 2: Load CCPA Framework into Vector Database (RAG) ---

Importing privacy_rag_mcp module...
>>> from privacy_rag_mcp import load_ccpa_framework

>>> vectordb_ccpa = load_ccpa_framework()

Loading embedding model: all-MiniLM-L12-v2...
 Model loaded

Loading CCPA/CPRA Framework from CSV...
 CCPA/CPRA requirements stored in ChromaDB

RAG system ready for queries!
```

> "Step 2 - load the CCPA framework into our vector database. This is the indexing phase of RAG.
>
> We're loading our CCPA_CPRA_Framework.csv - that's 102 regulatory requirements. Each one gets converted to a vector embedding using the all-MiniLM-L12-v2 model.
>
> Once loaded, ChromaDB can perform semantic similarity searches. This means we can search by meaning, not just keywords."

---

### [DEMO PART 3: Perform RAG Query - 90 seconds]

**[OUTPUT CONTINUES]**
```
--- STEP 3: Query RAG for 'Right to Delete' Information ---

Query: 'What does CCPA say about consumers' right to delete personal information?'

>>> retriever = vectordb_ccpa.as_retriever(search_kwargs={'k': 5})
>>> results = retriever.invoke('What does CCPA say about consumers' right to delete...')

 Found 5 relevant CCPA sections

Top 3 Results:

  [1] Right to Delete
      Category: Consumer Rights
      Reference: CCPA Section 1798.105
      Consumers have the right to request deletion of personal information
      collected from them. Businesses must delete upon request unless an...

  [2] Verification and Response
      Category: Verification and Response
      Reference: CCPA Section 1798.130
      Businesses must respond to consumer requests within 45 days, with
      option to extend another 45 days if needed...

  [3] Exceptions to Deletion
      Category: Consumer Rights
      Reference: CCPA Section 1798.105(d)
      Businesses may deny deletion requests when necessary to complete
      transactions, detect security incidents...
```

> "Step 3 - perform the query using RAG retrieval.
>
> Look at what happened. We created a retriever with k=5, meaning 'find the 5 most relevant sections.'
>
> The query is in natural language: 'What does CCPA say about consumers' right to delete personal information?'
>
> RAG converted this to a vector embedding, then searched our CCPA database for the most similar vectors.
>
> Result 1 is perfect - it's the exact section on Right to Delete, CCPA Section 1798.105.
>
> But notice Result 2 and Result 3 are also relevant. Result 2 covers response timeframes - if you're implementing deletion rights, you need to know the deadline. Result 3 covers exceptions - when you can legally refuse a deletion request.
>
> This is the power of semantic search. We didn't just search for the keyword 'delete' - we found contextually related requirements."

---

### [DEMO PART 4: Log to MCP - 60 seconds]

**[OUTPUT CONTINUES]**
```
--- STEP 4: Log Query to MCP Audit Trail ---

Creating session ID: rag_query_20251207_143521

>>> mcp_url = 'http://localhost:8080/mcp'
>>> payload = {
...     'jsonrpc': '2.0',
...     'method': 'insert_memory',
...     'params': {
...         'session_id': 'rag_query_20251207_143521',
...         'text': 'Query: What does CCPA say about consumers...'
...     },
...     'id': 1
... }

>>> response = requests.post(mcp_url, json=payload)
>>> response.json()

  {'jsonrpc': '2.0', 'result': {'status': 'success'}, 'id': 1}

 Query logged successfully!
```

> "Step 4 - log this query to the MCP server for audit trail.
>
> We create a unique session ID with a timestamp: rag_query_20251207_143521.
>
> Then we construct a JSON-RPC payload. The method is 'insert_memory' - this logs to the MCP memory table.
>
> The params include the session ID and the text we want to log. We're logging the query itself, the number of results found, and a preview of the top result.
>
> We send this to the MCP server using a POST request. The server responds with status: success.
>
> This is critical for compliance workflows. We now have a permanent record that this query was run, when it was run, and what was retrieved."

---

### [DEMO PART 5: Verify Audit Trail - 45 seconds]

**[OUTPUT CONTINUES]**
```
--- STEP 5: Verify Audit Trail in MCP ---

Checking MCP memory logs at http://localhost:8080/debug/memory

 Audit trail entry found:

  Session ID: rag_query_20251207_143521
  Timestamp: 2025-12-07T14:35:21.123456
  Text (preview): Query: What does CCPA say about consumers' right to delete personal information?
Results: 5 CCPA sections retrieved...

 Query successfully logged to audit trail!
```

> "Step 5 - verify the audit trail.
>
> We query the MCP debug endpoint at /debug/memory. This returns all logged sessions.
>
> We find our session by the session ID. And here it is - the query we just ran, with a timestamp, and the full text we logged.
>
> This is now permanent data. If an auditor asks, 'Show me all queries run against the CCPA framework in December,' we can retrieve this from the MCP database."

---

### [BROWSER DEMO - 45 seconds]

**[SCREEN: Switch to browser, navigate to localhost:8080/debug/memory]**

> "Let me show you this in the browser as well."

**[SCREEN: Show JSON output]**
```json
[
  {
    "id": 8,
    "session_id": "rag_query_20251207_143521",
    "text": "Query: What does CCPA say about consumers' right to delete personal information?\nResults: 5 CCPA sections retrieved\n\nTop Result: Category: Consumer Rights\nRequirement: Right to Delete\nConsumers have the right to request deletion of personal information...",
    "timestamp": "2025-12-07T14:35:21.123456"
  },
  {
    "id": 7,
    "session_id": "rag_query_20251207_142015",
    "text": "Query: What are the notice requirements for data collection?\nResults: 4 CCPA sections retrieved...",
    "timestamp": "2025-12-07T14:20:15.789012"
  }
]
```

> "Here's the raw JSON from the MCP server. You can see our query at the top - ID 8, session ID with timestamp, the full query text, and the results preview.
>
> Below it is a previous query from earlier today - notice requirements. Every query is logged, creating a complete audit trail."

---

### [RECAP - 60 seconds]

**[SCREEN: Show recap slide or return to terminal]**

> "Let me recap what we just demonstrated.
>
> We showed the core loop of our privacy gap analysis tool:
>
> **First**, we loaded the CCPA framework into a vector database. This is RAG indexing - converting regulatory text into searchable embeddings.
>
> **Second**, we performed a semantic search query. We asked in natural language, 'What does CCPA say about right to delete?' RAG found the 5 most relevant sections, ranked by semantic similarity.
>
> **Third**, we logged the query to the MCP server. This created a permanent audit trail with session ID, timestamp, and query details.
>
> **And fourth**, we verified the audit trail through the debug endpoint. The data is now stored and queryable.
>
> This is the foundation for automated privacy policy gap analysis. When we analyze a company's privacy policy, we're doing this same process - but instead of a single query, we're running dozens of queries to check for every CCPA requirement.
>
> And every single query, every result, every gap identified - all of it gets logged to MCP."

---

### [WHY THIS MATTERS - 60 seconds]

**[SCREEN: On-camera or slide]**

> "Now, why does this matter for compliance and security work?
>
> When you're analyzing privacy policies for regulatory compliance, you need two things:
>
> **One: Accuracy**. You need to find the right requirements. RAG provides this through semantic search - it finds relevant sections even if the exact keywords don't match.
>
> **Two: Auditability**. You need to prove what you checked and when. MCP provides this through structured logging - every query is tracked with timestamps and session IDs.
>
> Together, RAG and MCP create an automated compliance checking system that's both accurate and auditable.
>
> This isn't hypothetical. When we run a full gap analysis on a company's privacy policy - and you'll see this in the next lesson - we're running this exact loop dozens of times. For each CCPA requirement, we query the policy to see if it's addressed. And MCP logs every step.
>
> The result is a compliance report that stands up to legal review, backed by a complete audit trail."

---

### [PRACTICAL EXAMPLE - 45 seconds]

**[SCREEN: Show example or code]**

> "Here's a practical scenario. Your legal team is preparing for a CCPA audit. The auditor asks:
>
> 'Show me how you verified that your privacy policy addresses the right to delete.'
>
> With this system, you pull up the MCP logs, filter for queries related to 'right to delete,' and show the auditor:
>
> - **When** the query was run: timestamp
> - **What** was searched: the exact query text
> - **What** was found: the retrieved CCPA sections
> - **How** it was analyzed: the top results and their relevance scores
>
> All from the MCP audit trail. This is documentation-ready evidence of your compliance verification process.
>
> That's the value of integrating RAG with MCP - not just smart search, but provable, auditable search."

---

### [TRANSITION TO NEXT LESSON - 20 seconds]

> "In the next lesson, we're going to look at the full privacy policy gap analysis workflow. We'll take a real company's privacy policy, run it through this RAG + MCP system, and generate a complete compliance report.
>
> You'll see how all of this comes together in a production tool."

---

### [WRAP-UP - 20 seconds]

> "So to recap: RAG provides semantic search over regulatory data. MCP provides audit logging. Together, they create the foundation for automated, auditable compliance checking.
>
> I encourage you to run this demo yourself. Start the MCP server, run the script, and look at the audit trail. See how the data flows through the system.
>
> Thanks for watching, and I'll see you in the next lesson."

---

## Key Teaching Points Covered

| Concept | Explanation in Script |
|---------|---------------------|
| **RAG Indexing** | "Converting regulatory text into searchable embeddings" |
| **Semantic Search** | "Search by meaning, not just keywords" |
| **Retrieval Quality** | "Found exact section plus contextually related requirements" |
| **MCP Logging** | "Permanent record with session ID, timestamp, query details" |
| **Audit Trail** | "Queryable history of all compliance checks" |
| **Integration Value** | "Accurate AND auditable compliance checking" |
| **Legal Review** | "Documentation-ready evidence of verification process" |

---

## Script Timing

- **Intro**: 30 seconds
- **Setup**: 20 seconds
- **Demo Part 1 (MCP Check)**: 30 seconds
- **Demo Part 2 (Load Framework)**: 45 seconds
- **Demo Part 3 (RAG Query)**: 90 seconds (1.5 minutes)
- **Demo Part 4 (Log to MCP)**: 60 seconds
- **Demo Part 5 (Verify Trail)**: 45 seconds
- **Browser Demo**: 45 seconds
- **Recap**: 60 seconds
- **Why This Matters**: 60 seconds
- **Practical Example**: 45 seconds
- **Transition**: 20 seconds
- **Wrap-up**: 20 seconds

**Total**: ~9 minutes (perfect for 10-minute LinkedIn Learning lesson)

---

## Visual Cues for Editor

### Terminal Output
1. **Split screen**: MCP server (left) + demo script (right)
2. **Step 1**: Hold on "MCP Server Status: RUNNING"
3. **Step 2**: Show embedding model loading message
4. **Step 3**: Slow scroll through top 3 results
5. **Step 4**: Zoom in on JSON-RPC payload structure
6. **Step 5**: Highlight session ID in audit trail

### Browser Screens
1. **/debug/memory**: Show full JSON array
2. **Highlight**: Current session (top of list)
3. **Scroll**: Show historical queries

### Graphics to Add
1. **Flow diagram**: Query → RAG → Results → MCP → Audit Trail
2. **Integration diagram**: RAG + MCP working together
3. **Recap slide**: 4-step process illustrated
4. **Value proposition**: Accuracy + Auditability = Compliance

---

## Demo Script Commands

### Preparation
```bash
# Terminal 1: Start MCP server
cd privacy_gap_analysis
python privacy_mcp_server.py

# Terminal 2: Run demo (interactive mode)
python scripts/02_04_demo_mcp_rag_integration.py

# Terminal 2: Run demo (quick mode for recording)
python scripts/02_04_demo_mcp_rag_integration.py --quick
```

### Browser URLs to Show
```
http://localhost:8080/health
http://localhost:8080/debug/memory
http://localhost:8080/debug/confidence
```

---

## Key Quotes for Emphasis

> "This is the power of semantic search - we found contextually related requirements, not just keyword matches."

> "RAG provides accuracy. MCP provides auditability. Together: compliance checking that stands up to legal review."

> "Every query, every result, every gap identified - all logged to MCP with complete traceability."

> "This is documentation-ready evidence of your compliance verification process."

---

## Post-Production Tips

### Pacing
- **Normal speed** for demo output
- **Slow down** when explaining RAG results (students need to understand semantic similarity)
- **Slow down** during JSON-RPC payload explanation
- **Normal speed** for recap

### B-roll Suggestions
- Diagram of RAG retrieval process
- Example compliance audit report
- MCP database schema showing memory table
- Split-screen comparison: keyword search vs semantic search

### Annotations to Add
- Arrow pointing to session ID in output
- Highlight semantic similarity in results
- Circle timestamp in audit trail
- Underline CCPA section references

---

## Alternative Demo Format (If Time Allows)

### Live Python REPL (Instead of Demo Script)

If you prefer to show a true interactive Python session:

```python
# Start Python REPL
$ python3

# Import and load
>>> from privacy_rag_mcp import load_ccpa_framework
>>> import requests
>>> from datetime import datetime
>>> vectordb = load_ccpa_framework()

# Query
>>> retriever = vectordb.as_retriever(search_kwargs={"k": 5})
>>> query = "What does CCPA say about consumers' right to delete personal information?"
>>> results = retriever.invoke(query)

# Show results
>>> for i, doc in enumerate(results[:3], 1):
...     print(f"\n[{i}] {doc.page_content[:200]}")

# Log to MCP
>>> session_id = f"rag_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
>>> payload = {
...     "jsonrpc": "2.0",
...     "method": "insert_memory",
...     "params": {
...         "session_id": session_id,
...         "text": f"Query: {query}\nResults: {len(results)} sections"
...     },
...     "id": 1
... }
>>> response = requests.post("http://localhost:8080/mcp", json=payload)
>>> response.json()

# Verify
>>> import requests
>>> requests.get("http://localhost:8080/debug/memory").json()[-1]
```

This shows the actual code students would type, but requires more careful editing to keep timing tight.

---

**This script is ready for recording!**

**Estimated recording time**: 10 minutes
**Estimated editing time**: Add 5-10 minutes for graphics/b-roll
**Final lesson length**: 8-9 minutes
