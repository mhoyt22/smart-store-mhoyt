# Python Standard Library Imports
import sys
from pathlib import Path

# External imports
from pyspark.sql import DataFrame
from pyspark.sql.functions import year, month, dayofweek, col, sum as spark_sum

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Local module imports
from utils.logger import logger  # noqa: E402

def calculate_sales_count(products_df: DataFrame, sales_df: DataFrame) -> DataFrame:
    """
    Calculate product sales count by joining product and sales data and grouping by ProductID.

    Args:
        products_df (DataFrame): Spark DataFrame containing product details.
        sales_df (DataFrame): Spark DataFrame containing sales details.

    Returns:
        DataFrame: Spark DataFrame with product sales count.
    """
    logger.info("Starting transformation: calculating sales count by product.")
    try:
        # Join sales data with product details and calculate count
        sales_with_count = sales_df.join(
            products_df.select("ProductID", "UnitPrice"),
            on="ProductID"
        ).withColumn("Count", col("SaleAmount") / col("UnitPrice"))

        # Group by ProductID to calculate total count
        count_by_product = sales_with_count.groupBy("ProductID").sum("Count")
        logger.info("Transformation completed successfully.")
        return count_by_product

    except Exception as e:
        logger.error(f"Error during transformation: {e}")
        raise ValueError(f"Error during transformation: {e}")


def cube_sales_by_date(sales_df: DataFrame) -> DataFrame:
    """Cube sales data by Year, Month, and DayOfWeek."""
    try:
        logger.info("Cubing sales data by Year, Month, and DayOfWeek.")
        cubed_df = sales_df.withColumn("Year", year(col("SaleDate"))) \
                           .withColumn("Month", month(col("SaleDate"))) \
                           .withColumn("DayOfWeek", dayofweek(col("SaleDate")))

        cubed_sales = cubed_df.groupBy("Year", "Month", "DayOfWeek").agg(
            spark_sum("SaleAmount").alias("TotalSales")
        )
        return cubed_sales
    except Exception as e:
        raise ValueError(f"Error during cubing: {e}")
    

def cube_sales_by_date_and_store(sales_df: DataFrame) -> DataFrame:
    """
    Cube sales data by Year, Month, DayOfWeek, and StoreID.

    Args:
        sales_df (DataFrame): Input sales DataFrame.

    Returns:
        DataFrame: Cubed sales DataFrame.
    """
    try:
        logger.info("Cubing sales data by Year, Month, DayOfWeek, and StoreID.")

        # Add Year, Month, and DayOfWeek columns
        cubed_df = sales_df.withColumn("Year", year(col("SaleDate"))) \
                           .withColumn("Month", month(col("SaleDate"))) \
                           .withColumn("DayOfWeek", dayofweek(col("SaleDate")))

        # Group by Year, Month, DayOfWeek, and StoreID, and aggregate Total Sales
        cubed_sales = cubed_df.groupBy("Year", "Month", "DayOfWeek", "StoreID").agg(
            spark_sum("SaleAmount").alias("TotalSales")
        )
        
        logger.info("Cubing completed successfully.")
        return cubed_sales

    except Exception as e:
        logger.error(f"Error during cubing: {e}")
        raise ValueError(f"Error during cubing: {e}")