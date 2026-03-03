CREATE DATABASE cross_market;
USE cross_market;
CREATE TABLE cryptocurrencies (
    id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(100),
    current_price DECIMAL(18,6),
    market_cap BIGINT,
    market_cap_rank INT,
    total_volume BIGINT,
    circulating_supply DECIMAL(20,6),
    total_supply DECIMAL(20,6),
    ath DECIMAL(18,6),
    atl DECIMAL(18,6),
    date DATE
);
CREATE TABLE crypto_prices (
    coin_id VARCHAR(50),
    date DATE,
    price_usd DECIMAL(18,6),
    PRIMARY KEY (coin_id, date),
    FOREIGN KEY (coin_id) REFERENCES cryptocurrencies(id)
);
CREATE TABLE oil_prices (
    date DATE PRIMARY KEY,
    price_usd DECIMAL(18,6)
);
CREATE TABLE stock_prices (
    date DATE,
    open DECIMAL(18,6),
    high DECIMAL(18,6),
    low DECIMAL(18,6),
    close DECIMAL(18,6),
    volume BIGINT,
    ticker VARCHAR(20),
    PRIMARY KEY (date, ticker)
);