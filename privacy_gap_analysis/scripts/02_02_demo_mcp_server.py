#!/usr/bin/env python3
"""
MCP Server Demo - LinkedIn Learning Chapter 2, Lesson 02
Demonstrates Model Context Protocol for audit trails and compliance logging

This script demonstrates:
1. Starting MCP server
2. Logging analysis sessions
3. Tracking token usage
4. Storing gap analysis data
5. Viewing audit trails
"""

import requests
import time
import json
from datetime import datetime
from uuid import uuid4


MCP_URL = "http://localhost:8080"


def print_banner(text):
    """Print visual banner"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_section(text):
    """Print section header"""
    print("\n" + "-"*80)
    print(f"  {text}")
    print("-"*80)


def check_server():
    """Check if MCP server is running"""
    try:
        response = requests.get(f"{MCP_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def demo_insert_memory():
    """Demo: Log analysis session to memory"""

    print_section("DEMO 1: Logging Analysis Session")

    session_id = f"privacy_analysis_DemoCompany_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"\n Creating analysis session: {session_id}")

    analysis_text = """Gap Analysis for DemoCompany

**Critical Gaps Identified:**
1. Missing Right to Delete disclosure (CCPA Section 1798.105)
2. No 'Do Not Sell' link on homepage (CCPA Section 1798.135)
3. Inadequate data retention policies (CPRA Section 1798.100)

**Recommendations:**
- Add Right to Delete section to privacy policy
- Implement 'Do Not Sell or Share My Personal Information' link
- Define specific data retention periods
"""

    # Call MCP server
    payload = {
        "jsonrpc": "2.0",
        "method": "insert_memory",
        "params": {
            "session_id": session_id,
            "text": analysis_text
        },
        "id": 1
    }

    print("\n⏳ Sending to MCP server...")
    print(f"   Endpoint: {MCP_URL}/mcp")
    print(f"   Method: insert_memory")

    response = requests.post(f"{MCP_URL}/mcp", json=payload)

    if response.status_code == 200:
        print("\n Session logged successfully!")
        print(f"   Session ID: {session_id}")
        print(f"   Text length: {len(analysis_text)} characters")
        print(f"   Timestamp: {datetime.now().isoformat()}")
    else:
        print(f"\n Error: {response.status_code}")

    return session_id


def demo_insert_token_usage():
    """Demo: Track token consumption"""

    print_section("DEMO 2: Tracking Token Usage")

    print("\n Recording token usage for analysis:")
    print("   Model: gpt-4o")
    print("   Prompt tokens: 3,847")
    print("   Completion tokens: 1,203")
    print("   Total tokens: 5,050")

    payload = {
        "jsonrpc": "2.0",
        "method": "insert_token_usage",
        "params": {
            "timestamp": datetime.now().isoformat(),
            "query": "Gap analysis for DemoCompany",
            "model_used": "gpt-4o",
            "tokens_prompt": 3847,
            "tokens_completion": 1203,
            "tokens_total": 5050
        },
        "id": 2
    }

    print("\n⏳ Logging to MCP...")

    response = requests.post(f"{MCP_URL}/mcp", json=payload)

    if response.status_code == 200:
        print("\n Token usage logged!")
        print("\n This enables:")
        print("   • Cost tracking per analysis")
        print("   • Usage monitoring over time")
        print("   • Budget forecasting")
        print("   • Audit trail for AI usage")


def demo_insert_gap_analysis():
    """Demo: Store structured gap analysis"""

    print_section("DEMO 3: Storing Gap Analysis Data")

    gaps = [
        {
            "title": "Right to Delete Disclosure",
            "description": "Privacy policy missing consumer right to request deletion",
            "priority": "Critical"
        },
        {
            "title": "Do Not Sell Link",
            "description": "Website lacks 'Do Not Sell or Share' link on homepage",
            "priority": "Critical"
        },
        {
            "title": "Data Retention Periods",
            "description": "No specific retention timeframes defined",
            "priority": "High"
        }
    ]

    recommendations = [
        "Add Right to Delete section with request process",
        "Implement 'Do Not Sell' link per CCPA Section 1798.135",
        "Define retention periods for each data category"
    ]

    print(f"\n Storing {len(gaps)} compliance gaps:")
    for i, gap in enumerate(gaps, 1):
        print(f"   {i}. {gap['title']} ({gap['priority']})")

    payload = {
        "jsonrpc": "2.0",
        "method": "insert_gap_analysis",
        "params": {
            "session_id": f"privacy_analysis_DemoCompany_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "company": "DemoCompany",
            "gaps": gaps,
            "recommendations": recommendations,
            "priority_level": "Critical"
        },
        "id": 3
    }

    print("\n⏳ Storing in MCP...")

    response = requests.post(f"{MCP_URL}/mcp", json=payload)

    if response.status_code == 200:
        print("\n Gap analysis stored!")
        print("\n Compliance audit trail now includes:")
        print("   • Each gap with CCPA reference")
        print("   • Priority classification")
        print("   • Specific recommendations")
        print("   • Timestamp and session linkage")


def demo_view_audit_trail():
    """Demo: View complete audit trail"""

    print_section("DEMO 4: Viewing Audit Trail")

    print("\n Retrieving audit trail from MCP server...")

    # Get health stats
    print("\n1⃣  Server Health & Statistics:")
    health = requests.get(f"{MCP_URL}/health").json()
    print(f"   Status: {health['status']}")
    print(f"   Total Sessions: {health['stats']['total_sessions']}")
    print(f"   Total Analyses: {health['stats']['total_analyses']}")
    print(f"   Total Feedback: {health['stats']['total_feedback']}")
    print(f"   Token Logs: {health['stats']['total_token_logs']}")

    # Get recent memory entries
    print("\n2⃣  Recent Analysis Sessions:")
    memory = requests.get(f"{MCP_URL}/debug/memory").json()

    if memory:
        latest_sessions = list(memory.keys())[-3:]  # Last 3 sessions
        for session_id in latest_sessions:
            print(f"   • {session_id}")
    else:
        print("   (No sessions yet)")

    # Get token usage
    print("\n3⃣  Token Usage Log:")
    tokens = requests.get(f"{MCP_URL}/debug/tokens").json()

    if tokens:
        total_tokens = sum(t['tokens_total'] for t in tokens)
        print(f"   Total tokens consumed: {total_tokens:,}")
        print(f"   Total API calls: {len(tokens)}")

        if tokens:
            latest = tokens[-1]
            print(f"   Latest: {latest['model_used']} - {latest['tokens_total']} tokens")
    else:
        print("   (No token logs yet)")

    # Get gap analysis
    print("\n4⃣  Gap Analysis Store:")
    gaps = requests.get(f"{MCP_URL}/debug/gaps").json()

    if gaps:
        total_gaps = sum(len(g['gaps']) for g in gaps)
        print(f"   Total gaps identified: {total_gaps}")
        print(f"   Companies analyzed: {len(gaps)}")
    else:
        print("   (No gap analyses yet)")


def demo_compliance_value():
    """Demo: Show compliance value proposition"""

    print_banner("WHY THIS MATTERS FOR COMPLIANCE")

    print("""
 For security and compliance tools, audit trails are NON-NEGOTIABLE.

Questions auditors WILL ask:
   • When was this analysis run?
   • What data was analyzed?
   • What model was used?
   • How many tokens were consumed?
   • What was the confidence level?
   • Who approved the results?

 MCP gives us structured logging for ALL of this.
    """)

    print_section("Example: Retrieving Full Audit Trail")

    print("""
When you see a Session ID in a report:

   "Session ID: privacy_analysis_Audit_Caddie_20251202_140343"

You can retrieve the COMPLETE audit trail:

    Input:
      • Company: auditcaddie.com
      • Privacy policy: 3,200 characters
      • Terms & Conditions: 1,800 characters

    Analysis:
      • CCPA requirements used: 35 sections
      • Model: gpt-4o
      • Temperature: 0.3
      • Tokens consumed: 4,847

    Output:
      • Gaps identified: 23
      • Critical gaps: 9
      • High priority: 8
      • Medium priority: 6

    Human Feedback:
      • Rating: 4/5 (excellent)
      • Comments: "Comprehensive analysis"

   ⏰ Timestamp: 2025-12-02 14:03:43

This is a COMPLETE audit trail for compliance and legal review.
    """)


def run_full_demo():
    """Run complete MCP server demonstration"""

    print_banner("MCP Server Demo - Model Context Protocol")
    print("\n This demo shows how MCP provides audit trails for AI compliance tools")

    # Check server
    print("\n⏳ Checking if MCP server is running...")

    if not check_server():
        print("\n MCP server is not running!")
        print("\n To start the server:")
        print("   1. Open a new terminal")
        print("   2. Run: python privacy_mcp_server.py")
        print("   3. Wait for 'Running on http://127.0.0.1:8080'")
        print("   4. Re-run this demo\n")
        return

    print(f" MCP server is running at {MCP_URL}")

    input("\n⏸  Press Enter to start Demo 1: Logging Analysis Session...")

    # Demo 1: Insert memory
    session_id = demo_insert_memory()

    input("\n⏸  Press Enter to start Demo 2: Tracking Token Usage...")

    # Demo 2: Token tracking
    demo_insert_token_usage()

    input("\n⏸  Press Enter to start Demo 3: Storing Gap Analysis...")

    # Demo 3: Gap analysis
    demo_insert_gap_analysis()

    input("\n⏸  Press Enter to start Demo 4: Viewing Audit Trail...")

    # Demo 4: View audit trail
    demo_view_audit_trail()

    input("\n⏸  Press Enter to see why this matters for compliance...")

    # Compliance value
    demo_compliance_value()

    print_banner(" Demo Complete!")

    print("""
 MCP Server Endpoints You Can Explore:

   Health Check:
   http://localhost:8080/health

   Debug Endpoints:
   http://localhost:8080/debug/memory
   http://localhost:8080/debug/confidence
   http://localhost:8080/debug/feedback
   http://localhost:8080/debug/tokens
   http://localhost:8080/debug/gaps

 Try opening these in your browser to see the audit data!
    """)


def run_quick_demo():
    """Quick non-interactive demo"""

    print_banner("MCP Server Quick Demo")

    if not check_server():
        print("\n MCP server not running. Start with: python privacy_mcp_server.py\n")
        return

    print(f"\n MCP server running at {MCP_URL}")

    demo_insert_memory()
    time.sleep(1)

    demo_insert_token_usage()
    time.sleep(1)

    demo_insert_gap_analysis()
    time.sleep(1)

    demo_view_audit_trail()
    time.sleep(1)

    demo_compliance_value()

    print_banner(" Demo Complete!")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\n MCP Server Demo")
        print("="*60)
        print("\nUsage:")
        print("  python demo_mcp_server.py              # Interactive demo")
        print("  python demo_mcp_server.py --quick      # Quick auto-run")
        print("\nPrerequisite:")
        print("  MCP server must be running:")
        print("  python privacy_mcp_server.py")
        print("="*60 + "\n")
    else:
        run_full_demo()


if __name__ == "__main__":
    main()
