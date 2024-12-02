# Python Standard Library Imports
import sys
from pathlib import Path

# External imports
from pyspark.sql import DataFrame

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Local module imports
from utils.logger import logger  # noqa: E402


def save_to_csv_and_parquet(spark_df: DataFrame, output_dir: Path, file_name: str) -> None:
    """
    Save Spark DataFrame to both CSV and Parquet formats.

    Args:
        spark_df (DataFrame): The Spark DataFrame to save.
        output_dir (Path): The directory where the files will be saved.
        file_name (str): Base name for the output files.
    """
    logger.info("Starting the save operation for CSV and Parquet files.")
    try:
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory created: {output_dir}")

        # Convert Spark DataFrame to Pandas DataFrame
        logger.info("Converting Spark DataFrame to Pandas DataFrame.")
        pandas_df = spark_df.toPandas()

        # Save to CSV
        csv_path = output_dir.joinpath( f"{file_name}.csv")
        logger.info(f"Saving DataFrame to CSV at {csv_path}.")
        pandas_df.to_csv(csv_path, index=False)

        # Save to Parquet
        parquet_path = output_dir.joinpath(f"{file_name}.parquet")
        logger.info(f"Saving DataFrame to Parquet at {parquet_path}.")
        pandas_df.to_parquet(parquet_path, index=False)

        logger.info("Save operation completed successfully.")

    except Exception as e:
        logger.error(f"Error while saving files: {e}")
        raise ValueError(f"Failed to save DataFrame to files: {e}")