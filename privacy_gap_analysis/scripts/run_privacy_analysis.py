#!/usr/bin/env python3
"""
End-to-End Privacy Policy Gap Analysis Workflow
Integrates: Privacy Scraper → PDF Extraction → RAG → MCP → GPT-4.1 → Report

Cardinal Security - Privacy Compliance Workflow
"""

import sys
import os
from pathlib import Path

# Import privacy scraper
from privacy_policy_scraper import scrape_privacy_policy, scrape_policy_documents

# Import RAG/MCP system
from privacy_rag_mcp import analyze_privacy_policy, analyze_policy_documents

###############################################################################
#                    Human Feedback Collection
###############################################################################
def collect_user_feedback(session_id: str, company_name: str) -> dict:
    """
    Collect user feedback on gap analysis quality
    This enables human reinforcement learning for model improvement
    """
    import requests

    print("\n" + "="*70)
    print("HUMAN FEEDBACK - Reinforcement Learning")
    print("="*70)
    print("Help improve the analysis quality by providing feedback!")
    print()

    try:
        # Ask for overall rating
        print(" How would you rate the overall quality of this gap analysis?")
        print("   1 = Poor (many gaps missed, inaccurate)")
        print("   2 = Fair (some gaps missed)")
        print("   3 = Good (most gaps identified)")
        print("   4 = Excellent (comprehensive and accurate)")
        print("   5 = Outstanding (exceeded expectations)")
        print()

        rating_input = input("Rating (1-5) or press Enter to skip: ").strip()

        if not rating_input:
            print("⏭  Feedback skipped")
            return None

        try:
            rating = int(rating_input)
            if rating < 1 or rating > 5:
                print("  Invalid rating, skipping feedback")
                return None
        except ValueError:
            print("  Invalid rating, skipping feedback")
            return None

        # Convert to rating label
        rating_labels = {
            1: "poor",
            2: "fair",
            3: "good",
            4: "excellent",
            5: "outstanding"
        }
        rating_label = rating_labels.get(rating, "good")

        # Ask for specific feedback
        print()
        print(" Any specific comments? (optional)")
        print("   Examples:")
        print("   - 'Missed critical gap in data retention policies'")
        print("   - 'Good coverage but recommendations could be more specific'")
        print("   - 'Excellent analysis, very thorough'")
        print()

        comments = input("Comments (or press Enter to skip): ").strip()

        # Log to MCP server
        feedback_data = {
            "session_id": session_id,
            "question": f"Gap Analysis Quality for {company_name}",
            "rating": rating_label,
            "numeric_rating": rating,
            "comments": comments if comments else None
        }

        # Send to MCP server
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "insert_feedback",
                "params": feedback_data,
                "id": 1
            }
            response = requests.post("http://localhost:8080/mcp", json=payload, timeout=5)

            if response.status_code == 200:
                print("\n Feedback recorded! Thank you for improving the system.")
                print(f"   Rating: {rating}/5 ({rating_label})")
                if comments:
                    print(f"   Comments: {comments}")
            else:
                print(f"\n  Could not save feedback: HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"\n  Could not connect to MCP server: {e}")
            print("   Make sure MCP server is running at http://localhost:8080")

        print()
        return feedback_data

    except KeyboardInterrupt:
        print("\n\n⏭  Feedback cancelled")
        return None


###############################################################################
#                    Complete Workflow Function
###############################################################################
def run_complete_privacy_analysis(company_url: str, company_name: str = None):
    """
    Complete end-to-end privacy policy & terms gap analysis workflow:

    1. Scrape privacy policy and terms & conditions from company website
    2. Extract text from downloaded PDFs
    3. Load both documents into vector database
    4. Retrieve CCPA/CPRA requirements
    5. Perform gap analysis using GPT-4 on combined documents
    6. Generate comprehensive compliance report

    Args:
        company_url: Company homepage URL
        company_name: Optional company name (auto-detected if not provided)

    Returns:
        Dictionary with analysis results and report path
    """

    print("\n" + "="*70)
    print("PRIVACY POLICY GAP ANALYSIS WORKFLOW")
    print("Cardinal Security - CCPA/CPRA Compliance")
    print("="*70)
    print(f"Target: {company_url}")
    print("="*70 + "\n")

    # Extract company name from URL if not provided
    if not company_name:
        from urllib.parse import urlparse
        domain = urlparse(company_url).netloc
        company_name = domain.replace('www.', '').replace('.com', '').replace('.', ' ').title()
        print(f" Detected company name: {company_name}")

    # Step 1: Scrape Policy Documents (Privacy Policy + Terms & Conditions)
    print("\n" + "-"*70)
    print("STEP 1: SCRAPING POLICY DOCUMENTS")
    print("-"*70)

    policy_docs = scrape_policy_documents(company_url)

    if not policy_docs['privacy_policy'] and not policy_docs['terms_conditions']:
        print("\n FAILED: Could not scrape any policy documents from website")
        print("  Please ensure:")
        print("    - The website has a privacy policy and/or terms & conditions")
        print("    - The policy links are accessible")
        print("    - Your internet connection is stable")
        return None

    if policy_docs['privacy_policy']:
        print(f"\n Privacy policy downloaded: {policy_docs['privacy_policy']}")
    if policy_docs['terms_conditions']:
        print(f" Terms & conditions downloaded: {policy_docs['terms_conditions']}")

    # Step 2: Perform Gap Analysis with RAG and MCP
    print("\n" + "-"*70)
    print("STEP 2: GAP ANALYSIS WITH RAG & MCP")
    print("-"*70)

    result = analyze_policy_documents(
        privacy_pdf_path=policy_docs['privacy_policy'],
        terms_pdf_path=policy_docs['terms_conditions'],
        company_name=company_name
    )

    if not result:
        print("\n FAILED: Gap analysis could not be completed")
        return None

    # Step 3: Display Results
    print("\n" + "="*70)
    print(" ANALYSIS COMPLETE")
    print("="*70)
    print(f"\n Company: {company_name}")
    if policy_docs['privacy_policy']:
        print(f" Privacy Policy: {policy_docs['privacy_policy']}")
    if policy_docs['terms_conditions']:
        print(f" Terms & Conditions: {policy_docs['terms_conditions']}")
    print(f" Report: {result['report_path']}")
    print(f"\n Session ID: {result['analysis']['session_id']}")
    print(f" Tokens Used: {result['analysis']['tokens_used']}")
    print(f"⏰ Timestamp: {result['analysis']['timestamp']}")

    print("\n" + "-"*70)
    print("NEXT STEPS:")
    print("-"*70)
    print(f"1. Review the gap analysis report: {result['report_path']}")
    print("2. Prioritize gaps based on severity (Critical → High → Medium → Low)")
    print("3. Draft updated privacy policy language addressing identified gaps")
    print("4. Implement required notices and consumer rights mechanisms")
    print("5. Update website with 'Do Not Sell or Share My Personal Information' link")
    print("6. Review MCP logs at: http://localhost:8080/debug/gaps")
    print("="*70 + "\n")

    # Step 4: Collect User Feedback (Human Reinforcement Learning)
    feedback = collect_user_feedback(result['analysis']['session_id'], company_name)
    if feedback:
        result['user_feedback'] = feedback

    return result

###############################################################################
#                         CLI Interface
###############################################################################
def main():
    """Command-line interface for privacy analysis"""

    print("\n" + "="*70)
    print("PRIVACY POLICY GAP ANALYSIS - CCPA/CPRA COMPLIANCE")
    print("Cardinal Security Privacy Compliance Workflow")
    print("="*70)

    # Check if URL provided as argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        company = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Interactive mode
        print("\nNo URL provided. Starting interactive mode...\n")
        url = input("Enter company homepage URL: ").strip()

        if not url:
            print(" No URL provided. Exiting.")
            sys.exit(1)

        use_auto_name = input(f"Auto-detect company name? (y/n): ").strip().lower()
        company = None if use_auto_name == 'y' else input("Enter company name: ").strip()

    # Ensure MCP server is running
    print("\n  IMPORTANT: Ensure MCP server is running")
    print("   Run: python privacy_mcp_server.py")
    print("   Check: http://localhost:8080/health\n")

    proceed = input("MCP server running? Press Enter to continue or Ctrl+C to exit...")

    # Run analysis
    result = run_complete_privacy_analysis(url, company)

    if result:
        print("\n Privacy policy gap analysis completed successfully!")
    else:
        print("\n Privacy policy gap analysis failed.")
        sys.exit(1)

###############################################################################
#                         Example Usage
###############################################################################
if __name__ == '__main__':
    # Example usage:
    # python run_privacy_analysis.py https://auditcaddie.com "Audit Caddie"
    # python run_privacy_analysis.py https://example.com

    main()
