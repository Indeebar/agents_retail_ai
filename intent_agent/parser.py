from intent_agent.ml.infer import IntentClassifier
from intent_agent.rules.budget import extract_budget
from intent_agent.rules.category import extract_category
from intent_agent.rules.intent_rules import extract_intent_rule_based


import os

# Construct absolute path relative to this file
model_dir = os.path.join(os.path.dirname(__file__), "models", "intent_classifier")
csv_path = os.path.join(os.path.dirname(__file__), "data", "intent_dataset.csv")

ml_intent_classifier = IntentClassifier(
    model_path=model_dir,
    csv_path=csv_path
)


def extract_intent(text: str) -> str:
    """
    ML-first intent extraction with rule-based fallback.
    """
    try:
        return ml_intent_classifier.predict(text)
    except Exception:
        return extract_intent_rule_based(text)


def parse_user_query(text: str):
    if not text or not text.strip():
        return {
            "intent": None,
            "category": None,
            "budget": None
        }
    
    return {
        "intent": extract_intent(text),
        "category": extract_category(text),
        "budget": extract_budget(text)
    }


if __name__ == "__main__":
    query = "I want a budget phone under 15000 for gaming"
    result = parse_user_query(query)
    print(result)
