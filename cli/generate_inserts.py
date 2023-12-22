import os
import json
import psycopg2
from loader import Loader

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EMPLOYEES_PATH = os.path.join(BASE_DIR, "data", "personnel.json")
STOCK_PATH = os.path.join(BASE_DIR, "data", "stock.json")

# Load data from JSON files
with open(EMPLOYEES_PATH) as file:
    employees = json.loads(file.read())

with open(STOCK_PATH) as file:
    items = json.loads(file.read())

# Create a loader for personnel and generate insert statements
personnel_loader = Loader(model="personnel")
personnel_inserts = personnel_loader.generate_insert_statements()

# Create a loader for stock and generate insert statements
stock_loader = Loader(model="stock")
stock_inserts = stock_loader.generate_insert_statements()

# Combine all insert statements into a single list
all_inserts = personnel_inserts + stock_inserts

# Write the insert statements to a SQL file
sql_file_path = os.path.join(BASE_DIR, "insert_data.sql")
with open(sql_file_path, "w") as sql_file:
    sql_file.write("\n".join(all_inserts))

print(f"SQL insert statements written to: {sql_file_path}")

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'oatley123',
}

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Create a cursor
cursor = conn.cursor()

try:
    # Begin the transaction
    cursor.execute("BEGIN;")

    # Execute the insert statements
    for insert_statement in all_inserts:
        cursor.execute(insert_statement)

    # Commit the transaction
    cursor.execute("COMMIT;")
    print("Transaction committed successfully.")

except Exception as e:
    # If there is an error, rollback the transaction
    cursor.execute("ROLLBACK;")
    print(f"Error: {e}")
    print("Transaction rolled back.")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
