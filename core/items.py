"""Module Description: This module contains the Item and Item Pool class."""

import math
import random
try:
    from core.errors import (
        InvalidItemNameError, InvalidItemPriceError,
        InvalidItemPoolError, DuplicateItemError, NonExistingItemError)
except ImportError:
    pass


class Item:
    """Represents an item with a name and price."""

    def __init__(self, name, price):
        """Initialize the item with a name and price."""
        if not isinstance(name, str) or name == '':
            raise InvalidItemNameError(name)
        self.name = name
        if not isinstance(price, (float, int)) or not price > 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        """Calculate the order of the item's price."""
        return math.floor(round(math.log(self.price, 10), 10))

    def get_price_str(self, quantity=None, hide_price=False, order=None):
        """Get a formatted string representation of the item's price."""
        if order is None:
            order = self.get_order()
        prc_str = '${:0' + str(order + 4) + '.2f}'
        prc_str = prc_str.format(self.price * (quantity or 1))
        if hide_price:
            prc_str = f'${"?" * (order + 1)}.??'
        return f'{prc_str}'

    def get_list_item_str(self, quantity=None, leading_dash=True):
        """Get a formatted string representation
        of the item for the shopping list."""
        if quantity is None:
            qnt_str = ''
        else:
            qnt_str = f' ({quantity}x)'

        dash = ''
        if leading_dash:
            dash = '- '
        return f'{dash}{self.name}{qnt_str}'

    def __repr__(self):
        return f'Item({self.name}, {self.price})'

    def __eq__(self, other):
        return (
            isinstance(other, Item) and self.name == other.name
            and self.price == other.price)


class ItemPool:
    """Represents a pool of items that can be used in a shopping list."""

    def __init__(self, items=None):
        """Initialize the item pool."""
        if not items:
            items = {}
        if not isinstance(items, dict):
            raise InvalidItemPoolError()
        for key, val in items.items():
            if not isinstance(key, str) or not isinstance(val, Item):
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        """Add an item to the pool."""
        if not isinstance(item, Item):
            raise InvalidItemPoolError()
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        """Remove an item from the pool."""
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        """Get the size of the item pool."""
        return len(self.items)

    def sample_items(self, sample_size):
        """Get a sample of items from the pool."""
        return (
            random.sample(list(self.items.values()),
                          min(sample_size, len(self.items))))

    def __repr__(self):
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        return isinstance(other, ItemPool) and self.items == other.items
