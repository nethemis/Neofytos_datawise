import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


def calculate_conversion_rate(database_name: str):
    """
    Item level analysis
    This part of the code is performing item-level analysis by calculating the conversion rate for
    different columns such as "region", "category", and "style".
    """
    data = query_data_item_level(database_name)

    for column in ["region", "category", "style"]:

        grouped = (
            data[data.type == "PRODUCT"]
            .groupby(by=[column, "order_journey"], as_index=False)
            .agg(counts=("order_journey", "count"))
            .sort_values(by=[column, "order_journey"], ascending=False)
        )
        grouped["percentage"] = grouped.groupby(column)["counts"].transform(
            lambda x: x / x.sum() * 100
        )
        grouped.sort_values(by="percentage", ascending=False, inplace=True)

        grouped = grouped.loc[grouped[column] != "not_applicable"]

        generate_bar_plot(data=grouped, x=column, y="percentage", hue="order_journey")

    """
    Order-level analysis:
    This part of the code is performing order-level analysis by processing the data to determine the
    purchase status for each trade account in each category. 
    
    Assumptions: An account has bought any sample and at a later time any product.
    """
    data = query_data_order_level(database_name)

    for column in ["region", "category", "style"]:

        # Create separate DataFrames for samples and products
        samples = data[data["type"] == "SAMPLE"]
        products = data[data["type"] == "PRODUCT"]

        # Find the earliest purchase for samples and products for each trade_account_id and category
        samples_earliest = (
            samples.groupby(["trade_account_id", column])["created_at"]
            .min()
            .reset_index()
        )
        samples_earliest["bought_sample"] = True

        products_earliest = (
            products.groupby(["trade_account_id", column])["created_at"]
            .min()
            .reset_index()
        )
        products_earliest["bought_product"] = True

        # Merge the two DataFrames on trade_account_id and category
        merged = pd.merge(
            samples_earliest,
            products_earliest,
            on=["trade_account_id", column],
            how="outer",
        )

        # Determine the status for each trade account in each category
        merged["status"] = None

        # Determine the purchase status
        merged.loc[
            (merged["bought_sample"] == True)
            & (merged["bought_product"] == True)
            & (merged["created_at_y"] > merged["created_at_x"]),
            "status",
        ] = "Sample then Product"
        merged.loc[
            (merged["bought_sample"] == True) & (merged["bought_product"] != True),
            "status",
        ] = "Only Sample"
        merged.loc[
            (merged["bought_product"] == True) & (merged["bought_sample"] != True),
            "status",
        ] = "Only Product"

        # Group by category and status, and count the occurrences
        grouped_counts = (
            merged.groupby([column, "status"]).size().reset_index(name="counts")
        )

        # Calculate the total counts for each category
        total_counts = grouped_counts.groupby(column)["counts"].transform("sum")

        # Calculate the percentage for each category and status combination
        grouped_counts["percentage"] = (grouped_counts["counts"] / total_counts) * 100

        # Sort the DataFrame based on category and status
        grouped_counts = grouped_counts.sort_values([column, "status"]).reset_index(
            drop=True
        )

        grouped_counts = grouped_counts.loc[grouped_counts[column] != "not_applicable"]

        generate_bar_plot(data=grouped_counts, x=column, y="percentage", hue="status")


def query_data_item_level(database_name: str):
    engine = create_engine(f"sqlite:///{database_name}")

    query = """
    SELECT
        sales.order_journey,
        users.region,
        users.trade_account_id,
        items.category,
        items.style,
        type,
        created_at        
    FROM
        sales
    JOIN
        users ON sales.trade_account_id = users.trade_account_id
    JOIN
        items ON sales.item_number = items.item_number
    WHERE
        type = 'PRODUCT'
    """

    df = pd.read_sql_query(query, engine)

    return df


def query_data_order_level(database_name: str):
    engine = create_engine(f"sqlite:///{database_name}")

    query = """
    SELECT
        sales.order_journey,
        users.region,
        users.trade_account_id,
        items.category,
        items.style,
        type,
        created_at        
    FROM
        sales
    JOIN
        users ON sales.trade_account_id = users.trade_account_id
    JOIN
        items ON sales.item_number = items.item_number
    """

    df = pd.read_sql_query(query, engine)

    return df


def generate_bar_plot(data, x, y, hue):

    plt.figure(
        figsize=(8, 4),
        dpi=100,
    )

    sns.barplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
    )

    plt.xlabel("", fontsize=1)
    plt.xticks(fontsize=10)
    plt.ylabel("order_journey percentage", fontsize=12)
    plt.yticks(fontsize=10)

    # Get the handles and labels of the axis
    handles, labels = plt.gca().get_legend_handles_labels()

    plt.title(x.capitalize(), loc="left", fontsize=20)

    # Create the legend
    plt.legend(
        handles=handles,
        title_fontsize=20,
        fontsize=9,
        bbox_to_anchor=(0.9, 1.15),
        frameon=False,
        ncol=3,
    )

    plt.tight_layout()
    plt.xticks(rotation=60)
    plt.savefig(
        "plots/" + x + "_" + y + "_" + hue + "_bar_plot.pdf",
        transparent=True,
        bbox_inches="tight",
    )

    print("Export completed: plots/" + x + "_" + y + "_" + hue + "_bar_plot.pdf")
    pass


database_name = "database/my_database.db"
calculate_conversion_rate(database_name)
