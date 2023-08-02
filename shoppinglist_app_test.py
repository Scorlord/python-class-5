import math

import pytest
from core.shoppinglist import ShoppingList
from app_cli import AppCLI
from core.appengine import AppEngine
from core.items import Item, ItemPool
from core.errors import (
    InvalidItemNameError, InvalidItemPriceError, InvalidShoppingListSizeError,
    InvalidItemPoolError, DuplicateItemError, NonExistingItemError)


def test_valid_item_init():
    item = Item('bread', 3.25)
    assert item.name == 'bread'
    assert math.isclose(item.price, 3.25)


def test_invalid_item_init():
    with pytest.raises(InvalidItemNameError):
        Item('', 3.25)
    with pytest.raises(InvalidItemPriceError):
        Item('bread', -3.25)


def test_item_get_order():
    item = Item('bread', 3.25)
    assert item.get_order() == 0
    item.price = 1000.0
    assert item.get_order() == 3


def test_item_get_list_item_str():
    item = Item('bread', 3.25)
    assert item.get_list_item_str() == '- bread'
    assert item.get_list_item_str(quantity=2) == '- bread (2x)'
    assert item.get_list_item_str(
        quantity=2, leading_dash=True) == '- bread (2x)'


def test_item_get_price_str():
    item = Item('bread', 3.25)
    assert item.get_price_str() == '$3.25'
    assert item.get_price_str(hide_price=True) == '$?.??'
    assert item.get_price_str(order=3) == '$0003.25'


def test_item_repr():
    item = Item('bread', 3.25)
    assert repr(item) == 'Item(bread, 3.25)'

def test_item_eq():
    item1 = Item('bread', 3.25)
    item2 = Item('bread', 3.25)
    item3 = Item('butter', 4.10)
    assert item1 == item2
    assert item1 != item3

def test_itempool_valid_init():
    items = {
        'bread': Item('bread', 3.25),
        'milk': Item('milk', 2.50),
        'eggs': Item('eggs', 1.75)
    }
    item_pool = ItemPool(items)
    assert item_pool.items == items

def test_itempool_empty_init():
    item_pool = ItemPool()
    assert item_pool.items == {}

def test_itempool_invalid_init():
    with pytest.raises(InvalidItemPoolError):
        ItemPool(123)
    with pytest.raises(InvalidItemPoolError):
        ItemPool({1: Item('item1', 10.0), 2: Item('item2', 20.0)})
    with pytest.raises(InvalidItemPoolError):
        ItemPool({'item1': 10.0, 'item2': 'item2'})

def test_itempool_add_item_valid():
    item_pool = ItemPool()
    item1 = Item('bread', 3.25)
    item_pool.add_item(item1)
    assert item_pool.items == {'bread': item1}

    item2 = Item('milk', 2.50)
    item_pool.add_item(item2)
    assert item_pool.items == {'bread': item1, 'milk': item2}

def test_itempool_add_item_invalid():
    item_pool = ItemPool()
    with pytest.raises(InvalidItemPoolError):
        item_pool.add_item('invalid_item')
    item1 = Item('bread', 3.25)
    item2 = Item('bread', 2.50)
    item_pool.add_item(item1)
    with pytest.raises(DuplicateItemError):
        item_pool.add_item(item2)

def test_itempool_remove_item_valid():
    item_pool = ItemPool()
    item1 = Item('bread', 3.25)
    item2 = Item('milk', 2.50)
    item_pool.add_item(item1)
    item_pool.add_item(item2)

    item_pool.remove_item('bread')
    assert item_pool.items == {'milk': item2}

def test_itempool_remove_item_invalid():
    item_pool = ItemPool()
    with pytest.raises(NonExistingItemError):
        item_pool.remove_item('bread')

def test_itempool_get_size():
    item_pool = ItemPool()
    item1 = Item('bread', 3.25)
    item2 = Item('milk', 2.50)
    item_pool.add_item(item1)
    item_pool.add_item(item2)
    assert item_pool.get_size() == 2

def test_itempool_sample_items():
    item_pool = ItemPool()
    item1 = Item('bread', 3.25)
    item2 = Item('milk', 2.50)
    item_pool.add_item(item1)
    item_pool.add_item(item2)
    sample = item_pool.sample_items(1)
    assert len(sample) == 1
    assert sample[0] in [item1, item2]

def test_itempool_repr():
    item_pool = ItemPool()
    item1 = Item('bread', 3.25)
    item2 = Item('milk', 2.50)
    item_pool.add_item(item1)
    item_pool.add_item(item2)
    assert repr(item_pool) == "ItemPool({'bread': Item(bread, 3.25), 'milk': Item(milk, 2.5)})"

def test_itempool_eq():
    item_pool1 = ItemPool()
    item_pool2 = ItemPool()
    item1 = Item('bread', 3.25)
    item2 = Item('milk', 2.50)
    item_pool1.add_item(item1)
    item_pool1.add_item(item2)
    item_pool2.add_item(item1)
    item_pool2.add_item(item2)
    assert item_pool1 == item_pool2

def test_invalid_item_name_error_init_non_string():
    non_string_input = 123  
    with pytest.raises(InvalidItemNameError) as exc_info:
        raise InvalidItemNameError(non_string_input)
    exc = exc_info.value
    expected_error_message = f'Item name must be a string (not {type(non_string_input)}).'
    assert str(exc) == expected_error_message

def test_invalid_shopping_list_size_error_init():
    with pytest.raises(InvalidShoppingListSizeError) as exc_info:
        raise InvalidShoppingListSizeError()
    exc = exc_info.value
    expected_error_message = 'Invalid List Size!'
    assert str(exc) == expected_error_message

def test_process_answer():
    def process_answer(cmd, correct_answer):
        try:
            answer = round(float(cmd), 2)
            if answer == correct_answer:
                return 'Correct!'
            else:
                return (
                    f'Not Correct! (Expected ${correct_answer:.02f})\n'
                    f'You answered ${answer:.02f}.'
                )
        except ValueError:
            return "The provided answer is not a valid number!"
    result = process_answer("10.50", 10.50)
    assert result == 'Correct!'
    result = process_answer("7.25", 10.50)
    expected_message = (
        'Not Correct! (Expected $10.50)\n'
        'You answered $7.25.'
    )
    assert result == expected_message
    result = process_answer("invalid", 10.50)
    assert result == "The provided answer is not a valid number!"

def test_init_attributes_with_values():
    shopping_list = ["item1", "item2", "item3"]
    items = {"item1": 10, "item2": 5, "item3": 7}
    instance = AppEngine(shopping_list, items)
    assert instance.items == {"item1": 10, "item2": 5, "item3": 7}
    assert instance.shopping_list == ["item1", "item2", "item3"]
    assert instance.continue_execution is True
    assert instance.message is None
    assert instance.correct_answer is None
    assert instance.status is None

def test_init_attributes_defaults():
    instance = AppEngine()
    assert instance.items is None
    assert instance.shopping_list is None
    assert instance.continue_execution is True
    assert instance.message is None
    assert instance.correct_answer is None
    assert instance.status is None

def test_process_answer_correct():
    instance = AppEngine()
    instance.correct_answer = 13.0
    cmd = "13"
    instance.process_answer(cmd)
    assert instance.message == "Correct!"

def test_process_answer_incorrect():
    instance = AppEngine()
    instance.correct_answer = 12.3
    cmd = "4.56"
    instance.process_answer(cmd)
    assert instance.message == 'Not Correct! (Expected $12.30)\nYou answered $4.56.'

def test_process_answer_invalid_input():
    instance = AppEngine()
    instance.correct_answer = 13
    cmd = "not_a_number"
    instance.process_answer(cmd)
    assert instance.message is None

def test_process_add_item_valid():
    instance = AppEngine()
    instance.items = ItemPool()
    cmd = "add item_name: 12.34"
    instance.process_add_item(cmd)
    assert instance.message == 'Item(item_name, 12.34) added successfully.'

def test_process_add_item_invalid_format():
    app_engine = AppEngine(items={})
    cmd = "add invalid_item_format"
    result_message = app_engine.process_add_item(cmd)
    assert result_message == 'Cannot add "invalid_item_format".\nUsage: add <item_name>: <item_price>'

def test_process_add_item_empty_name():
    app_engine = AppEngine(items={})
    cmd = "add : 10.99"
    result_message = app_engine.process_add_item(cmd)
    assert result_message == 'Item name string cannot be empty.'

"""def test_process_add_item_success():
    app_engine = AppEngine(itmes={})
    cmd = "add Item1: 10.99"
    result_message = app_engine.process_add_item(cmd)
    assert result_message == 'Item(name=Item1, price=10.99) added successfully.'"""

def test_process_add_item_invalid_price():
    app_engine = AppEngine(items={})
    cmd = "add Item1: not_a_number"
    result_message = app_engine.process_add_item(cmd)
    assert result_message == 'could not convert string to float: "not_a_number"'

def test_process_del_item_success():
    item_name = "Item1"
    items = ItemPool({item_name: Item(item_name, 10.99)})
    app_engine = AppEngine(items=items)
    cmd = f"del {item_name}"
    app_engine.process_del_item(cmd)
    assert item_name not in app_engine.items.items

def test_process_del_item_non_existing():
    item_name = "Test"
    app_engine = AppEngine(items=ItemPool())
    cmd = f"del {item_name}"
    with pytest.raises(NonExistingItemError):
        app_engine.process_del_item(cmd)

def test_shopping_list_init_with_defaults():
    shopping_list = ShoppingList()
    assert shopping_list.list == []

def test_refresh_updates_list():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    assert len(shopping_list.list) == 0
    shopping_list.refresh(item_pool, size=2, quantities=[2, 3])
    assert len(shopping_list.list) > 0

def test_refresh_none_method():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    assert shopping_list.list == []  # Check if the list is initially an empty list
    # Don't call refresh in this test, instead just pass None as item_pool
    shopping_list.refresh(item_pool, size=2, quantities=[2, 3])
    # Check if the list is not an empty list after manual refresh
    assert shopping_list.list != [] 


def test_refresh_sets_random_size():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    pool_size = item_pool.get_size()
    shopping_list.refresh(item_pool, size=None)
    assert 0 <= len(shopping_list.list) <= pool_size
    shopping_list.refresh(item_pool, size=None)

    assert len(shopping_list.list) != pool_size

def test_refresh_raises_value_error_invalid_size():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.refresh(item_pool, size="invalid_size")

    with pytest.raises(ValueError):
        shopping_list.refresh(item_pool, size=-5)

def test_refresh_raises_invalid_shopping_list_size_error():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    pool_size = item_pool.get_size()

    with pytest.raises(InvalidShoppingListSizeError):
        shopping_list.refresh(item_pool, size=pool_size + 1)

def test_refresh_raises_value_error_invalid_quantities():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.refresh(item_pool, quantities=5)
    
    with pytest.raises(ValueError):
        shopping_list.refresh(item_pool, quantities="invalid_quantities")

def test_refresh_raises_value_error_invalid_quantity_elements():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.refresh(item_pool, quantities=[1, "invalid_element", 3])
    
    with pytest.raises(ValueError):
        shopping_list.refresh(item_pool, quantities=[1, -5, 3])

def test_quantities_smaller_than_size():
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items = {"Item1": item1, "Item2": item2}
    item_pool = ItemPool(items=items)
    pool_size = item_pool.get_size()
    shopping_list = ShoppingList()
    shopping_list.refresh(item_pool, size=pool_size, quantities=[2])
    expected_quantities = [2, 1, 1]
    assert shopping_list.list == list(zip(item_pool.sample_items(2), expected_quantities))

def test_quantities_larger_than_size():
    item1 = Item("Item1", 10)
    items = {"Item1": item1}
    item_pool = ItemPool(items=items)
    pool_size = item_pool.get_size()
    shopping_list = ShoppingList()
    shopping_list.refresh(item_pool, size=pool_size, quantities=[2, 3])
    expected_quantities = [2, 3, 1]
    assert shopping_list.list == list(zip(item_pool.sample_items(3), expected_quantities))

def test_get_total_price(self):
    # Create a list of items and quantities
    item1 = Item("Item1", 10)
    item2 = Item("Item2", 20)
    items_list = [item1, item2]
    quantities = [2, 3]

    # Create a ShoppingList object and refresh it with the items and quantities
    shopping_list = ShoppingList()
    shopping_list.refresh(item_pool=None, quantities=quantities)
    shopping_list.list = list(zip(items_list, quantities))

    # Calculate the expected total price manually
    expected_total_price = round((item1.price * quantities[0]) + (item2.price * quantities[1]), 2)

    # Compare the expected total price with the result from the get_total_price method
    assert shopping_list.get_total_price() == expected_total_price

