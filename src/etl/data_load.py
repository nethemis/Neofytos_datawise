from sqlalchemy import create_engine


def load_data(df, database_name):

    # Create a new SQLite database (or connect to an existing one)
    # database_name = "database/my_database.db"
    engine = create_engine(f"sqlite:///{database_name}")

    # Create the 'users' table
    users_columns = ["trade_account_id", "region", "sales_territory"]
    users_df = df[users_columns].drop_duplicates()
    users_df.to_sql("users", engine, if_exists="replace", index=False)

    # Create the 'items' table
    items_columns = [
        "item_number",
        "category",
        "collection",
        "color_name",
        "style",
        "motif",
        "att_type",
    ]
    items_df = df[items_columns].drop_duplicates()
    items_df.to_sql("items", engine, if_exists="replace", index=False)

    # Create the 'sales' table
    sales_columns = [
        "cart_id",
        "created_at",
        "trade_account_id",
        "item_number",
        "type",
        "quantity",
        "revenue",
        "order_journey",
    ]
    sales_df = df[sales_columns]
    sales_df.to_sql("sales", engine, if_exists="replace", index=False)

    print("Database and tables created successfully.")
