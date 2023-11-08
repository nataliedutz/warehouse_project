from datetime import datetime
from loader import Loader
import colors


class User:
    '''User class representing users in the system'''
    def __init__(self, user_name="Anonymous"):
        '''Initialize the User object.
        Args:
            user_name (str): Name of the user.'''
        self._name = user_name
        self._is_authenticated = False

    def authenticate(self, password:str)->False:
        '''Placeholder authentication method. Always returns False.
        Args:
            password (str): Password input.
        Returns:
            bool: Always False.'''
        return False

    def greet(self):
        '''Print a message to the user'''
        print(f"{colors.ANSI_PURPLE}Hello, {self._name}!\nWelcome to our Warehouse Database.\nIf you don't find what you are looking for,\nplease ask one of our staff members to assist you.{colors.ANSI_RESET}")

    def is_named(self, name:str):
        '''Check if the provided name matches the user's name.
        Args:
            name (str): Name to compare.
        Returns:
            bool: True if names match, False otherwise.'''
        if name==self._name:
            return name
        else:
            return False

    def bye(self, actions:list):
        '''Print a thank you message and optionally, the summary of actions taken during the session.
        Args:
            actions (list): List of actions taken during the session.'''
        print(f"{colors.ANSI_PURPLE}\n{'*'*50}Thank you for your visit, {self._name}!{'*'*50}\n")

    
    def __str__(self):
        return self._name
    

class Employee(User):
    '''Class representing an employee in the system, inheriting from User.'''
    def __init__(self, user_name:str, password:str, head_of:list=[]):
        '''Initialize the Employee object.
        Args:
            user_name (str): Name of the employee.
            password (str): Password for employee authentication.
            head_of (list): List of departments the employee is head of.'''      
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of

   
    # Method for employee authentication
    def authenticate(self, password:str):
        '''Authenticate the employee with the provided password.
        Args:
            password (str): Password input.
        Returns:
            bool: True if the provided password matches the employee's password, False otherwise.'''
        if self.__password==password:
            return True
        else:
            return False

    def order(self, item:str, amount:int):
        print(f"Order placed: {amount} * {item}")

    def greet(self):
        '''Print a specialized greeting message for employees.'''
        print(f"{colors.ANSI_PURPLE}Hello, {self._name}!\nIf you experience a problem with the system,\nplease contact technical support.{colors.ANSI_RESET}")

    def bye(self, actions:list):
        '''Print a thank you message and the summary of actions taken during the session for employees.
        Args:
            actions (list): List of actions taken during the session.'''
        super().bye(actions)
        if len(actions)==0:
            print(f"\n{colors.ANSI_RESET}{'*'*20}You have not done any action in specific.")
        else:
            print(f"{colors.ANSI_RESET}\nSummary of action this session:")
            for id, stmt in enumerate(actions):
                print(" "*20,id+1,".",stmt)


class Item:
    '''Item class representing items in the warehouse'''
    def __init__(self, state: str=None, category: str=None, date_of_stock: datetime=None, warehouse: int=None):
        self.state = state
        self.category = category
        self.date_of_stock = date_of_stock
        self.warehouse = warehouse

    def __str__(self)->str:
        return f"{self.state} {self.category}"

    def list_items_by_warehouse():
        stock = Loader(model="stock")
        warehouse_item_dict = {}

        for i in stock.objects:
            if i not in warehouse_item_dict:
                warehouse_item_dict[i] = []
                for j in i.stock:
                    warehouse_item_dict[i].append(str(j))

        for i in warehouse_item_dict.keys():
            total_items_in_warehouse_item_dict = [str(item) for item in warehouse_item_dict[i]]
            print("***********************************")
            print(f"{colors.ANSI_PURPLE}Items in warehouse {i}:{colors.ANSI_RESET}\n", *total_items_in_warehouse_item_dict, sep="\n")
            print(f"{colors.ANSI_BLUE}\nTotal items in {i}: {len(total_items_in_warehouse_item_dict)}{colors.ANSI_RESET}\n")
            print("***********************************")
        return warehouse_item_dict

class Warehouse:
    '''Class representing a warehouse and managing its operations.'''
    def __init__(self, warehouse_id:int=None):
        '''Initialize the Item object.
        Args:
            state (str): State of the item.
            category (str): Category of the item.
            date_of_stock (str): Date when the item was stocked.
            warehouse (str): Identifier for the warehouse where the item is stocked.'''
        self.warehouse_id = warehouse_id
        self.stock = []
        

    def occupancy(self)->int:
        return f"The total number of items in the stock of Warehouse {self.warehouse_id}: {len(self.stock)}"
    
    def add_item(self, item):
        self.stock.append(item)

    def search(self,search_item)->list:
        search_item_list=[item for item in self.stock if str(item)[1]==search_item.lower()]
        return search_item_list
    
    def __str__(self)->str:
        return f"Warehouse {self.warehouse_id}"
    
    def search_and_order_item(self):
        search_item=input(f"\n{colors.ANSI_PURPLE}Which item are you looking for?: {colors.ANSI_RESET}").lower()
        location=[]
        item_count_in_warehouse_dict={}
        stock=Loader(model="stock")
        for warehouse in stock:
            for item in warehouse.stock:
                if search_item.lower()==str(item).lower():
                    date_str = item.date_of_stock
                    date_format = '%Y-%m-%d %H:%M:%S'
                    days=(datetime.now()-datetime.strptime(date_str, date_format)).days
                    location.append(f"{str(warehouse)} (in stock for {days} days)") 
                    if str(warehouse) in item_count_in_warehouse_dict:
                        item_count_in_warehouse_dict[str(warehouse)]+=1
                    else:
                        item_count_in_warehouse_dict[str(warehouse)]=1
        
        # print(f"item_count_in_warehouse_dict:{item_count_in_warehouse_dict}")
        return location, item_count_in_warehouse_dict, search_item
    
    def browse_by_category(self):
        # Initializing an empty list for all the categories
        items_by_category = [] 
        stock=Loader(model="stock")
        for warehouse in stock:
            for item in warehouse.stock:
                items_by_category.append(item.category)
        dict_item_category_count={i:items_by_category.count(i) for i in items_by_category}
        dict_id_category={}
        print()
        for id,(key,value) in enumerate(dict_item_category_count.items()):
            dict_id_category[id+1]=key
            print(f"{' '*20}{id+1} {key} ({value}")
        print()
        return dict_id_category
