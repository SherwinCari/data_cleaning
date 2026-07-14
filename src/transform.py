import pandas as pd

def transform_data(df):

    #remove duplicates if there are any
    df = df.drop_duplicates()
    # Column name
    df.columns = df.columns.str.strip()

    # Date
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors='coerce')
    df["Order_Date"] = df["Order_Date"].fillna(df["Order_Date"].median())
    df["Order_Date"] = df["Order_Date"].dt.strftime("%m/%d/%Y")

    # category
    df["Category"] = df["Category"].str.strip().str.title()
    df["Product"] = df["Product"].str.strip().str.title()
    df["Category"] = df["Category"].replace({"Electronic": "Electronics"})
    product_to_category = (
    df.dropna(subset=["Category"])
        .groupby("Product")["Category"]
        .agg(lambda x: x.mode()[0])
    )
    df["Category"] = df["Category"].fillna(df["Product"].map(product_to_category))

    # quantity
    df["Quantity"] = df["Quantity"].astype(str).str.extract(r'(\d+)')[0]
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Quantity"] = df["Quantity"].replace("-", "")
    df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
    df["Quantity"] = df["Quantity"].astype(int)

    # price 
    df["Price"] = df["Price"].astype(str).str.extract(r'(\d+\.?\d*)')[0]    
    df["Price"] = pd.to_numeric(df["Price"], errors='coerce')
    df["Price"] = df["Price"].replace("-","")
    df["Price"] = df["Price"].fillna(df["Price"].median()).round(2)
    # Total
    df["Total"] = None
    df["Total"] = pd.to_numeric(df["Total"], errors='coerce')
    df["Total"] = df["Total"].fillna(df["Quantity"] * df["Price"]).round(2)

    df = df.drop_duplicates() 
    return df