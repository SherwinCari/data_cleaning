import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import requests
import os
from dotenv import load_dotenv
import datetime as dt



#Uses utc +8 Philippine Standard Time

load_dotenv()

def extract_data(city):
  url = "https://api.openweathermap.org/data/2.5/weather"
  params = {
        "q" : city,
        "appid" : os.getenv("openweatherapi"),
        "units" : "metric"
    }
  response = requests.get(url, params=params)
  data = response.json()

  result = {
      "location": data["name"],
      "country": data["sys"]["country"],
      "temperature": data["main"]["temp"],
      "feels_like": data["main"]["feels_like"],
      "temp_min": data["main"]["temp_min"],
      "temp_max": data["main"]["temp_max"],
      "pressure": data["main"]["pressure"],
      "humidity": data["main"]["humidity"],
      "weather": data["weather"][0]["description"],
      "wind_speed": data["wind"]["speed"],
      "wind_direction": data["wind"].get("deg"),
      "cloudiness": data["clouds"]["all"],
      "visibility": data.get("visibility"),
      "sunrise": data["sys"]["sunrise"],   # unix timestamp
      "sunset": data["sys"]["sunset"],     # unix timestamp
      "timestamp": data["dt"],             # when this reading was recorded
  }

  return result

def transform_data(raw_data):
  df = pd.DataFrame(raw_data)
  df = df.drop_duplicates()

  df["temperature"] = df["temperature"].round(1)

  df["sunrise"] = pd.to_datetime(df["sunrise"], unit="s", utc=True).dt.tz_convert("Asia/Manila").dt.tz_localize(None)
  df["sunset"] = pd.to_datetime(df["sunset"], unit="s", utc=True).dt.tz_convert("Asia/Manila").dt.tz_localize(None)
  df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("Asia/Manila").dt.tz_localize(None)

  df = df.drop_duplicates()

  return df


def load_data(df: pd.DataFrame):
  
  os.makedirs("datas", exist_ok = True)
  df.to_csv(r"datas\weather_data.csv", index=False)

  engine = create_engine("postgresql://postgres:admin123@localhost:5432/weather_data")

  try:
    df.to_sql("weather", engine, if_exists="append", index=False)
    print(f"Insert Successful : {len(df)} rows")
  except Exception as e:
    print(f"Insert Failed: {e}")






if __name__ == "__main__": 
  cities = ["Copenhagen", "Zurich", "Helsinki"]
  raw_data = [extract_data(city) for city in cities]
  transform = transform_data(raw_data)
  load_data(transform)