def clean_data(df):

    df.fillna(
        value={
            col: "not_applicable" for col in df.select_dtypes(include="object").columns
        },
        inplace=True,
    )

    # Simplify the dataset by aggregating together order of the same client, item, type, etc
    # In order to simplify the analysis, without losing information.
    df = df.groupby(
        ["cart_id", "created_at", "trade_account_id", "item_number", "type"],
        as_index=False,
    ).agg(
        {
            "quantity": "sum",
            "revenue": "sum",
            **{
                col: "first"
                for col in df.columns
                if col
                not in [
                    "cart_id",
                    "created_at",
                    "trade_account_id",
                    "item_number",
                    "type",
                    "quantity",
                    "revenue",
                ]
            },
        }
    )

    df["style"] = df["style"].str.replace("0,Country", "Country")

    return df
