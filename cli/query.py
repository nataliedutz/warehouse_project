"""
CLI for Warehouse Management System.

This module provides a Command Line Interface (CLI) for interacting
with a Warehouse Management System. It includes commands for user
authentication, checking stock levels,
and performing various warehouse operations.
"""
import os
import json
from datetime import datetime
from typing import List, Tuple

import colors
from classes import Employee, Item, User, Warehouse
from data import stock
from loader import Loader

personnel_loader = Loader(model="personnel")  # List of Employee objects
stock_loader = Loader(model="stock")  # List of Warehouse objects
stock = stock_loader.objects

class AuthenticationError(Exception):
    """
    Exception raised for authentication errors during user login.

    This exception can be raised when there is
    an issue with user authentication.
    """

    pass


def get_user_name() -> str:
    """
    Get the username from the user.

    Returns:
        str: The entered username.
    """
    username = input(
        f"\n{colors.ANSI_BLUE}Please enter the username: {colors.ANSI_YELLOW}"
    )
    return username.capitalize()


def validate_user(personnel, password, user_name) -> Employee:
    """
    Validate the user and return the authorized employee.

    Args:
        personnel: List of Employee objects.
        password (str): The entered password.
        user_name (str): The entered username.

    Returns:
        Employee: The authorized employee.
    """
    for staff in personnel:
        if staff.is_named(user_name):
            if staff.authenticate(password):
                staff.is_authenticated = True
                print(f"{colors.ANSI_RESET}{'-' * 150}")
                staff.greet()
                return staff

    # If no matching user is found, return None or raise an exception
    raise AuthenticationError("Authentication failed")


def user_authentication(user_name, user_input=input):
    """
    Authenticate the user and return either User or Employee object.

    Args:
        user_name (str): The entered username.
        user_input: Function to use for receiving user input
        (for testing purposes).

    Returns:
        Union[User, Employee]: The authenticated user.
    """
    entry_mode = user_input(
        f"\n{colors.ANSI_RESET}ENTRY MODE:\n"
        f"{'*' * 20} {colors.ANSI_BLUE}1.GUEST {colors.ANSI_RESET}{'*' * 20}\n"
        f"{'*' * 20} {colors.ANSI_BLUE}2.EMPLOYEE {colors.ANSI_RESET}"
        f"{'*' * 20}\n\n Enter the number associated with the entry mode: "
    )

    if entry_mode == "1":
        user = User(user_name)
        print(f"{'-' * 150}")
        user.greet()
        return user
    elif entry_mode == "2":
        password = user_input(f"Please enter your password: {colors.ANSI_YELLOW}")
        authorized_employee = validate_user(personnel_loader, password, user_name)
        if not authorized_employee:
            user_decision = user_input(
                f"{colors.ANSI_RED}Incorrect password for "
                f"the given username.\n"
                f"Do you want to try entering the password again? "
                f"(y/n): {colors.ANSI_YELLOW}"
            )
            if user_decision.lower() == "y":
                start_shopping()
        return authorized_employee
    else:
        print(
            f"{colors.ANSI_RED}Invalid input, "
            f"please select a correct option.{colors.ANSI_RESET}"
        )


def search_item_in_stock(stock, search_item) -> Tuple[List[str], dict, str]:
    """
    Search for an item in the warehouse stock.

    Args:
        stock (List[dict]): The list of items in stock.
        search_item (str): The item to search for.

    Returns:
        Tuple: A tuple containing the locations where the item is found,
            a dictionary with the count of the item in each warehouse,
            and the searched item.
    """
    location = []
    item_count_in_warehouse_dict = {}

    for item in stock:
        if item.get("category", "").lower() == search_item.lower():
            warehouse_id = item.get("warehouse", "")
            location.append(f"{item.get('state', '')} - Warehouse {warehouse_id}")
            if warehouse_id in item_count_in_warehouse_dict:
                item_count_in_warehouse_dict[warehouse_id] += 1
            else:
                item_count_in_warehouse_dict[warehouse_id] = 1

    return location, item_count_in_warehouse_dict, search_item


def search_and_order_item(stock) -> Tuple[List[str], dict, str]:
    """
    Search for an item in the warehouse stock and provide options for ordering.

    Args:
        stock (List[dict]): The list of items in stock.

    Returns:
        Tuple: A tuple containing the locations where the item is found,
            a dictionary with the count of the item in each warehouse,
            and the searched item.
    """
    search_item = input(
        f"\n{colors.ANSI_RESET}Enter the item that you are searching: "
        f"{colors.ANSI_YELLOW}"
    ).lower()
    location = []
    item_count_in_warehouse_dict = {}

    for warehouse in stock:
        for item in warehouse.stock:
            if isinstance(item, Item):
                item_name = (
                    f"{item.state.lower()} " f"{item.category.lower()}"
                )
                if search_item in item_name:
                    
                    warehouse_id = warehouse.warehouse_id
                    location.append(
                        f"{item.state} {item.category.lower()}"
                        f" - Warehouse {warehouse_id}"
                    )
                    if warehouse_id in item_count_in_warehouse_dict:
                        item_count_in_warehouse_dict[warehouse_id] += 1
                    else:
                        item_count_in_warehouse_dict[warehouse_id] = 1

    return location, item_count_in_warehouse_dict, search_item

def process_search_and_order(actions, authorized_employee):
    """
    Search for an item, display availability, and provide options for ordering.

    Args:
        actions (List[str]): List of actions taken during the session.
        authorized_employee (Employee): The authorized employee.

    Returns:
        None
    """
    location, item_count_in_warehouse_dict, search_item = search_and_order_item(stock)
    if len(location) > 0:
        print(f"\n{colors.ANSI_RESET}Quantity Availability: {len(location)}\n")
        print("Location:")
        for i in location:
            print(f"{' ' * 15}{colors.ANSI_BLUE}{i}{colors.ANSI_RESET}")
        for warehouse, count in item_count_in_warehouse_dict.items():
            if max(item_count_in_warehouse_dict.values()) == count:
                print(
                    f"\nMaximum availability: {colors.ANSI_BLUE}{count} "
                    f"in {warehouse}{colors.ANSI_RESET}\n"
                )
        print("." * 120)

        if isinstance(authorized_employee, Employee):
            place_order = input(
                f"Do you want to place an order for the item {search_item}?"
                f" (y/n) - {colors.ANSI_YELLOW}"
            )
            if place_order.lower() == "y":
                placing_order(
                    search_item, sum(item_count_in_warehouse_dict.values()), actions
                )

    else:
        print(f"{colors.ANSI_RED}\nNot in stock")

    actions.append(f"Searched for {search_item}")
    continue_session = input(
        f"\n{'*' * 20}  {colors.ANSI_BLUE}Do you want "
        f"to continue with another operation? "
        f"(y/n){colors.ANSI_RESET}  {'*' * 20}   -   {colors.ANSI_YELLOW}"
    )
    if continue_session in ("y", "Y"):
        run(actions, authorized_employee)


def validate_order_quantity(search_item):
    """Validate and return the order quantity entered by the user."""
    try:
        return int(input(f"{colors.ANSI_BLUE}\nHow much quantity of "
                         f"{search_item} do you want to order? "
                         f"{colors.ANSI_YELLOW}"))
    except ValueError:
        print(f"{colors.ANSI_RED}Invalid input! Please enter a valid integer.{colors.ANSI_RESET}")
        return None

def placing_order(search_item, total_item_count_in_warehouses, actions):
    order_quantity = validate_order_quantity(search_item)

    if order_quantity is not None:
        if order_quantity <= total_item_count_in_warehouses:
            for warehouse in stock_loader:
                for item in warehouse.stock:
                    if isinstance(item, Item) and item.category.lower() == search_item.lower():
                        warehouse.stock.remove(item)
                        # Update the order quantity
                        order_quantity -= 1  

                        if order_quantity == 0:
                            break

            # save_stock_data_to_json(stock_loader.objects)
            print(f"{colors.ANSI_RESET}{'%' * 150}")
            print(f"\n{' ' * 50}{colors.ANSI_GREEN}Order placed: "
                  f"{order_quantity} * {search_item}{colors.ANSI_RESET}\n")
            print(f"{'%' * 150}")
            actions.append(f"Ordered {order_quantity} of {search_item}")

        else:
            print(f"{colors.ANSI_RESET}{'-' * 100}")
            print(f"{colors.ANSI_RED}There are not this many available. "
                  f"The maximum quantity that can be ordered is "
                  f"{colors.ANSI_RESET} {total_item_count_in_warehouses}.")
            print("-" * 100)
            ask_order_max = input(
                f"{colors.ANSI_BLUE}Do you want to order the {search_item} "
                f"in maximum quantity of {total_item_count_in_warehouses}? "
                f"(y/n) -  {colors.ANSI_YELLOW}")

            if ask_order_max.lower() == "y":
                for warehouse in stock_loader:
                    for item in warehouse.stock:
                        if isinstance(item, Item) and item.category.lower() == search_item.lower():
                            warehouse.stock.remove(item)
                            # Update the order quantity
                            order_quantity -= 1
                
                            if order_quantity == 0:
                                break

                # save_stock_data_to_json(stock_loader.objects)            
                print(f"{colors.ANSI_RESET}{'%' * 150}")
                print(f"\n{' ' * 50}{colors.ANSI_GREEN}Order placed: "
                      f"{total_item_count_in_warehouses} * "
                      f"{search_item}{colors.ANSI_RESET}\n")
                print(f"{'%' * 150}")
                actions.append(f"Ordered {total_item_count_in_warehouses} of {search_item}")

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
STOCK_JSON_PATH = os.path.join(BASE_DIR, "data", "stock.json")

# def save_stock_data_to_json(stock):
#     BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#     stock_json = os.path.join(BASE_DIR, "data/stock.json")

#     stock_data = {"stock": []}

#     for warehouse in stock:
#         for item in warehouse.stock:
#             item_dict = {
#                 "category": item.category,
#                 "state": item.state,
#                 "quantity": item.quantity,
#                 "warehouse": warehouse.warehouse_id,
#             }
#             stock_data["stock"].append(item_dict)

#     with open(stock_json, "w+") as json_file:
#         json_file.seek(0)
#         json_file.write(json.dumps(stock_data))


# def save_stock_data_to_json():
#     BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#     stock_json=os.path.join(BASE_DIR, "data/stock.json")
#     if os.path.isfile(stock_json):
#         with open(stock_json, "w+") as jsonFile:
#             jsonFile.seek(0)
#             jsonFile.write(json.dumps(stock))

# def save_stock_data_to_json(stock):
#     BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#     stock_json = os.path.join(BASE_DIR, "data/stock.json")

#     stock_data = {"stock": []}

#     for warehouse in stock:
#         for item in warehouse.stock:
#             item_dict = {
#                 "category": item.category,
#                 "state": item.state,
#                 "quantity": item.quantity,
#                 "warehouse": warehouse.warehouse_id,
#             }
#             stock_data["stock"].append(item_dict)

#     with open(stock_json, "w+") as json_file:
#         json_file.seek(0)
#         json_file.write(json.dumps(stock_data))


def category_selection(actions, authorized_employee):
    """Browse items by category."""
    category_select = Warehouse()
    dict_id_category = category_select.browse_by_category()
    select_category = input(f"Type the category number to browse: {colors.ANSI_YELLOW}")
    print()

    category_name = None

    for key_id, value_id in dict_id_category.items():
        if key_id == int(select_category):
            category_name = value_id
            count_items_by_category = 0

            for warehouse in stock_loader:
                for item in warehouse.stock:
                    if value_id == item.category:
                        count_items_by_category += 1
                        print(
                            f"{' ' * 25}{colors.ANSI_GREEN}{item.state} "
                            f"{item.category}, {warehouse}"
                        )

    if int(select_category) not in dict_id_category.keys():
        print(f"{colors.ANSI_RED}Invalid input!{colors.ANSI_RESET}")

    if category_name is not None:
        print(f"{colors.ANSI_RESET}{'.' * 120}")
        print(f"\nTotal items in this category are: {count_items_by_category}\n")
        print("." * 120)
        actions.append(f"Browsed the category {category_name}")

    continue_session = input(
        f"\n{'*' * 20}  {colors.ANSI_BLUE}Do you want to continue "
        f"with another operation? (y/n){colors.ANSI_RESET}"
        f"  {'*' * 20}   -   {colors.ANSI_YELLOW}"
    )

    if continue_session.lower() == "y":
        run(actions, authorized_employee)


def select_operation(user_input=input):
    """
    Display the main menu and return the user's selection.

    param user_input:
        Function to use for receiving user input (for testing purposes).
    return: User's menu selection.
    """
    try:
        print("Main Menu:")
        print("1. List items by warehouse")
        print("2. Search an item and place an order")
        print("3. Browse by category")
        print("4. Quit")

        user_selection = user_input("Enter your selection (1-4): ")

        # Attempt to convert the user input to an integer
        selection = int(user_selection)

        if 1 <= selection <= 4:
            return str(selection)
        else:
            print(f"{colors.ANSI_RED}Invalid input! Please enter a number between 1 and 4.{colors.ANSI_RESET}")
            return select_operation(user_input=user_input)
    except ValueError:
        print(f"{colors.ANSI_RED}Invalid input! Please enter a valid number.{colors.ANSI_RESET}")
        return select_operation(user_input=user_input)

def item_list_by_warehouse():
    """List items by warehouse."""
    total_items = 0  # Initialize total_items counter
    warehouses = []

    for warehouse in stock_loader:
        # Create a list to store item info in the warehouse
        warehouse_items = []

        for item in warehouse.stock:
            if isinstance(item, Item):
                item_name = f"{item.state.lower()} {item.category.lower()}"
                warehouse_items.append(item_name)

        # Print warehouse and item info
        print(f"{colors.ANSI_BLUE}Warehouse: {warehouse} {colors.ANSI_RESET}")

        for item_name in warehouse_items:
            print(f"  {colors.ANSI_BLUE}{item_name}{colors.ANSI_RESET}")

        print(
            f"{colors.ANSI_BLUE}Total items in {warehouse}: "
            f"{len(warehouse.stock)} {colors.ANSI_RESET} "
        )
        print(f"{'-' * 100}")

        total_items += len(warehouse.stock)
        # Append warehouse to the list
        warehouses.append(warehouse)

    print(f"Total items in all warehouses: {total_items}")
    return total_items, warehouses


def run(actions, authorized_employee=None, user_input=input):
    """Run the main program."""
    total_items = 0  # Initialize total_items counter

    while True:
        menu_selection = select_operation(user_input=user_input)
        search_item = None
        warehouse = None

        # If the user selects operation 1
        if menu_selection == "1":
            # Get the result of item_list_by_warehouse()
            total_items, warehouses = item_list_by_warehouse()
            actions.append(
                f"Listed {total_items} items from " f"{len(warehouses)} Warehouses"
            )

        # Else, if user picks operation 2
        elif menu_selection == "2":
            search_result = search_and_order_item(stock)
            location, item_count_in_warehouse_dict, search_item = search_result
            # Continue with the rest of the operations using the obtained data
            if len(location) > 0:
                print(
                    f"\n{colors.ANSI_BLUE}Quantity Availability: " f"{len(location)}\n"
                )
                print("Location:")
                for i in location:
                    print(f"{' ' * 15}{colors.ANSI_BLUE}{i}{colors.ANSI_RESET}")
                for warehouse, count in item_count_in_warehouse_dict.items():
                    if max(item_count_in_warehouse_dict.values()) == count:
                        print(
                            f"\nMaximum availability: "
                            f"{colors.ANSI_BLUE}{count} "
                            f"in {warehouse}{colors.ANSI_RESET}\n"
                        )
                print("." * 120)

                if isinstance(authorized_employee, Employee):
                    place_order = input(
                        f"Do you want to place an order for the item "
                        f"{search_item}? (y/n) - {colors.ANSI_YELLOW}"
                    )
                    if place_order.lower() in ("y", "Y"):
                        placing_order(
                            search_item,
                            sum(item_count_in_warehouse_dict.values()),
                            actions,
                        )
            else:
                search_item = ""
                print(f"{colors.ANSI_RED}\nNot in stock")

            if search_item is not None:
                actions.append(f"Searched for {search_item}")
            continue_session = input(
                f"\n{'*' * 20}  {colors.ANSI_BLUE}Do you want to continue "
                f"with another operation? (y/n){colors.ANSI_RESET}  "
                f"{'*' * 20}   -   {colors.ANSI_YELLOW}"
            )
            if continue_session.lower() != "y":
                break

        # Else, if user picks operation 3
        elif menu_selection == "3":
            category_selection(actions, authorized_employee)

        # Else, if user selects operation 4
        elif menu_selection == "4":
            break

        else:
            print("*" * 150)
            print(
                f"{colors.ANSI_RED}Invalid input, please enter a number "
                f"between 1 and 4 for a valid operation{colors.ANSI_RESET}"
            )
            print("*" * 150)


def start_shopping():
    """Starts the shopping application."""
    actions = []
    username = get_user_name()
    authorized_employee = user_authentication(username)

    # Determine the log file path based on the authorized_employee type
    if isinstance(authorized_employee, User):
        log_file = "log/user_log.txt"
    elif isinstance(authorized_employee, Employee):
        log_file = "log/employee_log.txt"
    # Handle the case where neither User nor Employee is authenticated
    else:
        print("Unexpected authorized_employee type:", type(authorized_employee))
        return

    # Create the log directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    run(actions, authorized_employee, user_input=input)

    print()

    actions = [i + " " + "\n" for i in actions]
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if isinstance(authorized_employee, Employee):
        authorized_employee.bye(actions)
        employee_log_path = os.path.join(BASE_DIR, "log/employee_log.txt")
        with open(employee_log_path, 'a') as file1:
            for action in actions:
                log_entry = f"{username}. {action.strip()}. {timestamp}.\n"
                file1.write(log_entry)

    else:
        authorized_employee.bye(actions)
        user_log_path = os.path.join(BASE_DIR, "log/user_log.txt")
        with open(user_log_path, 'a') as file1:
            for action in actions:
                log_entry = f"{username}. {action.strip()}. {timestamp}.\n"
                file1.write(log_entry)


if __name__=="__main__":
    start_shopping()
