class InventorySystem:
    def __init__(self):
        self._inventory = {"AA11BB": 3}

    def reserve(self, sku, quantity):
        items_in_stock = self._inventory.get(sku, 0)
        if items_in_stock >= quantity:
            self._inventory[sku] = items_in_stock - quantity
        else:
            raise InsufficientInventoryError()


class InsufficientInventoryError(Exception):
    pass
