import random
from core.errors import *
from core.shoppinglist import *
from core.items import *

class AppEngine:
    def __init__(self, shoppingList = None, items = None):
        self.items = items
        self.shopping_list = shoppingList
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None
        
    def process_answer(self, cmd):
        answer = round(float(cmd), 2)
        if answer == self.correct_answer:
            self.message = 'Correct!'
        else:
            self.message = f'Not Correct! (Expected ${self.correct_answer:.02f})\nYou answered ${answer:.02f}.'
        self.correct_answer = None

    def process_add_item(self, cmd):
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple)==2:
            name, price = item_tuple
            item = Item(name, float(price))
            self.items.add_item(item)
            self.message = f'{item} added successfully.'
        else:
            self.message = f'Cannot add "{item_str}".\n'
            self.message += 'Usage: add <item_name>: <item_price>'

    def process_del_item(self, cmd):
        item_name = cmd[4: ]
        self.items.remove_item( item_name )
        self.message =f'{item_name} removed successfully.'
