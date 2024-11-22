"""
Module 5: ETL to Data Warehouse Script
File: scripts/etl_to_dw.py
This script handles the ETL (Extract, Transform, Load) process. It extracts prepared data
from 'data/prepared/', transforms it (if needed), and loads it into the 'data/smart_sales.db' database.
"""

import pandas as pd
import sqlite3
import sys
import pathlib

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402

# Constants
DW_DIR: pathlib.Path = pathlib.Path("data").joinpath("dw")
DB_PATH: pathlib.Path = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR: pathlib.Path = pathlib.Path("data").joinpath("prepared")

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete existing records if they exist"""
    try:
        cursor.execute("DROP TABLE IF EXISTS customers;")
        cursor.execute("DROP TABLE IF EXISTS products;")
        cursor.execute("DROP TABLE IF EXISTS sales;")
        logger.info("Existing records deleted from all tables.")
    except sqlite3.Error as e:
        logger.error(f"Error deleting records: {e}")
        raise

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Verify mapping & insert 'customers' data to dw"""
    try:
        # Check required columns
        required_columns = {"CustomerID", "Name", "Region", "JoinDate", "LoyaltyPoints","PreferredContactMethod","StandardDateTime"}
        if not required_columns.issubset(customers_df.columns):
            logger.error(f"Missing columns in 'customers' DataFrame: {required_columns - set(customers_df.columns)}")
            return
        
        # Map CSV columns to database table columns
        customers_df = customers_df.rename(
            columns={
                "CustomerID": "customer_id",  
                "Name": "name",
                "Region": "region",
                "JoinDate": "join_date",
                "LoyaltyPoints": "loyalty_points",
                "PreferredContactMethod": "preferred_contact_method",
                "StandardDateTime": "standard_date_time",
            }
        )

        # Load 'customers' data
        customers_df.to_sql("customers", cursor.connection, if_exists="append", index=False)
        logger.info("'customers' data loaded.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting customers: {e}")
        raise

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Verify mapping & insert 'products' data to dw"""
    try:
        # Check required columns
        required_columns = {"ProductID", "ProductName", "Category", "UnitPrice", "StockQuantity","Supplier"}
        if not required_columns.issubset(products_df.columns):
            logger.error(f"Missing columns in 'products' DataFrame: {required_columns - set(products_df.columns)}")
            return
         
        # Map CSV columns to database table columns
        products_df = products_df.rename(
            columns={
                "ProductID": "product_id",  
                "ProductName": "product_name",
                "Category": "category",
                "UnitPrice": "unit_price",
                "StockQuantity": "stock_quantity",
                "Supplier": "supplier",
            }
        )

        # Load 'products' data
        products_df.to_sql("products", cursor.connection, if_exists="append", index=False)
        logger.info("'products' data loaded.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting products: {e}")
        raise

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Verify mapping & insert 'sales' data to dw"""
    try:
        # Check required columns
        required_columns = {"TransactionID", "SaleDate", "CustomerID", "ProductID", "StoreID","CampaignID", "SaleAmount", "DiscountPercent", "PaymentType"}
        if not required_columns.issubset(sales_df.columns):
            logger.error(f"Missing columns in 'sales' DataFrame: {required_columns - set(sales_df.columns)}")
            return
        
        # Map CSV columns to database table columns
        sales_df = sales_df.rename(
            columns={
                "TransactionID": "transaction_id",  
                "SaleDate": "sales_date",
                "CustomerID": "customer_id",
                "ProductID": "product_id",
                "StoreID": "store_id",
                "CampaignID": "campaign_id",
                "SaleAmount": "sales_amount",
                "DiscountPercent": "discount_percent",
                "PaymentType": "payment_type",
            }
        )
       
        # Load 'sales' data
        sales_df.to_sql("sales", cursor.connection, if_exists="append", index=False)
        logger.info("'sales' data loaded.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting sales: {e}")
        raise

def load_data_to_db() -> None:
    """Load prepared data into the data warehouse using the correct table names."""
    try:
        # Ensure the database directory exists
        db_dir = pathlib.Path(DB_PATH).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Drop the tables if they exist
        delete_existing_records(cursor)

        # Extract prepared data
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

        # Load data to DW
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        # Commit and close the connection
        conn.commit()
        logger.info("Prepared data successfully loaded into the data warehouse.")

    except sqlite3.Error as e:
        logger.error(f"Error during database load: {e}")

    except Exception as e:
        logger.error(f"Error during ETL: {e}")
        raise
    finally:
        if conn:
            conn.close()

def main() -> None:
    """Main function for running the ETL process."""
    logger.info("Starting etl_to_dw ...")
    load_data_to_db()
    logger.info("Finished etl_to_dw complete.")

if __name__ == "__main__":
    main()