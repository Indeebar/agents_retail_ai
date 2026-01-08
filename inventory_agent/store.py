# inventory_agent/store.py

class InventoryStore:
    def __init__(self):
        # Initial mock state (can come from DB later)
        self._stock = {
            "SKU012": 0,
            "SKU013": 5,
            "SKU014": 12,
            "SKU015": 30,
            "SKU023": 0
        }

    def get_stock(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def update_stock(self, sku: str, delta: int):
        current = self.get_stock(sku)
        self._stock[sku] = max(0, current + delta)

    def all_stock(self):
        return self._stock
