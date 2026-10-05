import pandas as pd
import psycopg2
import requests


def extract_rates(start_date, currencies):
    response = requests.get(
        "https://api.frankfurter.dev/v2/providers/ecb/rates",
        params={"from": start_date, "quotes": ",".join(currencies)},
        timeout=30,
    )
    response.raise_for_status()
    raw_rates = response.json()
    return raw_rates


def transform_rates(raw_rates):
    df = pd.DataFrame(raw_rates)
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date": "rate_date", "quote": "currency_code"})
    df = df[["rate_date", "currency_code", "rate"]]

    df = df.dropna()
    df = df[df["rate"] > 0]
    df = df.drop_duplicates(subset=["rate_date", "currency_code"])

    return df


def extract_currencies():
    response = requests.get(
        "https://api.frankfurter.dev/v2/currencies",
        timeout=30,
    )
    response.raise_for_status()
    raw_currencies = response.json()
    return raw_currencies


def transform_currencies(raw_currencies, currencies):
    df = pd.DataFrame(raw_currencies)
    df = df.rename(columns={"iso_code": "code"})
    df = df[["code", "name"]]

    df = df.dropna()
    df = df[df["code"].isin(currencies)]
    df = df.drop_duplicates(subset=["code"])
    return df


def load(currencies_df, rates_df):
    rates_rows = list(rates_df.itertuples(index=False, name=None))
    currencies_rows = list(currencies_df.itertuples(index=False, name=None))

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="exchange_rate",
        user="etl",
        password="etl",
    )

    cursor = connection.cursor()

    cursor.executemany(
        "INSERT INTO currencies (code, name) VALUES (%s, %s)"
        " ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name",
        currencies_rows,
    )
    cursor.executemany(
        "INSERT INTO daily_rates (rate_date, currency_code, rate) VALUES (%s, %s, %s)"
        " ON CONFLICT (rate_date, currency_code) DO UPDATE SET rate = EXCLUDED.rate",
        rates_rows,
    )

    connection.commit()

    cursor.close()
    connection.close()


def main():
    currencies = ["USD", "GBP", "JPY"]

    raw_currencies = extract_currencies()
    currencies_df = transform_currencies(raw_currencies, currencies)

    raw_rates = extract_rates("2026-01-01", currencies)
    rates_df = transform_rates(raw_rates)

    load(currencies_df, rates_df)
    print("Pipeline finished:", len(rates_df), "rows")


if __name__ == "__main__":
    main()
