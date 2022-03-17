class Order:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self._is_filled = False

    def fill(self, warehouse):
        if warehouse.has_inventory(self.product, self.quantity):
            warehouse.remove(self.product, self.quantity)
            self._is_filled = True

    def is_filled(self):
        return self._is_filled
