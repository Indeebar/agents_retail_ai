def extract_intent_rule_based(text: str):
    text=text.lower()
    intent_keywords = {
        "purchase": ["want","buy", "purchase", "order", "checkout"],
        "compare": ["compare", "better", "vs"],
        "reserve": ["reserve", "book", "try in store"],
        "support": ["return", "refund", "exchange", "complaint"],
        "browse": ["show", "browse", "look", "find"]
    }
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in text:
                return intent
    return "browse"

