from typing import optional,TypeDict,List

class SalesAgentInput(TypeDict):
    query: str
    user_id:Optional[str]
    session_id:Optional[str]

class IntentResult(TypedDict):
    intent: str            # purchase | browse | support | unknown
    category: Optional[str]
    budget: Optional[int]
    confidence: Optional[float]

class RecommendationItem(TypedDict):
    product_id: str
    name: str
    price: int

class RecommendationResult(TypedDict):
    items: List[RecommendationItem]
    source: str

class SalesAgentResponse(TypedDict):
    intent: IntentResult
    recommendation: Optional[RecommendationResult]
    