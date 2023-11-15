from datetime import datetime
from collections import defaultdict
from data import personnel, stock
from loader import Loader
import colors as colors
from typing import List

#from datetime import datetime
from loader import Loader
import colors 

class User:
    def __init__(self, user_name="Anonymous", password=None):
        self._name = user_name
        self.is_authenticated = False

    def authenticate(self, password=None):
        """
        Authenticate the user.

        Args:
            password (str): The entered password.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        self.is_authenticated = False  # Placeholder for actual authentication logic
        return self.is_authenticated

    def is_named(self, name):
        """
        Check if the user is named with the given name.

        Args:
            name (str): The name to compare.

        Returns:
            bool: True if the user is named as provided, False otherwise.
        """
        return name == self._name

    def greet(self):
        """
        Display a greeting message for the user.
        """
        print(f"{colors.ANSI_PURPLE}{' ' * 30}Hello, {self._name}!\n{' ' * 20}Welcome to our Warehouse Database.\n{' ' * 16}If you don't find what you are looking for,\n{' ' * 14}Please ask one of our staff members to assist you.{colors.ANSI_RESET}")

    def bye(self, actions):
        """
        Display a farewell message for the user.

        Args:
            actions (list): List of actions taken during the session.
        """
        print(f"{colors.ANSI_BLUE}\n{'-' * 75}  Thank you for your visit, {self._name}.  {'-' * 75}{colors.ANSI_RESET}\n")

        if len(actions) == 0:
            print(f"\n{colors.ANSI_RESET}{' ' * 20}You have not done any action in specific!")
        else:
            print(f"{colors.ANSI_RESET}\nSummary of action this session:")
            for id, stmt in enumerate(actions):
                print(" " * 20, id + 1, ".", stmt)


class Employee(User):
    def __init__(self, user_name, password, head_of=None):
        super().__init__(user_name, password)
        self.__password = password
        self.head_of = []
        if head_of:
            self.head_of = [Employee(**employee) for employee in head_of]

    def authenticate(self, password):
        return password == self.__password

    def order(self, item, amount):
        print(f"User {self._name} ordered {amount} {item}")

    def greet(self):
        print(f"Hello, {self._name}!\nIf you experience a problem with the system, \nplease contact technical support.")

    def bye(self, actions):
        super().bye(actions)
        if actions:
            print("\nSummary of actions this session:")
            for id, stmt in enumerate(actions):
                print(" " * 20, id + 1, ".", stmt)


class Item:
    def __init__(self, state=None, category=None, date_of_stock=None, warehouse=None):
        self.state = state
        self.category = category
        self.date_of_stock = date_of_stock
        self.warehouse = warehouse

    def __str__(self):
        """
        Return a string representing the item.

        Returns:
            str: The string representation of the item.
        """
        if self.state is not None and self.category is not None:
            return f"{self.state} {self.category}"
        return ""


class Warehouse:
    def __init__(self, warehouse_id=None):
        self.warehouse_id = warehouse_id
        self.stock = []

    def occupancy(self):
        """
        Return the total amount of items currently in the warehouse.

        Returns:
            int: The total amount of items.
        """
        return len(self.stock)

    def add_item(self, item):
        """
        Add an item to the warehouse stock.

        Args:
            item: The item to be added.
        """
        self.stock.append(item)

    def search(self, search_item):
        """
        Search for an item in the warehouse stock.

        Args:
            search_item (str): The item to search for.

        Returns:
            list: List of tuples containing items and their dates of stock.
        """
        search_item_list = []

        for item in self.stock:
            if str(item).lower() == search_item.lower():
                if isinstance(item, Item):  # Check if item is an instance of the Item class
                    search_item_list.append((item, item.date_of_stock))
                else:
                    # If item is a string representation, create a dummy Item without date
                    search_item_list.append((Item(), None))

        return search_item_list


    def __str__(self):
        """
        Return a string representing the warehouse.

        Returns:
            str: The string representation of the warehouse.
        """
        return f"Warehouse {self.warehouse_id}"

    def browse_by_category(self):
        """
        Browse items in the warehouse by category.

        Returns:
            dict: A dictionary mapping category IDs to category names.
        """
        list_item_category = []
        stock = Loader(model="stock")
        for warehouse in stock:
            for item in warehouse.stock:
                list_item_category.append(item.category)
        dict_item_category_count = {i: list_item_category.count(i) for i in list_item_category}
        dict_id_category = {}
        print()
        for id, (key, value) in enumerate(dict_item_category_count.items()):
            dict_id_category[id + 1] = key
            print(f"{' ' * 20}{colors.ANSI_PURPLE}{id + 1} {key} ({value}){colors.ANSI_RESET}")
        print()
        return dict_id_category



