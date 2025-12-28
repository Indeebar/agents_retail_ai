from intent_agent.ml.infer import IntentClassifier
from intent_agent.rules.budget import extract_budget
from intent_agent.rules.category import extract_category
from intent_agent.rules.intent_rules import extract_intent_rule_based


ml_intent_classifier = IntentClassifier(
    model_path="intent_agent/models/intent_classifier",
    csv_path="intent_agent/data/intent_dataset.csv"
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
    return {
        "intent": extract_intent(text),
        "category": extract_category(text),
        "budget": extract_budget(text)
    }


if __name__ == "__main__":
    query = "I want a budget phone under 15000 for gaming"
    result = parse_user_query(query)
    print(result)
