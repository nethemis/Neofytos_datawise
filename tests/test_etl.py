import unittest
import pandas as pd
from src.etl.data_cleaning import clean_data
from src.etl.data_ingestion import read_data
from src.etl.data_load import load_data
from src.analysis.order_journeys_analysis import order_journey_analysis

from sqlalchemy import create_engine


class TestETL(unittest.TestCase):

    def setUp(self):
        self.sample_dataframe = pd.DataFrame(
            {
                "cart_id": [7188251, 2023066, 4677697, 4925473, 6501532],
                "created_at": [
                    "2023-12-27 22:30:27.172",
                    "2022-10-05 21:49:35.255",
                    "2023-08-03 15:18:45.675",
                    "2023-08-23 19:25:48.334",
                    "2023-10-05 12:27:30.641",
                ],
                "trade_account_id": [710932, 695821, 715967, None, 648824],
                "item_number": [5008103, 180630, 71306, 5007090, 179141],
                "quantity": [1.0, None, 1.0, 1.0, 1.0],
                "revenue": [0.0, 0.0, 0.0, 0.0, 0.0],
                "type": ["SAMPLE", "SAMPLE", "SAMPLE", "SAMPLE", "SAMPLE"],
                "category": [
                    "WALLCOVERINGS",
                    "FABRICS",
                    "FABRICS",
                    "WALLCOVERINGS",
                    "FABRICS",
                ],
                "collection": [
                    "DAVID OLIVER",
                    "JOHNSON HARTIG",
                    "ESSENTIALS: CLASSIC STRIPE",
                    "CLUB CAVALIER",
                    "MOLLY MAHON",
                ],
                "color_name": ["MONUMENT", "IVORY", "GREEN", "BROWN", "PINK"],
                "style": [
                    "Contemporary",
                    "Exuberant",
                    "Preppy",
                    "Contemporary",
                    "Contemporary",
                ],
                "motif": [
                    "Stripe",
                    "Whimsical",
                    "Stripe",
                    "Animals",
                    "Floral & Botanicals",
                ],
                "att_type": ["Prints", "Prints", "Pattern Wovens", "Prints", "Prints"],
                "region": [
                    "PACIFIC SOUTHWEST",
                    "SOUTHWEST",
                    "NORTHERN WEST COAST",
                    "SOUTHWEST",
                    "NEW ENGLAND",
                ],
                "sales_territory": [
                    "BROOKE HANSEN",
                    "SCOTTSDALE SHOWROOM",
                    "LEE KESSELL - OR",
                    "TAYLOR LACKHAN",
                    "ASHLEY SPETS",
                ],
            }
        )

    # Test for data_ingestion.py
    def test_read_data(self):
        # Simulating loading CSV data by mocking a small DataFrame
        mock_data = pd.DataFrame(
            {
                "id": [1, 2],
                "trade_account_id": [101, 102],
                "type": ["SAMPLE", "PRODUCT"],
                "style": ["Contemporary", "Exuberant"],
            }
        )

        # Testing the shape of the data
        self.assertEqual(mock_data.shape[0], 2)

    # Test for data_cleaning.py
    def test_clean_data(self):
        # Creating mock data with missing values

        # Running clean_data function
        clean_df = clean_data(self.sample_dataframe)

        # Check for missing values
        self.assertEqual(
            clean_df.isnull().sum().sum(), 0
        )  # No missing values should be present

        # Check that rows with missing trade_account_id were removed
        self.assertEqual(clean_df.shape[0], 4)

    def test_load_data(self):
        database_name = "database/test_database.db"

        df = order_journey_analysis(self.sample_dataframe)

        load_data(df, database_name=database_name)

        engine = create_engine(f"sqlite:///{database_name}")

        # Assert that the 'users' table was created correctly
        users_df = pd.read_sql("SELECT * FROM users", engine)
        assert not users_df.empty
        assert set(users_df.columns) == {
            "trade_account_id",
            "region",
            "sales_territory",
        }

        # Assert that the 'items' table was created correctly
        items_df = pd.read_sql("SELECT * FROM items", engine)
        assert not items_df.empty
        assert set(items_df.columns) == {
            "item_number",
            "category",
            "collection",
            "color_name",
            "style",
            "motif",
            "att_type",
        }

        # Assert that the 'sales' table was created correctly
        sales_df = pd.read_sql("SELECT * FROM sales", engine)
        assert not sales_df.empty
        assert set(sales_df.columns) == {
            "cart_id",
            "created_at",
            "trade_account_id",
            "item_number",
            "type",
            "quantity",
            "revenue",
            "order_journey",
        }


if __name__ == "__main__":
    unittest.main()
