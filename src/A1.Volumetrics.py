import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


def get_volumetrics(database_name: str):
    data = query_data(database_name)
    print("data: ", data.head())

    labels = (
        data["order_journey"].str.replace("_", " ").str.capitalize()
    )  # ["Direct sales", "Sample to product"]

    generate_pie_chart(
        x=data["Count"],
        labels=labels,
        title="Order Journey Distribution by number of orders",
        filename="order_journey_by_orders",
    )

    generate_pie_chart(
        x=data["Sum"],
        labels=labels,
        title="Order Journey Distribution by total revenue",
        filename="order_journey_by_revenue",
    )


def query_data(database_name: str):
    # Create a database engine
    engine = create_engine(f"sqlite:///{database_name}")

    # Modify the SQL query to perform GROUP BY, COUNT, SUM, and ORDER BY
    query = """
    SELECT 
        order_journey, 
        COUNT(order_journey) AS Count, 
        SUM(revenue) AS Sum
    FROM 
        sales
    WHERE
        type = 'PRODUCT'
    GROUP BY 
        order_journey
    ORDER BY 
        Sum DESC
    """

    df = pd.read_sql_query(query, engine)

    return df


def generate_pie_chart(x, labels, title, filename):
    """
    Generates a pie chart for the order journey distribution based on queried data.

    Parameters:
        database_name (str): The name of the SQLite database file.
    """
    # Query the data from the database

    plt.figure(figsize=(8, 8))
    plt.pie(
        x=x,
        labels=labels,
        autopct="%1.1f%%",
        textprops={"fontsize": 18},
        startangle=180,
        colors=sns.color_palette("pastel"),
        explode=(0.005, 0.005),
    )

    # Add a title
    plt.title(title, fontsize=16)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.axis("equal")

    plt.savefig("plots/" + filename + ".pdf", transparent=True)
    print("Generated " + filename + " pie chart!")
    pass


database_name = "database/my_database.db"
get_volumetrics(database_name)
