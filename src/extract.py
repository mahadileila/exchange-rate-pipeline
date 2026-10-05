import requests
from config import API_URL

def extract_rates(start_date, currencies):
    response = requests.get(
        API_URL + "/providers/ecb/rates",
        params={"from": start_date, "quotes": ",".join(currencies)},
        timeout=30,
    )
    response.raise_for_status()
    raw_rates = response.json()
    return raw_rates

def extract_currencies():
    response = requests.get(
        API_URL + "/currencies",
        timeout=30,
    )
    response.raise_for_status()
    raw_currencies = response.json()
    return raw_currencies