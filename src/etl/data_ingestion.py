import pandas as pd
import sqlalchemy


def read_data():
    # Load CSV data
    df = pd.read_csv(
        "data/cart_item_22_23.csv", parse_dates=["created_at"], index_col="id"
    )
    return df


def load_data_from_db(engine):
    query = "SELECT * FROM orders;"
    df = pd.read_sql(query, engine)
    return df


if __name__ == "__main__":
    data = load_data()
    print(data.head())
