import pandas as pd
from sqlalchemy import create_engine


def read_database(database_name: str) -> dict:
    """
    Reads the specified SQLite database and returns the contents of its tables as DataFrames.

    Parameters:
        database_name (str): The name of the SQLite database file.

    Returns:
        dict: A dictionary with table names as keys and their corresponding DataFrames as values.
    """
    # Create a database engine
    engine = create_engine(f"sqlite:///{database_name}")

    # List of tables to read from the database
    table_names = ["users", "items", "sales"]

    dataframes = {}

    for table in table_names:
        try:
            dataframes[table] = pd.read_sql_table(table, engine)
        except Exception as e:
            print(f"Error reading table {table}: {e}")

    return dataframes
