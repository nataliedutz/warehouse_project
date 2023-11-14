from loader import Loader
from data import personnel, stock
from datetime import datetime
from classes import User, Employee, Item, Warehouse
import colors
from typing import List, Tuple
personnel_loader = Loader(model="personnel")  # List of Employee objects
stock_loader = Loader(model="stock")  # List of Warehouse objects

def get_user_name() -> str:
    """
    Get the username from the user.

    Returns:
        str: The entered username.
    """
    username = input(f"\n{colors.ANSI_CYAN}Please enter the username: {colors.ANSI_YELLOW}")
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
        if str(staff) == user_name:
            if staff.authenticate(password):
                staff.is_authenticated = True
                print(f"{colors.ANSI_RESET}{'-' * 150}")
                staff.greet()
                return staff

def user_authentication(user_name) -> User:
    """
    Authenticate the user and return either User or Employee object.

    Args:
        user_name (str): The entered username.

    Returns:
        User: The authenticated user.
    """
    entry_mode = input(f"\n{colors.ANSI_RESET}ENTRY MODE:\n{'*' * 20} {colors.ANSI_YELLOW}1.GUEST    {colors.ANSI_RESET}{'*' * 20}\n{'*' * 20} {colors.ANSI_YELLOW}2.EMPLOYEE {colors.ANSI_RESET}{'*' * 20}\n\nEnter the number associated with the entry mode: ")
    
    if entry_mode == "1":
        user = User(user_name)
        print(f"{'-' * 150}")
        user.greet()
        return user
    elif entry_mode == "2":
        password = input(f"Please enter your password: {colors.ANSI_YELLOW}")
        authorized_employee = validate_user(personnel_loader, password, user_name)
        if not authorized_employee:
            user_decision = input(f"{colors.ANSI_RED}Incorrect password for the given username.\nDo you want to change your username and password? (y/n): {colors.ANSI_YELLOW}")
            if user_decision.lower() == "y":
                start_shopping()
        return authorized_employee
    else:
        print(f"{colors.ANSI_RED}INVALID INPUT, Please select the correct option.{colors.ANSI_RESET}")

def placing_order(search_item, total_item_count_in_warehouses):
    """
    Place an order for a specific item.

    Args:
        search_item (str): The item to be ordered.
        total_item_count_in_warehouses (int): The total count of the item in all warehouses.

    Returns:
        None
    """
    order_quantity = int(input(f"{colors.ANSI_WHITE}\nHow much quantity of {search_item} do you want to order? {colors.ANSI_YELLOW}"))
    
    if order_quantity <= total_item_count_in_warehouses:
        print(f"{colors.ANSI_RESET}{'%' * 150}")
        print(f"\n{' ' * 50}{colors.ANSI_GREEN}Order placed: {order_quantity} * {search_item}{colors.ANSI_RESET}\n")
        print(f"{'%' * 150}")
    else:
        print(f"{colors.ANSI_RESET}{'-' * 100}")
        print(f"{colors.ANSI_RED}There are not this many available. The maximum quantity that can be ordered is {total_item_count_in_warehouses}. {colors.ANSI_RESET}")
        print("-" * 100)
        ask_order_max = input(f"Do you want to order the {search_item} in maximum quantity of {total_item_count_in_warehouses}? (y/n) -  {colors.ANSI_YELLOW} ")
        if ask_order_max.lower() == "y":
            print(f"{colors.ANSI_RESET}{'%' * 150}")
            print(f"\n{' ' * 50}{colors.ANSI_GREEN}Order placed: {total_item_count_in_warehouses} * {search_item}{colors.ANSI_RESET}\n")
            print(f"{'%' * 150}")

def search_item_in_stock(warehouse, search_item) -> Tuple[List[str], dict, str]:
    """
    Search for an item in a specific warehouse's stock.

    Args:
        warehouse (Warehouse): The warehouse to search for the item.
        search_item (str): The item to search for.

    Returns:
        Tuple: A tuple containing the locations where the item is found,
            a dictionary with the count of the item in each warehouse,
            and the searched item.
    """
    location = []
    item_count_in_warehouse_dict = {}

    for item, date_str in warehouse.search(search_item):
        date_format = '%Y-%m-%d %H:%M:%S'
        days = (datetime.now() - datetime.strptime(date_str, date_format)).days
        location.append(f"{str(warehouse)} (in stock for {days} days)")
        if str(warehouse) in item_count_in_warehouse_dict:
            item_count_in_warehouse_dict[str(warehouse)] += 1
        else:
            item_count_in_warehouse_dict[str(warehouse)] = 1

    return location, item_count_in_warehouse_dict, search_item

def search_and_order_item(stock) -> Tuple[List[str], dict, str]:
    """
    Search for an item in the warehouse stock and provide options for ordering.

    Args:
        stock (List[Warehouse]): The list of warehouses with items in stock.

    Returns:
        Tuple: A tuple containing the locations where the item is found,
            a dictionary with the count of the item in each warehouse,
            and the searched item.
    """
    search_item = input(f"\n{colors.ANSI_RESET}Enter the item that you are searching: {colors.ANSI_YELLOW}").lower()
    location = []
    item_count_in_warehouse_dict = {}

    for warehouse in stock:
        search_result = search_item_in_stock(warehouse, search_item)
        location.extend(search_result[0])
        item_count_in_warehouse_dict.update(search_result[1])

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
            print(f"{' ' * 15}{colors.ANSI_PURPLE}{i}{colors.ANSI_RESET}")
        for warehouse, count in item_count_in_warehouse_dict.items():
            if max(item_count_in_warehouse_dict.values()) == count:
                print(f"\nMaximum availability: {colors.ANSI_BLUE}{count} in {warehouse}{colors.ANSI_RESET}\n")
        print("." * 120)

        if isinstance(authorized_employee, Employee):
            place_order = input(f"Do you want to place an order for the item {search_item}? (y/n) - {colors.ANSI_YELLOW}")
            if place_order.lower() in ("y", "Y"):
                placing_order(search_item, sum(item_count_in_warehouse_dict.values()))
    else:
        print(f"{colors.ANSI_RED}\nNot in stock")

    actions.append(f"Searched for {search_item}")
    continue_session = input(
        f"\n{'*' * 20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {'*' * 20}   -   {colors.ANSI_YELLOW}")
    if continue_session in ("y", "Y"):
        run(actions, authorized_employee)


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
                        print(f"{' ' * 25}{colors.ANSI_GREEN}{item.state} {item.category}, {warehouse}")

    if int(select_category) not in dict_id_category.keys():
        print(f"{colors.ANSI_RED}Invalid input!{colors.ANSI_RESET}")

    if category_name is not None:
        print(f"{colors.ANSI_RESET}{'.' * 120}")
        print(f"\nTotal items in this category are: {count_items_by_category}\n")
        print("." * 120)
        actions.append(f"Browsed the category {category_name}")

    continue_session = input(
        f"\n{'*' * 20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {'*' * 20}   -   {colors.ANSI_YELLOW}")

    if continue_session.lower() == "y":
        run(actions, authorized_employee)


def select_operation():
    """Select the operation from the menu."""
    print(f"{colors.ANSI_RESET}\n{'-' * 150}")
    print(f"{colors.ANSI_RESET}The following is the menu, please choose the specific numeric associated with the choice. ")
    print(f"{' ' * 25}1. List items by warehouse")
    print(f"{' ' * 25}2. Search an item and place an order")
    print(f"{' ' * 25}3. Browse by category")
    print(f"{' ' * 25}4. Quit")
    print("-" * 150)

    menu_selection = input(f"\nPlease type the number associated with the operation:  {colors.ANSI_YELLOW}")
    return menu_selection


def item_list_by_warehouse():
    """List items by warehouse."""
    new_item_dict = {}

    for warehouse in stock_loader:
        if warehouse not in new_item_dict:
            new_item_dict[warehouse] = []

            for item in warehouse.stock:
                new_item_dict[warehouse].append(str(item))

    for warehouse, items in new_item_dict.items():
        total_items_in_warehouse = [str(item) for item in items]

        print(f"{colors.ANSI_RED}Items in Warehouse {warehouse}: {colors.ANSI_RESET}")

        for item in total_items_in_warehouse:
            print(item)

        print(f"{colors.ANSI_GREEN}Total items in {warehouse}: {len(total_items_in_warehouse)} {colors.ANSI_RESET} ")
        print(f"{'-' * 100}")

    return new_item_dict


def run(actions, authorized_employee=None):
    """Run the main program."""
    menu_selection = select_operation()

    # If the user selects operation 1
    if menu_selection == "1":
        new_item_dict = item_list_by_warehouse()
        total_items = sum(len(items) for items in new_item_dict.values())
        actions.append(f"Listed {total_items} items from {len(new_item_dict.keys())} Warehouses")

        continue_session = input(
            f"\n{'*' * 20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  "
            f"{'*' * 20}   -   {colors.ANSI_YELLOW}")

        if continue_session.lower() == "y":
            run(actions, authorized_employee)

    # Else, if they pick 2
    elif menu_selection == "2":
        search_and_order_item()

    # Else, if they pick 3
    elif menu_selection == "3":
        category_selection(actions, authorized_employee)

    # Else, if they pick 4
    elif menu_selection == "4":
        pass

    else:
        print("*" * 150)
        print(
            f"{colors.ANSI_RED}Invalid input, please enter a number between 1 and 4 for a valid operation{colors.ANSI_RESET}")
        print("*" * 150)


def start_shopping():
    """Start the shopping application."""
    actions = []
    username = get_user_name()
    authorized_employee = user_authentication(username)
    run(actions, authorized_employee)

    print()

    if isinstance(authorized_employee, User):
        authorized_employee.bye(actions)
    else:
        authorized_employee.bye(actions)


# start_shopping()  # Uncomment to start the shopping application
