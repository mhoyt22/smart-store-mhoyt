import pandas as pd

# File paths
input_file_path = r"C:\Users\mhoyt\OneDrive - nwmissouri.edu\MIS\44432\smart-store-mhoyt\data\raw\products_data.csv"
output_file_path = r"C:\Users\mhoyt\OneDrive - nwmissouri.edu\MIS\44432\smart-store-mhoyt\data\prepared\products_data_prepared.csv"

# Clear out the existing content in the output file
open(output_file_path, 'w').close()

# Load the data
products_data = pd.read_csv(input_file_path)

# Initial count of products (rows)
initial_rows = products_data.shape[0]
print(f"Initial number of products: {initial_rows}")

# Replace blank or negative 'StockQuantity' with 0
if 'StockQuantity' in products_data.columns:
    products_data['StockQuantity'] = products_data['StockQuantity'].fillna(0)  # Replace NaN with 0
    products_data['StockQuantity'] = products_data['StockQuantity'].apply(lambda x: 0 if x < 0 else x)  # Replace negatives with 0

# Final count of products (rows)
final_rows = products_data.shape[0]
print(f"Prepared number of products: {final_rows}")

# Write the cleaned data to the new location
products_data.to_csv(output_file_path, index=False)
print(f"Cleaned product data has been saved to {output_file_path}")