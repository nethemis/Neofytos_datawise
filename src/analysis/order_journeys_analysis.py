import pandas as pd


def order_journey_analysis(df):

    samples = df[df["type"] == "SAMPLE"]
    products = df[df["type"] == "PRODUCT"]

    # Merge samples with corresponding products based on trade_account_id and item_number
    merged = pd.merge(
        samples,
        products,
        on=["trade_account_id", "item_number"],
        suffixes=("_sample", "_product"),
        indicator=True,
    )

    # Check if the sample purchase is before the product purchase
    merged["sample_to_product"] = (
        merged["created_at_sample"] < merged["created_at_product"]
    )

    # Merge the result back into the original DataFrame
    df = df.merge(
        merged[["trade_account_id", "item_number", "sample_to_product"]],
        on=["trade_account_id", "item_number"],
        how="left",
    )

    df.drop_duplicates(
        inplace=True,
        subset=df.keys().drop(["created_at", "cart_id", "quantity", "revenue"]),
        ignore_index=True,
    )

    # Create 'order_journey'
    df["order_journey"] = "sample_only"  # Default for samples without product
    # Set to 'direct_sale' for product purchases that have no corresponding sample
    df.loc[(df["type"] == "PRODUCT"), "order_journey"] = "direct_sale"
    # Set to 'sample_to_product' where applicable
    df.loc[
        df["sample_to_product"] & df["type"].isin(["SAMPLE", "PRODUCT"]),
        "order_journey",
    ] = "sample_to_product"

    # Drop the 'sample_to_product' column as it's no longer needed
    df = df.drop(columns=["sample_to_product"])

    return df
