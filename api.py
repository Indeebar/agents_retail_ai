from fastapi import FastAPI
from pydantic import BaseModel

from sales_agent.orchestrator import handle_user_query

app = FastAPI(
    title="Retail AI Agentic System",
    description="Agentic AI backend for retail product recommendations",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query_retail_ai(request: QueryRequest):
    """
    System API endpoint.
    Wraps the Sales Agent.
    """
    return handle_user_query(request.query)
