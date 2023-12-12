"""
This module contains unit tests for the classes in the 'classes' module.

The tests cover the functionality and behavior of the
User, Employee, Item, and Warehouse classes.
Additionally, it checks for the existence and inheritance of these classes.

Each test case focuses on specific aspects of the classes,
including creation, authentication,
ordering, warehouse operations, and item properties.

"""

import unittest
from datetime import datetime

from classes import Employee, Item, User, Warehouse


class TestClasses(unittest.TestCase):
    """Test case for checking class existence and inheritance."""

    def setUp(self):
        """
        Set up any necessary preconditions for the test cases.

        This method is called before each individual test method is run.
        If there are no specific preconditions to set up,
        this method can remain empty.
        """
        pass

    def test_classes_exist(self):
        """Test if essential classes exist."""
        # Check if Warehouse class exists
        self.assertTrue(
            hasattr(Warehouse, "__name__"), "Warehouse class does not exist."
        )

        # Check if Item class exists
        self.assertTrue(hasattr(Item, "__name__"), "Item class does not exist.")

        # Check if User class exists
        self.assertTrue(hasattr(User, "__name__"), "User class does not exist.")

        # Check if Employee class exists
        self.assertTrue(hasattr(Employee, "__name__"), "Employee class does not exist.")

    def test_for_inheritance(self):
        """Test if Employee class inherits from User class."""
        self.assertTrue(
            issubclass(Employee, User), "Employee class does not inherit from User."
        )


class TestUser(unittest.TestCase):
    """Test case for the User class."""

    def test_user_creation_without_arguments(self):
        """Test user creation without arguments."""
        user = User()
        self.assertEqual(user._name, "Anonymous")
        self.assertFalse(user.is_authenticated)

    def test_user_creation_with_user_name(self):
        """Test user creation with a provided user name."""
        user_name = "Thomas"
        user = User(user_name)
        self.assertEqual(user._name, user_name)
        self.assertFalse(user.is_authenticated)

    def test_user_authentication(self):
        """Test user authentication."""
        user = User("Alice")
        self.assertFalse(user.authenticate("some_password"))
        self.assertFalse(user.is_authenticated)

    def test_user_name_matching(self):
        """Test user name matching."""
        user = User("Alice")
        self.assertTrue(user.is_named("Alice"))
        self.assertFalse(user.is_named("Bob"))


class TestEmployee(unittest.TestCase):
    """Test case for the Employee class."""

    def test_employee_creation(self):
        """Test employee creation."""
        user_name = "Fritz"
        password = "secretpassword"
        employee = Employee(user_name, password)
        # Check if _name attribute is equal to the provided user_name
        self.assertEqual(employee._name, user_name)
        # Check if employee password matches provided password
        self.assertTrue(employee.authenticate(password))
        # Check if with wrong password employee authentication is unsuccessful
        self.assertFalse(employee.authenticate("wrong_password"))
        # Check if with wrong password is_authenticated attribute stays False
        self.assertFalse(employee.is_authenticated)

    def test_employee_order(self):
        """Test employee order."""
        # Create an Employee object with a specified user name and password
        employee = Employee("Natalie", "employee_password")
        # Initialize an empty list to store actions performed by the employee
        actions = []
        # Define the item_name variable representing the item's name
        item_name = "example_item"
        # Call the 'order' method of the Employee object
        # to place an order for 5 'item_name'
        employee.order(item_name, 5)
        # Append the action performed to the 'actions' list
        actions.append(f"Ordered 5 {item_name}")
        # Assert that the 'actions' list contains the expected action
        self.assertEqual(actions, [f"Ordered 5 {item_name}"])


class TestWarehouse(unittest.TestCase):
    """Test case for the Warehouse class."""

    def test_warehouse_creation_with_no_argument(self):
        """Test warehouse creation with no argument."""
        # Create a warehouse without passing a warehouse_id argument
        warehouse = Warehouse()
        # Check if warehouse_id property is None when no argument is passed
        self.assertIsNone(warehouse.warehouse_id)

    def test_warehouse_creation_with_warehouse_id_argument(self):
        """Test warehouse creation with a warehouse_id argument."""
        # Define a specific warehouse ID
        warehouse_id = 1
        # Create a warehouse with the specified warehouse_id
        warehouse = Warehouse(warehouse_id)
        # Check if warehouse_id property contains
        # the same value as the argument passed
        self.assertEqual(warehouse.warehouse_id, warehouse_id)

    def test_warehouse_creation_stock_is_empty_list(self):
        """Test if warehouse creation results in an empty stock."""
        # Create a warehouse
        warehouse = Warehouse()
        # Check if the stock property is an empty list after warehouse creation
        self.assertEqual(len(warehouse.stock), 0)

    def test_occupancy_method_returns_length_of_stock(self):
        """Test if the occupancy method returns the length of the stock."""
        # Create a warehouse
        warehouse = Warehouse()
        # Add items to the warehouse's stock
        item1 = Item(state="new", category="electronics")
        item2 = Item(state="used", category="books")
        warehouse.add_item(item1)
        warehouse.add_item(item2)
        # Check if the occupancy method returns
        # the same as the length of the stock property
        self.assertEqual(warehouse.occupancy(), len(warehouse.stock))

    def test_add_item_increases_total_items_in_stock(self):
        """Test if adding an item increases the total items in stock."""
        # Create a warehouse
        warehouse = Warehouse()
        # Add an item to the warehouse's stock
        item = Item(state="new", category="electronics")
        warehouse.add_item(item)
        # Check if the length of the stock property
        # increases after adding an item
        self.assertEqual(len(warehouse.stock), 1)

    def test_search_method_returns_correct_items(self):
        """Test if the search method returns correct items."""
        # Create a warehouse
        warehouse = Warehouse()
        # Add items to the warehouse's stock
        item1 = Item(state="new", category="electronics")
        item2 = Item(state="used", category="books")
        warehouse.add_item(item1)
        warehouse.add_item(item2)

        # Search for items with state "used" and category "books"
        search_result = warehouse.search("used books")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0][0].state, "used")
        self.assertEqual(search_result[0][0].category, "books")

        # Search for items with state "new" and category "electronics"
        search_result = warehouse.search("new electronics")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0][0].state, "new")
        self.assertEqual(search_result[0][0].category, "electronics")

        # Search for items with state "used" and category
        # "electronics" (non-existent item)
        self.assertEqual(len(warehouse.search("used electronics")), 0)

    class TestItem(unittest.TestCase):
        """Test case for the Item class."""

    def test_item_properties(self):
        """Test different cases of Item creation."""
        # Test Case 1
        item1 = Item(
            state="New",
            category="Electronics",
            date_of_stock=datetime(2023, 1, 15),
            warehouse="A1",
        )
        assert item1.state == "New"
        assert item1.category == "Electronics"
        assert item1.date_of_stock == datetime(2023, 1, 15)
        assert str(item1) == "New Electronics"

        # Test Case 2
        item2 = Item(
            state="Used",
            category="Mouse",
            date_of_stock=datetime(2023, 2, 20),
            warehouse="B2",
        )
        assert item2.state == "Used"
        assert item2.category == "Mouse"
        assert item2.date_of_stock == datetime(2023, 2, 20)
        assert str(item2) == "Used Mouse"

        # Test Case 3 (Testing default values)
        item3 = Item()
        assert item3.state is None
        assert item3.category is None
        assert item3.date_of_stock is None
        assert str(item3) == ""


print("All tests passed!")

if __name__ == "__main__":
    unittest.main()
