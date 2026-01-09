def apply_pricing_rules(products, budget=None):
    """
    Applies simple pricing and offers.
    Rules (v1):
    - 10% discount on electronics above ₹30,000
    - Cap price to budget if budget exists
    """
    if not products:
        return []

    updated = []

    for product in products:
        price = int(product.get("price", 0))
        category = product.get("category")

        # Rule 1: Discount
        if category == "electronics" and price > 30000:
            price = int(price * 0.9)  # 10% off

        # Rule 2: Budget cap
        if budget is not None and price > budget:
            continue

        new_product = product.copy()
        new_product["final_price"] = price
        updated.append(new_product)

    return updated
