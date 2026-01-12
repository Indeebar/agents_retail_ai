from intent_agent.ml.infer import IntentClassifier
from intent_agent.rules.budget import extract_budget
from intent_agent.rules.category import extract_category
from intent_agent.rules.intent_rules import extract_intent_rule_based


import os

# Construct absolute path relative to this file
model_dir = os.path.join(os.path.dirname(__file__), "models", "intent_classifier")
expanded_csv_path = os.path.join(os.path.dirname(__file__), "data", "intent_dataset_expanded.csv")
original_csv_path = os.path.join(os.path.dirname(__file__), "data", "intent_dataset.csv")

# Use expanded dataset if available, otherwise fall back to original
csv_path = expanded_csv_path if os.path.exists(expanded_csv_path) else original_csv_path

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


def is_product_seeking_query(text: str) -> bool:
    """
    Uses the transformer model to determine if the query is product-seeking.
    This expands beyond simple keyword matching to understand context.
    """
    # We'll use a combination of category detection and intent prediction
    # to determine if the query is seeking products
    detected_category = extract_category(text)
    predicted_intent = extract_intent(text)
    text_lower = text.lower()
    
    # Negative indicators that strongly suggest non-product queries
    negative_indicators = [
        "track", "status", "return", "refund", "delivery", 
        "shipping", "package", "complaint", "issue",
        "problem", "exchange", "support", "help", "customer service",
        "cancel", "modify", "change", "update", "fix"
    ]
    
    # Check for strong negative indicators
    for indicator in negative_indicators:
        if indicator in text_lower:
            # Even if ML predicts purchase intent, these phrases usually mean non-product queries
            return False
    
    # If a category is detected, it's likely product-seeking
    if detected_category and detected_category != "unknown":
        return True
    
    # Certain intents indicate product-seeking behavior when combined with other signals
    product_related_intents = ["browse", "purchase", "compare"]
    if predicted_intent in product_related_intents:
        # For these intents, also check if there are product-related terms
        product_terms = [
            "show me", "find me", "what", "need", "want", "buy", "get", "laptop", 
            "phone", "camera", "watch", "shoe", "product", "item", "deal",
            "offer", "recommend", "suggest", "best", "good", "nice", "looking for",
            "look for", "i want", "i need", "i'm looking for", "any good", "good",
            "best", "top", "available", "have", "got", "in", "for", "under", "below"
        ]
        for term in product_terms:
            if term in text_lower:
                return True
    
    # General product-related keywords that indicate seeking behavior
    general_product_terms = [
        "show me", "find me", "what", "need", "want", "buy", "get", "laptop", 
        "phone", "camera", "watch", "shoe", "product", "item", "deal",
        "offer", "recommend", "suggest", "best", "good", "nice", "looking for",
        "look for", "i want", "i need", "i'm looking for", "any good", "good",
        "best", "top", "available", "have", "got", "in", "for", "under", "below"
    ]
    
    for term in general_product_terms:
        if term in text_lower:
            return True
    
    return False


def parse_user_query(text: str):
    if not text or not text.strip():
        return {
            "intent": "unknown",
            "category": None,
            "budget": None,
            "is_product_seeking": False
        }
    
    intent = extract_intent(text)
    category = extract_category(text)
    budget = extract_budget(text)
    
    return {
        "intent": intent,
        "category": category,
        "budget": budget,
        "is_product_seeking": is_product_seeking_query(text)
    }


if __name__ == "__main__":
    query = "I want a budget phone under 15000 for gaming"
    result = parse_user_query(query)
    print(result)
