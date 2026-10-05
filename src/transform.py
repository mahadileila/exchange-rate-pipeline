import pandas as pd

def transform_currencies(raw_currencies, currencies):
    df = pd.DataFrame(raw_currencies)
    df = df.rename(columns={"iso_code": "code"})
    df = df[["code", "name"]]

    df = df.dropna()
    df = df[df["code"].isin(currencies)]
    df = df.drop_duplicates(subset=["code"])
    return df

def transform_rates(raw_rates):
    df = pd.DataFrame(raw_rates)
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date": "rate_date", "quote": "currency_code"})
    df = df[["rate_date", "currency_code", "rate"]]

    df = df.dropna()
    df = df[df["rate"] > 0]
    df = df.drop_duplicates(subset=["rate_date", "currency_code"])

    return df
