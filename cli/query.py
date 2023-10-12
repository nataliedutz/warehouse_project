from data import stock
from datetime import datetime
from collections import Counter

# Get the user name
username = input("Welcome, what is your user name? ")

# Greet the user
def greet(username):
    '''This function greets the user.'''
    return f"Hello, {username}!"

# Show the menu and ask to pick a choice
def show_menu():
    '''This function shows the menu and asks the user to make a choice between 3 operations'''
    print("What do you want to do?")
    print("1. List items by warehouse")
    print("2. Search an item and place an order")
    print("3. Browse by category")
    print("4. Quit")

    picked_number = input("Please select by typing 1, 2, 3 or 4: ")
    
    # User picks option 1:
    if picked_number == "1":
        # Initialize variables for amounts in both warehouses
        available_amount_warehouse1 = 0
        available_amount_warehouse2 = 0
        # For loop iterating over all items in stock
        for item in stock:
            print(f"{item['state']} {item['category']}") # Print item name
            if item["warehouse"] == 1: # Check if item is in warehouse 1
                available_amount_warehouse1 += 1 # Increment amount in warehouse 1 by 1
            elif item["warehouse"] == 2: # Check if item is i warehouse 2
                available_amount_warehouse2 += 1 # Increment amount in warehouse 2 by 1
            print(f"Items in warehouse 1: {available_amount_warehouse1}")
            print(f"Items in warehouse 2: {available_amount_warehouse2}")    

    elif picked_number == "2":
        # Use of lower() for input and lists to avoid errors
        search_item = input("What is the name of the item you are looking for? ").lower()
        # Initialize list for all search_items found in stock
        found_items = [] 
        # Initialize dict for handling of warehouses
        warehouse_stock = {1: 0, 2: 0, "Unknown Warehouse": 0} 
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
            
                if item['warehouse'] in warehouse_stock:
                    warehouse_stock[item['warehouse']] += 1
                else:
                    warehouse_stock["Unknown Warehouse"] += 1
                print(f"- Warehouse {item['warehouse']} (in stock for {days_in_stock} days)")

            max_availability_warehouse = max(warehouse_stock, key=warehouse_stock.get)
            max_availability = warehouse_stock[max_availability_warehouse]
            print(f"Maximum availability: {max_availability} in Warehouse {max_availability_warehouse}")

            ask_order = input(f"Do you want to place an order for the item {search_item}? (y/n)") 
            # Use lower function in case user inputs "Y" to avoid errors
            if ask_order.lower() == "y": 
                # Store answer as integer
                order_amount = int(input(f"How many items of {search_item} do you want to order?")) 
                # Check if order amount is available
                if order_amount <= total_count: 
                    # If it is, print this message about placed order with order details
                    print(f"Order placed: {order_amount} {search_item}") 
                else:
                    print("***********************************************************")
                    print(f"Unfortunately, the item is not available {order_amount} times.")
                    print("***********************************************************")
                    ask_order_max = input(f"Do you want to order the maximum amount of {total_count}? (y/n)") 
                    # Use lower function in case user inputs "Y" to avoid errors
                    if ask_order_max.lower() == "y": 
                        print(f"Order placed: {total_count} {search_item}.")
        else:
            # Print this info lines, if search_item is not in stock
            print("Amount available: 0") 
            print("Location: Not in stocḱ")

    elif picked_number == "3":
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
        
    elif picked_number == "4":
        return    
    else:
        print("******************************************************")
        print("No valid input, please enter a number between 1 and 4.")
        print("******************************************************")


greet(username)
show_menu()
print(f"Thank you for your visit, {username}!")