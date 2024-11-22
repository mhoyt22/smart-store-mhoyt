# File: scripts/data_prep.py

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

# Ensure the 'data/dw' directory exists
DW_DIR.mkdir(parents=True, exist_ok=True)

def create_dw() -> None:
    """Create the data warehouse by creating Customers, Products, and Sales tables."""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQL to create Customers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date DATE,
            loyalty_points INTEGER,
            preferred_contact_method TEXT
        );
        """)

        # SQL to create Products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            stock_quantity INTEGER,
            supplier TEXT
        );
        """)

        # SQL to create Sales table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            transaction_id INTEGER PRIMARY KEY,
            sales_date DATE,
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            campaign_id INTEGER,
            sales_amount REAL,
            discount_percent INTEGER,
            payment_type TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """)

        # close the connection
        conn.close()
        logger.info("Data warehouse created successfully.")

    except sqlite3.Error as e:
        logger.error(f"Error connecting to the database: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

def main() -> None:
    """Main function to create the data warehouse."""
    logger.info("Starting data warehouse creation...")
    create_dw()
    logger.info("Data warehouse creation complete.")

if __name__ == "__main__":
    main()
