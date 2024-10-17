from sqlalchemy import create_engine
import pandas as pd


def recommenndation_system(database_name: str):

    df = query_data(database_name)

    for category in df.category.unique():
        item_revenue = (
            df.loc[df.category == category][["item_number", "revenue"]]
            .groupby("item_number")
            .sum()
            .sort_values(by="revenue", ascending=False)
        )
        print("Top 10 items by revenue in the " + category + "category.")
        print(item_revenue.head(10))
        print()


def query_data(database_name: str):
    engine = create_engine(f"sqlite:///{database_name}")

    query = """
    SELECT
        items.category,
        items.item_number,
        revenue,
        items.style,
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


database_name = "database/my_database.db"
recommenndation_system(database_name)
