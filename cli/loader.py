"""Data loader."""
import json
import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EMPLOYEES_PATH = os.path.join(BASE_DIR, "data", "personnel.json")
STOCK_PATH = os.path.join(BASE_DIR, "data", "stock.json")

employees = []
items = []

with open(EMPLOYEES_PATH) as file:
    employees = json.loads(file.read())

with open(STOCK_PATH) as file:
    items = json.loads(file.read())
# # Remove the lines above

# # Database connection parameters
# db_params = {
#     'host': 'localhost',
#     'port': '5432',
#     'database': 'warehouse_management',
#     'user': 'postgres',
#     'password': 'oatley123',
# }

# # Establish a connection to the PostgreSQL database
# conn = psycopg2.connect(**db_params)

# # Create a cursor
# cursor = conn.cursor()

# # Execute a query to retrieve all items
# cursor.execute("SELECT * FROM item;")
# rows = cursor.fetchall()

# # Get column names
# columns = [column[0] for column in cursor.description]

# # Convert rows into a list of dictionaries
# items = [dict(zip(columns, row)) for row in rows]

# # Convert the items list to JSON
# items_json = json.dumps(items)

# # Close the cursor and connection
# cursor.close()
# conn.close()


def _import(name):
    """Dynamically import a package."""
    try:
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
    except Exception:
        mod = None
    return mod


class MissingClassError(Exception):
    """Missing class exception."""

    def __init__(self, name=None, message="Missing class"):
        """Construct object."""
        self.class_name = name
        self.message = f"Missing class {name}."
        super().__init__(self.message)


class Loader:
    """Main data loader class."""

    model = None
    objects = None

    def __init__(self, *args, **kwargs):
        """Construct object."""
        if "model" not in kwargs:
            raise Exception("The loader requires a `model` "
                            "keyword argument to work.")
        self.model = kwargs["model"]
        self.parse()

    def parse(self):
        """Instantiate objects from the data."""
        if self.model == "personnel":
            self.objects = self.__parse_personnel()
        if self.model == "stock":
            self.objects = self.__parse_stock()

    def __load_class(self, name):
        """Return a class."""
        classes = _import("classes")
        if not hasattr(classes, name):
            raise MissingClassError(name)
        return getattr(classes, name)

    def __parse_personnel(self):
        """Parse the personnel list."""
        Employee = self.__load_class("Employee")  # noqa: N806

        return [Employee(**employee) for employee in employees]

    def __parse_stock(self):
        """Parse the stock."""
        Item = self.__load_class("Item")  # noqa: N806
        Warehouse = self.__load_class("Warehouse")  # noqa: N806
        warehouses = {}
        for item in items:
            warehouse_id = str(item["warehouse"])
            if warehouse_id not in warehouses.keys():
                warehouses[warehouse_id] = Warehouse(warehouse_id)
            warehouses[warehouse_id].add_item(Item(**item))
        return list(warehouses.values())

    def __iter__(self, *args, **kwargs):
        """Iterate through the objects."""
        yield from self.objects

    def to_dict(self):
        """Return a dictionary."""
        data = None
        if self.model == "stock":
            data = []
            for warehouse in self.objects:
                for item in warehouse.stock:
                    item_dict = vars(item)
                    item_dict["warehouse"] = warehouse.id
                    data.append(item_dict)
        return data

# Add new functions to generate inserts:
    
    def generate_insert_statements(self):
        """Generate SQL insert statements for the loaded data."""
        if self.model == "personnel":
            return self.__generate_personnel_inserts()
        elif self.model == "stock":
            return self.__generate_stock_inserts()
        else:
            return []

    def __generate_personnel_inserts(self):
        """Generate SQL insert statements for personnel data."""
        inserts = []
        for employee in self.objects:
            inserts.append(
                f"INSERT INTO employee (name, password, head_of) VALUES "
                f"('{employee.name}', '{employee.password}', {employee.head_of});"
            )
        return inserts

    def __generate_stock_inserts(self):
        """Generate SQL insert statements for stock data."""
        inserts = []
        for warehouse in self.objects:
            for item in warehouse.stock:
                # Check if quantity attribute is present in the item
                if hasattr(item, 'quantity') and item.quantity is not None:
                    inserts.append(
                        f"INSERT INTO item (state, category, warehouse_id, date_of_stock, quantity) VALUES "
                        f"('{item.state}', '{item.category}', {item.warehouse_id}, '{item.date_of_stock}', {item.quantity});"
                    )
                else:
                    inserts.append(
                        f"INSERT INTO item (state, category, warehouse_id, date_of_stock) VALUES "
                        f"('{item.state}', '{item.category}', {item.warehouse_id}, '{item.date_of_stock}');"
                    )
        return inserts
