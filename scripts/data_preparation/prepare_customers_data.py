import pandas as pd

# File paths
input_file_path = r"C:\Users\mhoyt\OneDrive - nwmissouri.edu\MIS\44432\smart-store-mhoyt\data\raw\customer_data.csv"
output_file_path = r"C:\Users\mhoyt\OneDrive - nwmissouri.edu\MIS\44432\smart-store-mhoyt\data\prepared\customers_data_prepared.csv"

# Load the data
customer_data = pd.read_csv(input_file_path)

# Clear out the existing content in the output file
open(output_file_path, 'w').close()

# Initial counts of columns and rows (customers)
initial_rows = customer_data.shape[0]
print(f"Initial number of customers: {initial_rows}")

# Remove duplicates
customer_data = customer_data[customer_data['Name'] != 'Hermione Grager']

# Round 'LoyaltyPoints' column to whole numbers
if 'LoyaltyPoints' in customer_data.columns:
    customer_data['LoyaltyPoints'] = customer_data['LoyaltyPoints'].round(0).astype(int)

# Final counts of columns and rows (customers)
final_rows = customer_data.shape[0]
print(f"Prepared number of customers: {final_rows}")

# Write the cleaned data to the new location
customer_data.to_csv(output_file_path, index=False)
print(f"Cleaned customer data has been saved to {output_file_path}")