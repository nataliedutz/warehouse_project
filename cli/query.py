from datetime import datetime

from collections import Counter

from functools import wraps

from data import stock, personnel

class WarehouseManagementSystem:
    '''This class contains all the functions for the warehouse managment system.'''
    def __init__(self, stock, personnel):
        self.stock = stock
        self.personnel = personnel
        self.warehouse_stock = {}
        self.actions = []
        self.username = None

    def get_username(self):
        '''This function gets the username via user input.'''
        return input("Welcome, what is your user name? ")

    def greet_user(self, username):
        '''This function greets the user.'''
        print(f"Hello, {username}!")

    def authenticate_user(self):
        '''This function checks if user ise employee before placing an order, 
        because only employees are allowed to place an order.'''
        password = input("Please, type your employee password: ")
        for user in self.personnel:
            if user["user_name"] == self.username and user["password"] == password:
                return True
        return False

    def employee_only(func):
        '''This is a decorator used for functions only available to employees'''
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.authenticate_user():
                return func(self, *args, **kwargs)
            else:
                print("Authentication failed. Only employees can place an order.")
        return wrapper
    
    def list_items_by_warehouse(self):
        '''This function prints a list of the items by warehouse
        with information about how long they have been in stock.'''
        current_datetime = datetime.now()  # Get the current date and time
        warehouses = {}  # Initialize a dictionary to store items grouped by warehouse

        for item in self.stock:
            warehouse_id = item["warehouse"]
            if warehouse_id not in warehouses:
                warehouses[warehouse_id] = []
            warehouses[warehouse_id].append(item)

        for warehouse_id, items in warehouses.items():
            print(f"Items in warehouse {warehouse_id}:")
            for item in items:
                stock_date = datetime.strptime(item["date_of_stock"], "%Y-%m-%d %H:%M:%S")
                days_in_stock = (current_datetime - stock_date).days
                print(f"- {item['state']} {item['category'].lower()} (in stock for {days_in_stock} days)")

            total_items_in_warehouse = len(items)
            print(f"Total items in warehouse {warehouse_id}: {total_items_in_warehouse}")

        total_items = sum(len(items) for items in warehouses.values())
        print(f"Total items in all warehouses: {total_items}")
        self.actions.append("Listed items by warehouse.")

    def search_an_item(self, search_item):
        '''The user searches for an item'''
        search_item_lower = search_item.lower()  # Convert search_item to lowercase once
        found_items = []
        for item in self.stock:
            item_name = f"{item['state'].lower()} {item['category'].lower()}"
            if search_item_lower in item_name:
                found_items.append(item)
        return found_items

    def update_warehouse_stock(self, found_items):
        '''This function counts the items in the warehouse'''
        for item in found_items:
            warehouse_id = item["warehouse"]
            self.warehouse_stock[warehouse_id] = self.warehouse_stock.get(warehouse_id, 0) + 1

    def search_item(self):
        '''The user searches for an item and orders an item'''
        search_item = input("What is the name of the item? ")
        found_items = self.search_an_item(search_item)

        if found_items:
            warehouse_items = {}  # Dictionary to store items organized by warehouse
            for item in found_items:
                warehouse_id = item["warehouse"]
                if warehouse_id not in warehouse_items:
                    warehouse_items[warehouse_id] = []
                warehouse_items[warehouse_id].append(item)

            print(f"{search_item}: Available {len(found_items)} times in total.")
            for warehouse_id, items in warehouse_items.items():
                print(f"Warehouse {warehouse_id}: Available {len(items)} times.")
                for item in items:
                    stock_date = datetime.strptime(item["date_of_stock"], "%Y-%m-%d %H:%M:%S")
                    days_in_stock = (datetime.now() - stock_date).days
                    print(f"- {item['state']} {item['category']} (in stock for {days_in_stock} days)")

            # Update warehouse stock with the found items
            self.update_warehouse_stock(found_items)
            ask_for_order = input(f"Do you want to place an order for {search_item}?(y/n)")
            if ask_for_order.lower() == "y":
                self.order_an_item(search_item, found_items)
        else:
            print(f"No items found matching '{search_item}' in stock.")

    @employee_only
    def order_an_item(self, search_item, found_items):
        '''The user orders an item from the warehouse; includes an authority check,
        because only employees have permission to place an order'''
        total_count = len(found_items)
        if total_count > 0:
            max_availability_warehouse = max(self.warehouse_stock, key=self.warehouse_stock.get)
            max_availability = self.warehouse_stock[max_availability_warehouse]

            # Authentication check
            if not self.authenticate_user():
                print("Authentication failed. Placing order denied.")
                return           
            warehouse_id = found_items[0]["warehouse"]

            # Ask for order amount with error handling
            while True:
                try:
                    order_amount = int(input(f"How many items of {search_item} do you want to order?"))
                    if order_amount <= 0:
                        print("Invalid quantity. Please enter a positive number.")
                    elif order_amount <= max_availability:
                        print(f"You have ordered {order_amount} of {search_item}.")
                        self.warehouse_stock[warehouse_id] -= order_amount
                        self.actions.append(f"You have ordered {order_amount} {search_item}.")
                    elif order_amount > max_availability:
                        print("***********************************************************")
                        print(f"Unfortunately, the item is not available {order_amount} times.")
                        print("***********************************************************")
                        ask_order_max = input(f"Do you want to order the maximum amount of {total_count}? (y/n)")
                        if ask_order_max.lower() == "y":
                            warehouse_id = found_items[0]["warehouse"]
                            order_amount = min(order_amount, max_availability)  # Ensure ordering available items
                            self.warehouse_stock[warehouse_id] -= order_amount
                            print(f"You have ordered {total_count} {search_item}.")
                            self.actions.append(f"Ordered {total_count} of the item {search_item}.")

                        else:
                            print("Order canceled.")
                    else:
                        print("Order canceled.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")
                else:
                    break  # Exit the loop if valid input is provided
        else:
            print(f"No items found matching '{search_item}' in stock.")

    def browse_by_category(self):
        '''The user can choose a category by typing a number,
        and then browse all products in that category.'''
        categories = [item["category"] for item in self.stock]
        category_counts = Counter(categories)

        for index, (category, count) in enumerate(category_counts.items(), start=1):
            print(f"{index}. {category} ({count} available)")

        while True:
            try:
                category_choice = int(input("Type the number of the category to browse: "))
                chosen_category = list(category_counts.keys())[category_choice - 1]
                break
            except (ValueError, IndexError):
                print("Invalid choice. Please select a valid number.")

        print(f"List of {chosen_category} available:")
        for item in self.stock:
            if item["category"] == chosen_category:
                print(
                    f"{item['state']} {item['category']}, Warehouse {item['warehouse']}")
        self.actions.append(f"Browsed items in category {chosen_category}.")

    def run(self):
        '''This function executes the warehouse management system application.'''
        self.username = self.get_username()
        self.greet_user(self.username)
        while True:
            print("What do you want to do?")
            print("1. List items by warehouse")
            print("2. Search an item and place an order")
            print("3. Browse by category")
            print("4. Quit")
            operation = input("Please select an operation by typing 1, 2, 3, or 4: ")

            if operation == "1":
                self.list_items_by_warehouse()
            elif operation == "2":
                self.search_item()

            elif operation == "3":
                self.browse_by_category()
            elif operation == "4":
                print("Thank you for using Warehouse Management System!")
                break
            else:
                print("*" * 50)
                print(operation, "is not a valid operation.")
                print("*" * 50)
            another_operation = input(
                "Do you want to perform another operation? (y/n): ")
            if another_operation.lower() not in ["y", "yes"]:
                self.print_session_summary()
                break

    def print_session_summary(self):
        '''This functions prints all the operations the user did during the session'''
        print("**************************************")
        print(f"Thank you for your visit, {self.username}!")
        print("**************************************")
        print("In this session you did the following:")
        print("**************************************")
        for action in self.actions:
            print("- ", action)


# Usage
if __name__ == "__main__":
    system = WarehouseManagementSystem(stock, personnel)
    system.run()
