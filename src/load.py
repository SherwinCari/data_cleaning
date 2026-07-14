import pandas as pd
import os

def load_data(df: pd.DataFrame):
    os.makedirs("datas", exist_ok=True)
    df.to_csv(r"datas\cleaned_data_set.csv")