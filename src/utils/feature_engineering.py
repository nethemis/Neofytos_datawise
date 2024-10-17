def add_features(df):
    df["month"] = df["created_at"].dt.month
    return df
