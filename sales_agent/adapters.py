from typing import Dict, Optional, List


def adapt_intent_output(intent_result: Dict) -> Dict:

    if not intent_result:
        return {
            "intent": None,
            "category": None,
            "budget": None,
            "is_product_seeking": False
        }

    return {
        "intent": intent_result.get("intent"),
        "category": intent_result.get("category"),
        "budget": intent_result.get("budget"),
        "is_product_seeking": intent_result.get("is_product_seeking", False)
    }


def adapt_recommendation_output(
    recommendations: Optional[List[Dict]]
) -> List[Dict]:

    if not recommendations:
        return []

    return recommendations
