from data import warehouse1, warehouse2

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
    print("3. Quit")
    picked_number = input("Please select by typing 1, 2 or 3: ")
    
   
    if picked_number == "1":
        print(f"Items in warehouse 1: {warehouse1}")
        print(f"Items in warehouse 2: {warehouse2}")
    elif picked_number == "2":
        # Use of lower() for input and lists to avoid errors
        search_item = input("What is the name of the item you are looking for? ").lower()
        count_in_warehouse1 = sum(1 for item in warehouse1 if item.lower() == search_item)
        count_in_warehouse2 = sum(1 for item in warehouse2 if item.lower() == search_item)
        total_count = count_in_warehouse1 + count_in_warehouse2
        if total_count > 0:
            print(f"Amount available: {total_count}.")
            if search_item.lower() in map(str.lower, warehouse1) and search_item.lower() in map(str.lower, warehouse2):
                print(f"Location: Both warehouses")
                if count_in_warehouse2 == count_in_warehouse1:
                    print(f"Same quantity available in both warehouses: {count_in_warehouse1} in each.")
                elif count_in_warehouse1 > count_in_warehouse2:
                    print(f"Maximum availability: {count_in_warehouse1} in Warehouse 1")
                elif count_in_warehouse2 > count_in_warehouse1:
                    print(f"Maximum availability: {count_in_warehouse2} in Warehouse 2")
            elif search_item.lower() in map(str.lower, warehouse1) and search_item.lower() not in map(str.lower, warehouse2):
                print("Location: Warehouse 1")
            elif search_item.lower() in map(str.lower, warehouse2) and search_item.lower() not in map(str.lower, warehouse1):
                print(f"Location: Warehouse 2.")
            
            ask_order = input(f"Do you want to place an order for the item {search_item}? (y/n)")
            if ask_order.lower() == "y":
                order_amount = int(input(f"How many items of {search_item} do you want to order?"))
                if order_amount <= total_count:
                    print(f"Order placed: {order_amount} {search_item}")
                else: 
                    print("***********************************************************")
                    print(f"Unfortunately, the item is not available {order_amount} times.")
                    print("***********************************************************")
                    ask_order_max = input(f"Do you want to order the maximum amount of {total_count}? (y/n)")
                    if ask_order_max.lower() == "y":
                        print(f"Order placed: {total_count} {search_item}.")
        else:
            print("Amount available: 0")
            print("Location: Not in stocḱ")
    elif picked_number == "3":
        return    
    else:
        print("******************************************************")
        print("No valid input, please enter a number between 1 and 3.")
        print("******************************************************")


greet(username)
show_menu()
print(f"Thank you for your visit, {username}!")