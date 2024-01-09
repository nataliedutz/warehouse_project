import os
import json
import psycopg2
from classes import Employee, Item


def generate_sql_inserts(data, table_name):
    inserts = []
    for entry in data:
        try:
            if isinstance(entry, dict):
                # Handle dictionaries, excluding 'employee_id'
                columns = ', '.join(k for k in entry.keys() if k != 'employee_id')
                
                # Handle values, converting 'None' to 'NULL'
                values = ', '.join(
                    f"'{v}'" if v is not None and isinstance(v, str) else 'NULL' if v is None and k != 'employee_id' else str(v) for k, v in entry.items()
                )

                # Special handling for the 'head_of' attribute
                head_of_list = entry.get('head_of', [])
                
                # Construct the values string for head_of
                head_of_values = create_head_of_values(head_of_list)
                values += f", {head_of_values}" if head_of_values else ""


                insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING employee_id;"
                inserts.append(insert_statement)

        except Exception as e:
            print(f"Error generating SQL insert for entry: {entry}")
            print(f"Error details: {e}")

    return inserts



def create_values_string(values):
    # Create a string of values by joining each value
    return ', '.join(f"'{v}'" if isinstance(v, str) else str(v) for v in values)

def create_head_of_values(head_of_list):
    if head_of_list:
        # Convert the list of dictionaries to a string representation
        entries = [f"('{entry['user_name']}', '{entry['password']}')" for entry in head_of_list]
        return f"({', '.join(entries)})"
    # return 'NULL'

def write_sql_to_file(sql_statements, output_file):
    with open(output_file, 'w') as f:
        f.write('\n'.join(sql_statements))

def main():

    # Read data from JSON files
    base_dir = os.path.dirname(os.path.realpath(__file__))
    employees_path = os.path.join(base_dir, "data", "personnel.json")
    stock_path = os.path.join(base_dir, "data", "stock.json")

    employees_data = []
    with open(employees_path) as file:
        employees_data = json.loads(file.read())

    stock_data = []  
    with open(stock_path) as file:
        stock_data = json.loads(file.read())

    # Create a list of dictionaries for employees
    employees = []
    for entry in employees_data:
        employee = Employee(user_name=entry['user_name'], password=entry['password'])

        # Check if 'head_of' is present in the entry and it's a list
        if 'head_of' in entry and isinstance(entry['head_of'], list):
            head_of_list = entry['head_of']
        else:
            head_of_list = None  # Set head_of to None if not present

        employees.append({
            'name': employee._name,
            'password': employee.get_password(),
            'head_of': head_of_list
        })

    
    items = [Item(**entry) for entry in stock_data]

    # Generate SQL insert statements for employees
    employee_inserts = generate_sql_inserts(employees, 'employee')

    # Generate SQL insert statements for items
    item_inserts = generate_sql_inserts(items, 'item')

    # # Print the generated SQL insert statements
    # print("\nGenerated SQL insert statements for employees:")
    # for statement in employee_inserts:
    #     print(statement)

    # print("\nGenerated SQL insert statements for items:")
    # for statement in item_inserts:
    #     print(statement)

    all_inserts = employee_inserts + item_inserts

    sql_output_file = os.path.join(base_dir, "insert_data.sql")
    write_sql_to_file(all_inserts, sql_output_file)

    print(f"\nSQL insert statements written to: {sql_output_file}")

    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'port': '5432',
        'database': 'warehouse_management',
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

        # Execute the insert statements for employees and items
        for insert_statement in all_inserts:
            cursor.execute(insert_statement)

        # Execute the updates for head_of relationship
        for employee in employees:
            if employee.head_of:
                for head_of_employee in employee.head_of:
                    cursor.execute(f"UPDATE employee SET head_of = head_of || ARRAY['{head_of_employee['_name']}'] WHERE name = '{employee['_name']}';")

        # Commit the transaction
        cursor.execute("COMMIT;")
        print("\nTransaction committed successfully.")

    except Exception as e:
        # If there is an error, rollback the transaction
        cursor.execute("ROLLBACK;")
        print(f"\nError: {e}")
        print("Transaction rolled back.")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
