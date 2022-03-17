import pytest

from ..order import Order

talisker = "Talisker"


class InMemoryWarehouse:
    def __init__(self):
        self.inventory = {}

    def add(self, product, quantity):
        self.inventory[product] = self.inventory.get(product, 0) + quantity

    def has_inventory(self, product, quantity):
        return self.inventory[product] >= quantity

    def get_inventory(self, product):
        return self.inventory[product]

    def remove(self, product, quantity):
        self.inventory[product] -= quantity


class TestOrderState:

    @pytest.fixture()
    def warehouse(self):
        warehouse = InMemoryWarehouse()
        warehouse.add(talisker, 50)
        return warehouse

    def test_order_is_filled_if_enough_items_in_warehouse(self, warehouse):
        order = Order(talisker, 50)

        order.fill(warehouse)

        assert order.is_filled()

    def test_order_is_not_filled_if_not_enough_items_in_warehouse(self, warehouse):
        order = Order(talisker, 51)

        order.fill(warehouse)

        assert not order.is_filled()

    def test_items_are_transferred_from_the_warehouse_if_enough_items_in_warehouse(self, warehouse):
        order = Order(talisker, 50)

        order.fill(warehouse)

        assert warehouse.get_inventory(talisker) == 0

    def test_items_are_not_transferred_from_the_warehouse_if_not_enough_items_in_warehouse(self, warehouse):
        order = Order(talisker, 51)

        order.fill(warehouse)
        assert warehouse.get_inventory(talisker) == 50

