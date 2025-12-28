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
    return "unknown"
