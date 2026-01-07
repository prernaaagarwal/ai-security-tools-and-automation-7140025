#!/usr/bin/env python3
"""
RAG Retrieval Demo - LinkedIn Learning Chapter 2
Interactive demonstration of Retrieval-Augmented Generation

This script demonstrates:
1. Loading CCPA framework into vector database (INDEXING)
2. Retrieving relevant documents (RETRIEVAL)
3. Showing how GPT-4 uses context (GENERATION)
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from privacy_rag_mcp import load_ccpa_framework
import time


def print_banner(text):
    """Print a visual banner"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)


def print_section(text):
    """Print a section header"""
    print("\n" + "-"*80)
    print(f"  {text}")
    print("-"*80)


def demo_indexing():
    """Demo: INDEXING PHASE - Load CCPA framework into vector database"""

    print_banner("PHASE 1: INDEXING - Loading CCPA Framework into Vector Database")

    print("\n Loading CCPA/CPRA compliance requirements...")
    print("   File: CCPA_CPRA_Framework.csv")
    print("   Each row = 1 compliance requirement")
    print("\n⏳ Building vector embeddings with all-MiniLM-L12-v2...")

    # Load the framework
    vectordb = load_ccpa_framework()

    print("\n Vector database created!")
    print("   - All CCPA requirements indexed")
    print("   - Embeddings stored in ChromaDB")
    print("   - Ready for semantic search")

    return vectordb


def demo_retrieval(vectordb, query, top_k=3):
    """Demo: RETRIEVAL PHASE - Search for relevant requirements"""

    print_banner(f"PHASE 2: RETRIEVAL - Semantic Search")

    print(f"\n Query: \"{query}\"")
    print(f"   Retrieving top {top_k} most relevant CCPA requirements...")

    # Create retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": top_k})

    # Retrieve documents
    print("\n⏳ Searching vector database...")
    results = retriever.invoke(query)

    print(f"\n Found {len(results)} relevant requirements:")

    # Display results
    for i, doc in enumerate(results, 1):
        print_section(f"Result #{i}")

        # Show metadata if available
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"\n Metadata:")
            for key, value in doc.metadata.items():
                print(f"   {key}: {value}")

        # Show content
        print(f"\n Content:")
        content = doc.page_content

        # Pretty print content (wrap at 76 characters)
        lines = content.split('\n')
        for line in lines:
            if len(line) <= 76:
                print(f"   {line}")
            else:
                # Wrap long lines
                words = line.split()
                current_line = "   "
                for word in words:
                    if len(current_line) + len(word) + 1 <= 76:
                        current_line += word + " "
                    else:
                        print(current_line)
                        current_line = "   " + word + " "
                if current_line.strip():
                    print(current_line)

    return results


def demo_generation_context(results):
    """Demo: GENERATION PHASE - Show context that would go to GPT-4"""

    print_banner("PHASE 3: GENERATION - Context for GPT-4")

    print("\n Building context for GPT-4...")

    # Build context like the real system does
    ccpa_context = "\n\n".join([doc.page_content for doc in results])

    print(f"\n Context prepared ({len(ccpa_context)} characters)")
    print("\n This context would be sent to GPT-4 in the prompt:")

    print_section("GPT-4 Prompt Structure")

    print("""
   System Prompt:
   "You are a Privacy Compliance Officer specializing in CCPA/CPRA.
    Analyze privacy policies and identify gaps..."

   User Prompt:
   "CCPA/CPRA REQUIREMENTS:
   [Retrieved context from vector database]

   COMPANY PRIVACY POLICY:
   [Extracted policy text]

   Perform a comprehensive gap analysis..."
    """)

    print_section("Retrieved Context (First 500 characters)")
    print(f"\n   {ccpa_context[:500]}...")

    return ccpa_context


def run_interactive_demo():
    """Run the complete interactive demo"""

    print("\n" + "="*80)
    print("  RAG (Retrieval-Augmented Generation) Demo")
    print("  LinkedIn Learning: AI Automation - Chapter 2")
    print("="*80)

    print("\n This demo shows how RAG works in our Privacy Compliance Tool:")
    print("   1. INDEXING: Load compliance requirements into vector database")
    print("   2. RETRIEVAL: Search for relevant requirements")
    print("   3. GENERATION: Provide context to GPT-4 for analysis")

    input("\n⏸  Press Enter to start Phase 1: INDEXING...")

    # Phase 1: Indexing
    vectordb = demo_indexing()

    input("\n⏸  Press Enter to start Phase 2: RETRIEVAL...")

    # Phase 2: Retrieval - Multiple queries to demonstrate
    queries = [
        ("right to delete personal information", 3),
        ("data retention policies", 2),
        ("consumer request methods", 2),
    ]

    all_results = []

    for i, (query, top_k) in enumerate(queries, 1):
        print(f"\n\n{'='*80}")
        print(f"  RETRIEVAL EXAMPLE {i}/{len(queries)}")
        print(f"{'='*80}")

        results = demo_retrieval(vectordb, query, top_k)
        all_results.append(results)

        if i < len(queries):
            input(f"\n⏸  Press Enter for next retrieval example...")

    input("\n⏸  Press Enter to start Phase 3: GENERATION CONTEXT...")

    # Phase 3: Show generation context
    demo_generation_context(all_results[0])

    print("\n" + "="*80)
    print("   Demo Complete!")
    print("="*80)
    print("\n Key Takeaways:")
    print("   1. Vector databases enable semantic search (meaning-based, not keyword)")
    print("   2. Retrieval finds the MOST RELEVANT requirements for each query")
    print("   3. GPT-4 uses this context to perform accurate gap analysis")
    print("   4. RAG combines retrieval precision with GPT-4's reasoning power")
    print("\n" + "="*80 + "\n")


def run_quick_demo():
    """Run a quick, non-interactive demo for screen recording"""

    print("\n" + "="*80)
    print("  RAG Quick Demo - Privacy Compliance Tool")
    print("="*80)

    # Phase 1: Indexing
    vectordb = demo_indexing()

    time.sleep(1)

    # Phase 2: Retrieval
    query = "right to delete personal information"
    results = demo_retrieval(vectordb, query, top_k=3)

    time.sleep(1)

    # Phase 3: Context
    demo_generation_context(results)

    print("\n" + "="*80)
    print("   Demo Complete!")
    print("="*80 + "\n")


def main():
    """Main entry point"""

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick demo (no pauses)
        run_quick_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\n RAG Retrieval Demo")
        print("="*60)
        print("\nUsage:")
        print("  python demo_rag_retrieval.py              # Interactive demo with pauses")
        print("  python demo_rag_retrieval.py --quick      # Quick demo (no pauses)")
        print("\nFor LinkedIn Learning Chapter 2:")
        print("  Use interactive mode during live coding")
        print("  Use quick mode for screen recording")
        print("="*60 + "\n")
    else:
        # Interactive demo (with pauses)
        run_interactive_demo()


if __name__ == "__main__":
    main()
