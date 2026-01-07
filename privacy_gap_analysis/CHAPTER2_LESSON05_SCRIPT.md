# Chapter 2, Lesson 05 - Complete Narration Script
## "Security Considerations for Production RAG/MCP Systems"

---

## COMPLETE NARRATION SCRIPT

### [INTRO - 35 seconds]

> "In this lesson, we're going to talk about security. Our demo works, but it's not production-ready yet.
>
> In production, you need to think about access control, input validation, rate limiting, secrets management, and audit logging.
>
> These aren't optional for compliance tools. If your AI system gets compromised or leaks data, you're liable. Your clients trust you with their sensitive compliance data.
>
> I'm going to show you five security controls we need to add before deploying this tool to real clients. Let's get started."

---

### [SECURITY CONTROL 1: Sandboxing & Access Control - 90 seconds]

**[SCREEN: Show demo script or code editor]**

> "Let's start with access control. Right now, our MCP server has a big problem."

**[SCREEN: Show privacy_mcp_server.py - current debug endpoint]**

```python
@app.route('/debug/gaps', methods=['GET'])
def debug_gaps():
    # Returns ALL gap analyses
    # No authentication, no authorization
    return jsonify(gap_analysis_store)
```

> "Look at this debug endpoint. Anyone can access it. There's no authentication, no authorization. If you know the URL - localhost:8080/debug/gaps - you can see all the gap analyses for every client.
>
> This is a massive security risk. Imagine a competitor discovering this endpoint. They could see all your client's compliance gaps, their weaknesses, their legal exposure. That's confidential business information.
>
> Here's the fix."

**[SCREEN: Show hardened version]**

```python
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
```

> "We add an API key decorator. Before the endpoint runs, it checks the X-API-Key header. If the key doesn't match the environment variable MCP_API_KEY, it returns 401 Unauthorized.
>
> Now only clients with the correct API key can access the endpoint. This is a simple but effective access control mechanism."

---

### [SECURITY CONTROL 2: Input Validation - 2 minutes]

**[SCREEN: Show run_privacy_analysis.py - input handling]**

> "Security control two: input validation.
>
> Look at this code from our privacy analysis script."

```python
url = input("Enter company homepage URL: ").strip()
company_name = input("Enter company name: ").strip()

scrape_privacy_policy(url)
```

> "We're taking user input directly and passing it to our web scraper. No validation. A user could enter 'javascript:alert(1)' or 'file:///etc/passwd'.
>
> This opens us up to command injection, path traversal, and other attacks.
>
> Here's how we fix it."

**[SCREEN: Show validation functions]**

```python
import re
from urllib.parse import urlparse

def validate_url(url):
    # Must be HTTP/HTTPS
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL scheme - must be HTTP or HTTPS")

    # Must have valid domain
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid domain")

    # Only allow HTTP/HTTPS schemes
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Only HTTP/HTTPS allowed")

    return url

def validate_company_name(name):
    # Only alphanumeric and safe punctuation
    if not re.match(r'^[a-zA-Z0-9\s\-_\.]+$', name):
        raise ValueError("Invalid company name")
    if len(name) > 100:
        raise ValueError("Company name too long")
    return name

# Usage
url = validate_url(input("Enter URL: ").strip())
company_name = validate_company_name(input("Enter company: ").strip())
```

> "We create validation functions. The URL validator checks three things: the scheme must be HTTP or HTTPS, the domain must be valid, and we explicitly block javascript: and file: schemes.
>
> The company name validator uses a regex to only allow alphanumeric characters and basic punctuation. We also add a length limit to prevent buffer overflows.
>
> Let's test this."

**[SCREEN: Run demo showing validation tests]**

```
Testing URL validation:
  ✓ https://example.com              -> PASS
  X javascript:alert(1)               -> BLOCKED
  X file:///etc/passwd                -> BLOCKED
  ✓ http://valid-site.com             -> PASS
```

> "The validation works. Legitimate URLs pass, malicious ones are blocked. This is input sanitization in action."

---

### [SECURITY CONTROL 3: Rate Limiting & Cost Controls - 2 minutes]

**[SCREEN: Show slide or code]**

> "Security control three: rate limiting and cost controls.
>
> Here's a scary scenario. An attacker finds your tool and writes a script to run 1,000 gap analyses in a row. Each analysis costs about 50 cents in GPT-4 API calls. That's a $500 bill.
>
> Or imagine an infinite loop in your code - it keeps calling GPT-4 until you hit your credit card limit.
>
> We need two protections: rate limiting and budget caps."

**[SCREEN: Show rate limiting code]**

```python
import time
from collections import defaultdict

request_times = defaultdict(list)

def rate_limit(client_id, max_requests=5, window_seconds=60):
    now = time.time()

    # Clean old requests outside the time window
    request_times[client_id] = [
        t for t in request_times[client_id]
        if now - t < window_seconds
    ]

    # Check if limit exceeded
    if len(request_times[client_id]) >= max_requests:
        raise Exception("Rate limit exceeded")

    # Log this request
    request_times[client_id].append(now)
```

> "This is a simple in-memory rate limiter. For each client - identified by API key or IP address - we track when they made requests. If they exceed 5 requests in 60 seconds, we reject the request.
>
> This prevents abuse."

**[SCREEN: Show budget caps code]**

```python
# Budget caps to prevent runaway costs
MAX_TOKENS_PER_ANALYSIS = 10000  # ~$0.15 per analysis
MAX_DAILY_ANALYSES = 100
MAX_DAILY_COST = 50.00  # USD

def check_budget(tokens_used, daily_cost):
    if tokens_used > MAX_TOKENS_PER_ANALYSIS:
        raise Exception(f"Analysis exceeded token limit: {tokens_used}")
    if daily_cost > MAX_DAILY_COST:
        raise Exception(f"Daily cost limit exceeded: ${daily_cost:.2f}")
```

> "And we add budget caps. Each analysis has a token limit - if it exceeds 10,000 tokens, something's wrong, so we abort. We also cap daily costs at $50.
>
> These two controls together prevent runaway costs."

**[SCREEN: Demo rate limiting in action]**

```
Simulating rate limit enforcement:
  ✓ Request 1: ALLOWED
  ✓ Request 2: ALLOWED
  ✓ Request 3: ALLOWED
  ✓ Request 4: ALLOWED
  ✓ Request 5: ALLOWED
  X Request 6: BLOCKED - Rate limit exceeded
  X Request 7: BLOCKED - Rate limit exceeded
```

> "Here's the rate limiter in action. First five requests go through, then we start blocking. It works."

---

### [SECURITY CONTROL 4: Secrets Management - 90 seconds]

**[SCREEN: Show vulnerable code]**

> "Security control four: secrets management.
>
> This is a mistake I see all the time."

```python
# DON'T DO THIS
openai_client = OpenAI(api_key="sk-abc123...")
```

> "Hardcoded API key directly in the code. If you commit this to git, your key is exposed forever in the git history. Anyone who clones your repo has your API key.
>
> Or this variation:"

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-abc123..."
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

> "Still hardcoded, just in an environment variable. This is still bad.
>
> Here's the correct approach."

**[SCREEN: Show .env file]**

```
# File: .env
OPENAI_API_KEY=sk-abc123...
MCP_API_KEY=secret-key-here
```

**[SCREEN: Show .gitignore]**

```
# File: .gitignore
.env
*.env
.env.*
```

**[SCREEN: Show correct code]**

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

openai_key = os.getenv("OPENAI_API_KEY", "")
if not openai_key:
    raise ValueError("OPENAI_API_KEY not set")

openai_client = OpenAI(api_key=openai_key)
```

> "We store secrets in a .env file that's never committed to git - notice it's in .gitignore. We load it with python-dotenv, and we validate that the key is present before proceeding.
>
> For production, use AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault. But for development, .env files are fine - as long as you never commit them."

---

### [SECURITY CONTROL 5: Audit Logging - 90 seconds]

**[SCREEN: Show code or slide]**

> "Security control five: audit logging and monitoring.
>
> You need visibility into what's happening in your system. For a compliance tool, this is absolutely critical.
>
> You need to log:
> - Who ran an analysis - the user or API key
> - When it ran - timestamp
> - What data was analyzed - company name, URLs
> - What model was used - GPT-4, which version
> - How much it cost - tokens consumed, dollar amount
> - What was the output - how many gaps, confidence scores
> - Any errors or anomalies
>
> Good news: we already have this."

**[SCREEN: Show MCP logging code]**

```python
# Log analysis session
mcp_client.insert_memory(
    session_id="privacy_analysis_Company_20251207_143521",
    text="Full gap analysis results..."
)

# Track API costs
mcp_client.insert_token_usage(
    session_id="privacy_analysis_Company_20251207_143521",
    model="gpt-4",
    tokens_total=5050
)

# Store compliance findings
mcp_client.insert_gap_analysis(
    session_id="privacy_analysis_Company_20251207_143521",
    company="Example Corp",
    gaps=[...]
)
```

> "The MCP server we built in lesson 2 provides all of this. Every analysis gets logged to memory. Token usage is tracked. Gaps are stored with timestamps. Confidence scores are recorded.
>
> This gives us a complete audit trail."

**[SCREEN: Browser - navigate to localhost:8080/debug/tokens]**

> "Let me show you what this looks like."

**[SCREEN: Show JSON output]**

```json
{
  "total_tokens_today": 4847,
  "total_cost_today": "$0.12",
  "queries": [
    {
      "query": "Gap analysis for Example Corp",
      "model": "gpt-4",
      "tokens": 4847,
      "timestamp": "2025-12-12T10:30:45"
    }
  ]
}
```

> "Here's the token usage endpoint. We can see total tokens consumed today, estimated cost, and a breakdown by query. This is our audit trail for compliance and cost monitoring.
>
> If an auditor asks, 'Show me all analyses run in December,' we query the MCP database and generate that report instantly."

---

### [RECAP - 60 seconds]

**[SCREEN: Show checklist slide or return to demo]**

> "Let me recap the five security controls.
>
> **Control 1: Sandboxing and Access Control.** API key authentication on all sensitive endpoints. No unauthorized access to client data.
>
> **Control 2: Input Validation.** Strict validation of URLs and company names. Block malicious input before it reaches your system.
>
> **Control 3: Rate Limiting and Cost Controls.** Five requests per minute per client. Token limits per analysis. Daily budget caps. No runaway costs.
>
> **Control 4: Secrets Management.** Environment variables for secrets, never committed to git. Cloud secrets managers for production.
>
> **Control 5: Audit Logging and Monitoring.** MCP server logs everything - who, what, when, how much. Complete audit trail for compliance review.
>
> These five controls make your RAG and MCP system production-ready. Without them, you're not ready for real clients."

---

### [WHY THIS MATTERS - 45 seconds]

**[SCREEN: On-camera or slide]**

> "Here's why this matters.
>
> When you're building AI tools for regulated industries - finance, healthcare, legal, compliance - security isn't optional. You're handling sensitive data. Privacy policies, legal documents, compliance findings.
>
> If your system gets compromised, you could leak confidential information about your client's legal vulnerabilities. That's a lawsuit. That's lost business.
>
> And if your API costs run out of control, that's money out of your pocket - or worse, an angry client who got a $10,000 bill because you didn't implement rate limiting.
>
> Security is part of the architecture from day one. Not an afterthought."

---

### [TRANSITION TO NEXT CHAPTER - 25 seconds]

> "Now that we have the foundations in place - RAG for semantic search, MCP for audit trails, and security controls for production deployment - we're ready to build the full automation workflow.
>
> In Chapter 3, we're going to automate the compliance checking process. We'll see how to use AI to identify gaps, but also where AI can go wrong and where you still need human review.
>
> That's the balance we're looking for: AI for efficiency, humans for judgment."

---

### [WRAP-UP - 20 seconds]

> "So to wrap up: production-ready AI systems need five security controls. Access control, input validation, rate limiting, secrets management, and audit logging.
>
> Implement these controls before you deploy to real clients. Your data, your costs, and your reputation depend on it.
>
> Thanks for watching. I'll see you in the next chapter."

---

## Key Teaching Points Covered

| Concept | Explanation in Script |
|---------|---------------------|
| **Access Control** | "API key authentication - no unauthorized access to client data" |
| **Input Validation** | "Block malicious input before it reaches your system" |
| **Rate Limiting** | "5 requests per minute - prevents abuse and runaway costs" |
| **Secrets Management** | "Environment variables, never committed to git" |
| **Audit Logging** | "MCP logs everything - complete audit trail for compliance" |
| **Production Readiness** | "Security is part of the architecture from day one" |
| **Real-World Risk** | "Leaked data = lawsuit. Runaway costs = angry clients" |

---

## Script Timing

- **Intro**: 35 seconds
- **Control 1 (Access Control)**: 90 seconds (1.5 minutes)
- **Control 2 (Input Validation)**: 120 seconds (2 minutes)
- **Control 3 (Rate Limiting)**: 120 seconds (2 minutes)
- **Control 4 (Secrets Management)**: 90 seconds (1.5 minutes)
- **Control 5 (Audit Logging)**: 90 seconds (1.5 minutes)
- **Recap**: 60 seconds
- **Why This Matters**: 45 seconds
- **Transition**: 25 seconds
- **Wrap-up**: 20 seconds

**Total**: ~11.5 minutes (fits comfortably in 12-minute lesson slot)

---

## Visual Cues for Editor

### Code Sections
1. **Vulnerable vs Hardened**: Side-by-side comparison with X and ✓ markers
2. **Control 1**: Highlight @require_api_key decorator
3. **Control 2**: Show validation tests passing/failing in terminal
4. **Control 3**: Animate rate limiting counter (requests 1-7)
5. **Control 4**: Show .env and .gitignore files
6. **Control 5**: Browser showing MCP debug endpoints

### Graphics to Add
1. **Security Checklist**: 5 controls with checkmarks
2. **Vulnerable vs Hardened**: Code comparison graphic
3. **Authentication Flow**: API key → validation → access granted/denied
4. **Rate Limiting Graph**: Requests over time hitting limit
5. **Secrets Management Flow**: .env → dotenv → app (with X on git)
6. **Audit Trail Dashboard**: Sample MCP logs visualization

### Annotations to Add
- Red X on vulnerable code examples
- Green checkmark on hardened code
- Arrow pointing to @require_api_key decorator
- Circle validation regex pattern
- Highlight rate limit threshold (5 requests)
- Underline "never committed to git"
- Box around MCP logging methods

---

## Demo Script Commands

### Preparation
```bash
# Run the security demo (interactive mode)
cd privacy_gap_analysis/scripts
python 02_05_demo_security_controls.py

# Run the security demo (quick mode for recording)
python 02_05_demo_security_controls.py --quick
```

### Browser URLs to Show
```
http://localhost:8080/debug/tokens
http://localhost:8080/debug/memory
http://localhost:8080/debug/gaps
```

---

## Key Quotes for Emphasis

> "If your AI system gets compromised or leaks data, you're liable."

> "Security isn't optional for compliance tools."

> "These five controls make your system production-ready. Without them, you're not ready for real clients."

> "Security is part of the architecture from day one. Not an afterthought."

> "Leaked data = lawsuit. Runaway costs = angry clients."

---

## Post-Production Tips

### Pacing
- **Slow down** during vulnerable code examples (let risk sink in)
- **Normal speed** for hardened code solutions
- **Emphasize** the rate limiting demo (visual proof)
- **Slow down** for secrets management (common mistake)

### B-roll Suggestions
- Newspaper headlines about data breaches
- API cost dashboard showing high charges
- Git commit history showing exposed secrets
- Security audit report mockup
- MCP dashboard with real data

### Annotations to Add
- Red "VULNERABLE" label on bad code
- Green "HARDENED" label on fixed code
- Animated rate limiter counter
- Cost meter showing budget cap
- Padlock icon on secured endpoints

---

## Alternative Demo Approach

If you prefer live coding instead of the demo script:

1. Start with vulnerable MCP server (no auth)
2. Show in browser - anyone can access /debug/gaps
3. Add @require_api_key decorator live
4. Test with curl showing 401 Unauthorized
5. Repeat for each security control

This requires more careful scripting but shows the "before and after" more dramatically.

---

## Slides/Diagrams Needed

### 1. Security Checklist (Intro Slide)
```
PRODUCTION-READY SECURITY: 5 CONTROLS

1. Sandboxing & Access Control
2. Input Validation & Sanitization
3. Rate Limiting & Cost Controls
4. Secrets Management
5. Audit Logging & Monitoring
```

### 2. Vulnerable vs Hardened Code (Repeated for each control)
```
[X] VULNERABLE          |  [✓] HARDENED
------------------------|------------------------
No authentication       |  API key required
No input validation     |  Strict validation
No rate limits          |  5 req/min limit
Hardcoded secrets       |  .env + .gitignore
No audit trail          |  MCP logging
```

### 3. Authentication Flow Diagram
```
Request
  → Check X-API-Key header
    → Valid? → Allow access
    → Invalid? → 401 Unauthorized
```

### 4. Rate Limiting Visualization
```
Requests over time:
Request 1 ✓
Request 2 ✓
Request 3 ✓
Request 4 ✓
Request 5 ✓
Request 6 X (LIMIT REACHED)
Request 7 X (BLOCKED)
```

### 5. Secrets Management Workflow
```
.env file → dotenv → Application
    ↓
.gitignore (NEVER COMMIT)
```

### 6. Audit Trail Components
```
MCP Server Logs:
├── insert_memory (analysis sessions)
├── insert_token_usage (API costs)
├── insert_gap_analysis (findings)
└── insert_confidence (quality scores)
```

---

**This script is ready for recording!**

**Estimated recording time**: 12 minutes
**Estimated editing time**: Add 10-15 minutes for graphics/diagrams
**Final lesson length**: 10-11 minutes
