import unittest
from io import StringIO
from unittest.mock import patch

import query
from data import stock
from query import item_list_by_warehouse


class TestQueryFunctions(unittest.TestCase):

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_user_authentication_guest_mode(self, mock_print, mock_input):
        user_obj = query.user_authentication("Natalie")
        self.assertIsInstance(user_obj, query.User)
        self.assertEqual(
            user_obj._name, "Natalie",
            "Guest user should have the correct name"
            )
        self.assertFalse(
            user_obj.is_authenticated,
            "Guest user should not be authenticated"
            )

    @patch('builtins.input', side_effect=['2', 'coppers'])
    @patch('builtins.print')
    def test_user_authentication_employee_mode(self, mock_print, mock_input):
        user_name = "Jeremy"
        user_obj = query.user_authentication(user_name)
        self.assertTrue(isinstance(user_obj, query.Employee))
        self.assertTrue(
            user_obj.is_authenticated,
            "Employee should be authenticated"
            )

    @patch('builtins.input', side_effect=["1"])
    @patch('builtins.print')
    def test_select_operation(self, mock_print, mock_input):
        query.select_operation()
        call_args_list = mock_print.call_args_list
        output_characters = (call[0][0] for call in call_args_list)
        actual_output = "".join(output_characters)

        print(f"Actual Output: {actual_output}")
        self.assertIn("1. List items by warehouse", actual_output)

    @patch('builtins.input', side_effect=["second hand printer"])
    @patch('builtins.print')
    def test_search_and_order_item(self, mock_print, mock_input):
        location, item_count_in_warehouse_dict, search_item = \
            query.search_and_order_item(stock)
        # Example assertions for search_and_order_item
        self.assertEqual(len(location), 12, "Incorrect number of locations")
        self.assertEqual(
            item_count_in_warehouse_dict[1], 4,
            "Incorrect item count for Warehouse 1"
            )

    @patch('sys.stdout', new_callable=StringIO)
    def test_item_list_by_warehouse(self, mock_stdout):
        # Call the function
        item_list_by_warehouse()

        # Define the expected output
        expected_output = [
            "elegant pen drive",
            "exceptional mouse",
            "original laptop",
            "Total items in Warehouse 4: 1223",
            "Total items in all warehouses: 5000"
        ]

        # Check if each line of the expected output
        # is present in the actual output
        actual_output = mock_stdout.getvalue()
        for line in expected_output:
            self.assertIn(line, actual_output)


if __name__ == "__main__":
    unittest.main()
