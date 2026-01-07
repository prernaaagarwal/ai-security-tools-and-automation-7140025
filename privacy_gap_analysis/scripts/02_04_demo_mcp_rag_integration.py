#!/usr/bin/env python3
"""
LinkedIn Learning Course - Chapter 2, Lesson 04
Demo: MCP + RAG Integration - Simple Query with Audit Trail

This demo shows how RAG (Retrieval-Augmented Generation) and MCP (Model Context Protocol)
work together to provide semantic search over regulatory data with complete audit logging.

Usage:
    python 02_04_demo_mcp_rag_integration.py          # Interactive mode (pauses for explanation)
    python 02_04_demo_mcp_rag_integration.py --quick  # Quick mode (auto-run for recording)
"""

import sys
import time
import requests
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import privacy_rag_mcp
sys.path.insert(0, str(Path(__file__).parent))

def print_section(title, width=80):
    """Print a section header"""
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width + "\n")

def print_step(step_num, title):
    """Print a step header"""
    print(f"\n--- STEP {step_num}: {title} ---\n")

def pause(message="Press Enter to continue...", quick_mode=False):
    """Pause for user input unless in quick mode"""
    if not quick_mode:
        input(f"\n{message}")
    else:
        time.sleep(1.5)

def demo_intro(quick_mode=False):
    """Introduction to the demo"""
    print_section("MCP + RAG Integration Demo")

    print("This demo shows how RAG and MCP work together:")
    print()
    print("  1. Start MCP server (audit tracking)")
    print("  2. Load CCPA framework into vector database (RAG indexing)")
    print("  3. Query for specific requirement (RAG retrieval)")
    print("  4. Log query to MCP (audit trail)")
    print()
    print("GOAL: Query 'What does CCPA say about Right to Delete?'")
    print("      and track the entire process in the audit trail.")

    pause("Ready to begin? Press Enter...", quick_mode)

def demo_mcp_server_check(quick_mode=False):
    """Check if MCP server is running"""
    print_step(1, "Verify MCP Server is Running")

    print("Checking MCP server at http://localhost:8080...")

    try:
        response = requests.get("http://localhost:8080/health", timeout=2)
        if response.status_code == 200:
            health_data = response.json()
            print("\n MCP Server Status: RUNNING")
            print(f"   Service: {health_data.get('service', 'Privacy Policy MCP Server')}")
            print(f"   Total Sessions: {health_data.get('stats', {}).get('total_sessions', 0)}")
            print(f"   Total Analyses: {health_data.get('stats', {}).get('total_analyses', 0)}")
            print()
            return True
    except requests.exceptions.RequestException:
        print("\n ERROR: MCP server is not running!")
        print()
        print("To start the MCP server, run in another terminal:")
        print("  $ cd privacy_gap_analysis")
        print("  $ python privacy_mcp_server.py")
        print()
        return False

    pause("MCP server verified. Press Enter to continue...", quick_mode)
    return True

def demo_load_ccpa_framework(quick_mode=False):
    """Load CCPA framework into RAG"""
    print_step(2, "Load CCPA Framework into Vector Database (RAG)")

    print("Importing privacy_rag_mcp module...")
    print(">>> from privacy_rag_mcp import load_ccpa_framework")
    print()

    pause("Press Enter to load framework...", quick_mode)

    from privacy_rag_mcp import load_ccpa_framework

    print(">>> vectordb_ccpa = load_ccpa_framework()")
    print()
    print("Loading embedding model: all-MiniLM-L12-v2...")
    print(" Model loaded")
    print()
    print("Loading CCPA/CPRA Framework from CSV...")

    vectordb_ccpa = load_ccpa_framework()

    print(" CCPA/CPRA requirements stored in ChromaDB")
    print()
    print("RAG system ready for queries!")

    pause("Framework loaded. Press Enter to continue...", quick_mode)

    return vectordb_ccpa

def demo_rag_query(vectordb_ccpa, quick_mode=False):
    """Perform RAG query"""
    print_step(3, "Query RAG for 'Right to Delete' Information")

    query = "What does CCPA say about consumers' right to delete personal information?"

    print(f"Query: '{query}'")
    print()
    print(">>> retriever = vectordb_ccpa.as_retriever(search_kwargs={'k': 5})")
    print(f">>> results = retriever.invoke('{query[:50]}...')")
    print()

    pause("Press Enter to execute query...", quick_mode)

    retriever = vectordb_ccpa.as_retriever(search_kwargs={"k": 5})
    results = retriever.invoke(query)

    print(f" Found {len(results)} relevant CCPA sections")
    print()

    # Display top 3 results
    print("Top 3 Results:")
    print()

    for i, doc in enumerate(results[:3], 1):
        content = doc.page_content

        # Extract key information
        lines = content.split('\n')
        category = ""
        requirement = ""
        reference = ""

        for line in lines:
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
            elif line.startswith("Requirement:"):
                requirement = line.replace("Requirement:", "").strip()
            elif line.startswith("Reference:"):
                reference = line.replace("Reference:", "").strip()

        print(f"  [{i}] {requirement}")
        print(f"      Category: {category}")
        print(f"      Reference: {reference}")

        # Show snippet of description
        description_start = content.find('\n', content.find("Requirement:"))
        if description_start != -1:
            snippet = content[description_start:description_start+150].strip()
            if '\n' in snippet:
                snippet = snippet[:snippet.find('\n')]
            print(f"      {snippet}...")
        print()

    pause("Query complete. Press Enter to log to MCP...", quick_mode)

    return query, results

def demo_log_to_mcp(query, results, quick_mode=False):
    """Log query to MCP server"""
    print_step(4, "Log Query to MCP Audit Trail")

    session_id = f"rag_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"Creating session ID: {session_id}")
    print()
    print(">>> mcp_url = 'http://localhost:8080/mcp'")
    print(">>> payload = {")
    print("...     'jsonrpc': '2.0',")
    print("...     'method': 'insert_memory',")
    print("...     'params': {")
    print(f"...         'session_id': '{session_id}',")
    print(f"...         'text': 'Query: {query[:40]}...'")
    print("...     },")
    print("...     'id': 1")
    print("... }")
    print()

    pause("Press Enter to send to MCP server...", quick_mode)

    mcp_url = "http://localhost:8080/mcp"

    payload = {
        "jsonrpc": "2.0",
        "method": "insert_memory",
        "params": {
            "session_id": session_id,
            "text": f"Query: {query}\nResults: {len(results)} CCPA sections retrieved\n\nTop Result: {results[0].page_content[:200] if results else 'None'}..."
        },
        "id": 1
    }

    try:
        response = requests.post(mcp_url, json=payload, timeout=5)
        response_data = response.json()

        print(">>> response = requests.post(mcp_url, json=payload)")
        print(f">>> response.json()")
        print()
        print(f"  {response_data}")
        print()

        # Handle both response formats: dict with status or string result
        result = response_data.get('result', '')
        if (isinstance(result, dict) and result.get('status') == 'success') or \
           (isinstance(result, str) and 'inserted' in result.lower()):
            print(" Query logged successfully!")

    except requests.exceptions.RequestException as e:
        print(f" ERROR: Failed to log to MCP: {e}")
        return None

    pause("Logged to MCP. Press Enter to verify audit trail...", quick_mode)

    return session_id

def demo_view_audit_trail(session_id, quick_mode=False):
    """View the audit trail"""
    print_step(5, "Verify Audit Trail in MCP")

    print("Checking MCP memory logs at http://localhost:8080/debug/memory")
    print()

    pause("Press Enter to fetch audit trail...", quick_mode)

    try:
        response = requests.get("http://localhost:8080/debug/memory", timeout=5)
        memory_logs = response.json()

        # MCP returns dict with session_id as keys, values are arrays of log entries
        # Find our session
        our_log = None
        if session_id in memory_logs:
            # Get the first (most recent) log entry for this session
            logs_for_session = memory_logs[session_id]
            if logs_for_session and len(logs_for_session) > 0:
                our_log = logs_for_session[-1]  # Get the last entry

        if our_log:
            print(" Audit trail entry found:")
            print()
            print(f"  Session ID: {session_id}")
            print(f"  Timestamp: {our_log.get('timestamp', 'N/A')}")
            print(f"  Text (preview): {our_log.get('text', '')[:100]}...")
            print()
            print(" Query successfully logged to audit trail!")
        else:
            print(" Session not found in logs (may need to refresh)")

    except requests.exceptions.RequestException as e:
        print(f" ERROR: Failed to retrieve audit trail: {e}")
    except Exception as e:
        print(f" ERROR: Failed to parse audit trail: {e}")

    pause("Audit trail verified. Press Enter for summary...", quick_mode)

def demo_recap(quick_mode=False):
    """Recap what was demonstrated"""
    print_section("DEMO RECAP: What We Just Did")

    print("We demonstrated the core loop of the privacy gap analysis tool:")
    print()
    print("  [1] Started MCP server for audit tracking")
    print("  [2] Loaded CCPA framework into vector database (RAG indexing)")
    print("  [3] Queried for specific requirement (RAG retrieval)")
    print("      - Used semantic search to find relevant sections")
    print("      - Retrieved top 5 most relevant CCPA requirements")
    print("  [4] Logged query to MCP (audit trail)")
    print("      - Created session ID for traceability")
    print("      - Stored query and results in MCP memory")
    print("  [5] Verified audit trail through debug endpoint")
    print()
    print("KEY INSIGHT:")
    print("  RAG provides semantic search over regulatory data.")
    print("  MCP provides complete audit logging of all queries.")
    print("  Together: Compliance search with full traceability.")
    print()
    print("This is the foundation for automated privacy policy gap analysis.")
    print()

def run_full_demo():
    """Run full interactive demo with pauses"""
    print("\n" + "=" * 80)
    print("  INTERACTIVE MODE")
    print("  This demo will pause between steps for explanation")
    print("=" * 80)

    demo_intro(quick_mode=False)

    if not demo_mcp_server_check(quick_mode=False):
        print("\nDemo aborted. Please start MCP server first.")
        return

    vectordb = demo_load_ccpa_framework(quick_mode=False)
    query, results = demo_rag_query(vectordb, quick_mode=False)
    session_id = demo_log_to_mcp(query, results, quick_mode=False)

    if session_id:
        demo_view_audit_trail(session_id, quick_mode=False)

    demo_recap(quick_mode=False)

    print("Demo complete!")

def run_quick_demo():
    """Run quick demo for screen recording"""
    print("\n" + "=" * 80)
    print("  QUICK MODE - Auto-running for screen recording")
    print("=" * 80)
    time.sleep(2)

    demo_intro(quick_mode=True)

    if not demo_mcp_server_check(quick_mode=True):
        print("\nDemo aborted. Please start MCP server first.")
        return

    vectordb = demo_load_ccpa_framework(quick_mode=True)
    query, results = demo_rag_query(vectordb, quick_mode=True)
    session_id = demo_log_to_mcp(query, results, quick_mode=True)

    if session_id:
        demo_view_audit_trail(session_id, quick_mode=True)

    demo_recap(quick_mode=True)

    print("Demo complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    else:
        run_full_demo()
