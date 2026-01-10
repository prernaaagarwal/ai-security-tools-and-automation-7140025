# Exercise Files for Chapter 4: Framework Mapping & Evidence Collection

## Overview

These exercise files demonstrate:
1. **Lesson 01:** How AI-powered compliance analysis can be applied to different frameworks (NIST CSF 2.0)
2. **Lesson 03:** How AI-generated compliance reports serve as audit evidence for SOC 2 and other frameworks

## Files Included

### Lesson 01: Framework Mapping Files

### 1. `NIST_CSF_Framework.csv`
**Location:** `data/frameworks/NIST_CSF_Framework.csv`

A structured CSV file containing the NIST Cybersecurity Framework 2.0 controls in the same format as the CCPA framework:

- **108 controls** across 6 functions (Govern, Identify, Protect, Detect, Respond, Recover)
- **Same 4-column structure:** Category, Requirement, Body, Reference
- **Machine-readable format** perfect for RAG (Retrieval-Augmented Generation)

**Sample rows:**
```csv
Category,Requirement,Body,Reference
Govern - Policy,Organizational Cybersecurity Policy,Organizational cybersecurity policy is established...,GV.PO-01
Identify - Asset Management,Physical Devices Inventory,Physical devices and systems are inventoried...,ID.AM-01
Protect - Data Security,Data at Rest Protection,Data-at-rest is protected through encryption...,PR.DS-01
```

### 2. `AcmeCorp_Security_Policy.txt`
**Location:** `data/sample_policies/AcmeCorp_Security_Policy.txt`

A realistic corporate Information Security Policy for a fictional company "Acme Corporation." This policy demonstrates:

- **Comprehensive coverage** of NIST CSF areas (governance, risk management, asset management, access control, etc.)
- **Intentional gaps** to make the analysis interesting (e.g., no MFA for email, 90-day log retention, incomplete cloud inventory)
- **Real-world complexity** including legacy systems, budget constraints, and phased implementations

**Key Sections:**
1. Executive Summary
2. Governance and Oversight
3. Risk Management
4. Asset Management
5. Identity and Access Management
6. Data Protection
7. Security Awareness and Training
8. Secure Development and Operations
9. Network Security
10. Incident Response and Business Continuity
11. Compliance and Audit
12. Policy Maintenance

### 3. `AcmeCorp_NIST_CSF_Gap_Analysis_SAMPLE_OUTPUT.md`
**Location:** `data/sample_policies/AcmeCorp_NIST_CSF_Gap_Analysis_SAMPLE_OUTPUT.md`

A complete sample output showing what the AI-powered gap analysis would produce when analyzing Acme Corp's security policy against NIST CSF 2.0.

**Report Includes:**
- **Executive Summary** with overall compliance score (78%)
- **24 identified gaps** prioritized as High (9), Medium (10), Low (5)
- **Detailed gap analysis** for each finding with:
  - NIST CSF reference (e.g., PR.AA-02)
  - Current state from policy
  - Gap description
  - Risk assessment
  - Detailed recommendations
  - Estimated effort and cost
  - Confidence score
- **Prioritized remediation roadmap** (Immediate, Short-term, Medium-term, Long-term)
- **Compliance summary by NIST CSF function** (table showing % compliance per function)
- **Cost-benefit analysis** with ROI rankings
- **Attestation section** for CISO approval

---

### Lesson 03: Evidence Collection Files

### 4. `mcp_access_logs_CC6.1.json`
**Purpose:** Demonstrates audit evidence for **SOC 2 CC6.1 - Logical Access Controls**

A complete year of MCP server audit logs (12 sessions across 2025) showing:
- **User authentication** for all system access (authenticated user emails)
- **Session tracking** with unique session IDs for complete audit trail
- **Timestamp documentation** (ISO 8601 format with timezone)
- **Access attribution** (user, IP address, user agent for every action)
- **Audit retention** (365 days minimum)

**Key Metrics:**
- 12 total sessions | 3 unique users | 11 companies analyzed
- 229 total gaps identified | $9.88 total API cost
- 100% session success rate

**Auditor Use Case:** Demonstrates logical access controls are implemented, tracked, and auditable.

---

### 5. `mcp_monitoring_logs_CC7.2.json`
**Purpose:** Demonstrates audit evidence for **SOC 2 CC7.2 - System Monitoring**

System monitoring logs showing continuous monitoring for anomalies and quality:
- **Token usage tracking** (baseline 8,500 tokens, ±20% anomaly threshold)
- **Confidence score monitoring** (89% average, 0.70 minimum threshold)
- **Anomaly detection** (5 anomalies detected and resolved in 2025)
- **Quality metrics** (confidence scores, performance metrics)
- **Alert system** (automated alerts with 4-hour SLA for medium severity)

**Monitoring Capabilities:**
- Real-time tracking of token usage, confidence scores, performance
- Automated anomaly detection with defined thresholds
- Investigation and resolution tracking for all anomalies
- 99.97% system uptime | 100% session success rate

**Auditor Use Case:** Demonstrates system components are continuously monitored for anomalies with automated detection and response.

---

### 6. `README_EVIDENCE_FILES.md`
**Purpose:** Complete documentation for the evidence files

Comprehensive guide explaining:
- What each evidence file demonstrates
- How to map technical logs to compliance criteria
- Real-world audit scenarios and responses
- Key takeaways for building similar systems
- Evidence package structure for SOC 2 audits

**Learning Focus:** Understanding what makes good audit evidence and how AI systems generate it automatically.

---

## How to Use These Files

### For Students Learning the Concepts

1. **Review the NIST CSF Framework CSV**
   - Compare it to `CCPA_CPRA_Framework.csv`
   - Notice the same 4-column structure (demonstrates framework portability)
   - Observe how NIST controls are more granular than CCPA (108 vs 35)

2. **Read Acme Corp's Security Policy**
   - This represents a "real world" security policy with strengths and weaknesses
   - Try to manually identify gaps before looking at the AI analysis
   - Note the specific language used (this is what AI will analyze)

3. **Study the Sample Gap Analysis Output**
   - See how AI identifies specific gaps with NIST references
   - Learn the structure of a professional gap analysis report
   - Understand how confidence scores work (0.68 - 0.97 range)
   - Observe prioritization methodology (High/Medium/Low)

### For Running the Demo Script

**Option 1: Conceptual Demo (No Actual Analysis)**

The `04_01_demo_framework_mapping.py` script demonstrates concepts without actually running AI analysis:

```bash
cd privacy_gap_analysis
python scripts/04_01_demo_framework_mapping.py          # Interactive mode
python scripts/04_01_demo_framework_mapping.py --quick  # Quick mode for recording
```

This shows:
- Framework comparison table (CCPA, GDPR, NIST, SOC 2, etc.)
- Why structure matters for AI
- NIST CSF hierarchy and structure
- Side-by-side comparison of CCPA vs NIST
- Code examples for multi-framework support

**Option 2: Actual Analysis (Requires Code Modification)**

To actually run AI-powered NIST CSF gap analysis on Acme Corp's policy:

1. **Modify `privacy_rag_mcp.py`** to add NIST CSF support:
   - Add `load_nist_csf_framework()` function (sample code in demo script)
   - Add `analyze_security_policy_nist()` function
   - Use same RAG logic as CCPA analysis

2. **Run the analysis:**
   ```bash
   python analyze_nist_gap.py data/sample_policies/AcmeCorp_Security_Policy.txt "Acme Corp"
   ```

3. **Compare AI output** to the sample output provided

## Learning Objectives

By working with these exercise files, students will understand:

1. **Framework Portability**
   - Same AI tool can handle multiple frameworks (CCPA, NIST, GDPR, SOC 2)
   - Key requirement: Structured data format (CSV with Category, Requirement, Body, Reference)

2. **Gap Analysis Process**
   - How AI compares policy text against framework requirements
   - How gaps are identified, prioritized, and documented
   - Why confidence scores matter (AI isn't always certain)

3. **Professional Deliverables**
   - What a client-ready gap analysis report looks like
   - How to prioritize remediation (Immediate → Short-term → Long-term)
   - Why cost-benefit analysis matters for executive buy-in

4. **Real-World Complexity**
   - Policies have strengths AND weaknesses
   - Budget constraints affect security posture
   - Phased remediation is realistic (not everything can be fixed immediately)

5. **AI Limitations**
   - Confidence scores reveal AI uncertainty
   - Human review (CISO approval) is non-negotiable
   - Some gaps require business context AI can't provide

## Key Takeaways

### What Makes NIST CSF AI-Friendly?

✅ **Structured hierarchy** (Functions → Categories → Subcategories)
✅ **Clear control IDs** (GV.PO-01, ID.AM-01, PR.DS-01) for citations
✅ **Specific requirements** (not vague principles)
✅ **Machine-readable** (easily converted to CSV)

### How This Differs from CCPA

| Aspect | CCPA/CPRA | NIST CSF |
|--------|-----------|----------|
| **Focus** | Privacy (consumer rights) | Cybersecurity (risk management) |
| **Controls** | 35 requirements | 108 subcategories |
| **Structure** | Legal sections (§1798.100) | Hierarchical (GV.PO-01) |
| **Use Case** | Privacy policies | Security policies, controls |
| **Audience** | Consumers, regulators | Security teams, executives |

### Same RAG Technology, Different Framework

The key insight: **Once you structure a compliance framework as CSV, you can apply the same RAG + AI analysis to ANY framework.**

This is why:
- `load_ccpa_framework()` and `load_nist_csf_framework()` use identical logic
- The vector database and embeddings are the same
- Gap analysis prompts are similar (just different framework names)
- MCP logging and audit trails work the same way

## Extending This Approach

Students can apply this same methodology to:

1. **SOC 2** (64 Trust Service Criteria)
2. **GDPR** (99 articles)
3. **ISO 27001** (114 controls in Annex A)
4. **PCI DSS** (12 requirements, 78 sub-requirements)
5. **HIPAA Security Rule** (Administrative, Physical, Technical safeguards)
6. **DORA** (EU Digital Operational Resilience Act)

**All you need:** Convert the framework to CSV format with the 4-column structure.

## Questions to Consider

1. **Why does Acme Corp have a 78% compliance score?**
   - What are the high-priority gaps?
   - Are these gaps typical for mid-sized organizations?
   - Which gaps are "quick wins" (low cost, high risk reduction)?

2. **How does AI determine confidence scores?**
   - Gap #2 (MFA) has 0.97 confidence (very clear from policy text)
   - Gap #22 (OT/ICS) has 0.71 confidence (ambiguous, may not apply)
   - What makes some gaps more certain than others?

3. **Could this analysis be wrong?**
   - Yes! AI might misinterpret policy language
   - Example: "We do not currently..." vs "We do not and will not..."
   - This is why CISO review is required before client delivery

4. **How long would manual analysis take?**
   - Reading 108 NIST controls: ~2 hours
   - Reading Acme's 12-section policy: ~1.5 hours
   - Identifying and documenting 24 gaps: ~8-10 hours
   - **Total manual effort:** 12-14 hours
   - **AI analysis time:** 37 seconds (per sample output)
   - **Time savings:** ~99.9% (but still needs CISO review ~1 hour)

---

## Additional Resources

- **NIST CSF 2.0 Official:** https://www.nist.gov/cyberframework
- **NIST CSF Quick Start Guide:** Available on NIST website
- **Mapping to Other Frameworks:** NIST provides mappings to ISO 27001, COBIT, etc.
- **Sample Policies:** Use Acme Corp as a template for creating realistic test policies

---

**Created for:** LinkedIn Learning Course - AI Security Tools & Automation
**Chapter 4, Lesson 01:** Mapping AI to Compliance Frameworks
**Purpose:** Educational demonstration of multi-framework AI analysis
