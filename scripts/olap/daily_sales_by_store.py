"""
Module 6: OLAP and Cubing Script 2
File: scripts/olap/daily_sales_by_store.py

Purpose: Identify the store with the highest sales by day of the week.

This example script handles OLAP cubing with Python. 
It ingests data from a data warehouse,
performs aggregations for multiple dimensions, 
and creates OLAP cubes. 
The cubes are saved as CSV files for further analysis.
"""

import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger

# Constants
DW_DIR: pathlib.Path = pathlib.Path("data").joinpath("dw")
DB_PATH: pathlib.Path = DW_DIR.joinpath("smart_sales.db")
OLAP_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("olap_cubing_outputs")

# Create output directory if it does not exist
OLAP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def ingest_sales_data_from_dw() -> pd.DataFrame:
    """Ingest sales data from SQLite data warehouse."""
    try:
        conn = sqlite3.connect(DB_PATH)
        sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
        conn.close()
        logger.info("Sales data successfully loaded from SQLite data warehouse.")
        return sales_df
    except Exception as e:
        logger.error(f"Error loading sales table data from data warehouse: {e}")
        raise

def create_daily_sales_cube(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily sales by store and identify the store with the most sales by day of the week."""
    try:
        sales_df["sales_date"] = pd.to_datetime(sales_df["sales_date"])
        sales_df["DayOfWeek"] = sales_df["sales_date"].dt.day_name()

        # Aggregate sales by store and day of the week
        grouped = sales_df.groupby(["DayOfWeek", "store_id"])["sales_amount"].sum().reset_index()

        # Identify the store with the highest sales for each day of the week
        max_sales = grouped.loc[grouped.groupby("DayOfWeek")["sales_amount"].idxmax()].reset_index(drop=True)
        max_sales.rename(columns={"sales_amount": "max_sales_amount"}, inplace=True)

        logger.info("Daily sales cube created with the highest sales by store and day of the week.")
        return max_sales
    except Exception as e:
        logger.error(f"Error creating daily sales cube: {e}")
        raise

def write_cube_to_csv(cube: pd.DataFrame, filename: str) -> None:
    """Write the OLAP cube to a CSV file."""
    try:
        output_path = OLAP_OUTPUT_DIR.joinpath(filename)
        cube.to_csv(output_path, index=False)
        logger.info(f"OLAP cube saved to {output_path}.")
    except Exception as e:
        logger.error(f"Error saving OLAP cube to CSV file: {e}")
        raise

def main():
    """Main function for OLAP cubing."""
    logger.info("Starting OLAP Cubing process for daily sales by store...")
    sales_df = ingest_sales_data_from_dw()
    daily_sales_cube = create_daily_sales_cube(sales_df)
    write_cube_to_csv(daily_sales_cube, "daily_sales_by_store.csv")
    logger.info("OLAP Cubing process completed successfully.")
    logger.info(f"Please see outputs in {OLAP_OUTPUT_DIR}")

if __name__ == "__main__":
    main()