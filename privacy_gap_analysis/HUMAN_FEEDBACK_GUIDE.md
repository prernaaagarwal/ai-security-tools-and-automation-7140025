# Human Feedback Reinforcement Learning System

## Overview

The Privacy Compliance Calculator now includes a comprehensive human feedback reinforcement learning (HFRL) system that automatically collects and stores feedback data to improve analysis quality over time.

## 🎯 Three Feedback Mechanisms

### 1. **Automatic Confidence Scoring**

**What it measures:**
- Analysis comprehensiveness (length and detail)
- CCPA section reference frequency
- Data coverage (requirements analyzed vs policy sections)
- Structured format quality

**Score Calculation:**
- Base score: 0.5
- Analysis length (0-0.2): More detailed analysis = higher score
- CCPA references (0-0.2): More specific citations = higher score
- Data coverage (0-0.15): More requirements/sections = higher score
- Format structure (0-0.15): Better formatting = higher score
- **Final Range**: 0.0 to 1.0

**Logged to MCP:** `http://localhost:8080/debug/confidence`

**Example:**
```json
{
  "timestamp": "2025-12-27T17:12:50.406455",
  "query": "CCPA/CPRA Gap Analysis for BLodgic",
  "response": "**BLodgic Privacy Policy CCPA/CPRA...",
  "confidence_score": 1.0,
  "is_high_confidence": true,
  "is_low_confidence": false
}
```

### 2. **Structured Gap Analysis Store**

**What it captures:**
- Identified gaps with titles and priorities
- Specific recommendations (top 10)
- Overall priority assessment (Critical/High/Medium/Low)
- Session linkage for tracking

**Parsing Logic:**
- Extracts "Gap X:" patterns from analysis
- Identifies priority levels (Critical/High/Medium/Low)
- Parses recommendation sections
- Calculates overall priority based on gap severity

**Logged to MCP:** `http://localhost:8080/debug/gaps`

**Example:**
```json
{
  "timestamp": "2025-12-27T17:12:50.408931",
  "company": "BLodgic",
  "gaps": [
    {
      "title": "Right to Know Disclosure",
      "description": "Disclosure of categories and specific pieces...",
      "priority": "Critical"
    }
  ],
  "recommendations": [
    "Update the policy to include detailed categories...",
    "Add right to delete disclosure section..."
  ],
  "priority_level": "High",
  "session_id": "privacy_analysis_BLodgic_20251227_171250"
}
```

### 3. **Interactive User Feedback**

**What it collects:**
- Overall quality rating (1-5 scale)
- Optional comments and specific feedback
- Session ID for correlation with analysis

**User Experience:**
After each analysis, users are prompted:
```
📊 How would you rate the overall quality of this gap analysis?
   1 = Poor (many gaps missed, inaccurate)
   2 = Fair (some gaps missed)
   3 = Good (most gaps identified)
   4 = Excellent (comprehensive and accurate)
   5 = Outstanding (exceeded expectations)

Rating (1-5) or press Enter to skip: 4

💬 Any specific comments? (optional)
Comments: Excellent analysis, very comprehensive
```

**Logged to MCP:** `http://localhost:8080/debug/feedback`

**Example:**
```json
{
  "timestamp": "2025-12-27T17:12:54.053960",
  "session_id": "privacy_analysis_BLodgic_20251227_171250",
  "question": "Gap Analysis Quality for BLodgic",
  "rating": "excellent",
  "numeric_rating": 4,
  "comments": "Excellent analysis, very comprehensive"
}
```

## 📊 How to Use

### Running Analysis with Feedback

```bash
cd scripts
python run_privacy_analysis.py https://example.com "Example Company"
```

The system will automatically:
1. ✅ Calculate confidence score after GPT-4 analysis
2. ✅ Parse and store structured gap data
3. ✅ Prompt you for user feedback at the end

### Skipping Feedback

If you want to skip the feedback prompt:
- Just press **Enter** when asked for rating

### Viewing Feedback Data

**Health Check:**
```bash
curl http://localhost:8080/health
```

**Confidence Scores:**
```bash
curl http://localhost:8080/debug/confidence | python -m json.tool
```

**Gap Analysis Store:**
```bash
curl http://localhost:8080/debug/gaps | python -m json.tool
```

**User Feedback:**
```bash
curl http://localhost:8080/debug/feedback | python -m json.tool
```

## 🔬 Using Data for Model Improvement

### 1. Identify Low-Confidence Analyses

```bash
curl -s http://localhost:8080/debug/confidence | \
  python -c "import sys, json; data = json.load(sys.stdin); \
  print([x for x in data if x['confidence_score'] < 0.6])"
```

### 2. Find Poorly-Rated Analyses

```bash
curl -s http://localhost:8080/debug/feedback | \
  python -c "import sys, json; data = json.load(sys.stdin); \
  print([x for x in data if x.get('numeric_rating', 5) < 3])"
```

### 3. Analyze Gap Patterns

```bash
curl -s http://localhost:8080/debug/gaps | \
  python -c "import sys, json; data = json.load(sys.stdin); \
  gaps = [g for entry in data for g in entry['gaps']]; \
  print(f'Total gaps identified: {len(gaps)}'); \
  print(f'Critical: {sum(1 for g in gaps if g[\"priority\"]==\"Critical\")}')"
```

## 🔄 Feedback Loop Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. User runs privacy compliance analysis          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  2. GPT-4 performs gap analysis                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  3. System calculates confidence score (automatic)  │
│     - Logs to MCP: confidence_store                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  4. System parses gap data (automatic)              │
│     - Logs to MCP: gap_analysis_store               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  5. User provides quality rating (interactive)      │
│     - Logs to MCP: feedback_store                   │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  6. Data aggregation for model fine-tuning          │
│     - Correlate confidence + feedback + gaps        │
│     - Identify improvement opportunities            │
│     - Update prompts or model parameters            │
└─────────────────────────────────────────────────────┘
```

## 📈 Key Metrics Tracked

| Metric | Source | Purpose |
|--------|--------|---------|
| Confidence Score | Automatic calculation | Identify analyses needing review |
| Gap Count | Parsed from analysis | Track comprehensiveness |
| Priority Distribution | Gap analysis | Monitor critical gap detection |
| User Rating | Human feedback | Validate analysis quality |
| Comments | Human feedback | Qualitative improvement insights |
| Token Usage | OpenAI API | Cost tracking and optimization |

## 🎯 Best Practices

1. **Always provide feedback** - Even a quick rating helps improve the system
2. **Be specific in comments** - Mention what was good or what was missed
3. **Review low-confidence analyses** - These may need manual verification
4. **Track patterns over time** - Look for recurring gaps or issues
5. **Export data periodically** - Use for model fine-tuning or reporting

## 🔧 Advanced: Exporting Feedback Data

### Export to JSON file
```bash
curl -s http://localhost:8080/debug/feedback > feedback_export_$(date +%Y%m%d).json
curl -s http://localhost:8080/debug/confidence > confidence_export_$(date +%Y%m%d).json
curl -s http://localhost:8080/debug/gaps > gaps_export_$(date +%Y%m%d).json
```

### Combine all data
```python
import requests
import json
from datetime import datetime

# Fetch all data
feedback = requests.get("http://localhost:8080/debug/feedback").json()
confidence = requests.get("http://localhost:8080/debug/confidence").json()
gaps = requests.get("http://localhost:8080/debug/gaps").json()

# Combine by session_id
combined = {
    "export_date": datetime.now().isoformat(),
    "feedback": feedback,
    "confidence": confidence,
    "gaps": gaps
}

# Save to file
with open(f"hfrl_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
    json.dump(combined, f, indent=2)

print("✅ Feedback data exported")
```

## 🚀 Future Enhancements

Planned improvements to the HFRL system:

- [ ] Persistent storage (currently in-memory)
- [ ] Analytics dashboard for visualizing trends
- [ ] Automated prompt optimization based on feedback
- [ ] Gap prediction ML model training
- [ ] A/B testing different analysis prompts
- [ ] Integration with model fine-tuning pipelines

## 📞 Support

For questions or issues with the feedback system:
1. Check MCP server is running: `curl http://localhost:8080/health`
2. Review this guide for usage examples
3. Check MCP server logs for errors

---

**Version**: 1.0
**Last Updated**: December 27, 2025
**System**: Cardinal Security Privacy Compliance Workflow
