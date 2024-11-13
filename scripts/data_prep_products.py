# File: scripts/process_products_data.py

import pathlib
import pandas as pd
import sys

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger

# Constants
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
FILE_NAME = "products_data.csv"

def read_products_data() -> pd.DataFrame:
    """Read raw product data from CSV."""
    file_path = RAW_DATA_DIR / FILE_NAME
    try:
        logger.info(f"Reading product data from {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if file is not found
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if any other error occurs

def main() -> None:
    """Main function for processing product data."""
    logger.info("Starting product data preparation...")
    df = read_products_data()
    # Replace blank or negative 'StockQuantity' with 0
    if 'StockQuantity' in df.columns:
        df['StockQuantity'] = df['StockQuantity'].fillna(0)  # Replace NaN with 0
        df['StockQuantity'] = df['StockQuantity'].apply(lambda x: 0 if x < 0 else x)  # Replace negatives with 0
        df['StockQuantity'] = df['StockQuantity'].astype(int)
    logger.info("Product data preparation complete.")

if __name__ == "__main__":
    main()