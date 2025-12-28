from intent_agent.parser import parse_user_query
from contracts import   IntentResult

def get_intent(query:str) -> IntentResult:
    raw=parse_user_query(query)

    return {
        "intent": raw.get("intent", "unknown"),
        "category": raw.get("category"),
        "budget": raw.get("budget"),
        "confidence": None  # optional, safe default
    }

from recommendation_agent.recommender import recommend_products
from .contracts import RecommendationResult


def get_recommendations(intent_data) -> RecommendationResult:
    items = recommend_products(
        query=intent_data["intent"],
        category=intent_data["category"],
        budget=intent_data["budget"]
    )

    clean_items = [
        {
            "product_id": item["id"],
            "name": item["name"],
            "price": item["price"]
        }
        for item in items
    ]

    return {
        "items": clean_items,
        "source": "recommendation_agent"
    }
