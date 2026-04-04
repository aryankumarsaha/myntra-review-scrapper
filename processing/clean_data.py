import pandas as pd

def clean_data(df):
    if df is None or df.empty:
        return pd.DataFrame()

    df.columns = [col.strip() for col in df.columns]

    required_cols = ["Price", "Rating", "Product Name", "Comment"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df["Price"] = df["Price"].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df["Price"] = pd.to_numeric(df["Price"], errors='coerce')

    df["Rating"] = df["Rating"].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

    # ⚠ safer cleaning
    df = df[df["Comment"].notna()]

    return df
# import pandas as pd

# def clean_data(df):
#     df["Price"] = df["Price"].astype(str).str.replace(r'[^0-9]', '', regex=True)
#     df["Price"] = pd.to_numeric(df["Price"], errors='coerce')

#     df["Rating"] = df["Rating"].astype(str).str.replace(r'[^0-9.]', '', regex=True)
#     df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

#     df = df.dropna()

#     return df
