"""Module Description: This module contains the ShoppingList class."""

import random
try:
    from core.errors import InvalidShoppingListSizeError
except ImportError:
    pass


class ShoppingList:
    """Class Description: This class represents a shopping list."""

    def __init__(self, size=None, quantities=None, item_pool=None):
        """Method Description: Initialize the ShoppingList object."""
        self.list = []
        if item_pool is not None:
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size=None, quantities=None):
        """Method Description: Refresh the shopping list with new items."""
        if size is None:
            size = random.randint(1, item_pool.get_size())
        if not isinstance(size, int) or size < 1:
            raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if not isinstance(quantities, list):
            raise ValueError()
        for elem in quantities:
            if not isinstance(elem, int) or elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        items_list = item_pool.sample_items(size)
        self.list = list(zip(items_list, quantities))

    def get_total_price(self):
        """Method Description:
        Calculate the total price of the shopping list."""
        return round(sum(item.price * qnt for item, qnt in self.list), 2)

    def get_item_price(self, i):
        """Method Description:
        Calculate the price of an item at the given index."""
        return round(self.list[i][0].price * self.list[i][1], 2)

    def __len__(self):
        """Method Description: Get the length of the shopping list."""
        return len(self.list)
