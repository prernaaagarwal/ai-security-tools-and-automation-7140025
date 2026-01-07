#!/usr/bin/env python3
"""
Privacy Policy Gap Analysis with RAG and MCP
Evaluates privacy policies against CCPA/CPRA framework using RAG and GPT-4.1
"""

import os
import json
import requests
import pandas as pd
from typing import List, Dict
from datetime import datetime
import PyPDF2
from pathlib import Path
from dotenv import load_dotenv
from compliance_report_template import convert_markdown_to_compliance_report
from report_pdf_generator import convert_docx_to_pdf

###############################################################################
#                         Environment Setup
###############################################################################
load_dotenv()  # Load environment variables from .env file
os.environ["TOKENIZERS_PARALLELISM"] = "false"

###############################################################################
#                         Part 1: Vector Database Setup
###############################################################################
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from transformers import AutoTokenizer

# Load embedding model
print("Loading embedding model...")
embedding_model = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L12-v2'
)

# Load tokenizer for token counting
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L12-v2')

# Define directories for vector databases
ccpa_dir = './vectordb_ccpa'
privacy_policies_dir = './vectordb_privacy_policies'

###############################################################################
#                    Load CCPA/CPRA Framework into Vector DB
###############################################################################
def load_ccpa_framework():
    """Load CCPA/CPRA framework into vector database"""
    print("\n" + "="*60)
    print("Loading CCPA/CPRA Framework...")
    print("="*60)

    # Look for framework file in data/frameworks directory
    framework_path = Path(__file__).parent.parent / "data" / "frameworks" / "CCPA_CPRA_Framework.csv"
    if not framework_path.exists():
        framework_path = Path("data/frameworks/CCPA_CPRA_Framework.csv")
    if not framework_path.exists():
        framework_path = Path("CCPA_CPRA_Framework.csv")

    ccpa_df = pd.read_csv(str(framework_path), index_col=False)

    # Create combined text for better retrieval
    ccpa_df['Body'] = ccpa_df.apply(
        lambda row: f"Category: {row['Category']}\nRequirement: {row['Requirement']}\n{row['Body']}\nReference: {row['Reference']}",
        axis=1
    )

    documents_ccpa = DataFrameLoader(ccpa_df, page_content_column='Body').load()

    vectordb_ccpa = Chroma.from_documents(
        documents=documents_ccpa,
        embedding=embedding_model,
        persist_directory=ccpa_dir,
    )
    vectordb_ccpa.persist()

    print(f" CCPA/CPRA requirements stored: {vectordb_ccpa._collection.count()}")
    return vectordb_ccpa

###############################################################################
#                    PDF Text Extraction
###############################################################################
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from PDF file"""
    print(f"\n Extracting text from: {pdf_path}")

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""

            for page_num, page in enumerate(pdf_reader.pages):
                text += page.extract_text()
                print(f"  Page {page_num + 1}/{len(pdf_reader.pages)} extracted")

            print(f" Extracted {len(text)} characters")
            return text

    except Exception as e:
        print(f" Error extracting PDF: {e}")
        return ""

###############################################################################
#            Load Privacy Policy into Vector DB
###############################################################################
def load_privacy_policy(pdf_path: str, company_name: str):
    """Extract privacy policy from PDF and load into vector database"""
    print("\n" + "="*60)
    print(f"Loading Privacy Policy: {company_name}")
    print("="*60)

    # Extract text from PDF
    policy_text = extract_text_from_pdf(pdf_path)

    if not policy_text:
        print(" No text extracted from PDF")
        return None

    # Chunk the policy text (split by paragraphs or sections)
    # Simple chunking by double newlines
    chunks = [chunk.strip() for chunk in policy_text.split('\n\n') if chunk.strip()]

    print(f" Created {len(chunks)} chunks from policy")

    # Create documents
    documents = [
        Document(
            page_content=chunk,
            metadata={"company": company_name, "chunk_id": i}
        )
        for i, chunk in enumerate(chunks)
    ]

    # Create vector database
    vectordb_policy = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=privacy_policies_dir,
    )
    vectordb_policy.persist()

    print(f" Privacy policy stored: {vectordb_policy._collection.count()} chunks")
    return vectordb_policy


def load_policy_documents(privacy_pdf_path: str = None, terms_pdf_path: str = None, company_name: str = "Company"):
    """
    Extract both privacy policy and terms & conditions from PDFs and load into vector database.

    Args:
        privacy_pdf_path: Path to privacy policy PDF (optional)
        terms_pdf_path: Path to terms & conditions PDF (optional)
        company_name: Name of the company

    Returns:
        Vector database with combined policy documents
    """
    print("\n" + "="*60)
    print(f"Loading Policy Documents: {company_name}")
    print("="*60)

    all_documents = []
    total_chars = 0

    # Process Privacy Policy
    if privacy_pdf_path:
        print(f"\n Processing Privacy Policy...")
        policy_text = extract_text_from_pdf(privacy_pdf_path)

        if policy_text:
            total_chars += len(policy_text)
            # Chunk the policy text
            chunks = [chunk.strip() for chunk in policy_text.split('\n\n') if chunk.strip()]

            # Create documents with metadata indicating source
            privacy_docs = [
                Document(
                    page_content=chunk,
                    metadata={
                        "company": company_name,
                        "source": "Privacy Policy",
                        "chunk_id": i
                    }
                )
                for i, chunk in enumerate(chunks)
            ]
            all_documents.extend(privacy_docs)
            print(f"   Privacy Policy: {len(chunks)} chunks, {len(policy_text)} characters")
        else:
            print(f"    Privacy Policy: No text extracted")
    else:
        print(f"    Privacy Policy: Not provided")

    # Process Terms & Conditions
    if terms_pdf_path:
        print(f"\n Processing Terms & Conditions...")
        terms_text = extract_text_from_pdf(terms_pdf_path)

        if terms_text:
            total_chars += len(terms_text)
            # Chunk the terms text
            chunks = [chunk.strip() for chunk in terms_text.split('\n\n') if chunk.strip()]

            # Create documents with metadata indicating source
            terms_docs = [
                Document(
                    page_content=chunk,
                    metadata={
                        "company": company_name,
                        "source": "Terms & Conditions",
                        "chunk_id": i
                    }
                )
                for i, chunk in enumerate(chunks)
            ]
            all_documents.extend(terms_docs)
            print(f"   Terms & Conditions: {len(chunks)} chunks, {len(terms_text)} characters")
        else:
            print(f"    Terms & Conditions: No text extracted")
    else:
        print(f"    Terms & Conditions: Not provided")

    if not all_documents:
        print("\n No policy documents to load")
        return None

    # Create combined vector database
    print(f"\n Total: {len(all_documents)} chunks, {total_chars} characters")

    vectordb_policy = Chroma.from_documents(
        documents=all_documents,
        embedding=embedding_model,
        persist_directory=privacy_policies_dir,
    )
    vectordb_policy.persist()

    print(f" Policy documents stored: {vectordb_policy._collection.count()} chunks")
    return vectordb_policy

###############################################################################
#                         Part 2: MCP Client Integration
###############################################################################
class MCPClient:
    """MCP Client for tracking privacy analysis workflow"""

    def __init__(self, url: str):
        self.url = url

    def request(self, method: str, params: dict):
        payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': 1}
        r = requests.post(self.url, json=payload)
        r.raise_for_status()
        return r.json().get('result')

    def insert_memory(self, data):
        return self.request('insert_memory', data)

    def fetch_memory(self, session_id):
        return self.request('fetch_memory', {'session_id': session_id})

    def insert_confidence(self, query, response, score):
        return self.request('insert_confidence', {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'confidence_score': score,
            'is_high_confidence': score > 0.8,
            'is_low_confidence': score < 0.4
        })

    def insert_feedback(self, session_id, question, rating):
        return self.request('insert_feedback', {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'question': question,
            'rating': rating
        })

    def insert_token_usage(self, query, model, tp, tc, total):
        return self.request('insert_token_usage', {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'model_used': model,
            'tokens_prompt': tp,
            'tokens_completion': tc,
            'tokens_total': total
        })

# Initialize MCP client
mcp_client = MCPClient('http://localhost:8080/mcp')

###############################################################################
#                         Part 3: GPT-4.1 Integration
###############################################################################
from openai import OpenAI

# Initialize OpenAI client
openai_key = os.getenv("OPENAI_API_KEY", "")
if not openai_key:
    print("  WARNING: OPENAI_API_KEY not set in environment")

openai_client = OpenAI(api_key=openai_key)

# System prompt for privacy policy analysis
PRIVACY_ANALYSIS_PROMPT = """
You are a Privacy Compliance Officer specializing in California privacy law (CCPA/CPRA).
Your role is to analyze privacy policies and identify gaps against CCPA/CPRA requirements.

When analyzing:
- **Focus on CCPA/CPRA Compliance:** Evaluate strictly against California privacy law requirements
- **Identify Specific Gaps:** Point out missing disclosures, inadequate notices, or non-compliant language
- **Be Precise:** Reference specific CCPA/CPRA sections when identifying gaps
- **Provide Recommendations:** Suggest specific language or disclosures to add
- **Consumer Rights Focus:** Ensure all required consumer rights are clearly disclosed
- **Notice Requirements:** Verify all required notices are present and properly worded

Common gap areas to check:
1. Right to Know disclosure
2. Right to Delete disclosure
3. Right to Opt-Out of Sale/Sharing
4. Right to Correct inaccurate information
5. Right to Limit Use of Sensitive Personal Information
6. "Do Not Sell or Share My Personal Information" link
7. Categories of personal information collected
8. Business purposes for collection
9. Third-party sharing/selling disclosures
10. Data retention policies
11. Children's data protections (under 13 and 13-16)
12. Authorized agent procedures
13. Non-discrimination policy
14. Contact methods for exercising rights

If a requirement is missing or inadequate, clearly state what is missing and what needs to be added.
"""

def count_tokens(text: str) -> int:
    """Count tokens in text"""
    return len(tokenizer.encode(text))

def _calculate_confidence_score(analysis_text: str, num_requirements: int, num_policy_sections: int) -> float:
    """
    Calculate confidence score for gap analysis based on multiple factors

    Factors:
    - Length and detail of analysis
    - Number of requirements analyzed
    - Number of policy sections reviewed
    - Presence of specific CCPA section references
    - Structured format indicators
    """
    score = 0.5  # Base score

    # Factor 1: Analysis comprehensiveness (0-0.2)
    analysis_length = len(analysis_text)
    if analysis_length > 2000:
        score += 0.2
    elif analysis_length > 1000:
        score += 0.15
    elif analysis_length > 500:
        score += 0.1

    # Factor 2: CCPA section references (0-0.2)
    ccpa_refs = analysis_text.count("Section 1798.") + analysis_text.count("CCPA Section") + analysis_text.count("CPRA Section")
    if ccpa_refs >= 10:
        score += 0.2
    elif ccpa_refs >= 5:
        score += 0.15
    elif ccpa_refs >= 3:
        score += 0.1

    # Factor 3: Data coverage (0-0.15)
    if num_requirements >= 30 and num_policy_sections >= 2:
        score += 0.15
    elif num_requirements >= 20:
        score += 0.1
    elif num_requirements >= 10:
        score += 0.05

    # Factor 4: Structured format (0-0.15)
    structure_keywords = ["Gap", "Missing:", "Reference:", "Priority:", "Recommendation"]
    structure_count = sum(1 for keyword in structure_keywords if keyword in analysis_text)
    if structure_count >= 4:
        score += 0.15
    elif structure_count >= 3:
        score += 0.1
    elif structure_count >= 2:
        score += 0.05

    # Ensure score is between 0 and 1
    return min(1.0, max(0.0, score))


def _parse_gap_analysis(analysis_text: str) -> dict:
    """
    Parse gap analysis text to extract structured data

    Returns dict with:
    - gaps: List of identified gaps with titles and priorities
    - recommendations: List of recommendations
    - priority_summary: Overall priority assessment
    """
    import re

    gaps = []
    recommendations = []

    # Parse gaps (looking for "Gap X:" or "**Gap X:" patterns)
    gap_pattern = r'\*\*Gap \d+:?\s*([^\*\n]+)'
    gap_matches = re.findall(gap_pattern, analysis_text)

    # Alternative pattern for gaps without numbers
    if not gap_matches:
        gap_pattern = r'[-•]\s*\*\*([^:]+):\*\*\s*\*\*Missing:\*\*\s*([^\n]+)'
        gap_matches = re.findall(gap_pattern, analysis_text)

    for match in gap_matches:
        if isinstance(match, tuple):
            gap_title = match[0].strip()
            gap_desc = match[1].strip() if len(match) > 1 else ""
        else:
            gap_title = match.strip()
            gap_desc = ""

        # Extract priority if present
        priority = "Medium"  # Default
        if "Critical" in analysis_text[max(0, analysis_text.find(gap_title)-200):analysis_text.find(gap_title)+200]:
            priority = "Critical"
        elif "High" in analysis_text[max(0, analysis_text.find(gap_title)-200):analysis_text.find(gap_title)+200]:
            priority = "High"
        elif "Low" in analysis_text[max(0, analysis_text.find(gap_title)-200):analysis_text.find(gap_title)+200]:
            priority = "Low"

        gaps.append({
            "title": gap_title,
            "description": gap_desc[:200] if gap_desc else gap_title,
            "priority": priority
        })

    # Parse recommendations section
    rec_section = re.search(r'\*\*3\.\s*Recommendations[^\n]*\*\*(.+?)(?:\*\*4\.|---|\n\n\*\*|$)', analysis_text, re.DOTALL)
    if rec_section:
        rec_text = rec_section.group(1)
        # Extract bullet points or numbered items
        rec_items = re.findall(r'(?:[-•\*]|\d+\.)\s*([^\n]+)', rec_text)
        recommendations = [rec.strip() for rec in rec_items if len(rec.strip()) > 10]

    # Determine overall priority
    critical_count = sum(1 for g in gaps if g['priority'] == 'Critical')
    high_count = sum(1 for g in gaps if g['priority'] == 'High')

    if critical_count >= 3:
        priority_summary = "Critical"
    elif critical_count >= 1 or high_count >= 5:
        priority_summary = "High"
    else:
        priority_summary = "Medium"

    return {
        'gaps': gaps,
        'recommendations': recommendations[:10],  # Limit to top 10
        'priority_summary': priority_summary
    }


def perform_gap_analysis(company_name: str, vectordb_ccpa, vectordb_policy) -> Dict:
    """
    Perform CCPA/CPRA gap analysis on privacy policy using GPT-4.1
    """
    print("\n" + "="*60)
    print(f"Performing Gap Analysis: {company_name}")
    print("="*60)

    # Get all CCPA requirements
    ccpa_retriever = vectordb_ccpa.as_retriever(search_kwargs={"k": 35})  # Get all requirements
    ccpa_requirements = ccpa_retriever.invoke("CCPA CPRA requirements")

    # Get privacy policy content
    policy_retriever = vectordb_policy.as_retriever(search_kwargs={"k": 50})  # Get comprehensive policy content
    policy_docs = policy_retriever.invoke("privacy policy content")

    print(f" Retrieved {len(ccpa_requirements)} CCPA requirements")
    print(f" Retrieved {len(policy_docs)} policy sections")

    # Build context
    ccpa_context = "\n\n".join([doc.page_content for doc in ccpa_requirements])
    policy_context = "\n\n".join([doc.page_content for doc in policy_docs])

    # Create analysis prompt
    analysis_query = f"""
Analyze the following privacy policy for {company_name} against CCPA/CPRA requirements.

CCPA/CPRA REQUIREMENTS:
{ccpa_context}

COMPANY PRIVACY POLICY:
{policy_context}

Perform a comprehensive gap analysis and provide:
1. Executive Summary of compliance status
2. Detailed list of gaps with specific CCPA/CPRA sections
3. Recommendations for each gap
4. Priority level for each gap (Critical/High/Medium/Low)

Format your response as a structured report.
"""

    print("\n Calling GPT-4.1 for gap analysis...")

    # Build messages
    messages = [
        {"role": "system", "content": PRIVACY_ANALYSIS_PROMPT},
        {"role": "user", "content": analysis_query}
    ]

    # Call GPT-4.1
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3,  # Lower temperature for more consistent analysis
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    analysis_result = response.choices[0].message.content

    # Log to MCP
    session_id = f"privacy_analysis_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    mcp_client.insert_memory({
        'session_id': session_id,
        'text': f"Gap Analysis for {company_name}\n\n{analysis_result}"
    })

    # Track tokens
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    mcp_client.insert_token_usage(
        query=f"Gap analysis for {company_name}",
        model="gpt-4o",
        tp=prompt_tokens,
        tc=completion_tokens,
        total=total_tokens
    )

    # Calculate confidence score based on analysis characteristics
    confidence_score = _calculate_confidence_score(analysis_result, len(ccpa_requirements), len(policy_docs))

    # Log confidence score to MCP
    try:
        mcp_client.insert_confidence(
            query=f"CCPA/CPRA Gap Analysis for {company_name}",
            response=analysis_result[:500],  # First 500 chars
            score=confidence_score
        )
        print(f" Confidence score logged: {confidence_score:.2f}")
    except Exception as e:
        print(f"  Could not log confidence score: {e}")

    # Parse and log structured gap analysis
    try:
        parsed_gaps = _parse_gap_analysis(analysis_result)
        if parsed_gaps:
            mcp_client.request('insert_gap_analysis', {
                'session_id': session_id,
                'company': company_name,
                'gaps': parsed_gaps['gaps'],
                'recommendations': parsed_gaps['recommendations'],
                'priority_level': parsed_gaps['priority_summary']
            })
            print(f" Structured gap analysis logged: {len(parsed_gaps['gaps'])} gaps identified")
    except Exception as e:
        print(f"  Could not log gap analysis: {e}")

    print(f" Gap analysis complete")
    print(f"  Tokens used: {total_tokens} (prompt: {prompt_tokens}, completion: {completion_tokens})")

    return {
        'company': company_name,
        'session_id': session_id,
        'analysis': analysis_result,
        'tokens_used': total_tokens,
        'timestamp': datetime.now().isoformat()
    }

###############################################################################
#                         Part 4: Report Generation
###############################################################################
def generate_gap_report(analysis_result: Dict, output_path: str = None):
    """Generate a formatted gap analysis report"""

    if not output_path:
        company = analysis_result['company'].replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"{company}_CCPA_Gap_Analysis_{timestamp}.md"

    report = f"""# CCPA/CPRA Gap Analysis Report

**Company:** {analysis_result['company']}
**Analysis Date:** {analysis_result['timestamp']}
**Session ID:** {analysis_result['session_id']}

---

## Gap Analysis

{analysis_result['analysis']}

---

## Metadata

- **Model Used:** GPT-4.1
- **Tokens Consumed:** {analysis_result['tokens_used']}
- **Framework:** CCPA/CPRA (California Consumer Privacy Act / California Privacy Rights Act)

---

*Report generated by Privacy Policy Gap Analysis System with RAG and MCP*
*Powered by Cardinal Security Privacy Compliance Workflow*
"""

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n Markdown report saved: {output_path}")

    # Generate Professional Word document using Audit Caddie template
    docx_path = output_path.replace('.md', '.docx')
    try:
        # Prepare metadata for professional template
        metadata = {
            'company_name': analysis_result['company'],
            'report_title': 'CCPA COMPLIANCE ASSESSMENT REPORT',
            'subtitle': f"{analysis_result['company']} Privacy Policy\nCompliance Gap Analysis",
            'executive_summary': 'This report provides a comprehensive CCPA/CPRA compliance gap analysis, '
                               'identifying specific areas where the privacy policy requires updates to meet '
                               'California consumer privacy requirements.',
            'generated_by': 'Privacy Policy Gap Analysis System\nPowered by Cardinal Security',
            'analysis_date': datetime.now().strftime('%B %d, %Y')
        }

        convert_markdown_to_compliance_report(output_path, docx_path, metadata)
        print(f" Professional Word document saved: {docx_path}")

        # Generate PDF version
        pdf_path = output_path.replace('.md', '.pdf')
        try:
            convert_docx_to_pdf(docx_path, pdf_path)
            print(f" PDF report saved: {pdf_path}")
        except Exception as pdf_error:
            print(f" Warning: Could not generate PDF: {pdf_error}")
            print(f"  Install LibreOffice for PDF generation: brew install --cask libreoffice")

    except Exception as e:
        print(f" Warning: Could not generate Word document: {e}")

    return output_path

###############################################################################
#                         Part 5: Main Workflow
###############################################################################
def analyze_privacy_policy(pdf_path: str, company_name: str):
    """
    Complete workflow: Load policy, analyze against CCPA, generate report
    """
    print("\n" + "="*70)
    print("PRIVACY POLICY GAP ANALYSIS - CCPA/CPRA COMPLIANCE")
    print("="*70)
    print(f"Company: {company_name}")
    print(f"Policy: {pdf_path}")
    print("="*70)

    # Step 1: Load CCPA framework
    vectordb_ccpa = load_ccpa_framework()

    # Step 2: Load privacy policy from PDF
    vectordb_policy = load_privacy_policy(pdf_path, company_name)

    if not vectordb_policy:
        print(" Failed to load privacy policy")
        return None

    # Step 3: Perform gap analysis
    analysis_result = perform_gap_analysis(company_name, vectordb_ccpa, vectordb_policy)

    # Step 4: Generate report
    report_path = generate_gap_report(analysis_result)

    print("\n" + "="*70)
    print(" ANALYSIS COMPLETE")
    print("="*70)
    print(f"Report: {report_path}")
    print("="*70)

    return {
        'analysis': analysis_result,
        'report_path': report_path
    }


def analyze_policy_documents(privacy_pdf_path: str = None, terms_pdf_path: str = None, company_name: str = "Company"):
    """
    Complete workflow: Load both policy documents, analyze against CCPA, generate report

    Args:
        privacy_pdf_path: Path to privacy policy PDF (optional)
        terms_pdf_path: Path to terms & conditions PDF (optional)
        company_name: Name of the company

    Returns:
        Dictionary with analysis results and report path
    """
    print("\n" + "="*70)
    print("PRIVACY POLICY GAP ANALYSIS - CCPA/CPRA COMPLIANCE")
    print("="*70)
    print(f"Company: {company_name}")
    if privacy_pdf_path:
        print(f"Privacy Policy: {privacy_pdf_path}")
    if terms_pdf_path:
        print(f"Terms & Conditions: {terms_pdf_path}")
    print("="*70)

    # Step 1: Load CCPA framework
    vectordb_ccpa = load_ccpa_framework()

    # Step 2: Load policy documents (privacy policy and/or terms & conditions)
    vectordb_policy = load_policy_documents(
        privacy_pdf_path=privacy_pdf_path,
        terms_pdf_path=terms_pdf_path,
        company_name=company_name
    )

    if not vectordb_policy:
        print(" Failed to load policy documents")
        return None

    # Step 3: Perform gap analysis
    analysis_result = perform_gap_analysis(company_name, vectordb_ccpa, vectordb_policy)

    # Step 4: Generate report
    report_path = generate_gap_report(analysis_result)

    print("\n" + "="*70)
    print(" ANALYSIS COMPLETE")
    print("="*70)
    print(f"Report: {report_path}")
    print("="*70)

    return {
        'analysis': analysis_result,
        'report_path': report_path
    }

###############################################################################
#                         Example Usage
###############################################################################
if __name__ == '__main__':
    # Example: Analyze a privacy policy
    # pdf_path = "auditcaddie.com_privacy_policy.pdf"
    # company_name = "Audit Caddie"
    # result = analyze_privacy_policy(pdf_path, company_name)

    print("\nPrivacy Policy Gap Analysis System Ready")
    print("Usage:")
    print("  from privacy_rag_mcp import analyze_privacy_policy")
    print("  result = analyze_privacy_policy('path/to/policy.pdf', 'Company Name')")
