import os
import json

from data import personnel, stock

# Create a new directory named 'data' 
data_directory = 'data'
os.makedirs(data_directory, exist_ok=True)

if __name__ == "__main__":
    # Save personnel data to JSON file
    personnel_file_path = os.path.join(data_directory, 'personnel.json')
    with open(personnel_file_path, 'w') as personnel_file:
        json.dump(personnel, personnel_file)

    # Save stock data to JSON file
    stock_file_path = os.path.join(data_directory, 'stock.json')
    with open(stock_file_path, 'w') as stock_file:
        json.dump(stock, stock_file)
