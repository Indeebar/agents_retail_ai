from typing import List, Dict, Optional


def filter_by_category(
    products: List[Dict],
    category: Optional[str]
) -> List[Dict]:
    if not category:
        return products

    category = category.lower().strip()

    return [
        product
        for product in products
        if product.get("category", "").lower() == category
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
