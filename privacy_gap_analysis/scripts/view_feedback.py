#!/usr/bin/env python3
"""
Feedback Viewer - Educational Tool
LinkedIn Learning: AI Automation Course

Simple script to view accumulated feedback data from MCP server.
Shows students how feedback data accumulates over time.
"""

import requests
import sys
from datetime import datetime


MCP_URL = "http://localhost:8080"


def check_server():
    """Check if MCP server is running"""
    try:
        response = requests.get(f"{MCP_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_stats():
    """Get overall statistics"""
    try:
        response = requests.get(f"{MCP_URL}/health", timeout=5)
        return response.json()
    except:
        return None


def get_feedback():
    """Get all feedback entries"""
    try:
        response = requests.get(f"{MCP_URL}/debug/feedback", timeout=5)
        return response.json()
    except:
        return []


def get_confidence():
    """Get confidence scores"""
    try:
        response = requests.get(f"{MCP_URL}/debug/confidence", timeout=5)
        return response.json()
    except:
        return []


def get_gaps():
    """Get gap analysis data"""
    try:
        response = requests.get(f"{MCP_URL}/debug/gaps", timeout=5)
        return response.json()
    except:
        return []


def display_summary():
    """Display feedback summary"""

    print("\n" + "="*70)
    print("FEEDBACK DASHBOARD - Human Reinforcement Learning Data")
    print("="*70)

    # Check server
    if not check_server():
        print("\n MCP Server is not running!")
        print("   Start it with: python privacy_mcp_server.py")
        print("="*70 + "\n")
        return

    # Get stats
    stats = get_stats()
    if stats:
        print("\n OVERALL STATISTICS")
        print("-"*70)
        print(f"   Total Sessions: {stats['stats']['total_sessions']}")
        print(f"   Total Analyses: {stats['stats']['total_analyses']}")
        print(f"   User Feedback Entries: {stats['stats']['total_feedback']}")
        print(f"   Token Logs: {stats['stats']['total_token_logs']}")

    # Get feedback
    feedback = get_feedback()
    if feedback:
        print(f"\n USER FEEDBACK ({len(feedback)} entries)")
        print("-"*70)

        # Calculate average rating
        ratings = [f.get('numeric_rating', 0) for f in feedback if 'numeric_rating' in f]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            print(f"   Average Rating: {avg_rating:.1f}/5.0")

            # Rating distribution
            rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for r in ratings:
                rating_counts[r] = rating_counts.get(r, 0) + 1

            print(f"\n   Rating Distribution:")
            rating_labels = {1: "Poor", 2: "Fair", 3: "Good", 4: "Excellent", 5: "Outstanding"}
            for rating in [5, 4, 3, 2, 1]:
                count = rating_counts[rating]
                bar = "" * count
                print(f"   {rating} ({rating_labels[rating]:11s}): {bar} ({count})")

        # Show recent feedback
        print(f"\n   Recent Feedback:")
        for i, entry in enumerate(feedback[-5:], 1):  # Last 5
            rating = entry.get('rating', 'N/A')
            session = entry.get('session_id', 'Unknown')[:30]
            print(f"\n   {i}. Session: {session}")
            print(f"      Rating: {rating}")
            if entry.get('comments'):
                print(f"      Comments: {entry['comments']}")

    else:
        print("\n USER FEEDBACK")
        print("-"*70)
        print("   No feedback entries yet")
        print("   Run an analysis and provide feedback to see data here!")

    # Get confidence scores
    confidence = get_confidence()
    if confidence:
        print(f"\n CONFIDENCE SCORES ({len(confidence)} entries)")
        print("-"*70)

        scores = [c['confidence_score'] for c in confidence]
        avg_confidence = sum(scores) / len(scores)

        print(f"   Average Confidence: {avg_confidence:.2f}")
        print(f"   Highest: {max(scores):.2f}")
        print(f"   Lowest: {min(scores):.2f}")

        # Show recent
        print(f"\n   Recent Confidence Scores:")
        for i, entry in enumerate(confidence[-3:], 1):  # Last 3
            score = entry['confidence_score']
            query = entry.get('query', 'Unknown')[:40]
            status = " High" if entry.get('is_high_confidence') else "  Low"
            print(f"   {i}. {status} - {score:.2f} - {query}")

    # Get gap analysis
    gaps = get_gaps()
    if gaps:
        print(f"\n GAP ANALYSIS DATA ({len(gaps)} entries)")
        print("-"*70)

        total_gaps = sum(len(g['gaps']) for g in gaps)
        total_recs = sum(len(g['recommendations']) for g in gaps)

        print(f"   Total Gaps Identified: {total_gaps}")
        print(f"   Total Recommendations: {total_recs}")

        # Priority breakdown
        priority_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for gap_entry in gaps:
            for gap in gap_entry['gaps']:
                priority = gap.get('priority', 'Medium')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1

        print(f"\n   Gap Priority Breakdown:")
        for priority in ["Critical", "High", "Medium", "Low"]:
            count = priority_counts[priority]
            if count > 0:
                print(f"   {priority:8s}: {count}")

    print("\n" + "="*70)
    print(" MCP Server Endpoints:")
    print(f"   Health: {MCP_URL}/health")
    print(f"   Feedback: {MCP_URL}/debug/feedback")
    print(f"   Confidence: {MCP_URL}/debug/confidence")
    print(f"   Gaps: {MCP_URL}/debug/gaps")
    print("="*70 + "\n")


def export_data():
    """Export all feedback data to JSON"""
    import json

    print("\n Exporting feedback data...")

    data = {
        "export_date": datetime.now().isoformat(),
        "stats": get_stats(),
        "feedback": get_feedback(),
        "confidence": get_confidence(),
        "gaps": get_gaps()
    }

    filename = f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f" Data exported to: {filename}\n")


def main():
    """Main entry point"""

    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_data()
    else:
        display_summary()

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\nUsage:")
        print("  python view_feedback.py           # View dashboard")
        print("  python view_feedback.py --export  # Export data to JSON")
        print()


if __name__ == "__main__":
    main()
