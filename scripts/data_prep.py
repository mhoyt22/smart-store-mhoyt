# File: scripts/data_prep.py

import pathlib
import pandas as pd
import sys

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402
from scripts.data_preparation.data_scrubber import DataScrubber  # noqa: E402

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")
FILE_NAME = "customers_data.csv"

def read_raw_data(file_name: str) -> pd.DataFrame:
    """Read raw data from CSV."""
    file_path: pathlib.Path = RAW_DATA_DIR.joinpath(file_name)
    return pd.read_csv(file_path)

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """Save cleaned data to CSV."""
    file_path: pathlib.Path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def main() -> None:
    """Main function for pre-processing customer, product, and sales data."""
    logger.info("======================")
    logger.info("STARTING data_prep.py")
    logger.info("======================")

    logger.info("========================")
    logger.info("Starting CUSTOMERS prep")
    logger.info("========================")

    df_customers = read_raw_data("customers_data.csv")

    df_customers.columns = df_customers.columns.str.strip()  # Clean column names
    df_customers = df_customers.drop_duplicates()            # Remove duplicates

    df_customers['Name'] = df_customers['Name'].str.strip()  # Trim whitespace from column values
    df_customers = df_customers.dropna(subset=['CustomerID', 'Name'])  # Drop rows missing critical info
    
    scrubber_customers = DataScrubber(df_customers)
    scrubber_customers.check_data_consistency_before_cleaning()
    scrubber_customers.inspect_data()
    
    df_customers = scrubber_customers.handle_missing_data(fill_value="N/A")
    df_customers = scrubber_customers.parse_dates_to_add_standard_datetime('JoinDate')
    df_customers = scrubber_customers.convert_column_to_new_data_type('LoyaltyPoints', int)
    scrubber_customers.check_data_consistency_after_cleaning()

    save_prepared_data(df_customers, "customers_data_prepared.csv")

    logger.info("========================")
    logger.info("Starting PRODUCTS prep")
    logger.info("========================")

    df_products = read_raw_data("products_data.csv")

    df_products.columns = df_products.columns.str.strip()  # Clean column names
    df_products = df_products.drop_duplicates()            # Remove duplicates

    df_products['ProductName'] = df_products['ProductName'].str.strip()  # Trim whitespace from column values

    if 'StockQuantity' in df_products.columns:  # Replace blank or negative 'StockQuantity' with 0
        df_products['StockQuantity'] = df_products['StockQuantity'].fillna(0)  # Replace NaN with 0
        df_products['StockQuantity'] = df_products['StockQuantity'].apply(lambda x: 0 if x < 0 else x)  # Replace negatives with 0
        df_products['StockQuantity'] = df_products['StockQuantity'].astype(int)
    
    scrubber_products = DataScrubber(df_products)
    scrubber_products.check_data_consistency_before_cleaning()
    scrubber_products.inspect_data()

    scrubber_products.check_data_consistency_after_cleaning()
    save_prepared_data(df_products, "products_data_prepared.csv")

    logger.info("========================")
    logger.info("Starting SALES prep")
    logger.info("========================")

    df_sales = read_raw_data("sales_data.csv")

    df_sales.columns = df_sales.columns.str.strip()  # Clean column names
    df_sales = df_sales.drop_duplicates()            # Remove duplicates

    df_sales['SaleDate'] = pd.to_datetime(df_sales['SaleDate'], errors='coerce')  # Ensure sale_date is datetime
    df_sales = df_sales.dropna(subset=['TransactionID', 'SaleDate'])  # Drop rows missing key information

    
    if 'DiscountPercent' in df_sales.columns: # Replace blank 'DiscountPercent' with 0
        df_sales['DiscountPercent'] = df_sales['DiscountPercent'].fillna(0)
        df_sales['DiscountPercent'] = df_sales['DiscountPercent'].astype(int)

    valid_payment_types = ["Cash", "Card", "Gift Card"]
    if 'PaymentType' in df_sales.columns: # Replace invalid 'PaymentType' entries with 'Unknown'
        df_sales['PaymentType'] = df_sales['PaymentType'].apply(lambda x: x if x in valid_payment_types else "Unknown")
    
    scrubber_sales = DataScrubber(df_sales)
    scrubber_sales.check_data_consistency_before_cleaning()
    scrubber_sales.inspect_data()
    
    df_sales = scrubber_sales.handle_missing_data(fill_value="Unknown")
    scrubber_sales.check_data_consistency_after_cleaning()

    save_prepared_data(df_sales, "sales_data_prepared.csv")

    logger.info("======================")
    logger.info("FINISHED data_prep.py")
    logger.info("======================")

if __name__ == "__main__":
    main()