import pandas as pd

# File paths
input_file_path = r"C:\Users\mhoyt\OneDrive - nwmissouri.edu\MIS\44432\smart-store-mhoyt\data\raw\sales_data.csv"
output_file_path = r"C:\Users\mhoyt\OneDrive - nwmissouri.edu\MIS\44432\smart-store-mhoyt\data\prepared\sales_data_prepared.csv"

# Clear out the existing content in the output file
open(output_file_path, 'w').close()

# Load the data
sales_data = pd.read_csv(input_file_path)

# Initial count of sales (rows)
initial_rows = sales_data.shape[0]
print(f"Initial number of sales: {initial_rows}")

# Replace blank 'DiscountPercent' with 0
if 'DiscountPercent' in sales_data.columns:
    sales_data['DiscountPercent'] = sales_data['DiscountPercent'].fillna(0)

# Replace invalid 'PaymentType' entries with 'Unknown'
valid_payment_types = ["Cash", "Card", "Gift Card"]
if 'PaymentType' in sales_data.columns:
    sales_data['PaymentType'] = sales_data['PaymentType'].apply(lambda x: x if x in valid_payment_types else "Unknown")

# Final count of sales (rows)
final_rows = sales_data.shape[0]
print(f"Prepared number of sales (rows) after cleaning: {final_rows}")

# Write the cleaned data to the new location
sales_data.to_csv(output_file_path, index=False)
print(f"Cleaned sales data has been saved to {output_file_path}")