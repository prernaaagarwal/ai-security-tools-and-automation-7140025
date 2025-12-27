#!/usr/bin/env python3
"""
Simple Feedback Entry Tool
Educational script for LinkedIn Learning course

This demonstrates how to manually add feedback to the MCP server.
Useful for:
- Adding feedback after reviewing reports
- Batch feedback entry
- Understanding the feedback API
"""

import requests
import sys
from datetime import datetime

MCP_URL = "http://localhost:8080/mcp"


def add_feedback(session_id: str, rating: str, comments: str = None):
    """
    Add feedback to MCP server

    Args:
        session_id: Analysis session ID (from report)
        rating: Quality rating (poor/fair/good/excellent/outstanding)
        comments: Optional feedback comments
    """

    # Validate rating
    valid_ratings = ["poor", "fair", "good", "excellent", "outstanding"]
    if rating.lower() not in valid_ratings:
        print(f"❌ Error: Rating must be one of: {', '.join(valid_ratings)}")
        return False

    # Map to numeric
    rating_map = {
        "poor": 1,
        "fair": 2,
        "good": 3,
        "excellent": 4,
        "outstanding": 5
    }

    # Prepare payload
    payload = {
        "jsonrpc": "2.0",
        "method": "insert_feedback",
        "params": {
            "session_id": session_id,
            "question": "Manual Feedback Entry",
            "rating": rating.lower(),
            "numeric_rating": rating_map[rating.lower()],
            "comments": comments
        },
        "id": 1
    }

    try:
        # Send to MCP
        response = requests.post(MCP_URL, json=payload, timeout=5)
        response.raise_for_status()

        result = response.json()

        if "result" in result:
            print("\n✅ Feedback added successfully!")
            print(f"   Session: {session_id}")
            print(f"   Rating: {rating_map[rating.lower()]}/5 ({rating.lower()})")
            if comments:
                print(f"   Comments: {comments}")
            return True
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to MCP server")
        print("   Make sure it's running at http://localhost:8080")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def interactive_mode():
    """Interactive feedback entry"""

    print("\n" + "="*60)
    print("MANUAL FEEDBACK ENTRY TOOL")
    print("="*60)
    print("Add feedback for a previous analysis\n")

    # Get session ID
    print("📋 Enter the session ID from the analysis report")
    print("   (Example: privacy_analysis_BLodgic_20251227_171250)")
    session_id = input("\nSession ID: ").strip()

    if not session_id:
        print("❌ Session ID is required")
        return

    # Get rating
    print("\n📊 Rate the analysis quality:")
    print("   1 = poor")
    print("   2 = fair")
    print("   3 = good")
    print("   4 = excellent")
    print("   5 = outstanding")

    rating_input = input("\nRating (1-5): ").strip()

    try:
        rating_num = int(rating_input)
        if rating_num < 1 or rating_num > 5:
            print("❌ Rating must be 1-5")
            return
    except ValueError:
        print("❌ Rating must be a number 1-5")
        return

    rating_map = {1: "poor", 2: "fair", 3: "good", 4: "excellent", 5: "outstanding"}
    rating = rating_map[rating_num]

    # Get comments
    print("\n💬 Optional comments:")
    comments = input("Comments (or press Enter to skip): ").strip()

    # Submit
    add_feedback(session_id, rating, comments if comments else None)


def main():
    """Main entry point"""

    if len(sys.argv) == 1:
        # Interactive mode
        interactive_mode()

    elif len(sys.argv) == 3:
        # Command-line mode: session_id rating
        session_id = sys.argv[1]
        rating = sys.argv[2]
        add_feedback(session_id, rating)

    elif len(sys.argv) == 4:
        # Command-line mode: session_id rating comments
        session_id = sys.argv[1]
        rating = sys.argv[2]
        comments = sys.argv[3]
        add_feedback(session_id, rating, comments)

    else:
        print("\n📝 MANUAL FEEDBACK ENTRY TOOL")
        print("="*60)
        print("\nUsage:")
        print("  Interactive mode:")
        print("    python add_feedback.py")
        print("\n  Command-line mode:")
        print("    python add_feedback.py <session_id> <rating>")
        print("    python add_feedback.py <session_id> <rating> <comments>")
        print("\nExamples:")
        print("  python add_feedback.py privacy_analysis_BLodgic_20251227 excellent")
        print('  python add_feedback.py privacy_analysis_BLodgic_20251227 good "Nice work"')
        print("\nRatings: poor, fair, good, excellent, outstanding")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()
