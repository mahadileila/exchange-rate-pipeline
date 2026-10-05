import psycopg2
from config import DB_SETTINGS

def load(currencies_df, rates_df):
    rates_rows = list(rates_df.itertuples(index=False, name=None))
    currencies_rows = list(currencies_df.itertuples(index=False, name=None))

    connection = psycopg2.connect(**DB_SETTINGS)

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