# Python Standard Library Imports
import sys
from pathlib import Path

# External imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Local module imports
from utils.logger import logger  # noqa: E402


def visualize_sales_count(csv_file_path: Path) -> None:
    """
    Visualize sales count data saved in CSV format.

    Args:
        csv_file_path (Path): Path to the CSV file containing sales count data.
    """
    try:
        # Ensure the file exists
        if not csv_file_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_file_path}")

        # Load the data
        logger.info(f"Loading data from CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)

        # Check if required columns exist
        required_columns = {"ProductID", "sum(Count)"}
        if not required_columns.issubset(df.columns):
            raise ValueError(
                f"Missing required columns: {required_columns - set(df.columns)}"
            )

        # Rename columns for clarity
        df.rename(columns={"sum(Count)": "TotalSalesCount"}, inplace=True)

        # Plot using seaborn
        logger.info("Creating bar plot for sales count by product.")
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x="ProductID", 
            y="TotalSalesCount", 
            data=df, 
            hue="ProductID",
            palette="viridis",
            dodge=False,  # Since `hue` matches `x`, set dodge=False
            legend=False
            )
        plt.title("Sales Count by Product")
        plt.xlabel("Product ID")
        plt.ylabel("Total Sales Count")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save and show the plot
        output_plot_path = csv_file_path.parent.joinpath(
            "sales_count_visualization.png"
        )
        plt.savefig(output_plot_path)
        logger.info(f"Visualization saved to: {output_plot_path}")
        plt.show()

    except Exception as e:
        logger.error(f"An error occurred during visualization: {e}")
        raise ValueError(f"Failed to visualize data: {e}")

def visualize_cubed_sales_stacked(cubed_df_path: Path):
    """Visualize cubed sales data as a stacked bar chart."""

    logger.info(f"Reading cubed sales data from {cubed_df_path}.")
    cubed_df = pd.read_csv(cubed_df_path)

    # Convert day of the week to names
    day_of_week_map = {
        1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday",
        5: "Thursday", 6: "Friday", 7: "Saturday"
    }
    cubed_df["DayOfWeek"] = cubed_df["DayOfWeek"].map(day_of_week_map)

    # Pivot the data to reshape for stacked bar chart
    pivot_table = cubed_df.pivot_table(
        index="DayOfWeek", columns="StoreID", values="TotalSales", aggfunc="sum"
    ).fillna(0)

    # Plot stacked bar chart
    pivot_table.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 6),
        colormap="viridis"
    )

    plt.title("Total Sales by Day of the Week (Stacked by StoreID)")
    plt.xlabel("Day of Week")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="StoreID", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()