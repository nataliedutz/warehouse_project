from data import stock
from datetime import datetime
from collections import Counter

# Initialize dict for handling of warehouses
# warehouse_stock = {1: 0, 2: 0, "Unknown Warehouse": 0}
warehouse_stock = {}
session_activities = []

def get_username():
    '''This function gets the username'''
    username = input("Welcome, what is your user name? ")
    return username

# Greet the user
def greet(username):
    '''This function greets the user.'''
    return f"Hello, {username}!"

# Show the menu and ask to pick a choice
def get_selected_operation(stock, warehouse_stock):
    '''This function shows the menu and asks the user to make a choice between 3 operations'''
    print("What do you want to do?")
    print("1. List items by warehouse")
    print("2. Search an item and place an order")
    print("3. Browse by category")
    print("4. Quit")

    picked_number = input("Please select by typing 1, 2, 3 or 4: ")
    # User picks option 1:
    if picked_number == "1":
        return list_items_by_warehouse(stock)
        
    # User picks option 2:
    elif picked_number == "2":
        search_item = input("What is the name of the item you are looking for? ").lower()
        found_items = search_an_item(stock, search_item, warehouse_stock)
        if found_items:
            print_search_results(found_items, warehouse_stock)
            order_an_item(found_items, search_item, warehouse_stock)
        else:
            print("No items found.")
    
        
    elif picked_number == "3":
        return browse_by_category(stock)
        
    elif picked_number == "4":
        pass    
    
    else:
        print("******************************************************")
        print("No valid input, please enter a number between 1 and 4.")
        print("******************************************************")


def list_items_by_warehouse(stock):
    '''This function prints a list of all items in stock'''
    # Initialize variables for amounts in both warehouses
    warehouse_amounts = {}    #available_amount_warehouse1 = 0
    #available_amount_warehouse2 = 0
    # For loop iterating over all items in stock
    for item in stock:
        warehouse_id = item["warehouse"]
        warehouse_stock[warehouse_id] = warehouse_stock.get(warehouse_id, 0) + 1
        print(f"{item['state']} {item['category']}, Warehouse {warehouse_id}")
    for warehouse_id, available_amount in warehouse_amounts.items():
        print(f"Items in warehouse {warehouse_id}: {available_amount}")
    return "Listed items by warehouse."
   

def search_an_item(stock, search_item, warehouse_stock):
    # Use of lower() for input and lists to avoid errors
    #search_item = search_item.lower()
    # Initialize list for all search_items found in stock
    found_items = [] 
    # For loop iterating over all items in stock:
    for item in stock:
        state_lower = item["state"].lower()
        category_lower = item["category"].lower()
        # Get name of item to compare with user input
        concatenated_item = state_lower + " " + category_lower 
        # Check if user input (search_item) is equal to a concatenated_item
        if search_item == concatenated_item: 
            # If it is equal, add this item to the list found_items
            found_items.append(item) 
            # Update warehouse stock
            warehouse_id = item['warehouse']
            warehouse_stock[warehouse_id] = warehouse_stock.get(warehouse_id, 0) + 1
    if found_items:
        print(f"Found {len(found_items)} item(s) matching '{search_item}' in stock.")
    else:
        print(f"No items found matching '{search_item}' in stock.")
    return found_items

def print_search_results(found_items, warehouse_stock, search_item):
    if found_items:
        # Count all items in found_items list
        total_count = len(found_items) 
        print(f"Amount available: {total_count}.")
        print("Location:")
        current_datetime = datetime.now()
        # For loop iterating over all items in found_items list:
        for item in found_items:
            # Initialize datetime to count days in stock
            stock_date = datetime.strptime(item["date_of_stock"], "%Y-%m-%d %H:%M:%S") 
            # Calcualate days in stock
            days_in_stock = (current_datetime - stock_date).days
            
            for warehouse_id in warehouse_stock:
                if item['warehouse'] == warehouse_id:
                    warehouse_stock[warehouse_id] += 1
                    print(f"- Warehouse {warehouse_id} (in stock for {days_in_stock} days)")
                    session_activities.append(f"Found {total_count} item(s) matching '{search_item}' in stock.")

        max_availability_warehouse = max(warehouse_stock, key=warehouse_stock.get)
        max_availability = warehouse_stock[max_availability_warehouse]
        print(f"Maximum availability: {max_availability} in Warehouse {max_availability_warehouse}")
        return warehouse_stock
    return warehouse_stock

def order_an_item(found_items, search_item, warehouse_stock):
    total_count = len(found_items)
    max_availability_warehouse = max(warehouse_stock, key=warehouse_stock.get)
    max_availability = warehouse_stock[max_availability_warehouse]
    order_description = ""

    if total_count > 0:
        ask_order = input(f"Do you want to place an order for the item {search_item}? (y/n)") 
        if ask_order.lower() == "y": 
            order_amount = int(input(f"How many items of {search_item} do you want to order?")) 
            if order_amount <= total_count and order_amount <= max_availability: 
                warehouse_stock[max_availability_warehouse] -= order_amount  # Update the warehouse stock
                order_description = f"Ordered {order_amount} '{search_item}' from Warehouse {max_availability_warehouse}."
            else:
                print("***********************************************************")
                if order_amount > max_availability:
                    print(f"Unfortunately, the item is not available {order_amount} times in Warehouse {max_availability_warehouse}.")
                else:
                    print(f"Unfortunately, the item is not available {order_amount} times.")
                print("***********************************************************")
                ask_order_max = input(f"Do you want to order the maximum amount of {total_count}? (y/n)") 
                if ask_order_max.lower() == "y" and total_count <= max_availability: 
                    warehouse_stock[max_availability_warehouse] -= total_count  # Update the warehouse stock
                    order_description = f"Ordered {total_count} '{search_item}' from Warehouse {max_availability_warehouse}."
                else:
                    order_description = f"Attempted to order {order_amount} '{search_item}' but it was unavailable."
        else:
            order_description = f"Did not place an order for '{search_item}'."
    else:
        order_description = f"'{search_item}' is not in stock."

    session_activities.append(order_description)  # Add order description to session activities
    return order_description, warehouse_stock


def browse_by_category(stock):
    categories = [item["category"] for item in stock]
    # Count how many items are available of given category
    category_counts = Counter(categories)
    # Print available amount for each category that exists
    for index_number, (category, count) in enumerate(category_counts.items(), start=1):
        print(f"{index_number}. {category} ({count} available)")
    while True:
        try:
            category_choice = int(input("Type the number of the category to browse: "))
            if 1 <= category_choice <= len(category_counts):
                # Get a list of category names from the category_counts dict, 
                # Select the category at the index corresponding to user's chooise (list index begins with 0)
                chosen_category = list(category_counts.keys())[category_choice - 1]
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
                print("Invalid input. Please enter a number.")

    print(f"List of {chosen_category} available:")
    for item in stock:
        if item["category"] == chosen_category:
            print(f"{item['state']} {item['category']}, Warehouse", item['warehouse'])
    return f"Browsed items in the category '{chosen_category}'."

    
# Define the username and call the functions
username = get_username()
print(greet(username))
# Initialize a list for the record of actions taken during the session
session_actions = []
while True:
    operation_description = get_selected_operation(stock, warehouse_stock)
    session_actions.append(operation_description)

    # Ask if the user wants to perform another operation
    another_operation = input("Do you want to perform another operation? (y/n): ")
    if another_operation.lower() != 'y':
        print(f"Thank you for your visit, {username}!")
        print("In this session you have:")
        for idx, action in enumerate(session_actions, start=1):
            print(f"    {idx}. {action}")
        break