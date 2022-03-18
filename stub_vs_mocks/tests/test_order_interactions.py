from unittest.mock import Mock
import pytest

from ..order import Order

benriach = "Benriach"


@pytest.fixture()
def warehouse():
    warehouse = Mock()
    warehouse.remove = Mock()

    return warehouse


@pytest.fixture()
def order():
    return Order(benriach, 50)


class Test_Given_enough_products_are_in_stock:

    # Given
    @pytest.fixture()
    def mock_warehouse(self, warehouse):
        warehouse.has_inventory = Mock(return_value=True) # config mock as a stub
        return warehouse

    class Test_when_filling_order:

        # When
        @pytest.fixture(autouse=True)
        def filling_order(self, mock_warehouse, order):
            order.fill(mock_warehouse)

        # Then
        def test_then_products_are_removed_from_inventory(self, mock_warehouse):
            mock_warehouse.remove.assert_called_with(benriach, 50) # verification of behavior

        # Then
        def test_then_order_is_filled(self, mock_warehouse, order):
            assert order.is_filled() # state verification (side effect of behavior of our objects)


class Test_Given_not_enough_products_are_in_stock:

    # Given
    @pytest.fixture()
    def mock_warehouse(self, warehouse):
        warehouse.has_inventory = Mock(return_value=False)
        return warehouse

    class Test_when_filling_order:

        # When
        @pytest.fixture(autouse=True)
        def filling_order(self, mock_warehouse, order):
            order.fill(mock_warehouse)

        # Then
        def test_then_products_are_not_removed_from_inventory(self, mock_warehouse):
            mock_warehouse.remove.assert_not_called() # verification of behavior

        # Then
        def test_then_order_is_not_filled(self, mock_warehouse, order):
            assert not order.is_filled() # state verification (side effect of behavior of our objects)
