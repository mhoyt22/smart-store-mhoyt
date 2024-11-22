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
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verify database exists
        db_dir = pathlib.Path(DB_PATH).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        # Extract & Load Customers
        customers_data = extract_data(CUSTOMERS_DATA)
        logger.info("Loading customers data into database tables ...")
        customers_data.to_sql("customers", conn, if_exists="replace", index=False)
        logger.info("Customers data loaded.")

        # Extract & Load Products
        products_data = extract_data(PRODUCTS_DATA)
        logger.info("Loading products data into database tables ...")
        products_data.to_sql("products", conn, if_exists="replace", index=False)
        logger.info("Products data loaded.")

        # Extract & Load Sales
        sales_data = extract_data(SALES_DATA)
        logger.info("Loading sales data into database tables ...")
        sales_data.to_sql("sales", conn, if_exists="replace", index=False)
        logger.info("Sales data loaded.")

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