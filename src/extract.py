import pandas as pd

def extract_data():
    df = pd.read_csv(r"datas\messy_ecommerce_sales_data.csv")
    return df

