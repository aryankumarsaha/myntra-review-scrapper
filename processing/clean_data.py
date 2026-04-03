import pandas as pd

def clean_data(df):
    # Clean Price
    df["Price"] = df["Price"].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df["Price"] = pd.to_numeric(df["Price"], errors='coerce')

    # Clean Rating (IMPORTANT FIX)
    df["Rating"] = df["Rating"].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

    # Remove missing
    df = df.dropna()

    return df