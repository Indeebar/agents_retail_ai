# inventory_agent/checker.py

from inventory_agent.stock import STOCK_DATA


def filter_in_stock_products(products):
    """
    Removes out-of-stock products.
    """
    if not products:
        return []

    in_stock_products = []

    for product in products:
        sku = product.get("id")
        stock = STOCK_DATA.get(sku, 0)

        if stock > 0:
            in_stock_products.append(product)

    return in_stock_products
 