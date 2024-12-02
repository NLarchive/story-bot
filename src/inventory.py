# src/inventory.py
class Inventory:
    """Represents a character's inventory."""

    def __init__(self):
        self.items = {}

    def add_item(self, item: str, quantity: int = 1):
        self.items[item] = self.items.get(item, 0) + quantity

    def remove_item(self, item: str, quantity: int = 1):
        if item in self.items:
            self.items[item] -= quantity
            if self.items[item] <= 0:
                del self.items[item]

    def list_items(self) -> str:
        return ", ".join(f"{item} (x{quantity})" for item, quantity in self.items.items()) if self.items else "Empty"
