import io
import unittest.mock
import builtins
from contextlib import contextmanager
from query import get_user_name, validate_user, select_operation, item_list_by_warehouse, run, AuthenticationError
from classes import Employee

@contextmanager
def mock_input(mock):
    original_input = builtins.input
    __builtins__.input = lambda _: mock
    yield
    __builtins__.input = original_input

@contextmanager
def mock_output(mock):
    original_print = builtins.print
    __builtins__.print = lambda *value: [mock.append(val) for val in value]
    yield
    __builtins__.print = original_print

class TestGetUserName(unittest.TestCase):

    def test_get_user_name(self):
        mock_inputs = 'jennifer'
        with mock_input(mock_inputs):
            result = get_user_name()
        self.assertEqual(result, 'Jennifer')


class TestValidateUser(unittest.TestCase):

    def setUp(self):
        self.personnel = [
            Employee("Barbara", "password2"),
            Employee("Nicole", "password1"),
        ]


    def test_valid_user(self):
        mock_inputs = ['Nicole', 'password1']  
        with mock_input(mock_inputs):
            result = validate_user(self.personnel, "password1", "Nicole")
            self.assertIsNotNone(result)
            self.assertTrue(result.is_authenticated)


    def test_invalid_user(self):
        mock_inputs = ['Nadine', 'wrongpassword']
        with mock_input(mock_inputs), self.assertRaises(AuthenticationError):
            result = validate_user(self.personnel, "password1", "Nadine")
            self.assertIsNone(result)
            if result is not None:
                self.assertFalse(result.is_authenticated)
'''
class TestSelectOperation(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_select_operation_menu_display(self, mock_stdout):
        mock_inputs = ['1']
        with mock_input(mock_inputs):
            select_operation()

        printed_content = mock_stdout.getvalue()
        self.assertIn("1. List items by warehouse", printed_content)
        self.assertIn("2. Search an item and place an order", printed_content)
        self.assertIn("3. Browse by category", printed_content)
        self.assertIn("4. Quit", printed_content)


    def test_select_operation_and_run(self):
    mock_inputs = ['2', 'second hand printer', 'n']
    with mock_input(mock_inputs), mock_output([]) as mock_print:
        actions = []  # List to capture actions performed during the run
        select_operation_user_input = lambda _: '2'  # This will simulate selecting option 2

        menu_selection = select_operation(user_input=select_operation_user_input)
        self.assertEqual(menu_selection, '2')

        if menu_selection == '2':
            authorized_employee = None

            run(actions, authorized_employee, user_input=select_operation_user_input)

            printed_content = ''.join(call[0][0] for call in mock_print.call_args_list)

            self.assertIn("Enter the item that you are searching:", printed_content)
            self.assertIn("Not in stock", printed_content)
            self.assertIn("Do you want to continue with another operation? (y/n)", printed_content)
            self.assertIn("Searched for second hand printer", actions)


class TestItemListByWarehouse(unittest.TestCase):

 

    @unittest.mock.patch('query.get_user_name', return_value="SomeUsername")
    @unittest.mock.patch('classes.Warehouse', autospec=True)
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_item_list_by_warehouse(self, mock_stdout, mock_warehouse):
        # Mock the return value of the stock attribute
        mock_warehouse.return_value.stock = ["item1", "item2", "item3"]

        result = item_list_by_warehouse()

        # Check if the function returns the expected string
        self.assertEqual(result, "Listed 3 items")

        # Check if the last lines of the printed output match the expected pattern
        expected_output = "Total items in Warehouse: 3\n"
        self.assertIn(expected_output, mock_stdout.getvalue())'''

if __name__ == '__main__':
    unittest.main()
