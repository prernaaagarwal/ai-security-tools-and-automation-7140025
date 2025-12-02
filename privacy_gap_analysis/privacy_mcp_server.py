#!/usr/bin/env python3
"""
MCP Server for Privacy Policy Gap Analysis Workflow
Tracks conversation memory, confidence scores, feedback, and token usage
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, List, Optional
from uuid import uuid4
import uvicorn
from datetime import datetime

app = FastAPI(title="Privacy Policy MCP Server")

# In-memory stores for workflow tracking
memory_store = {}        # Stores Q&A conversation history and analysis results
confidence_store = []    # Stores confidence logs for gap analysis
feedback_store = []      # Stores user feedback on analysis quality
token_usage_store = []   # Tracks token consumption per analysis
gap_analysis_store = []  # Stores detailed gap analysis results

###############################################################################
#                         Pydantic Models
###############################################################################
class SearchRequest(BaseModel):
    query: str
    k: int = 1

class InsertMemoryRequest(BaseModel):
    session_id: str
    text: str

class MemoryRequest(BaseModel):
    session_id: str

class GapAnalysisRequest(BaseModel):
    company: str
    gaps: List[dict]
    recommendations: List[str]
    priority_level: str

###############################################################################
#                         MCP JSON-RPC Endpoint
###############################################################################
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    JSON-RPC endpoint for MCP supporting privacy analysis workflow.
    Supports:
      - search_documents: Search for CCPA requirements or policy content
      - insert_memory: Log Q&A pairs and analysis results
      - fetch_memory: Retrieve conversation/analysis history
      - insert_confidence: Log confidence scores for gap analysis
      - insert_feedback: Record user feedback on analysis quality
      - insert_token_usage: Track GPT-4.1 token consumption
      - insert_gap_analysis: Store detailed gap analysis results
    """
    payload = await request.json()
    method = payload.get("method")
    params = payload.get("params")
    req_id = payload.get("id")

    # 1) search_documents: Return dummy document(s) for the given query
    if method == "search_documents":
        query = params.get("query", "")
        k = params.get("k", 1)
        results = [{"text": f"Privacy requirement for query: '{query}'"} for _ in range(k)]
        return {"jsonrpc": "2.0", "result": results, "id": req_id}

    # 2) insert_memory: Log Q&A pair or analysis result
    elif method == "insert_memory":
        session_id = params.get("session_id")
        text = params.get("text")
        if not session_id or not text:
            return {"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid params"}, "id": req_id}

        if session_id not in memory_store:
            memory_store[session_id] = []

        entry = {
            "id": str(uuid4()),
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        memory_store[session_id].append(entry)
        return {"jsonrpc": "2.0", "result": "Memory inserted", "id": req_id}

    # 3) fetch_memory: Retrieve conversation/analysis history
    elif method == "fetch_memory":
        session_id = params.get("session_id")
        if not session_id:
            return {"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid params"}, "id": req_id}

        results = memory_store.get(session_id, [])
        return {"jsonrpc": "2.0", "result": results, "id": req_id}

    # 4) insert_confidence: Log gap analysis confidence
    elif method == "insert_confidence":
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": params.get("query", ""),
            "response": params.get("response", ""),
            "confidence_score": params.get("confidence_score", 0),
            "is_high_confidence": params.get("confidence_score", 0) > 0.8,
            "is_low_confidence": params.get("confidence_score", 0) < 0.4
        }
        confidence_store.append(log_entry)
        return {"jsonrpc": "2.0", "result": "Confidence log inserted", "id": req_id}

    # 5) insert_feedback: Record user feedback
    elif method == "insert_feedback":
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": params.get("session_id", ""),
            "question": params.get("question", ""),
            "rating": params.get("rating", "")  # "thumbs_up" or "thumbs_down"
        }
        feedback_store.append(feedback_entry)
        return {"jsonrpc": "2.0", "result": "Feedback inserted", "id": req_id}

    # 6) insert_token_usage: Track token consumption
    elif method == "insert_token_usage":
        token_entry = {
            "timestamp": params.get("timestamp", datetime.now().isoformat()),
            "query": params.get("query", ""),
            "model_used": params.get("model_used", ""),
            "tokens_prompt": params.get("tokens_prompt", 0),
            "tokens_completion": params.get("tokens_completion", 0),
            "tokens_total": params.get("tokens_total", 0)
        }
        token_usage_store.append(token_entry)
        return {"jsonrpc": "2.0", "result": "Token usage logged", "id": req_id}

    # 7) insert_gap_analysis: Store detailed gap analysis
    elif method == "insert_gap_analysis":
        gap_entry = {
            "timestamp": datetime.now().isoformat(),
            "company": params.get("company", ""),
            "gaps": params.get("gaps", []),
            "recommendations": params.get("recommendations", []),
            "priority_level": params.get("priority_level", ""),
            "session_id": params.get("session_id", "")
        }
        gap_analysis_store.append(gap_entry)
        return {"jsonrpc": "2.0", "result": "Gap analysis stored", "id": req_id}

    # 8) Method not recognized
    else:
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}

###############################################################################
#                         Debug Endpoints
###############################################################################
@app.get("/debug/memory")
async def debug_memory():
    """Return the current conversation memory for debugging"""
    return memory_store

@app.get("/debug/confidence")
async def debug_confidence():
    """Return the logged confidence data"""
    return confidence_store

@app.get("/debug/feedback")
async def debug_feedback():
    """Return the recorded user feedback"""
    return feedback_store

@app.get("/debug/tokens")
async def debug_tokens():
    """Return token usage statistics"""
    return token_usage_store

@app.get("/debug/gaps")
async def debug_gaps():
    """Return stored gap analysis results"""
    return gap_analysis_store

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Privacy Policy MCP Server",
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "total_sessions": len(memory_store),
            "total_analyses": len(gap_analysis_store),
            "total_feedback": len(feedback_store),
            "total_token_logs": len(token_usage_store)
        }
    }

###############################################################################
#                         Main Entry Point
###############################################################################
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Privacy Policy MCP Server")
    print("="*60)
    print("Starting server on http://0.0.0.0:8080")
    print("MCP Endpoint: http://0.0.0.0:8080/mcp")
    print("Health Check: http://0.0.0.0:8080/health")
    print("Debug Endpoints:")
    print("  - http://0.0.0.0:8080/debug/memory")
    print("  - http://0.0.0.0:8080/debug/confidence")
    print("  - http://0.0.0.0:8080/debug/feedback")
    print("  - http://0.0.0.0:8080/debug/tokens")
    print("  - http://0.0.0.0:8080/debug/gaps")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8080)
