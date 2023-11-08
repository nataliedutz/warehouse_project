from datetime import datetime
from collections import defaultdict
from data import personnel
from loader import Loader
from classes import User, Employee, Item, Warehouse
import colors

personnel=Loader(model="personnel") # list of Employee objects
stock=Loader(model="stock") # list of Warehouse objects (Warehouse.stock = [] of Item objects)

def get_user_name():
    '''This function gets the username via user input.'''
    username=input(f"\n{colors.ANSI_PURPLE}Please enter the username: {colors.ANSI_WHITE}")
    return username.capitalize()

def validate_user(personnel,password,user_name):
    '''This function checks if the user is an employee before placing an order,
        because only employees are allowed to place an order.'''
    for staff in personnel:
        if str(staff)==user_name:
            if staff.authenticate(password)==True:
                staff.is_authenticated=True
                print(f"{colors.ANSI_RESET}{'*'*150}")
                staff.greet()
                return staff
            

def user_authentication(user_name):
    entry_mode=input(f"\n{colors.ANSI_RESET}ENTRY MODE :\n{'*'*20} {colors.ANSI_PURPLE}1.GUEST    {colors.ANSI_RESET}{'*'*20}\n{'*'*20} {colors.ANSI_YELLOW}2.EMPLOYEE {colors.ANSI_RESET}{'*'*20}\n\n{colors.ANSI_PURPLE}Enter the corresponding number for your entry mode: {colors.ANSI_RESET}")
    # guest mode
    if entry_mode=="1":
        user=User(user_name)
        print(f"{'*'*150}")
        user.greet()
        return user
    #employee mode
    elif entry_mode=="2":
        password=input(f"{colors.ANSI_PURPLE}Please enter your password:{colors.ANSI_RESET}")
        authorised_employee=validate_user(personnel,password,user_name)
        if not authorised_employee:         
            user_decision=input(f"{colors.ANSI_RED}Incorrect password for the given username.\nDo  you want to change your username and password? (y/n) : {colors.ANSI_WHITE}")
            if user_decision=="Y" or user_decision=="y":
                kickstart_shopping()
        return authorised_employee
    else:
        print(f"INVALID INPUT, Pleaset select the correct option.")


def place_order(search_item,total_item_count_in_Warehouses):
    order_quantity = int(input(f"{colors.ANSI_PURPLE}\nHow much quantity of {search_item} do you want to order? {colors.ANSI_RESET}"))
    if order_quantity <= total_item_count_in_Warehouses:
        print(f"{colors.ANSI_RESET}{'*'*150}")
        print(f"\n{' '*50}{colors.ANSI_GREEN}Order placed: {order_quantity} * {search_item}{colors.ANSI_RESET}\n")
        print(f"{'*'*150}")
    else: 
        print(f"{colors.ANSI_RESET}{'*'*100}")
        print(f"{colors.ANSI_RED}There are not this many available. The maximum quantity that can be ordered is {total_item_count_in_Warehouses}. {colors.ANSI_RESET}")
        print("-"*100)
        ask_order_max = input(f"{colors.ANSI_PURPLE}Do you want to order the maximum quantity of {search_item} which is {total_item_count_in_Warehouses}? (y/n) -  {colors.ANSI_RESET} ")
        if ask_order_max.lower() in ("y","Y"):
            print(f"{colors.ANSI_RESET}{'*'*150}")
            print(f"\n{' '*50}{colors.ANSI_GREEN}Order placed: {total_item_count_in_Warehouses} * {search_item}{colors.ANSI_RESET}\n")
            print(f"{'*'*150}")


def search_and_order(actions,authorized_employee):
    search_warehouse=Warehouse()
    location, item_count_in_warehouse_dict, search_item=search_warehouse.search_and_order_item()
    if len(location)>0:
        print(f"\n{colors.ANSI_GREEN}Quantity Availability: {len(location)}{colors.ANSI_RESET}\n")
        print("Location:")
        for i in location:
            print(f"{' '*15}{colors.ANSI_GREEN}{i}{colors.ANSI_RESET}")
        for warehouse,count in item_count_in_warehouse_dict.items():
            if max(item_count_in_warehouse_dict.values())==count:                      
                print(f"\nMaximum availability: {colors.ANSI_GREEN}{count} in {warehouse}{colors.ANSI_RESET}\n")
        print("*"*120)
        if isinstance(authorized_employee, Employee)==True:   #"authorized_employee" is of Class Employe
            ask_for_order=input(f"{colors.ANSI_PURPLE}Do you want to place an order for the item {search_item}? (y/n) {colors.ANSI_RESET}")
            if ask_for_order.lower() in ("y", "Y"):
                place_order(search_item,sum(item_count_in_warehouse_dict.values()))
    else:
        print(f"{colors.ANSI_RED}\nNot in stock")

    actions.append(f"Searched for {search_item}")
    continue_session = input(f"\n{'*'*20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {'*'*20}   -   {colors.ANSI_WHITE}")
    if continue_session in ("y","Y"):
        select_operation(actions, authorized_employee)    


def select_category(actions, authorized_employee):
    category_select=Warehouse()
    dict_id_category=category_select.browse_by_category()
    ask_for_category=input(f"Type the category number to browse: {colors.ANSI_WHITE}")
    print()
    category_name=None
    for key_id, value_id in dict_id_category.items():
        if key_id==int(ask_for_category):
            category_name=value_id
            count_items_by_category=0
            for warehouse in stock:
                for item in warehouse.stock:
                    if value_id==item.category:
                        count_items_by_category+=1
                        print(f"{colors.ANSI_GREEN}{'- '}{item.state} {item.category}, {warehouse}")
    if int(ask_for_category) not in dict_id_category.keys():
        print(f"{colors.ANSI_RED}Invalid input !{colors.ANSI_RESET}")
    if not category_name==None:
        print(f"{colors.ANSI_RESET}{'*'*120}")
        print(f"\nTotal items in this category are: {count_items_by_category}\n")
        print("*"*120)
        actions.append(f"Browsed the category {category_name}")
        continue_session = input(f"\n{'*'*20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {'*'*20}   -   {colors.ANSI_GREEN}")
        if continue_session in ("y", "Y"):
            select_operation(actions,authorized_employee)



def select_operation(actions, authorized_employee): 
    print(f"{colors.ANSI_RESET}\n{'*'*150}")
    print(f"{colors.ANSI_PURPLE}To make a selection, enter the number corresponding to your choice from the menu below. {colors.ANSI_RESET}")
    print(f"{' '*25}1. List items by warehouse\n{' '*25}2. Search an item and place an order\n{' '*25}3. Browse by category\n{' '*25}4. Quit")
    print("-"*150)
    menu_selection = input(f"\n{colors.ANSI_PURPLE}Please type the number associated with the operation:  {colors.ANSI_RESET}")
    
    # If user selects operation 1
    if menu_selection == "1":
        new_item_dict=Item.list_items_by_warehouse()
        total_items=sum(len(i) for i in new_item_dict.values())
        actions.append(f"listed {total_items} items from {len(new_item_dict.keys())} Warehouses")
    
        continue_session = input(f"\n{'*'*20}  {colors.ANSI_PURPLE}Do you want to perform another operation? (y/n){colors.ANSI_RESET}  {'*'*20}   -   {colors.ANSI_WHITE}")
        if continue_session == "y" or continue_session=="Y":
            select_operation(actions, authorized_employee)

    # Else, if user picks 2
    elif menu_selection=="2":
        search_and_order(actions,authorized_employee)
        
    #     # Else, if user pick 3
    elif menu_selection == "3":
        select_category(actions, authorized_employee)
    
    # Else, if user picks 4
    elif menu_selection == "4":
            pass

    else:
        print("*"*150)
        print(f"{colors.ANSI_RED}Invalid input, please enter a number between 1 and 4.{colors.ANSI_RESET}")
        print("*"*150)

                    
def kickstart_shopping():
    actions=[]
    username=get_user_name()
    authorised_employee=user_authentication(username)
    select_operation(actions, authorised_employee)
    print()
    if isinstance(authorised_employee, User):
        authorised_employee.bye(actions)
    else:
        authorised_employee.bye(actions)

kickstart_shopping()
