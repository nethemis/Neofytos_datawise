from etl.data_ingestion import read_data
from etl.data_cleaning import clean_data
from utils.feature_engineering import add_features
from analysis.order_journeys_analysis import order_journey_analysis
from etl.data_load import load_data
from etl.read_database import read_database


def run_etl():
    # Load and clean data

    df = read_data()
    print("Data read")

    df = clean_data(df)
    print("Data cleaned")

    # Add features for modeling
    df = add_features(df)
    print("Features added")

    # Perform order journeys analysis
    df = order_journey_analysis(df)
    print("Order journey analysis completed")
    # print(f"Order Journeys:\n{journey_analysis}")

    database_name = "database/my_database.db"
    load_data(df, database_name="database/my_database.db")
    dataframes = read_database(database_name)

    # Print the contents of each DataFrame
    for table_name, df in dataframes.items():
        print(f"\nContents of table '{table_name}':")
        print(df)


if __name__ == "__main__":
    run_etl()
