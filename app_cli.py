"Module Providing Main Command Line Functions"

import random
from core.shoppinglist import ShoppingList
from core.appengine import AppEngine
from core.items import Item, ItemPool


class AppCLI:
    """Command-line interface for the shopping list application."""

    def __init__(self, shopping_list=None, items=None):
        self.app_engine = AppEngine(shopping_list, items)

    def run(self):
        "Function to Run Command Inputs"
        while True:
            prompt = 'What would you like to do? '
            if self.app_engine.correct_answer is not None:
                prompt = 'What amount should replace the questionmarks? $'
            cmd = input(prompt)
            self.execute_command(cmd)
            print(f'{self.app_engine.message}\n')
            self.app_engine.message = None

            if not self.app_engine.continue_execution:
                break

    def execute_command(self, cmd):
        "Function to Execute Commands Base off Input"
        if self.app_engine.correct_answer is not None:
            self.app_engine.process_answer(cmd)
        elif cmd in ('q', 'quit'):
            self.app_engine.continue_execution = False
            self.app_engine.message = 'Have a nice day!'
        elif cmd in ('a', 'ask'):
            self.process_ask()
        elif cmd in ('l', 'list'):
            self.app_engine.shopping_list.refresh(
                item_pool=self.app_engine.items
                )
            self.app_engine.message = (
                f'Shopping list with {len(self.app_engine.shopping_list)} '
                'items has been created.'
            )
        elif cmd.startswith('show'):
            self.process_show(cmd)
        elif cmd.startswith('add'):
            self.app_engine.process_add_item(cmd)
        elif cmd.startswith('del'):
            self.app_engine.process_del_item(cmd)
        else:
            self.app_engine.message = f'"{cmd}" is not a valid command.'

    def process_ask(self):
        """Function to ask a question or show the shopping list"""
        random_index = random.randint(
            0, len(self.app_engine.shopping_list.list)
            )
        self.app_engine.message = self.show_list(mask_index=random_index)
        if random_index < len(self.app_engine.shopping_list.list):
            self.app_engine.correct_answer = (
                self.app_engine.shopping_list.get_item_price(random_index)
                )
        else:
            self.app_engine.correct_answer = (
                self.app_engine.shopping_list.get_total_price()
                )

    def process_show(self, cmd):
        "Function to show either all items or shoppping list"
        what = cmd[5:].strip()
        if what == 'items':
            self.app_engine.message = self.show_items()
        elif what == 'list':
            self.app_engine.message = self.show_list()
        else:
            self.app_engine.message = f'Cannot show {what}.\n'
            self.app_engine.message += 'Usage: show list|items'

    def show_items(self):
        "Function to show all items"
        max_name, max_price = 0, 0
        for item in self.app_engine.items.items.values():
            max_name = max(max_name, len(item.name))
            max_price = max(max_price, len(item.get_price_str()))
        out = 'ITEMS\n'
        for item_name in sorted(self.app_engine.items.items.keys()):
            item = self.app_engine.items.items[item_name]
            padding = max_name - len(item.name)
            out += (
                item.get_list_item_str() + ' ...' +
                ('.' * padding) + ' ' + item.get_price_str() + '\n'
            )
        return out

    def show_list(self, mask_index=None):
        "Function to show or generate list"
        total = Item('TOTAL', self.app_engine.shopping_list.get_total_price())
        max_name_len = len(total.name) - 4
        max_order = total.get_order()

        for item, _ in self.app_engine.shopping_list.list:
            max_name_len = max(max_name_len, len(item.name))
            max_order = max(max_order, item.get_order())

        out = 'SHOPPING LIST\n'
        for i, (item, quantity) in enumerate(
            self.app_engine.shopping_list.list
        ):
            hide_price = mask_index == i
            padding = max_name_len - len(item.name)

            out += (
                item.get_list_item_str(quantity) + ' ...' +
                ('.' * padding) + ' '
                + item.get_price_str(quantity, hide_price, max_order) + '\n'
            )

        hide_price = mask_index == len(
            self.app_engine.shopping_list.list
        )
        q_len = 7

        total_line = (
            total.get_list_item_str(leading_dash=False))
        total_price = (
            total.get_price_str(order=max_order, hide_price=hide_price))

        padding = max_name_len - len(total.name) + q_len
        hline = ('-' * (len(total_line) +
                        len(total_price) + len(' ... ') + padding) + '\n')

        return (out + hline + total_line +
                ' ...' + ('.' * padding) + ' ' + total_price + '\n')


if __name__ == '__main__':
    # usage example
    item2 = Item('Macbook', 1999.99)
    item3 = Item('Milk', 4.25)
    item4 = Item('Hotel Room', 255.00)
    item5 = Item('Beef Steak', 25.18)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    ip.add_item(item4)
    ip.add_item(item5)
    sp = ShoppingList(size=3, quantities=[3, 2, 4], item_pool=ip)
    app = AppCLI(sp, ip)
    app.run()
