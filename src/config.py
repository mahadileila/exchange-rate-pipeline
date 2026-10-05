import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.frankfurter.dev/v2"
CURRENCIES = ["USD", "GBP", "JPY"]
START_DATE = "2026-01-01"
DB_SETTINGS = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname":os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD") 
}