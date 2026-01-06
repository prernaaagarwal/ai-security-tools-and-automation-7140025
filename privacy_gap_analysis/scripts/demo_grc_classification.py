#!/usr/bin/env python3
"""
GRC Data Classification Demo - LinkedIn Learning Chapter 2, Lesson 03
Demonstrates data classification for AI compliance tools

This script demonstrates:
1. GRC data types (Regulatory, Policies, Controls, Evidence)
2. Classification levels (Public, Internal, Confidential, Restricted)
3. AI deployment decisions based on classification
4. Practical examples from privacy compliance tool
"""

import os
import sys
from pathlib import Path
import pandas as pd


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


def print_classification_matrix():
    """Display GRC data classification matrix"""

    print_section("GRC DATA TYPES & CLASSIFICATIONS")

    print("""
┌──────────────────────┬────────────────────────┬─────────────────┬──────────┬──────────────────┐
│ Data Type            │ Examples               │ Classification  │ AI Risk  │ Used in Tool     │
├──────────────────────┼────────────────────────┼─────────────────┼──────────┼──────────────────┤
│ Regulatory           │ CCPA, GDPR, SOC 2,     │ Public          │ Low      │ ✅ CCPA CSV      │
│ Frameworks           │ NIST, ISO 27001        │                 │          │                  │
├──────────────────────┼────────────────────────┼─────────────────┼──────────┼──────────────────┤
│ Company              │ Privacy policies,      │ Public or       │ Medium   │ ✅ Scraped       │
│ Policies             │ Security policies,     │ Internal        │          │   policies       │
│                      │ Retention policies     │                 │          │                  │
├──────────────────────┼────────────────────────┼─────────────────┼──────────┼──────────────────┤
│ Control              │ Firewall configs,      │ Confidential    │ High     │ ❌ Not included │
│ Implementations      │ Access controls,       │                 │          │                  │
│                      │ Encryption settings    │                 │          │                  │
├──────────────────────┼────────────────────────┼─────────────────┼──────────┼──────────────────┤
│ Audit                │ Penetration tests,     │ Confidential    │ Very     │ ❌ Not included │
│ Evidence             │ Incidents, Logs,       │ or Restricted   │ High     │                  │
│                      │ Vulnerability scans    │                 │          │                  │
└──────────────────────┴────────────────────────┴─────────────────┴──────────┴──────────────────┘
    """)

    print("\n🎯 Key Principle:")
    print("   Before you load data into an AI system, you MUST classify it.")
    print("   Classification determines WHERE and HOW you can use AI.")


def print_ai_deployment_matrix():
    """Display AI deployment decision matrix"""

    print_section("AI DEPLOYMENT DECISION MATRIX")

    print("""
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
    """)

    print("\n📋 Decision Framework:")
    print("   • Public data      → Cloud AI is fine")
    print("   • Internal data    → Review DPAs, consider local models")
    print("   • Confidential     → On-prem or air-gapped only")
    print("   • Restricted       → Extreme caution, may not be suitable for AI")


def demo_ccpa_framework_classification():
    """Demo: Classify CCPA framework data"""

    print_section("DEMO 1: Classifying CCPA Framework (Regulatory Data)")

    # Find CCPA framework file
    framework_path = Path(__file__).parent.parent / "data" / "frameworks" / "CCPA_CPRA_Framework.csv"

    if not framework_path.exists():
        print(f"\n⚠️  CCPA framework not found at: {framework_path}")
        return

    print(f"\n📄 Loading: {framework_path.name}")

    # Load and display sample
    ccpa_df = pd.read_csv(framework_path)

    print(f"\n✓ Loaded {len(ccpa_df)} CCPA requirements")
    print("\n📋 Sample data (first 3 rows):")
    print()

    for i, row in ccpa_df.head(3).iterrows():
        print(f"   Row {i+1}:")
        print(f"   • Category: {row.get('Category', 'N/A')}")
        print(f"   • Requirement: {row.get('Requirement', 'N/A')}")
        print(f"   • Reference: {row.get('Reference', 'N/A')}")
        print(f"   • Body: {str(row.get('Body', ''))[:80]}...")
        print()

    print("🔍 Classification Analysis:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Data Type:        Regulatory Framework                  │")
    print("   │ Source:           Public CCPA/CPRA legislation          │")
    print("   │ Classification:   PUBLIC                                │")
    print("   │ Sensitivity:      None (publicly available law)         │")
    print("   │ AI Deployment:    ✅ Safe for cloud APIs                │")
    print("   │ Risk Level:       LOW                                   │")
    print("   └─────────────────────────────────────────────────────────┘")

    print("\n💡 Decision:")
    print("   This data CAN be loaded into cloud-based RAG systems.")
    print("   No confidentiality risk. No data processing concerns.")
    print("   This is exactly what we want AI to see - it's our reference standard.")


def demo_privacy_policy_classification():
    """Demo: Classify privacy policy data"""

    print_section("DEMO 2: Classifying Privacy Policies (Company Policy Data)")

    print("\n📄 Example: Public privacy policy from company website")

    sample_policy = """
Privacy Policy - Acme Corporation

Last Updated: December 1, 2025

This Privacy Policy describes how Acme Corporation collects, uses, and
shares personal information when you visit our website or use our services.

Information We Collect:
- Contact information (name, email, phone)
- Account credentials
- Usage data and analytics
- Cookies and tracking technologies

How We Use Your Information:
- To provide and improve our services
- To communicate with you
- To comply with legal obligations
    """

    print("\n📝 Sample content:")
    for line in sample_policy.split('\n')[:10]:
        if line.strip():
            print(f"   {line}")
    print("   ...")

    print("\n🔍 Classification Analysis:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Data Type:        Company Policy (Privacy)              │")
    print("   │ Source:           Public website                        │")
    print("   │ Classification:   PUBLIC (published policy)             │")
    print("   │ Sensitivity:      Low (intended for public viewing)     │")
    print("   │ AI Deployment:    ✅ Safe for cloud APIs                │")
    print("   │ Risk Level:       LOW to MEDIUM                         │")
    print("   └─────────────────────────────────────────────────────────┘")

    print("\n💡 Decision:")
    print("   This PUBLISHED policy is safe for cloud AI.")

    print("\n⚠️  BUT consider these scenarios:")
    print("   • DRAFT privacy policy (not published)    → INTERNAL/CONFIDENTIAL")
    print("   • Internal security policy                → CONFIDENTIAL")
    print("   • Employee data handling procedures       → CONFIDENTIAL")
    print("   • Incident response playbook              → CONFIDENTIAL")

    print("\n📌 Rule of thumb:")
    print("   If it's on your public website → Public classification")
    print("   If it's internal-only         → Confidential classification")


def demo_sensitive_data_classification():
    """Demo: Classify sensitive GRC data"""

    print_section("DEMO 3: Classifying Sensitive GRC Data")

    print("\n🔒 Examples of data that should NOT go to cloud AI:")

    examples = [
        {
            "type": "Control Implementation",
            "example": "Firewall configuration: 10.0.1.0/24 blocked, SSH port 2222, admin@internal.local",
            "classification": "CONFIDENTIAL",
            "risk": "HIGH",
            "reason": "Reveals internal network architecture and security controls",
            "deployment": "On-prem or air-gapped AI only"
        },
        {
            "type": "Audit Evidence",
            "example": "Vulnerability scan: 23 critical findings, SQL injection in /api/users endpoint",
            "classification": "CONFIDENTIAL",
            "risk": "VERY HIGH",
            "reason": "Exposes specific security vulnerabilities",
            "deployment": "Air-gapped AI only, or no AI"
        },
        {
            "type": "Audit Evidence",
            "example": "Security incident log: User john.doe@acme.com accessed 10,000 customer records",
            "classification": "RESTRICTED",
            "risk": "VERY HIGH",
            "reason": "Contains PII and incident details",
            "deployment": "Manual review only, no AI"
        }
    ]

    for i, ex in enumerate(examples, 1):
        print(f"\n   Example {i}: {ex['type']}")
        print("   " + "─" * 70)
        print(f"   Content:        {ex['example']}")
        print(f"   Classification: {ex['classification']}")
        print(f"   Risk Level:     {ex['risk']}")
        print(f"   Why:            {ex['reason']}")
        print(f"   AI Deployment:  {ex['deployment']}")

    print("\n⛔ Key Principle:")
    print("   Never send confidential control implementations or audit evidence")
    print("   to cloud-based AI systems. The risk far outweighs the benefit.")


def demo_production_options():
    """Demo: Show production deployment options"""

    print_section("PRODUCTION DEPLOYMENT OPTIONS")

    print("\n🏭 Three approaches for handling confidential GRC data:")

    print("\n1️⃣  Option 1: Local LLM (Open Source)")
    print("   ┌────────────────────────────────────────────────────────┐")
    print("   │ Models:      Llama 3, Mistral, Phi-3                  │")
    print("   │ Location:    On-premises servers                       │")
    print("   │ Data flow:   Nothing leaves your environment          │")
    print("   │ Cost:        Hardware + maintenance                    │")
    print("   │ Quality:     Lower than GPT-4 (but improving)         │")
    print("   │ Best for:    Highly sensitive compliance data          │")
    print("   └────────────────────────────────────────────────────────┘")

    print("\n2️⃣  Option 2: Enterprise Cloud AI (Azure OpenAI / AWS Bedrock)")
    print("   ┌────────────────────────────────────────────────────────┐")
    print("   │ Models:      GPT-4, Claude (via enterprise agreements) │")
    print("   │ Location:    Your cloud tenant                         │")
    print("   │ Data flow:   Stays in your cloud environment          │")
    print("   │ Guarantees:  No training on your data (contractual)   │")
    print("   │ Cost:        Higher than standard API                  │")
    print("   │ Quality:     Same as GPT-4/Claude                      │")
    print("   │ Best for:    Internal/confidential data with budget    │")
    print("   └────────────────────────────────────────────────────────┘")

    print("\n3️⃣  Option 3: Hybrid Approach (Recommended)")
    print("   ┌────────────────────────────────────────────────────────┐")
    print("   │ Public data     → Cloud API (OpenAI, Anthropic)       │")
    print("   │                   Cheaper, faster, better quality      │")
    print("   │                                                        │")
    print("   │ Confidential    → Local model or Azure OpenAI         │")
    print("   │                   Data stays controlled                │")
    print("   │                                                        │")
    print("   │ Pipelines:       Separated by classification          │")
    print("   │ Benefit:         Best of both worlds                  │")
    print("   └────────────────────────────────────────────────────────┘")


def demo_current_implementation():
    """Demo: Show current tool's approach"""

    print_section("CURRENT IMPLEMENTATION: Privacy Compliance Tool")

    print("\n🔍 How our tool handles data classification:")

    print("\n✅ What we DO send to cloud AI (OpenAI GPT-4):")
    print("   • CCPA_CPRA_Framework.csv           → PUBLIC regulatory text")
    print("   • Public privacy policies (scraped) → PUBLIC website content")
    print()
    print("   Risk: LOW - All publicly available information")

    print("\n❌ What we DON'T send to cloud AI:")
    print("   • Internal security policies        → Would be CONFIDENTIAL")
    print("   • Vulnerability scan results        → Would be CONFIDENTIAL/RESTRICTED")
    print("   • Customer PII data                 → Would be RESTRICTED")
    print("   • Incident response logs            → Would be CONFIDENTIAL/RESTRICTED")
    print()
    print("   Decision: This data would require on-prem or air-gapped deployment")

    print("\n⚙️  Configuration (from .env file):")
    print("   OPENAI_API_KEY=sk-***                # Cloud API (for public data only)")
    print("   # For confidential data, would need:")
    print("   # AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com")
    print("   # LOCAL_MODEL_PATH=/models/llama3-8b")

    print("\n📊 Data Flow Diagram:")
    print("""
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

   All data is PUBLIC → Safe for cloud AI
    """)


def run_full_demo():
    """Run complete GRC classification demo"""

    print_banner("GRC Data Classification Demo")
    print("\n🎯 Understanding what data can safely go into AI systems")

    input("\n⏸️  Press Enter to see GRC data types matrix...")
    print_classification_matrix()

    input("\n⏸️  Press Enter to see AI deployment decision matrix...")
    print_ai_deployment_matrix()

    input("\n⏸️  Press Enter for Demo 1: CCPA Framework Classification...")
    demo_ccpa_framework_classification()

    input("\n⏸️  Press Enter for Demo 2: Privacy Policy Classification...")
    demo_privacy_policy_classification()

    input("\n⏸️  Press Enter for Demo 3: Sensitive Data Classification...")
    demo_sensitive_data_classification()

    input("\n⏸️  Press Enter to see Production Deployment Options...")
    demo_production_options()

    input("\n⏸️  Press Enter to see Current Implementation...")
    demo_current_implementation()

    print_banner("✅ Demo Complete!")

    print("""
🎓 Key Takeaways:

1. Always classify GRC data BEFORE using AI
2. Public data → Cloud AI is safe
3. Confidential data → Requires on-prem or enterprise agreements
4. Restricted data → May not be suitable for AI at all
5. Use hybrid approach: public data to cloud, confidential stays local

💡 Data classification isn't just compliance—it determines your architecture!
    """)


def run_quick_demo():
    """Quick non-interactive demo"""

    print_banner("GRC Data Classification - Quick Demo")

    print_classification_matrix()
    print_ai_deployment_matrix()
    demo_ccpa_framework_classification()
    demo_privacy_policy_classification()
    demo_sensitive_data_classification()
    demo_production_options()
    demo_current_implementation()

    print_banner("✅ Demo Complete!")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\n📚 GRC Data Classification Demo")
        print("="*60)
        print("\nUsage:")
        print("  python demo_grc_classification.py              # Interactive")
        print("  python demo_grc_classification.py --quick      # Quick mode")
        print("\nDemonstrates:")
        print("  • GRC data types and classifications")
        print("  • AI deployment decision matrix")
        print("  • Classification examples")
        print("  • Production deployment options")
        print("="*60 + "\n")
    else:
        run_full_demo()


if __name__ == "__main__":
    main()
