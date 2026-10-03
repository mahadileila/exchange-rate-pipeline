import pandas as pd
import psycopg2
import requests


def extract(start_date, currencies):
    response  = requests.get(
        "https://api.frankfurter.dev/v2/providers/ecb/rates",
        params={"from": start_date, "quotes": ",".join(currencies)},
        timeout=30,
    )
    response.raise_for_status()
    raw_rates = response.json()
    return raw_rates


def transform(raw_rates):
    df = pd.DataFrame(raw_rates)
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date": "rate_date", "quote": "currency_code"})
    df = df[["rate_date", "currency_code", "rate"]]

    df = df.dropna()
    df = df[df["rate"] > 0]
    df = df.drop_duplicates(subset=["rate_date", "currency_code"])

    return df


def load(df):
    rows  = list(df.itertuples(index=False, name=None))

    connection = psycopg2.connect(
        host="localhost", port=5432,
        dbname="exchange_rate", user="etl", password="etl",
    )

    cursor = connection.cursor()

    cursor.executemany(
        "INSERT INTO daily_rates (rate_date, currency_code, rate) VALUES (%s, %s, %s)"
        " ON CONFLICT (rate_date, currency_code) DO UPDATE SET rate = EXCLUDED.rate",
        rows
    )

    connection.commit()

    cursor.close()
    connection.close()


def main():
    raw_rates = extract("2026-01-01", ["USD", "GBP"])
    df = transform(raw_rates)

    load(df)
    print("Pipeline finished:", len(df), "rows")


if __name__ == "__main__":
    main()