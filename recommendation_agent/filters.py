CATEGORY_MAP = {
    "tech": {"tech", "electronics", "gadgets", "devices", "wearables"},
    "footwear": {"footwear", "shoes", "sneakers", "boots"},
    "apparel": {"apparel", "clothing", "clothes"},
    "accessories": {"accessories", "bags", "belts"},
    "home": {"home", "kitchen", "furniture"}
}

from typing import List, Dict, Optional


def filter_by_category(
    products: List[Dict],
    category: Optional[str]
) -> List[Dict]:
    if not category:
        return products

    category = category.lower().strip()

    # Find canonical category
    canonical = None
    for key, aliases in CATEGORY_MAP.items():
        if category in aliases:
            canonical = key
            break

    if not canonical:
        return products  # fallback: don't filter

    return [
        product
        for product in products
        if product.get("category", "").lower() in CATEGORY_MAP[canonical]
    ]



def filter_by_budget(
    products: List[Dict],
    max_price: Optional[float]
) -> List[Dict]:
    if max_price is None:
        return products

    return [
        product
        for product in products
        if float(product.get("price", 0)) <= max_price
    ]
