# Chapter 2, Lesson 03 - Complete Narration Script
## "GRC Data Classification: What Data Can Safely Go Into AI?"

---

## 📝 COMPLETE NARRATION SCRIPT

### **[INTRO - ON CAMERA - 45 seconds]**

> "In this lesson, we're going to talk about something that's absolutely critical before you ever load data into an AI system: data classification.
>
> GRC data is not just documents. It's policies, regulations, control mappings, audit evidence, and sometimes sensitive internal findings. Not all of that data should ever go into an AI system, especially a cloud-hosted API.
>
> Some of it is public. Some of it is confidential. Some of it is legally restricted.
>
> That's why the first step before using AI in compliance isn't prompting - it's data classification. You have to decide what data is safe to send to a model, what must stay on your systems, and what can only be used in tightly controlled workflows.
>
> In this lesson, I'll show you exactly how to classify GRC data, and how that classification determines what AI architecture you can use. Let's dive in."

---

### **[VISUAL: Show Slides - 45 seconds]**

**[SLIDE 1: GRC Data Types]**

> "First, let me show you the four major categories of data that show up in every GRC program. Before we use AI, we need to classify everything into one of these four buckets. Each one carries a very different level of risk."

**[Point to slide as you narrate]**

> "**First**, regulatory frameworks. These are the laws and standards themselves - CCPA, GDPR, SOC 2, NIST, ISO 27001. They're public, stable, and designed to be shared. This is exactly what we want AI to see because this is what we measure everything else against.
>
> **Second**, compliance policies. These are where companies describe their intent - privacy policies, security policies, data retention policies. They might be public, like a website privacy policy, or internal, like a security operations manual. We use AI to compare these against regulations to find gaps.
>
> **Third**, control implementations. These are the actual technical controls - firewall configurations, access control lists, encryption settings. This data is highly sensitive. We do NOT put this into cloud-based AI at all.
>
> **And fourth**, audit evidence. This is where the real risk lives - penetration test results, security incidents, vulnerability scans, sometimes even customer PII. This stays locked down, even in AI-powered systems."

---

### **[TERMINAL DEMO PART 1 - 2 minutes]**

**[SCREEN: Switch to terminal]**

> "Let me show you how this works in practice. I'm going to run a demo that classifies real GRC data."

**[Type and run]**
```bash
python demo_grc_classification.py --quick
```

**[OUTPUT: Classification matrix appears]**

> "Here's our GRC data classification matrix. Look at this table - we have four data types across the top, and for each one, we're tracking examples, classification level, AI risk, and whether we use it in our tool."

**[Pause as table displays]**

```
┌──────────────────────┬────────────────────────┬─────────────────┬──────────┬──────────────────┐
│ Data Type            │ Examples               │ Classification  │ AI Risk  │ Used in Tool     │
├──────────────────────┼────────────────────────┼─────────────────┼──────────┼──────────────────┤
│ Regulatory           │ CCPA, GDPR, SOC 2,     │ Public          │ Low      │ ✅ CCPA CSV      │
│ Frameworks           │ NIST, ISO 27001        │                 │          │                  │
```

> "Regulatory frameworks are classified as PUBLIC with LOW risk. We absolutely use this in our tool - it's our CCPA framework CSV.
>
> Company policies can be public OR internal, with MEDIUM risk. We use publicly-scraped privacy policies.
>
> But look at control implementations and audit evidence - both are CONFIDENTIAL or RESTRICTED, with HIGH to VERY HIGH risk. We do NOT include these in our cloud-based tool. That would be a major security violation."

**[OUTPUT: AI Deployment Matrix appears]**

> "Now here's the critical part - the AI deployment decision matrix. This tells us WHERE we can run AI based on data classification."

```
┌──────────────────┬─────────────┬──────────────┬──────────────────┐
│ Classification   │ Cloud AI    │ On-Prem AI   │ Air-Gapped AI    │
├──────────────────┼─────────────┼──────────────┼──────────────────┤
│ Public           │ ✅ Safe     │ ✅ Safe      │ ✅ Safe          │
├──────────────────┼─────────────┼──────────────┼──────────────────┤
│ Internal         │ ⚠️  Caution │ ✅ Safe      │ ✅ Safe          │
├──────────────────┼─────────────┼──────────────┼──────────────────┤
│ Confidential     │ ❌ Avoid    │ ⚠️  Caution  │ ✅ Safe          │
├──────────────────┼─────────────┼──────────────┼──────────────────┤
│ Restricted       │ ❌ Never    │ ❌ Avoid     │ ⚠️  Caution      │
└──────────────────┴─────────────┴──────────────┴──────────────────┘
```

> "Public data? Cloud AI is fine. No restrictions.
>
> Internal data? You need to be cautious with cloud AI. Review your data processing agreements. Consider local models.
>
> Confidential data? Avoid cloud AI entirely. Use on-premises or air-gapped systems.
>
> Restricted data? This should almost never go into AI at all, even on-premises. This is the most sensitive data your organization has."

---

### **[TERMINAL DEMO PART 2 - 2.5 minutes]**

**[OUTPUT: Demo 1 appears - CCPA Framework]**

> "Let's look at a real example from our privacy compliance tool."

```
--------------------------------------------------------------------------------
  DEMO 1: Classifying CCPA Framework (Regulatory Data)
--------------------------------------------------------------------------------

📄 Loading: CCPA_CPRA_Framework.csv

✓ Loaded 102 CCPA requirements

📋 Sample data (first 3 rows):

   Row 1:
   • Category: Consumer Rights
   • Requirement: Right to Know
   • Reference: CCPA Section 1798.100
   • Body: Consumers have the right to request disclosure of categories...
```

> "We're loading our CCPA framework - 102 requirements from California privacy law. This is public regulatory text. Anyone can access this. California publishes it.
>
> Look at the classification analysis:"

```
🔍 Classification Analysis:
   ┌─────────────────────────────────────────────────────────┐
   │ Data Type:        Regulatory Framework                  │
   │ Source:           Public CCPA/CPRA legislation          │
   │ Classification:   PUBLIC                                │
   │ Sensitivity:      None (publicly available law)         │
   │ AI Deployment:    ✅ Safe for cloud APIs                │
   │ Risk Level:       LOW                                   │
   └─────────────────────────────────────────────────────────┘
```

> "Classification: PUBLIC. Sensitivity: None. AI deployment: safe for cloud APIs. Risk level: LOW.
>
> This is the ideal case - we WANT to send this to GPT-4 because it's our reference standard for compliance."

**[OUTPUT: Demo 2 appears - Privacy Policy]**

> "Now let's look at a company privacy policy."

```
--------------------------------------------------------------------------------
  DEMO 2: Classifying Privacy Policies (Company Policy Data)
--------------------------------------------------------------------------------

📝 Sample content:
   Privacy Policy - Acme Corporation
   Last Updated: December 1, 2025

   Information We Collect:
   - Contact information (name, email, phone)
   - Account credentials
   ...
```

> "This is a public privacy policy from a company website. Same classification analysis:"

```
🔍 Classification Analysis:
   ┌─────────────────────────────────────────────────────────┐
   │ Data Type:        Company Policy (Privacy)              │
   │ Source:           Public website                        │
   │ Classification:   PUBLIC (published policy)             │
   │ Sensitivity:      Low (intended for public viewing)     │
   │ AI Deployment:    ✅ Safe for cloud APIs                │
   │ Risk Level:       LOW to MEDIUM                         │
   └─────────────────────────────────────────────────────────┘
```

> "This PUBLISHED policy is safe for cloud AI. It's already public - anyone can read it on their website.
>
> BUT - and this is critical - look at these scenarios:"

```
⚠️  BUT consider these scenarios:
   • DRAFT privacy policy (not published)    → INTERNAL/CONFIDENTIAL
   • Internal security policy                → CONFIDENTIAL
   • Employee data handling procedures       → CONFIDENTIAL
   • Incident response playbook              → CONFIDENTIAL
```

> "If it's a DRAFT policy that hasn't been published yet? That's INTERNAL or CONFIDENTIAL. If it's an internal security policy? CONFIDENTIAL. If it's an incident response playbook? Definitely CONFIDENTIAL.
>
> The rule of thumb: if it's on your public website, it's public classification. If it's internal-only, it's confidential."

**[OUTPUT: Demo 3 appears - Sensitive Data]**

> "Now let me show you examples of data that should NEVER go to cloud AI."

```
🔒 Examples of data that should NOT go to cloud AI:

   Example 1: Control Implementation
   ──────────────────────────────────────────────────────────
   Content:        Firewall configuration: 10.0.1.0/24 blocked, SSH port 2222
   Classification: CONFIDENTIAL
   Risk Level:     HIGH
   Why:            Reveals internal network architecture and security controls
   AI Deployment:  On-prem or air-gapped AI only
```

> "Look at this firewall configuration example. It shows internal IP ranges, custom SSH ports, admin credentials. This reveals your entire network security architecture. If this got into the wrong hands, an attacker would know exactly how to target your systems.
>
> Classification: CONFIDENTIAL. AI deployment: on-prem or air-gapped only. Never cloud AI."

```
   Example 2: Audit Evidence
   ──────────────────────────────────────────────────────────
   Content:        Vulnerability scan: 23 critical findings, SQL injection in /api/users
   Classification: CONFIDENTIAL
   Risk Level:     VERY HIGH
   Why:            Exposes specific security vulnerabilities
   AI Deployment:  Air-gapped AI only, or no AI
```

> "Vulnerability scan results? Even worse. This shows exactly where you're vulnerable. Which endpoints have SQL injection flaws. How many critical findings you have.
>
> This should be air-gapped only, or better yet, don't use AI at all. Have humans review it."

---

### **[CODE WALKTHROUGH - 90 seconds]**

**[SCREEN: Switch to code editor, show privacy_rag_mcp.py]**

> "Let me show you how we handle this in our actual code."

**[Scroll to lines 49-56]**

```python
def load_ccpa_framework():
    """Load CCPA/CPRA framework into vector database"""

    # CCPA Framework = Public data
    # Safe to load into cloud-based RAG system
    ccpa_df = pd.read_csv("CCPA_CPRA_Framework.csv")

    documents_ccpa = DataFrameLoader(ccpa_df, page_content_column='Body').load()

    vectordb_ccpa = Chroma.from_documents(
        documents=documents_ccpa,
        embedding=embedding_model,
        persist_directory=ccpa_dir
    )
```

> "Look at this function - load_ccpa_framework. Notice the comment at the top: 'CCPA Framework = Public data. Safe to load into cloud-based RAG system.'
>
> We're loading a CSV file containing publicly available CCPA regulations. No confidentiality risk. No data processing concerns. This goes straight into ChromaDB, which then gets queried by OpenAI's GPT-4.
>
> That's perfectly fine because this data is PUBLIC."

**[Scroll to lines 100-138]**

```python
def load_privacy_policy(pdf_path):
    """Load privacy policy into vector database"""

    # Privacy policies = Usually public (from websites)
    # But could contain internal details
    policy_text = extract_text_from_pdf(pdf_path)
```

> "Now look at the load_privacy_policy function. Same comment pattern: 'Usually public from websites, but could contain internal details.'
>
> For this demo tool, we're scraping public privacy policies from company websites, so there's no confidentiality risk.
>
> But in a real organization? You're often analyzing DRAFT policies, internal procedures, audit documents. That changes everything about how you deploy AI."

---

### **[PRODUCTION OPTIONS - 2 minutes]**

**[SCREEN: Back to terminal output showing production options]**

> "Once data is classified as confidential or internal, the question isn't WHETHER you use AI. It's WHERE you run it. You have three options."

**[OUTPUT: Production options display]**

```
1️⃣  Option 1: Local LLM (Open Source)
   ┌────────────────────────────────────────────────────────┐
   │ Models:      Llama 3, Mistral, Phi-3                  │
   │ Location:    On-premises servers                       │
   │ Data flow:   Nothing leaves your environment          │
   │ Cost:        Hardware + maintenance                    │
   │ Quality:     Lower than GPT-4 (but improving)         │
   │ Best for:    Highly sensitive compliance data          │
   └────────────────────────────────────────────────────────┘
```

> "**Option 1**: Run everything locally using open-source models like Llama 3 or Mistral.
>
> Nothing leaves your environment. You have complete control. This is ideal for highly sensitive compliance data.
>
> The tradeoff? These models aren't as strong as GPT-4. Your analysis quality will be lower. But if you're dealing with restricted data, that's the price you pay for security."

```
2️⃣  Option 2: Enterprise Cloud AI (Azure OpenAI / AWS Bedrock)
   ┌────────────────────────────────────────────────────────┐
   │ Models:      GPT-4, Claude (via enterprise agreements) │
   │ Location:    Your cloud tenant                         │
   │ Data flow:   Stays in your cloud environment          │
   │ Guarantees:  No training on your data (contractual)   │
   │ Cost:        Higher than standard API                  │
   │ Quality:     Same as GPT-4/Claude                      │
   └────────────────────────────────────────────────────────┘
```

> "**Option 2**: Use enterprise cloud AI - Azure OpenAI or AWS Bedrock.
>
> You get the same GPT-4 and Claude models, but with contractual guarantees that your data stays in your cloud tenant and isn't used for training.
>
> This costs more than the standard OpenAI API, but you get much stronger models than local LLMs. Good middle ground for internal or confidential data."

```
3️⃣  Option 3: Hybrid Approach (Recommended)
   ┌────────────────────────────────────────────────────────┐
   │ Public data     → Cloud API (OpenAI, Anthropic)       │
   │ Confidential    → Local model or Azure OpenAI         │
   │ Pipelines:       Separated by classification          │
   │ Benefit:         Best of both worlds                  │
   └────────────────────────────────────────────────────────┘
```

> "**Option 3**, and this is what I recommend: a hybrid approach.
>
> Send public data to cloud APIs - OpenAI, Anthropic. It's cheaper, faster, and you get better quality.
>
> Send confidential data to local models or Azure OpenAI. Your data stays controlled.
>
> The key is separating your pipelines by classification. This way you get the best of both worlds - strong models where you can use them, tight control where you need it."

---

### **[CURRENT IMPLEMENTATION - 90 seconds]**

**[SCREEN: Show data flow diagram from demo output]**

> "Let me show you how our current tool implements this."

```
📊 Data Flow Diagram:

   ┌─────────────────┐
   │ CCPA Framework  │ (PUBLIC)
   │   CSV File      │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
   │   ChromaDB      │────▶│  OpenAI API  │────▶│   Report    │
   │ Vector Database │     │   (GPT-4)    │     │  Generated  │
   └────────┬────────┘     └──────────────┘     └─────────────┘
            ▲
            │
   ┌────────┴────────┐
   │ Privacy Policy  │ (PUBLIC - from website)
   │   PDF File      │
   └─────────────────┘
```

> "Our data flow is simple. CCPA framework - which is public - goes into ChromaDB. Public privacy policies from websites also go into ChromaDB.
>
> ChromaDB creates vector embeddings and stores them. When we run an analysis, we retrieve relevant sections and send them to the OpenAI API - that's GPT-4 in the cloud.
>
> GPT-4 compares the privacy policy against CCPA requirements and generates a gap analysis report.
>
> This entire pipeline works ONLY because all our data is public. If we were analyzing confidential data, we'd need a completely different architecture."

**[SCREEN: Show .env configuration]**

```
⚙️  Configuration (from .env file):

   OPENAI_API_KEY=sk-***                # Cloud API (for public data only)

   # For confidential data, would need:
   # AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com
   # LOCAL_MODEL_PATH=/models/llama3-8b
```

> "Look at our configuration file. We have an OpenAI API key - that's for cloud access. This is fine for our public data.
>
> But if we were handling confidential data, we'd need to add an Azure OpenAI endpoint or a local model path. Those configurations would route confidential data to controlled environments instead of the public OpenAI API."

---

### **[WRAP-UP - ON CAMERA - 30 seconds]**

> "So to recap: data classification isn't just a compliance checkbox. It fundamentally determines what AI architecture you can use.
>
> Public data can go to cloud APIs. Confidential data needs on-prem or enterprise agreements. Restricted data may not be suitable for AI at all.
>
> The key principle: classify FIRST, then choose your deployment model. Don't build your AI system and then try to retrofit security.
>
> In the next lesson, we'll look at human feedback and reinforcement learning - how we use human input to continuously improve AI compliance tools.
>
> Thanks for watching. I'll see you in the next lesson."

---

## 🎯 Key Teaching Points Covered

| Concept | Explanation in Script |
|---------|---------------------|
| **GRC data types** | "Regulatory, policies, controls, evidence" |
| **Classification levels** | "Public, internal, confidential, restricted" |
| **Risk assessment** | "Each type carries different AI risk" |
| **Deployment decisions** | "Cloud, on-prem, or air-gapped based on classification" |
| **Production options** | "Local LLM, enterprise cloud, or hybrid" |
| **Current implementation** | "Public data only, safe for cloud" |
| **Key principle** | "Classify first, then choose architecture" |

---

## 📊 Script Timing

- **Intro (on camera)**: 45 seconds
- **Visual slides**: 45 seconds
- **Terminal Demo Part 1** (matrices): 120 seconds (2 min)
- **Terminal Demo Part 2** (examples): 150 seconds (2.5 min)
- **Code Walkthrough**: 90 seconds (1.5 min)
- **Production Options**: 120 seconds (2 min)
- **Current Implementation**: 90 seconds (1.5 min)
- **Wrap-up (on camera)**: 30 seconds

**Total**: ~10.5 minutes (perfect for 11-12 minute lesson)

---

## 🎬 Visual Cues for Editor

### Terminal Output
1. **Classification matrix**: Hold for 5 seconds, let viewers read
2. **Deployment matrix**: Hold for 5 seconds, emphasize color coding
3. **Demo 1 (CCPA)**: Zoom in on classification box
4. **Demo 2 (Policy)**: Highlight "BUT consider" scenarios
5. **Demo 3 (Sensitive)**: Red border around examples
6. **Production options**: Split screen showing all 3 options

### Code Sections
1. **Lines 49-56**: Highlight "Public data" comment
2. **Lines 100-138**: Highlight "Usually public" comment
3. **.env file**: Mask actual API key, show # comments

### Graphics to Add
1. **GRC data types matrix** (professional table)
2. **Decision tree**: Classification → Deployment choice
3. **Data flow diagram**: More polished version
4. **Split screen**: Cloud vs On-prem vs Air-gapped
5. **Risk meter**: Visual gauge for each data type

---

## 📝 Key Quotes for Emphasis

> "Data classification isn't just compliance—it determines your architecture."

> "Classify FIRST, then choose your deployment model."

> "If it's on your public website, it's public. If it's internal-only, it's confidential."

> "Never send confidential control implementations to cloud-based AI. The risk far outweighs the benefit."

---

## 🔧 Demo Script Commands

### Terminal Demo
```bash
cd privacy_gap_analysis/scripts
python demo_grc_classification.py --quick
```

### Interactive Mode (for live demo)
```bash
python demo_grc_classification.py
# Press Enter at each pause point
```

---

## 🎥 Post-Production Tips

### Pacing
- **Slow down** during classification matrix (students reading table)
- **Normal speed** for examples
- **Emphasize** the "BUT consider" scenarios
- **Slow down** for key quotes

### B-roll Suggestions
- Lock icon for confidential data
- Cloud diagram for public data
- On-prem server racks
- Security team reviewing documents
- Data classification flowchart animation

### Annotations
- **Arrow** pointing to classification levels
- **Highlight** risk levels in matrix
- **Underline** "PUBLIC" vs "CONFIDENTIAL"
- **Circle** deployment decisions

---

**This script is ready for recording!** 🎥📹

**Estimated recording time**: 12 minutes
**Estimated editing time**: 10-15 minutes for graphics
**Final lesson length**: 10-11 minutes