"""
Classes module for user, employee, item, and warehouse representations.

This module defines the User, Employee, Item, and Warehouse classes,
which represent entities in a warehouse management system.
The classes encapsulate functionality related to user authentication,
item management, and warehouse operations.
"""
import colors
from loader import Loader


class MissingArgument(Exception):
    """Custom exception for missing arguments in the classes."""
    def __init__(self, argument, message):
        self.argument = argument
        self.message = message
        super().__init__(f"MissingArgument: {argument} is missing. {message}.")

class User:
    """Class representing a user in the system."""

    def __init__(self, user_name="Anonymous", password=None):
        """Initialize a User instance."""
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
        # Placeholder for actual authentication logic
        self.is_authenticated = False
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
        """Display a greeting message for the user."""
        print(
            f"{colors.ANSI_PURPLE}{' ' * 30}Hello, {self._name}!\n{' ' * 20}"
            f"Welcome to our Warehouse Database.\n{' ' * 16}If you don't find "
            f"what you are looking for,\n{' ' * 14}Please ask one of our "
            f"staff members to assist you.{colors.ANSI_RESET}"
        )

    def bye(self, actions):
        """
        Display a farewell message for the user.

        Args:
            actions (list): List of actions taken during the session.
        """
        print(
            f"{colors.ANSI_BLUE}\n{'-' * 75}  Thank you for "
            f"your visit, {self._name}.  {'-' * 75}{colors.ANSI_RESET}\n"
        )

        if len(actions) == 0:
            print(
                f"\n{colors.ANSI_RESET}{' ' * 20}"
                f"You have not done any action in specific."
            )
        else:
            print(f"{colors.ANSI_RESET}\nSummary of action this session:")
            for id, stmt in enumerate(actions):
                print(" " * 20, id + 1, ".", stmt)


class Employee(User):
    """Class representing an employee in the system."""

    def __init__(self, user_name, password, head_of=None):
        """Initialize an Employee instance."""
        super().__init__(user_name, password)
        self._name = user_name
        self.__password = password
        self.head_of = []
        if head_of:
            self.head_of = [Employee(**employee) for employee in head_of]

         # Check for missing arguments and raise exception
        if not user_name:
            raise MissingArgument("user_name", "An employee cannot be anonymous.")
        if not password:
            raise MissingArgument("password", "An employee requires authentication.")

    def authenticate(self, password):
        """
        Authenticate the employee.

        Args:
            password (str): The entered password.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        return password == self.__password

    def order(self, item, amount):
        """Place an order for an item."""
        print(f"User {self._name} ordered {amount} {item}")

    def greet(self):
        """Display a greeting message for the employee."""
        print(
            f"Hello, {self._name}!\nIf you experience a problem "
            f"with the system, \nplease contact technical support."
        )

    def bye(self, actions):
        """Display a farewell message for the employee."""
        super().bye(actions)


class Item:
    """Class representing an item in the warehouse."""

    def __init__(self, state=None, category=None, date_of_stock=None, warehouse=None):
        """Initialize an Item instance."""
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
    """Class representing a warehouse in the system."""

    def __init__(self, warehouse_id=None):
        """Initialize a Warehouse instance."""
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
                # Check if item is an instance of the Item class
                if isinstance(item, Item):
                    search_item_list.append((item, item.date_of_stock))
                else:
                    # If item is string repr., create pseudo Item without date
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
        dict_item_category_count = {
            i: list_item_category.count(i) for i in list_item_category
        }
        dict_id_category = {}
        print()
        for id, (key, value) in enumerate(dict_item_category_count.items()):
            dict_id_category[id + 1] = key
            print(
                f"{' ' * 20}{colors.ANSI_PURPLE}{id + 1} "
                f"{key} ({value}){colors.ANSI_RESET}"
            )
        print()
        return dict_id_category
