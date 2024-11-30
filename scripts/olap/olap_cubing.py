"""
Module 6: OLAP and Cubing Script
File: scripts/olap/olap_cubing.py

A cube is a precomputed, multidimensional structure 
where data is aggregated across all possible 
combinations of selected dimensions 
(e.g., DayOfWeek, ProductID).

Purpose: It allows for fast querying and analysis 
across many dimensions without needing to 
compute aggregations on the fly.
Structure: The result is stored as a 
multidimensional dataset that can be 
queried with SQL-like syntax 
or visualized in BI tools.


This example script handles OLAP cubing with Python. 
It ingests data from a data warehouse,
performs aggregations for multiple dimensions, 
and creates OLAP cubes. 
The cubes are saved as CSV files for further analysis.
Cubes might also be kept in Power BI, Snowflake, Looker, or another tool.

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

def create_olap_cube(sales_df: pd.DataFrame, dimensions: list, metrics: dict) -> pd.DataFrame:
    """Create an OLAP cube by aggregating data across multiple dimensions."""
    try:
        grouped = sales_df.groupby(dimensions)
        cube = grouped.agg(metrics).reset_index()
        cube["transaction_ids"] = grouped["transaction_id"].apply(list).reset_index(drop=True)
        explicit_columns = generate_column_names(dimensions, metrics)
        explicit_columns.append("transaction_ids")
        cube.columns = explicit_columns
        logger.info(f"OLAP cube created with dimensions: {dimensions}")
        return cube
    except Exception as e:
        logger.error(f"Error creating OLAP cube: {e}")
        raise

def generate_column_names(dimensions: list, metrics: dict) -> list:
    """Generate explicit column names for OLAP cube."""
    column_names = dimensions.copy()
    for column, agg_funcs in metrics.items():
        if isinstance(agg_funcs, list):
            for func in agg_funcs:
                column_names.append(f"{column}_{func}")
        else:
            column_names.append(f"{column}_{agg_funcs}")
    return [col.rstrip("_") for col in column_names]

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
    logger.info("Starting OLAP Cubing process...")
    sales_df = ingest_sales_data_from_dw()
    sales_df["sales_date"] = pd.to_datetime(sales_df["sales_date"])
    sales_df["DayOfWeek"] = sales_df["sales_date"].dt.day_name()
    sales_df["Month"] = sales_df["sales_date"].dt.month
    sales_df["Year"] = sales_df["sales_date"].dt.year

    dimensions = ["store_id", "discount_percent", "DayOfWeek"]
    metrics = {
        "sales_amount": ["sum", "mean"],
        "discount_percent": "mean",
        "transaction_id": "count",
    }

    olap_cube = create_olap_cube(sales_df, dimensions, metrics)
    write_cube_to_csv(olap_cube, "discount_impact_analysis_cube.csv")
    logger.info("OLAP Cubing process completed successfully.")
    logger.info(f"Please see outputs in {OLAP_OUTPUT_DIR}")

if __name__ == "__main__":
    main()