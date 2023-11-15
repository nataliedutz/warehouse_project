import unittest
import io
from unittest.mock import MagicMock
from contextlib import contextmanager
from query import *


class TestGetUserName(unittest.TestCase):
    
    
    def test_get_user_name(self):
        with self.mock_input('jennifer'):
            expected_result = 'Jennifer'
            result = get_user_name()
            self.assertEqual(result, expected_result)

    @contextmanager
    def mock_input(self, *inputs):
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            yield


class TestValidateUser(unittest.TestCase):

    def setUp(self):
        # Create a list of Employee objects for testing
        self.personnel = [
            Employee("Barbara", "password1"),
            Employee("Nicole", "password2"),
        ]

    def test_valid_user(self):
        with self.mock_input('Nicole', 'password1'):
            result = validate_user(self.personnel, "password1", "Nicole")
            self.assertIsNotNone(result)
            self.assertTrue(result.is_authenticated)

    def test_invalid_user(self):
        with self.mock_input('Nadine', 'wrongpassword'):
            result = validate_user(self.personnel, "password1", "Nadine")
            self.assertIsNone(result)
            if result is not None:
                self.assertFalse(result.is_authenticated)

    @contextmanager
    def mock_input(self, *inputs):
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            yield


class TestSelectOperation(unittest.TestCase):

    def test_select_operation_menu_display(self):
        with self.mock_input('1'), self.mock_output() as mock_print:
            select_operation()

        # Get the printed content from the mock_output
        printed_content = ''.join(call[0][0] for call in mock_print.call_args_list)

        # Check if all four menu options are present in the printed content
        self.assertIn("1. List items by warehouse", printed_content)
        self.assertIn("2. Search an item and place an order", printed_content)
        self.assertIn("3. Browse by category", printed_content)
        self.assertIn("4. Quit", printed_content)

    def test_select_operation_and_run(self):
        with self.mock_input('2', 'second hand printer', 'n'), self.mock_output() as mock_print:
            actions = []  # List to capture actions performed during the run
            select_operation_user_input = lambda _: '2'  # This will simulate selecting option 2

            # Capture the menu_selection value returned by select_operation
            menu_selection = select_operation(user_input=select_operation_user_input)

            # Check the selected menu option
            self.assertEqual(menu_selection, '2')

            # If option 2 is selected, simulate the run with the provided inputs
            if menu_selection == '2':
                actions = []  # List to capture actions performed during the run
                authorized_employee = None

                # Pass the user_input function to run
                run(actions, authorized_employee, user_input=select_operation_user_input)

                # Get the printed content from the mock_output
                printed_content = ''.join(call[0][0] for call in mock_print.call_args_list)

                # Assert statements based on the expected behavior after choosing option 2
                self.assertIn("Enter the item that you are searching:", printed_content)
                self.assertIn("Not in stock", printed_content)
                self.assertIn("Do you want to continue with another operation? (y/n)", printed_content)
                self.assertIn("Searched for second hand printer", actions)

    @contextmanager
    def mock_input(self, *inputs):
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            yield

    @contextmanager
    def mock_output(self):
        with unittest.mock.patch('builtins.print') as mock_print:
            yield mock_print


class TestItemListByWarehouse(unittest.TestCase):

    @contextmanager
    def mock_input(self, *inputs):
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            yield

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_item_list_by_warehouse(self, mock_stdout):
        # Create a list of Warehouse objects for testing
        warehouses = [
            Warehouse(stock=["item1", "item2", "item3"]),
            Warehouse(stock=["item4", "item5"]),
            Warehouse(stock=["item6", "item7", "item8"]),
        ]

        # Mock the stock_loader with the list of warehouses
        with unittest.mock.patch('your_module.stock_loader', warehouses):
            result = item_list_by_warehouse()

        # Check if the function returns the expected string
        self.assertEqual(result, "Listed 8 items")

        # Check if the last lines of the printed output match the expected pattern
        expected_output = (
            "Total items in Warehouse 1: 3\n"
            "Total items in Warehouse 2: 2\n"
            "Total items in Warehouse 3: 3\n"
        )

        self.assertIn(expected_output, mock_stdout.getvalue())


class TestSearchItemInStock(unittest.TestCase):

    @contextmanager
    def mock_input(self, *inputs):
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            yield

    @unittest.mock.patch('your_module.Warehouse.search')
    def test_search_item_in_stock(self, mock_search):
        # Mock the return value of the search method
        mock_search.return_value = [(Item(state='new', category='electronics'), '2023-01-01')]

        # Create a sample stock
        stock = [
            {'state': 'new', 'category': 'electronics', 'warehouse': 1},
            {'state': 'used', 'category': 'books', 'warehouse': 2},
            {'state': 'new', 'category': 'electronics', 'warehouse': 3},
        ]

        # Call the search_item_in_stock function with the sample stock and a search item ('electronics')
        result = search_item_in_stock(stock, 'electronics')

        # Define the expected values for the search result        
        expected_location = [
            'new - Warehouse 1',
            'new - Warehouse 3',
        ]
        expected_count_dict = {'1': 1, '3': 1}

        # Check if the actual result matches the expected values
        self.assertEqual(result[0], expected_location)
        self.assertEqual(result[1], expected_count_dict)
        self.assertEqual(result[2], 'electronics')


if __name__ == '__main__':
    unittest.main()
