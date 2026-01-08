# inventory_agent/checker.py

from inventory_agent.store import InventoryStore

store = InventoryStore()


def filter_in_stock_products(products):
    if not products:
        return []

    return [
        p for p in products
        if store.get_stock(p.get("id")) > 0
    ]
