# Chapter 2, Lesson 02 - Complete Narration Script
## "MCP Server: Building Audit Trails for AI Compliance Tools"

---

## 📝 COMPLETE NARRATION SCRIPT

### **[INTRO - 30 seconds]**

> "In this lesson, we're going to look at the MCP server - that's Model Context Protocol - and understand why it's critical for compliance and security tools.
>
> Here's the problem: when you're using AI to analyze privacy policies, contracts, or security configurations, you need more than just the answer. You need an audit trail. You need to know when the analysis was run, what data was used, which AI model processed it, and how confident the system was in its results.
>
> MCP solves this problem by providing structured logging and memory for AI workflows. Let's see exactly how it works."

---

### **[CODE WALKTHROUGH PART 1: Overview - 60 seconds]**

**[SCREEN: Show privacy_mcp_server.py, lines 1-50]**

> "Let's start by looking at the code. This is our MCP server. It's a FastAPI application that exposes a JSON-RPC endpoint - that's a standard protocol for remote procedure calls.
>
> The server has five key capabilities, and you can see them listed here:
>
> **First**, memory tracking. Every analysis session gets logged with a unique session ID.
>
> **Second**, confidence scoring. The system automatically calculates how confident it is in each analysis.
>
> **Third**, token usage tracking. Every API call to GPT-4 gets logged with the exact token count - this is crucial for cost tracking and budgeting.
>
> **Fourth**, gap analysis storage. For our privacy compliance tool, we store every identified gap with its CCPA reference, priority level, and recommendations.
>
> **And fifth**, user feedback. Human reviewers can rate the quality of each analysis, creating a reinforcement learning loop.
>
> Together, these create a complete audit trail for compliance workflows."

---

### **[CODE WALKTHROUGH PART 2: Insert Memory - 45 seconds]**

**[SCREEN: Scroll to lines 60-85, highlight insert_memory method]**

> "Let's look at the first method: insert_memory. This is straightforward - it takes a session ID and text content.
>
> Look at line 79 - we're inserting into a memory table with the session ID, the text of the analysis, and a timestamp that's automatically added.
>
> When we run a gap analysis on a privacy policy, this method gets called automatically. The entire analysis result - all the identified gaps, recommendations, CCPA references - gets logged here.
>
> This means we can always go back and see exactly what the AI found in any given analysis session."

---

### **[CODE WALKTHROUGH PART 3: Gap Analysis - 45 seconds]**

**[SCREEN: Scroll to lines 135-160, highlight insert_gap_analysis method]**

> "Now let's look at insert_gap_analysis. This is compliance-specific and it's the heart of our audit trail.
>
> Every gap we identify gets logged with these fields: company name, gap description, CCPA reference - like Section 1798.105 - priority level, recommendation, and timestamp.
>
> This is crucial for compliance workflows. If an auditor asks 'Show me all the critical gaps you've identified in the last six months,' we can query this table and generate that report instantly.
>
> The data is structured, searchable, and tamper-evident. That's what makes it suitable for compliance and legal review."

---

### **[TERMINAL DEMO PART 1: Starting Server - 30 seconds]**

**[SCREEN: Switch to terminal, split screen if possible]**

> "Let's see this in action. First, I'm going to start the MCP server."

**[SCREEN: Terminal 1 - Type and run]**
```bash
python privacy_mcp_server.py
```

**[OUTPUT APPEARS]**
```
============================================================
Privacy Policy MCP Server
============================================================
Starting server on http://0.0.0.0:8080
MCP Endpoint: http://0.0.0.0:8080/mcp
Health Check: http://0.0.0.0:8080/health
============================================================

 * Running on http://127.0.0.1:8080
```

> "Great, the server is running. Notice it's listening on port 8080. The main endpoint is /mcp for JSON-RPC calls, and we also have /health for monitoring."

---

### **[TERMINAL DEMO PART 2: Running Demo - 2 minutes]**

**[SCREEN: Terminal 2 - Type and run]**
```bash
python demo_mcp_server.py --quick
```

> "Now I'm going to run our demo script that shows the four main operations."

**[OUTPUT: Demo 1 appears]**
```
--------------------------------------------------------------------------------
  DEMO 1: Logging Analysis Session
--------------------------------------------------------------------------------

📝 Creating analysis session: privacy_analysis_DemoCompany_...

⏳ Sending to MCP server...
   Endpoint: http://localhost:8080/mcp
   Method: insert_memory

✅ Session logged successfully!
   Session ID: privacy_analysis_DemoCompany_20251227_...
   Text length: 412 characters
   Timestamp: 2025-12-27T...
```

> "First, we're logging an analysis session. Notice the session ID - this is unique and includes the company name and timestamp. This is what appears at the bottom of every report we generate. The entire gap analysis - all the findings - gets stored under this session ID."

**[OUTPUT: Demo 2 appears]**
```
--------------------------------------------------------------------------------
  DEMO 2: Tracking Token Usage
--------------------------------------------------------------------------------

💰 Recording token usage for analysis:
   Model: gpt-4o
   Prompt tokens: 3,847
   Completion tokens: 1,203
   Total tokens: 5,050

✅ Token usage logged!

📊 This enables:
   • Cost tracking per analysis
   • Usage monitoring over time
   • Budget forecasting
   • Audit trail for AI usage
```

> "Second, we're tracking token usage. This particular analysis used 5,050 tokens from GPT-4. At current pricing, that's about 7 cents per analysis. But more importantly, this creates an audit trail of AI usage - you can prove to auditors exactly which AI model processed which data and when."

**[OUTPUT: Demo 3 appears]**
```
--------------------------------------------------------------------------------
  DEMO 3: Storing Gap Analysis Data
--------------------------------------------------------------------------------

🔍 Storing 3 compliance gaps:
   1. Right to Delete Disclosure (Critical)
   2. Do Not Sell Link (Critical)
   3. Data Retention Periods (High)

✅ Gap analysis stored!

📋 Compliance audit trail now includes:
   • Each gap with CCPA reference
   • Priority classification
   • Specific recommendations
   • Timestamp and session linkage
```

> "Third, we're storing the structured gap analysis. Each gap has a priority level - Critical, High, Medium, or Low. Each gap has a specific CCPA reference. And each gap has an actionable recommendation.
>
> This structured data is what makes the system auditable. You're not just storing unstructured text - you're storing queryable compliance data."

**[OUTPUT: Demo 4 appears]**
```
--------------------------------------------------------------------------------
  DEMO 4: Viewing Audit Trail
--------------------------------------------------------------------------------

1️⃣  Server Health & Statistics:
   Status: healthy
   Total Sessions: 3
   Total Analyses: 2
   Total Feedback: 1
   Token Logs: 3

2️⃣  Recent Analysis Sessions:
   • privacy_analysis_BLodgic_20251227_115333
   • privacy_analysis_BLodgic_20251227_171250
   • privacy_analysis_DemoCompany_20251227_...

3️⃣  Token Usage Log:
   Total tokens consumed: 14,269
   Total API calls: 3
```

> "And finally, we can view the complete audit trail. Look at these statistics - we can see every session, every token consumed, every analysis run. This is the kind of data compliance and legal teams need."

---

### **[BROWSER DEMO - 60 seconds]**

**[SCREEN: Open browser, navigate to localhost:8080/health]**

> "Let me show you something even better - we can access this data through a web browser."

**[SCREEN: Show JSON output]**
```json
{
  "status": "healthy",
  "service": "Privacy Policy MCP Server",
  "timestamp": "2025-12-27T17:45:12.345678",
  "stats": {
    "total_sessions": 3,
    "total_analyses": 2,
    "total_feedback": 1,
    "total_token_logs": 3
  }
}
```

> "First, the health endpoint shows server status and statistics."

**[SCREEN: Navigate to localhost:8080/debug/memory]**

> "The debug/memory endpoint shows all conversation logs - every analysis session we've run."

**[SCREEN: Navigate to localhost:8080/debug/gaps]**

> "The debug/gaps endpoint shows all identified compliance gaps - structured, searchable data."

**[SCREEN: Navigate to localhost:8080/debug/tokens]**

> "And debug/tokens shows complete token usage history - every API call, every model, every cost."

---

### **[WHY THIS MATTERS - 90 seconds]**

**[SCREEN: Switch to on-camera or slide]**

> "Now let me explain why this matters for compliance and security work.
>
> When you're building AI tools for regulated industries - finance, healthcare, legal, privacy compliance - audit trails aren't optional. They're mandatory.
>
> Here are the questions auditors WILL ask you:

**[SCREEN: Show bullet points on slide]**
- When was this analysis run?
- What data was analyzed?
- What AI model was used?
- How many tokens were consumed?
- What was the confidence level?
- Who reviewed and approved the results?

> "Without MCP, you'd have to answer these questions manually. You'd be digging through log files, trying to correlate timestamps, reconstructing what happened.
>
> With MCP, every one of these questions has a structured answer in the database.
>
> Let me give you a concrete example."

**[SCREEN: Show example report or code]**

> "When you generate a compliance report, you'll see a line like this at the bottom:
>
> 'Session ID: privacy_analysis_Audit_Caddie_20251202_140343'
>
> That session ID is your key to the complete audit trail. With that ID, you can retrieve:
>
> The **input** - what website was analyzed, how many characters in the privacy policy.
>
> The **analysis** - which CCPA requirements were used, which AI model, what temperature setting, how many tokens consumed.
>
> The **output** - how many gaps were identified, what priority levels, which CCPA sections were missing.
>
> And the **human feedback** - what rating did a reviewer give, what comments did they leave.
>
> This is a COMPLETE audit trail that stands up to legal review and regulatory scrutiny.
>
> And here's the key point: MCP is still new - it only launched in late 2024. But it's solving a real problem that enterprises have: how do we connect AI models to our data securely and auditablly?
>
> For compliance and security workflows, that auditability is absolutely critical."

---

### **[PRACTICAL EXAMPLE - 60 seconds]**

**[SCREEN: Show terminal with demo_mcp_server output or browser]**

> "Let me show you a practical scenario. Imagine your legal team asks:
>
> 'Show me all analyses where we found Critical gaps in the Right to Delete disclosure.'
>
> With MCP, you can query the gap_analysis table:"

**[SCREEN: Show example query or output]**
```python
# Query MCP for critical gaps
gaps = requests.get("http://localhost:8080/debug/gaps").json()

critical_delete_gaps = [
    gap for analysis in gaps
    for gap in analysis['gaps']
    if gap['priority'] == 'Critical'
    and 'delete' in gap['title'].lower()
]

print(f"Found {len(critical_delete_gaps)} critical deletion gaps")
```

> "Or your CFO asks: 'How much have we spent on GPT-4 API calls this month?'

**[SCREEN: Show token calculation]**
```python
# Calculate API costs
tokens = requests.get("http://localhost:8080/debug/tokens").json()

total_tokens = sum(t['tokens_total'] for t in tokens)
cost_per_1k = 0.015  # GPT-4 pricing

total_cost = (total_tokens / 1000) * cost_per_1k
print(f"Total API cost: ${total_cost:.2f}")
```

> "These aren't hypothetical examples - these are real questions you'll get asked when deploying AI tools in enterprise environments.
>
> MCP gives you the structured data to answer them instantly."

---

### **[WRAP-UP - 30 seconds]**

> "So to recap: MCP provides structured logging for AI workflows. For our privacy compliance tool, it tracks sessions, token usage, gap analyses, and human feedback - creating a complete audit trail.
>
> In the next lesson, we'll see how human feedback flows through this system, creating a reinforcement learning loop that improves the tool over time.
>
> I encourage you to explore the MCP endpoints yourself. Start the server, run some analyses, and look at the data structures in the debug endpoints. You'll see how everything ties together.
>
> Thanks for watching, and I'll see you in the next lesson."

---

## 🎯 Key Teaching Points Covered

| Concept | Explanation in Script |
|---------|---------------------|
| **What is MCP** | "Model Context Protocol - structured logging for AI" |
| **Why it matters** | "Audit trails for compliance are non-negotiable" |
| **Memory tracking** | "Every session logged with unique ID" |
| **Token tracking** | "Cost monitoring and AI usage audit trail" |
| **Gap storage** | "Structured, searchable compliance data" |
| **Audit trail** | "Answer auditor questions instantly" |
| **Real-world value** | "Legal review and regulatory scrutiny" |

---

## 📊 Script Timing

- **Intro**: 30 seconds
- **Code Walkthrough (3 parts)**: 150 seconds (2.5 minutes)
- **Terminal Demo**: 150 seconds (2.5 minutes)
- **Browser Demo**: 60 seconds
- **Why This Matters**: 90 seconds (1.5 minutes)
- **Practical Example**: 60 seconds
- **Wrap-up**: 30 seconds

**Total**: ~9 minutes (perfect for 10-minute LinkedIn Learning lesson)

---

## 🎬 Visual Cues for Editor

### Code Sections
1. **Lines 1-50**: Highlight the 5 capabilities list
2. **Lines 60-85**: Zoom in on SQL INSERT statement
3. **Lines 135-160**: Highlight gap analysis fields

### Terminal Output
1. **Server start**: Hold on "Running on..." message
2. **Demo output**: Slow scroll through each demo section
3. **Audit trail**: Pause on statistics for 3 seconds

### Browser Screens
1. **/health**: Zoom in on stats object
2. **/debug/memory**: Show JSON structure
3. **/debug/gaps**: Highlight gap objects
4. **/debug/tokens**: Show token totals

### Graphics to Add
1. **Audit trail diagram**: Show session → analysis → gaps → feedback flow
2. **MCP architecture**: Show client → server → database
3. **Questions slide**: List auditor questions
4. **Example query**: Show Python code with syntax highlighting

---

## 🔧 Demo Script Commands

### Preparation
```bash
# Terminal 1: Start MCP server
cd privacy_gap_analysis/scripts
python privacy_mcp_server.py

# Terminal 2: Run demo
python demo_mcp_server.py --quick
```

### Browser URLs to Show
```
http://localhost:8080/health
http://localhost:8080/debug/memory
http://localhost:8080/debug/confidence
http://localhost:8080/debug/feedback
http://localhost:8080/debug/tokens
http://localhost:8080/debug/gaps
```

---

## 📝 Key Quotes for Emphasis

> "For compliance and security tools, audit trails are NON-NEGOTIABLE."

> "MCP gives us structured logging for all of this."

> "This is a COMPLETE audit trail that stands up to legal review."

> "MCP is solving a real problem: how do we connect AI models to enterprise data securely and auditablly?"

---

## 🎥 Post-Production Tips

### Pacing
- **Slow down** during code walkthrough (students taking notes)
- **Speed up** 1.2x during server startup loading
- **Normal speed** for terminal demo output
- **Slow down** for "why this matters" section

### B-roll Suggestions
- Database diagram showing tables
- Example audit report
- Compliance checklist
- Enterprise dashboard mockup

### Annotations to Add
- Arrow pointing to session ID in output
- Highlight token counts
- Circle priority levels
- Underline CCPA references

---

**This script is ready for recording!** 🎥📹

**Estimated recording time**: 10 minutes
**Estimated editing time**: Add 5-10 minutes for graphics/b-roll
**Final lesson length**: 8-9 minutes
