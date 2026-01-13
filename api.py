from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from sales_agent.orchestrator import handle_user_query

app = FastAPI(title="Retail AI Agent API", version="1.0.0")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    success: bool
    message: str
    intent: Optional[str] = None
    category: Optional[str] = None
    budget: Optional[float] = None
    products: Optional[List[Dict[str, Any]]] = None

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest) -> QueryResponse:
    result = handle_user_query(request.query)
    return QueryResponse(
        success=result.success,
        message=result.message,
        intent=result.intent,
        category=result.category,
        budget=result.budget,
        products=result.products
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)