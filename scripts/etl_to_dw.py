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

def load_data_to_db() -> None:
    """Load prepared data into the data warehouse using the correct table names."""
    try:
        # Connect to the SQLite database
        db_dir = pathlib.Path(DB_PATH).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

        # Drop the tables if they exist
        logger.info("Dropping existing tables if they exist...")
        cursor.execute("DROP TABLE IF EXISTS customers;")
        cursor.execute("DROP TABLE IF EXISTS products;")
        cursor.execute("DROP TABLE IF EXISTS sales;")
        conn.commit()
        logger.info("Existing tables dropped.")

        # Extract & Load Customers
        customers_file_path = PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv")
        try:
            logger.info("Extracting 'customers' data...")
            customers_data = pd.read_csv(customers_file_path)
            logger.info("'customers' data extracted.")
        except Exception as e:
            logger.error("Error extracting data from 'customer'")
            raise
        logger.info("Loading 'customers' data...")
        customers_data.to_sql("customers", conn, if_exists="replace", index=False)
        logger.info("'customers' data loaded.")

        # Extract & Load Products
        products_file_path = PREPARED_DATA_DIR.joinpath("products_data_prepared.csv")
        try:
            logger.info("Extracting 'products' data...")
            products_data = pd.read_csv(products_file_path)
            logger.info("'products' data extracted.")
        except Exception as e:
            logger.error("Error extracting data from 'prodcuts'")
            raise
        logger.info("Loading 'prodcuts' data...")
        products_data.to_sql("products", conn, if_exists="replace", index=False)
        logger.info("'products' data loaded.")

        # Extract & Load Sales
        sales_file_path = PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv")
        try:
            logger.info("Extracting 'sales' data...")
            sales_data = pd.read_csv(sales_file_path)
            logger.info("'sales' data extracted.")
        except Exception as e:
            logger.error("Error extracting data from 'sales'")
            raise
        logger.info("Loading 'sales' data...")
        sales_data.to_sql("sales", conn, if_exists="replace", index=False)
        logger.info("'sales' data loaded.")

        # Close connection
        conn.commit()
        conn.close()
        logger.info("Data successfully loaded into database and connection closed.")

    except Exception as e:
        logger.error(f"Error during ETL: {e}")
        raise


def main() -> None:
    """Main function for running the ETL process."""
    logger.info("Starting etl_to_dw ...")
    load_data_to_db()
    logger.info("Finished etl_to_dw complete.")

if __name__ == "__main__":
    main()