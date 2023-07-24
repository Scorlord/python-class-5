"""
Module containing custom exceptions for item-related errors.
"""


class InvalidItemNameError(Exception):
    """
    Exception raised when an invalid item name is encountered.

    Attributes:
        item (str): The invalid item name.
    """

    def __init__(self, item):
        if isinstance(item, str):
            super().__init__('Item name string cannot be empty.')
        else:
            super().__init__(f'Item name must be a string (not {type(item)}).')


class InvalidItemPriceError(Exception):
    """
    Exception raised when an invalid item price is encountered.

    Attributes:
        price: The invalid price argument.
    """

    def __init__(self, price):
        super().__init__(f'The price argument ("{price}") does'
                         'not appear to be any of the following: float, '
                         'an integer, or a string that'
                         'can be parsed to a non-negative float.')


class InvalidItemPoolError(Exception):
    """
    Exception raised when the item pool is not valid.

    Attributes:
        None
    """

    def __init__(self):
        super().__init__('ItemsPool needs to be set as a dictionary with'
                         'non-empty strings as keys and Item '
                         'instances as values.')


class NonExistingItemError(Exception):
    """
    Exception raised when a non-existing item is accessed.

    Attributes:
        item_name (str): The name of the non-existing item.
    """

    def __init__(self, item_name):
        super().__init__(f'Item named "{item_name}"'
                         'is not present in the item pool.')


class DuplicateItemError(Exception):
    """
    Exception raised when a duplicate item is encountered.

    Attributes:
        None
    """

    def __init__(self):
        super().__init__('Duplicate!')


class InvalidShoppingListSizeError(Exception):
    """
    Exception raised when an invalid shopping list size is encountered.

    Attributes:
        None
    """

    def __init__(self):
        super().__init__('Invalid List Size!')
