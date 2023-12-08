from unittest.mock import Mock, MagicMock, patch
import unittest
from io import StringIO
from data import personnel, stock
from loader import Loader
import query
from classes import User,Employee, Warehouse , Item
from contextlib import contextmanager


@contextmanager
def mock_input(mock):
    original_input = __builtins__.input
    __builtins__.input = lambda _: mock
    yield
    __builtins__.input = original_input


@contextmanager
def mock_output(mock):
    original_print = __builtins__.print
    __builtins__.print = lambda *value: [mock.append(val) for val in value]
    yield
    __builtins__.print = original_print


class TestQueryFunctions(unittest.TestCase):

    def test_user_authentication(self):
        # Test GUEST mode
        with mock_input("Natalie"):
            with mock_input("1"):
                prints = []
                with mock_output(prints):
                    user_obj = query.user_authentication("Natalie")

        # Check if the user is an instance of the User class
        self.assertIsInstance(user_obj, query.User)
        self.assertEqual(user_obj._name, "Natalie", "Guest user should have the correct name")
        self.assertFalse(user_obj.is_authenticated, "Guest user should not be authenticated")

                    

        # Test when the user answers with a name that is in the employees list
        with mock_input("Jeremy"):
            user_name = query.get_user_name()
            with patch("builtins.input",side_effect=["2", "coppers"]):
                prints_employee=[]
                with mock_output(prints_employee):
                    user_obj=query.user_authentication(user_name)
                self.assertTrue(isinstance(user_obj,Employee))

    def test_select_operation(self):
        # Test the output printed contains all the options available
        with mock_input("1"):
            prints = []
            with mock_output(prints):
                operation = query.select_operation()

            # Check if key phrases are present in the output
            self.assertIn("Main Menu:", prints)
            self.assertIn("1. List items by warehouse", prints)
            self.assertIn("2. Search an item and place an order", prints)
            self.assertIn("3. Browse by category", prints)
            self.assertIn("4. Quit", prints)

        
    def test_search_and_order_item(self):
        """Test the search_and_order_item function."""

        # Set up input for the search item
        with mock_input("second hand printer"):
            prints = []
            with mock_output(prints):
                location, item_count_in_warehouse_dict, search_item = query.search_and_order_item(stock)

        # Define the expected result based on your input data
        expected_location = [
            "Second hand - Warehouse 1",
            "Second hand - Warehouse 3",
            "Second hand - Warehouse 4",
            "Second hand - Warehouse 4",
            "Second hand - Warehouse 1",
            "Second hand - Warehouse 4",
            "Second hand - Warehouse 2",
            "Second hand - Warehouse 1",
            "Second hand - Warehouse 3",
            "Second hand - Warehouse 3",
            "Second hand - Warehouse 3",
            "Second hand - Warehouse 1",
        ]
        expected_item_count = {1: 4, 2: 1, 3: 4, 4: 3}
        expected_search_item = "second hand printer"

        # Compare the actual output with the expected output
        self.assertEqual(location, expected_location, "The locations list is not matching")
        self.assertEqual(item_count_in_warehouse_dict, expected_item_count, "The item count in the warehouse dict is not matching")
        self.assertEqual(search_item, expected_search_item, "The searched item is not matching")


 
    def test_item_list_by_warehouse(self):
        # Test the function returns a string saying "Listed 5000 items"
        prints = []
        with mock_output(prints):
            warehouses = query.item_list_by_warehouse()
        
        total_items = 0
        for warehouse in warehouses:
            for i in warehouse.stock:
                if isinstance(i, Item):
                    total_items += 1
        self.assertEqual(total_items, 5000, "Incorrect total items from all warehouses are 5000")



if __name__=="__main__":
    unittest.main()
