from extract import extract_currencies, extract_rates
from transform import transform_currencies, transform_rates
from load import load
from config import CURRENCIES, START_DATE

def main():
    raw_currencies = extract_currencies()
    currencies_df = transform_currencies(raw_currencies, CURRENCIES)

    raw_rates = extract_rates(START_DATE, CURRENCIES)
    rates_df = transform_rates(raw_rates)

    load(currencies_df, rates_df)
    print("Pipeline finished:", len(rates_df), "rows")


if __name__ == "__main__":
    main()