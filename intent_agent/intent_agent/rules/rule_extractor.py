import re

def extract_budget(text: str):
   text=text.lower()

   match = re.search(r'(\d+)\s*(k)?', text)

   if not match:
        return None

   amount = int(match.group(1))

   if match.group(2):
        amount = amount * 1000

   return amount




def extract_category(text: str):
    text=text.lower()

    category_keywords = {
        "electronics": ["phone", "laptop", "camera"],
        "clothing": ["shirt", "pants", "jacket"],
        "shoes": ["sneakers", "boots", "heels"]
    }

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text:
                return category

def extract_intent(text: str):
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


def parse_user_query(text: str):
    """
    Combine all extractors into structured output.
    """
    return {
        "intent": extract_intent(text),
        "category": extract_category(text),
        "budget": extract_budget(text)
    }


#code to check function

if __name__ == "__main__":
    tests = [
        "show me sneakers under 6000",
        "compare nike vs adidas shoes",
        "i want to buy a jacket",
        "reserve this shirt in store",
        "i want to return my order",
        "show me some good phones under 15k"
    ]

    for t in tests:
        print(t)
        print(parse_user_query(t))
        print()

