import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

API_URL = "https://api.frankfurter.dev/v2"
CURRENCIES = ["USD", "GBP", "JPY"]
START_DATE = "2026-01-01"
DB_SETTINGS = {
    host,
    port,
    name,
    user,
    password
}