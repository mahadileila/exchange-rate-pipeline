CREATE TABLE IF NOT EXISTS currencies (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_rates (
    rate_date     DATE          NOT NULL,
    currency_code CHAR(3)       NOT NULL REFERENCES currencies (code),
    rate          NUMERIC(18, 6) NOT NULL CHECK (rate > 0),
    PRIMARY KEY (rate_date, currency_code)
);