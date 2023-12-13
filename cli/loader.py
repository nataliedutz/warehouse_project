"""Data loader."""
import json
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EMPLOYEES_PATH = os.path.join(BASE_DIR, "data", "personnel.json")
STOCK_PATH = os.path.join(BASE_DIR, "data", "stock.json")

employees = []
iems = []

with open(EMPLOYEES_PATH) as file:
    employees = json.loads(file.read())

with open(STOCK_PATH) as file:
    items = json.loads(file.read())


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
