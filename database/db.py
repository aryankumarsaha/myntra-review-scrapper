import sqlite3
import pandas as pd

DB_NAME = "myntra.db"

def save_to_db(df: pd.DataFrame):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("reviews", conn, if_exists="replace", index=False)
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM reviews", conn)
    conn.close()
    return df