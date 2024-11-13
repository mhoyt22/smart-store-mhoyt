# File: scripts/process_sales_data.py

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
FILE_NAME = "sales_data.csv"

def read_sales_data() -> pd.DataFrame:
    """Read raw sales data from CSV."""
    file_path = RAW_DATA_DIR / FILE_NAME
    try:
        logger.info(f"Reading sales data from {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if file is not found
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if any other error occurs

def main() -> None:
    """Main function for processing sales data."""
    logger.info("Starting sales data preparation...")
    df = read_sales_data()
    # Replace blank 'DiscountPercent' with 0
    if 'DiscountPercent' in df.columns:
        df['DiscountPercent'] = df['DiscountPercent'].fillna(0)
        df['DiscountPercent'] = df['DiscountPercent'].astype(int)
    # Replace invalid 'PaymentType' entries with 'Unknown'
    valid_payment_types = ["Cash", "Card", "Gift Card"]
    if 'PaymentType' in df.columns:
        df['PaymentType'] = df['PaymentType'].apply(lambda x: x if x in valid_payment_types else "Unknown")
    logger.info("Sales data preparation complete.")

if __name__ == "__main__":
    main()