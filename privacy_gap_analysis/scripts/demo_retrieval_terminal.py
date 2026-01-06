#!/usr/bin/env python3
"""
Terminal Demo Script - LinkedIn Learning Chapter 2
Shows the exact commands from your course outline

This simulates the Python REPL commands for screencap:
>>> from privacy_rag_mcp import load_ccpa_framework
>>> vectordb = load_ccpa_framework()
>>> retriever = vectordb.as_retriever(search_kwargs={"k": 3})
>>> results = retriever.invoke("right to delete personal information")
>>> for doc in results:
...     print(doc.page_content[:200])
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*80)
print("  Python Interactive Terminal Demo - RAG Retrieval")
print("  LinkedIn Learning Chapter 2")
print("="*80 + "\n")

# Step 1: Import
print(">>> from privacy_rag_mcp import load_ccpa_framework")
from privacy_rag_mcp import load_ccpa_framework

print("✓ Imported load_ccpa_framework\n")

# Step 2: Load vector database
print(">>> vectordb = load_ccpa_framework()")
vectordb = load_ccpa_framework()
print("✓ Vector database loaded\n")

# Step 3: Create retriever
print('>>> retriever = vectordb.as_retriever(search_kwargs={"k": 3})')
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
print("✓ Retriever created (will return top 3 results)\n")

# Step 4: Perform retrieval
print('>>> results = retriever.invoke("right to delete personal information")')
results = retriever.invoke("right to delete personal information")
print(f"✓ Retrieved {len(results)} documents\n")

# Step 5: Display results
print(">>> for doc in results:")
print("...     print(doc.page_content[:200])")
print()

for i, doc in enumerate(results, 1):
    print(f"[Document {i}]")
    print(doc.page_content[:200])
    if len(doc.page_content) > 200:
        print("...")
    print()

print("="*80)
print("✅ Demo Complete - This is how RAG retrieval works!")
print("="*80)
print("\n💡 What just happened:")
print("   1. Loaded CCPA requirements into vector database")
print("   2. Created a retriever to search semantically")
print("   3. Queried: 'right to delete personal information'")
print("   4. Got back the 3 most relevant CCPA sections")
print("\n🎯 Key Point:")
print("   This is SEMANTIC search (meaning-based), not keyword search!")
print("   The system understood the INTENT of our query.\n")
