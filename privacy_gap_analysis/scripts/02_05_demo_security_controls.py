#!/usr/bin/env python3
"""
LinkedIn Learning Course - Chapter 2, Lesson 05
Demo: Security Considerations for RAG/MCP Systems

This demo shows 5 critical security controls needed for production deployment:
1. Sandboxing & Access Control
2. Input Validation & Sanitization
3. Rate Limiting & Cost Controls
4. Secrets Management
5. Audit Logging & Monitoring

Usage:
    python 02_05_demo_security_controls.py          # Interactive mode (pauses for explanation)
    python 02_05_demo_security_controls.py --quick  # Quick mode (auto-run for recording)
"""

import sys
import time
import os
import re
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path

def print_section(title, width=80):
    """Print a section header"""
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width + "\n")

def print_control(num, title):
    """Print a security control header"""
    print(f"\n{'=' * 80}")
    print(f"  SECURITY CONTROL {num}: {title}")
    print(f"{'=' * 80}\n")

def print_code_block(title, code, is_vulnerable=False):
    """Print a code block with header"""
    status = "VULNERABLE" if is_vulnerable else "HARDENED"
    marker = "X" if is_vulnerable else "✓"

    print(f"\n[{marker}] {title} ({status})")
    print("-" * 80)
    for line in code.strip().split('\n'):
        print(f"  {line}")
    print("-" * 80)

def pause(message="Press Enter to continue...", quick_mode=False):
    """Pause for user input unless in quick mode"""
    if not quick_mode:
        input(f"\n{message}")
    else:
        time.sleep(2)

def demo_intro(quick_mode=False):
    """Introduction to security considerations"""
    print_section("Security Considerations for RAG/MCP Systems")

    print("Our demo works, but it's NOT production-ready yet.")
    print()
    print("In production, you need to think about:")
    print("  - Access Control")
    print("  - Input Validation")
    print("  - Rate Limiting")
    print("  - Secrets Management")
    print("  - Audit Logging")
    print()
    print("These aren't optional for compliance tools.")
    print("If your AI system gets compromised or leaks data, you're liable.")
    print()
    print("Let's examine 5 critical security controls...")

    pause("Ready to begin? Press Enter...", quick_mode)

def demo_control_1(quick_mode=False):
    """Control 1: Sandboxing & Access Control"""
    print_control(1, "Sandboxing & Access Control")

    print("PROBLEM: Anyone can access your MCP server endpoints")
    print()

    vulnerable_code = """
@app.route('/debug/gaps', methods=['GET'])
def debug_gaps():
    # Returns ALL gap analyses
    # No authentication, no authorization
    return jsonify(gap_analysis_store)
"""

    print_code_block("Current MCP Server", vulnerable_code, is_vulnerable=True)

    print()
    print("RISK: Competitors could see your client's compliance gaps.")
    print("      Sensitive data exposed without authentication.")

    pause("Press Enter to see the hardened version...", quick_mode)

    hardened_code = """
from functools import wraps
from flask import request
import os

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('MCP_API_KEY'):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/debug/gaps', methods=['GET'])
@require_api_key  # Now requires valid API key
def debug_gaps():
    return jsonify(gap_analysis_store)
"""

    print_code_block("Hardened MCP Server", hardened_code, is_vulnerable=False)

    print()
    print("FIX: API key authentication using decorator pattern")
    print("     - Checks X-API-Key header against environment variable")
    print("     - Returns 401 Unauthorized if key is missing or invalid")
    print("     - Applied to all sensitive endpoints")

    pause("Control 1 complete. Press Enter...", quick_mode)

def demo_control_2(quick_mode=False):
    """Control 2: Input Validation & Sanitization"""
    print_control(2, "Input Validation & Sanitization")

    print("PROBLEM: Malicious input could break your system or manipulate results")
    print()

    vulnerable_code = """
url = input("Enter company homepage URL: ").strip()
company_name = input("Enter company name: ").strip()

# No validation! User could enter:
# - "javascript:alert(1)"
# - "file:///etc/passwd"
# - "'; DROP TABLE users; --"

scrape_privacy_policy(url)  # Potential command injection
"""

    print_code_block("Vulnerable Input Handling", vulnerable_code, is_vulnerable=True)

    print()
    print("RISK: XSS, command injection, or malformed data breaking the pipeline")

    pause("Press Enter to see the hardened version...", quick_mode)

    hardened_code = """
import re
from urllib.parse import urlparse

def validate_url(url):
    \"\"\"Validate URL is HTTP/HTTPS with valid domain\"\"\"
    # Must be HTTP/HTTPS
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL scheme - must be HTTP or HTTPS")

    # Must have valid domain
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid domain")

    # No javascript: or file: schemes
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Only HTTP/HTTPS allowed")

    return url

def validate_company_name(name):
    \"\"\"Validate company name contains only safe characters\"\"\"
    if not re.match(r'^[a-zA-Z0-9\s\-_\.]+$', name):
        raise ValueError("Invalid company name - only alphanumeric and basic punctuation allowed")
    if len(name) > 100:
        raise ValueError("Company name too long")
    return name

# Usage
url = input("Enter company homepage URL: ").strip()
url = validate_url(url)  # Validated

company_name = input("Enter company name: ").strip()
company_name = validate_company_name(company_name)  # Validated
"""

    print_code_block("Hardened Input Validation", hardened_code, is_vulnerable=False)

    print()
    print("FIX: Strict validation functions")
    print("     - URL validation: Only HTTP/HTTPS, valid domain")
    print("     - Company name: Alphanumeric + safe punctuation only")
    print("     - Length limits to prevent buffer overflows")

    # Demonstrate validation
    print("\nLet's test the validation:")

    test_cases = [
        ("https://example.com", True),
        ("javascript:alert(1)", False),
        ("file:///etc/passwd", False),
        ("http://valid-site.com", True),
    ]

    for test_url, should_pass in test_cases:
        try:
            validate_url(test_url)
            result = "PASS"
        except ValueError:
            result = "BLOCKED"

        expected = "PASS" if should_pass else "BLOCKED"
        status = "✓" if result == expected else "X"
        print(f"  {status} {test_url:40s} -> {result}")

    pause("Control 2 complete. Press Enter...", quick_mode)

def demo_control_3(quick_mode=False):
    """Control 3: Rate Limiting & Cost Controls"""
    print_control(3, "Rate Limiting & Cost Controls")

    print("PROBLEM: Runaway API costs if someone abuses your tool")
    print()
    print("SCENARIO: Attacker finds your tool, runs 1,000 gap analyses")
    print("          -> $500 OpenAI bill")
    print()

    pause("Press Enter to see the solution...", quick_mode)

    rate_limit_code = """
import time
from collections import defaultdict

# Simple in-memory rate limiter
request_times = defaultdict(list)

def rate_limit(client_id, max_requests=5, window_seconds=60):
    \"\"\"Enforce rate limit per client\"\"\"
    now = time.time()

    # Clean old requests outside the time window
    request_times[client_id] = [
        t for t in request_times[client_id]
        if now - t < window_seconds
    ]

    # Check if limit exceeded
    if len(request_times[client_id]) >= max_requests:
        raise Exception(f"Rate limit exceeded: {max_requests} requests per {window_seconds}s")

    # Log this request
    request_times[client_id].append(now)
    return True

# Usage before each analysis
client_id = request.headers.get('X-API-Key', request.remote_addr)
rate_limit(client_id, max_requests=5, window_seconds=60)
"""

    print_code_block("Rate Limiting Implementation", rate_limit_code, is_vulnerable=False)

    print()

    budget_code = """
# Budget caps to prevent runaway costs
MAX_TOKENS_PER_ANALYSIS = 10000  # ~$0.15 per analysis with GPT-4
MAX_DAILY_ANALYSES = 100
MAX_DAILY_COST = 50.00  # USD

def check_budget(tokens_used, daily_cost):
    \"\"\"Check if budget limits are exceeded\"\"\"
    if tokens_used > MAX_TOKENS_PER_ANALYSIS:
        raise Exception(f"Analysis exceeded token limit: {tokens_used} > {MAX_TOKENS_PER_ANALYSIS}")

    if daily_cost > MAX_DAILY_COST:
        raise Exception(f"Daily cost limit exceeded: ${daily_cost:.2f} > ${MAX_DAILY_COST}")

    return True
"""

    print_code_block("Budget Controls", budget_code, is_vulnerable=False)

    print()
    print("FIX: Two-layer protection")
    print("     1. Rate Limiting: 5 requests per 60 seconds per client")
    print("     2. Budget Caps: Token limits + daily cost limits")
    print()

    # Simulate rate limiting
    print("Simulating rate limit enforcement:")
    print()

    client = "test_client"
    request_times.clear()

    for i in range(7):
        try:
            rate_limit(client, max_requests=5, window_seconds=2)
            print(f"  ✓ Request {i+1}: ALLOWED")
            time.sleep(0.3)
        except Exception as e:
            print(f"  X Request {i+1}: BLOCKED - {e}")

    pause("Control 3 complete. Press Enter...", quick_mode)

def demo_control_4(quick_mode=False):
    """Control 4: Secrets Management"""
    print_control(4, "Secrets Management")

    print("PROBLEM: API keys hardcoded or committed to git")
    print()

    bad_practice_1 = """
# DON'T DO THIS - Hardcoded API key
openai_client = OpenAI(api_key="sk-abc123...")  # HARDCODED!
"""

    print_code_block("BAD PRACTICE 1: Hardcoded Keys", bad_practice_1, is_vulnerable=True)

    bad_practice_2 = """
# DON'T DO THIS - API key in code
import os
os.environ["OPENAI_API_KEY"] = "sk-abc123..."  # Still bad!
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
"""

    print_code_block("BAD PRACTICE 2: Keys in Code", bad_practice_2, is_vulnerable=True)

    print()
    print("RISK: API keys leaked in git history, visible in code reviews")
    print("      Attacker could use your keys to rack up charges")

    pause("Press Enter to see the correct approach...", quick_mode)

    # Show .env file example
    print("\n[FILE: .env]")
    print("-" * 80)
    print("  OPENAI_API_KEY=sk-abc123...")
    print("  MCP_API_KEY=secret-key-here")
    print("  DATABASE_URL=postgresql://...")
    print("-" * 80)

    print("\n[FILE: .gitignore]")
    print("-" * 80)
    print("  .env")
    print("  *.env")
    print("  .env.*")
    print("  secrets/")
    print("-" * 80)

    correct_practice = """
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
openai_key = os.getenv("OPENAI_API_KEY", "")
if not openai_key:
    raise ValueError("OPENAI_API_KEY not set in environment")

# Use the key securely
openai_client = OpenAI(api_key=openai_key)
"""

    print_code_block("CORRECT PRACTICE: Environment Variables", correct_practice, is_vulnerable=False)

    print()
    print("FIX: Environment variables + .gitignore")
    print("     - Store secrets in .env file (never committed)")
    print("     - Load with python-dotenv")
    print("     - Validate that required secrets are present")
    print()
    print("PRODUCTION: Use AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault")

    pause("Control 4 complete. Press Enter...", quick_mode)

def demo_control_5(quick_mode=False):
    """Control 5: Audit Logging & Monitoring"""
    print_control(5, "Audit Logging & Monitoring")

    print("PROBLEM: No visibility into what's happening in your system")
    print()
    print("You need to log:")
    print("  - Who ran an analysis (user/API key)")
    print("  - When it ran (timestamp)")
    print("  - What data was analyzed (company name, URLs)")
    print("  - What model was used (gpt-4, version)")
    print("  - How much it cost (tokens, USD)")
    print("  - What was the output (gap count, confidence)")
    print("  - Any errors or anomalies")
    print()

    pause("Press Enter to see our implementation...", quick_mode)

    print("GOOD NEWS: We already have this via MCP server!")
    print()

    mcp_logging = """
# MCP Server provides comprehensive audit logging:

# 1. Log analysis sessions
mcp_client.insert_memory(
    session_id="privacy_analysis_Company_20251207_143521",
    text="Full gap analysis results..."
)

# 2. Track API costs
mcp_client.insert_token_usage(
    session_id="privacy_analysis_Company_20251207_143521",
    model="gpt-4",
    tokens_prompt=3847,
    tokens_completion=1203,
    tokens_total=5050
)

# 3. Store compliance findings
mcp_client.insert_gap_analysis(
    session_id="privacy_analysis_Company_20251207_143521",
    company="Example Corp",
    gaps=[
        {
            "title": "Right to Delete Disclosure",
            "reference": "CCPA Section 1798.105",
            "priority": "Critical"
        }
    ]
)

# 4. Log confidence scores
mcp_client.insert_confidence(
    query="Gap analysis for Example Corp",
    response="16 gaps identified...",
    score=0.92
)
"""

    print_code_block("MCP Audit Logging", mcp_logging, is_vulnerable=False)

    print()
    print("Access logs at: http://localhost:8080/debug/*")
    print()
    print("Available endpoints:")
    print("  /debug/memory      - All analysis sessions")
    print("  /debug/tokens      - Token usage and costs")
    print("  /debug/gaps        - Compliance findings")
    print("  /debug/confidence  - Confidence scores")
    print("  /debug/feedback    - User feedback")

    pause("Control 5 complete. Press Enter for recap...", quick_mode)

def demo_recap(quick_mode=False):
    """Recap all security controls"""
    print_section("SECURITY CHECKLIST - RECAP")

    print("Production-ready security in 5 controls:")
    print()
    print("  [✓] 1. Sandboxing & Access Control")
    print("      - API key authentication on all endpoints")
    print("      - 401 Unauthorized for invalid keys")
    print()
    print("  [✓] 2. Input Validation & Sanitization")
    print("      - URL validation (HTTP/HTTPS only)")
    print("      - Company name sanitization")
    print("      - Length limits on all inputs")
    print()
    print("  [✓] 3. Rate Limiting & Cost Controls")
    print("      - 5 requests per 60 seconds per client")
    print("      - Max tokens per analysis: 10,000")
    print("      - Daily cost cap: $50")
    print()
    print("  [✓] 4. Secrets Management")
    print("      - .env files for local development")
    print("      - .gitignore to prevent commits")
    print("      - Cloud secrets manager for production")
    print()
    print("  [✓] 5. Audit Logging & Monitoring")
    print("      - MCP server logs all activities")
    print("      - Token usage tracked for cost monitoring")
    print("      - Compliance findings stored with timestamps")
    print()
    print("KEY INSIGHT:")
    print("  Security isn't an afterthought - it's part of the architecture from day one.")
    print()
    print("These controls make your RAG/MCP system production-ready for real clients.")
    print()

def run_full_demo():
    """Run full interactive demo with pauses"""
    print("\n" + "=" * 80)
    print("  INTERACTIVE MODE")
    print("  This demo will pause between security controls for explanation")
    print("=" * 80)

    demo_intro(quick_mode=False)
    demo_control_1(quick_mode=False)
    demo_control_2(quick_mode=False)
    demo_control_3(quick_mode=False)
    demo_control_4(quick_mode=False)
    demo_control_5(quick_mode=False)
    demo_recap(quick_mode=False)

    print("Demo complete!")

def run_quick_demo():
    """Run quick demo for screen recording"""
    print("\n" + "=" * 80)
    print("  QUICK MODE - Auto-running for screen recording")
    print("=" * 80)
    time.sleep(2)

    demo_intro(quick_mode=True)
    demo_control_1(quick_mode=True)
    demo_control_2(quick_mode=True)
    demo_control_3(quick_mode=True)
    demo_control_4(quick_mode=True)
    demo_control_5(quick_mode=True)
    demo_recap(quick_mode=True)

    print("Demo complete!")

# Helper function used in demo
def validate_url(url):
    """Validate URL is HTTP/HTTPS with valid domain"""
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL scheme - must be HTTP or HTTPS")

    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid domain")

    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Only HTTP/HTTPS allowed")

    return url

# Helper function for rate limiting demo
from collections import defaultdict
request_times = defaultdict(list)

def rate_limit(client_id, max_requests=5, window_seconds=60):
    """Enforce rate limit per client"""
    now = time.time()

    request_times[client_id] = [
        t for t in request_times[client_id]
        if now - t < window_seconds
    ]

    if len(request_times[client_id]) >= max_requests:
        raise Exception(f"Rate limit exceeded: {max_requests} requests per {window_seconds}s")

    request_times[client_id].append(now)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    else:
        run_full_demo()
