from extract import extract_data
from transform import transform_data
from load import load_data

def run():
    data = extract_data()

    clean = transform_data(data)
    
    load_data(clean)

run()