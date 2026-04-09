from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
import os

# Ensure the src module can be imported
sys.path.append(os.getcwd())
try:
    from src.rag_agent import RAGAgent
except ImportError:
    # Fallback if run directly from src/
    from rag_agent import RAGAgent

app = FastAPI(
    title="RAG Customer Support API",
    description="API for the RAG-powered Customer Support Agent.",
    version="1.0.0"
)

# Initialize RAG agent lazily or during startup
# For simplicity, we initialize it globally here.
agent = None

@app.on_event("startup")
def startup_event():
    global agent
    try:
        agent = RAGAgent()
        print("RAGAgent initialized successfully.")
    except Exception as e:
        print(f"Warning: Failed to initialize RAGAgent. Ensure your environment variables and Chroma DB are set up. Error: {e}")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/api/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    if agent is None:
        raise HTTPException(
            status_code=503, 
            detail="RAG Agent is not available. Please check server logs."
        )
    
    try:
        answer = agent.ask(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "agent_ready": agent is not None}

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
