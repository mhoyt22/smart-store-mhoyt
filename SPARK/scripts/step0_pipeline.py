# Python Standard Library Imports
import sys
from pathlib import Path

# External imports
from pyspark.sql import SparkSession

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Local module imports - REMEMBER TO IMPORT YOUR NEW FUNCTIONS HERE
from utils.logger import logger  # noqa: E402
from scripts.step1_extract import read_csv                  # noqa: E402
from scripts.step2_transform import calculate_sales_count, cube_sales_by_date_and_store   # noqa: E402
from scripts.step3_load import save_to_csv_and_parquet      # noqa: E402
from scripts.step4_visualize import visualize_sales_count, visualize_cubed_sales_stacked   # noqa: E402  

def main():
    """
    Main function to orchestrate the Spark pipeline.
    """
    logger.info("Starting Spark Sales Analysis Pipeline")

    # Initialize SparkSession
    spark = SparkSession.builder.appName("Spark Sales Analysis").getOrCreate()
    
    try:
        # File Paths
        data_dir = PROJECT_ROOT.joinpath("data")
        products_file = data_dir.joinpath("prepared", "products_data_prepared.csv")
        sales_file = data_dir.joinpath("prepared", "sales_data_prepared.csv")
        output_dir = data_dir.joinpath("output")

        # Step 1: Extract
        logger.info("Step 1: Extract - Reading data files")
        products_df = read_csv(spark, products_file)
        sales_df = read_csv(spark, sales_file)

        # Step 2: Transform
        logger.info("Step 2: Transform - Calculating sales count")
        sales_count_df = calculate_sales_count(products_df, sales_df)

        logger.info("Step 2: Transform - Calculating cube sales by date")
        cubed_sales_by_date_and_store_df = cube_sales_by_date_and_store(sales_df)


        # Step 3: Load
        logger.info("Step 3: Load - Saving results")
        save_to_csv_and_parquet(sales_count_df, output_dir, "sales_count")
        save_to_csv_and_parquet(cubed_sales_by_date_and_store_df, output_dir, "cubed_sales_by_date_and_store")

        # Step 4: Visualize
        logger.info("Step 4: Visualize - Generating sales count chart")
        visualize_sales_count(output_dir.joinpath("sales_count.csv"))
        visualize_cubed_sales_stacked(output_dir.joinpath("cubed_sales_by_date_and_store.csv"))

        logger.info("Pipeline execution completed successfully.")
    
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
    
    finally:
        # Stop SparkSession
        logger.info("Stopping SparkSession")
        spark.stop()

if __name__ == "__main__":
    main()