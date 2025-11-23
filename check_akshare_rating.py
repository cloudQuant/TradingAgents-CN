
import akshare as ak
import pandas as pd

try:
    print("Fetching fund_rating_all...")
    df = ak.fund_rating_all()
    print(df.head())
    print(df.columns)
except Exception as e:
    print(f"Error: {e}")
