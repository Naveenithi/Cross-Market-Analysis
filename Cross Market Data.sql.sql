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
SELECT name, market_cap
FROM cryptocurrencies
ORDER BY market_cap DESC
LIMIT 3;
SELECT name
FROM cryptocurrencies
WHERE circulating_supply >= 0.9 * total_supply;
SELECT name, current_price, ath
FROM cryptocurrencies
WHERE current_price >= 0.9 * ath;
SELECT MAX(price_usd)
FROM crypto_prices
WHERE coin_id = 'bitcoin';
SELECT 
(
 (MAX(price_usd) - MIN(price_usd)) / MIN(price_usd)
) * 100 AS percent_change
FROM crypto_prices
WHERE coin_id = 'bitcoin';
SELECT MAX(price_usd)
FROM oil_prices;
SELECT 
YEAR(date) AS year,
MAX(price_usd) - MIN(price_usd) AS volatility
FROM oil_prices
GROUP BY YEAR(date);
SELECT MAX(close)
FROM stock_prices
WHERE ticker = '^IXIC';
SELECT 
ticker,
YEAR(date) AS year,
MONTH(date) AS month,
AVG(close) AS avg_close
FROM stock_prices
GROUP BY ticker, YEAR(date), MONTH(date);
SELECT 
cp.date,
cp.price_usd AS bitcoin_price,
op.price_usd AS oil_price
FROM crypto_prices cp
JOIN oil_prices op
ON cp.date = op.date
WHERE cp.coin_id = 'bitcoin'
ORDER BY cp.date;
SELECT name, symbol, market_cap
FROM cryptocurrencies
ORDER BY market_cap DESC
LIMIT 3;
SELECT name, circulating_supply, total_supply
FROM cryptocurrencies
WHERE total_supply > 0
AND circulating_supply >= 0.9 * total_supply;
SELECT name, current_price, ath
FROM cryptocurrencies
WHERE current_price >= 0.9 * ath;
SELECT AVG(market_cap_rank) AS avg_rank
FROM cryptocurrencies
WHERE total_volume > 1000000000;
SELECT name, date
FROM cryptocurrencies
ORDER BY date DESC
LIMIT 1;
SELECT MAX(price_usd) AS highest_price
FROM crypto_prices
WHERE coin_id = 'bitcoin';
SELECT AVG(price_usd) AS avg_eth_price
FROM crypto_prices
WHERE coin_id = 'ethereum';
SELECT date, price_usd
FROM crypto_prices
WHERE coin_id = 'bitcoin'
AND YEAR(date) = 2025
AND MONTH(date) = 1
ORDER BY date;
SELECT coin_id, AVG(price_usd) AS avg_price
FROM crypto_prices
GROUP BY coin_id
ORDER BY avg_price DESC
LIMIT 1;
SELECT 
(
 (MAX(price_usd) - MIN(price_usd)) / MIN(price_usd)
) * 100 AS percent_change
FROM crypto_prices
WHERE coin_id = 'bitcoin';
SELECT MAX(price_usd) AS highest_oil_price
FROM oil_prices;
SELECT 
YEAR(date) AS year,
AVG(price_usd) AS avg_price
FROM oil_prices
GROUP BY YEAR(date)
ORDER BY year;
SELECT date, price_usd
FROM oil_prices
WHERE date BETWEEN '2020-03-01' AND '2020-04-30';
SELECT MIN(price_usd)
FROM oil_prices;
SELECT 
YEAR(date) AS year,
MAX(price_usd) - MIN(price_usd) AS volatility
FROM oil_prices
GROUP BY YEAR(date);
SELECT *
FROM stock_prices
WHERE ticker = '^GSPC'
ORDER BY date;
SELECT MAX(close)
FROM stock_prices
WHERE ticker = '^IXIC';
SELECT date, (high - low) AS daily_range
FROM stock_prices
WHERE ticker = '^GSPC'
ORDER BY daily_range DESC
LIMIT 5;
SELECT 
ticker,
YEAR(date) AS year,
MONTH(date) AS month,
AVG(close) AS avg_close
FROM stock_prices
GROUP BY ticker, YEAR(date), MONTH(date)
ORDER BY ticker, year, month;
SELECT AVG(volume)
FROM stock_prices
WHERE ticker = '^NSEI'
AND YEAR(date) = 2024;
SELECT 
AVG(cp.price_usd) AS avg_bitcoin,
AVG(op.price_usd) AS avg_oil
FROM crypto_prices cp
JOIN oil_prices op ON cp.date = op.date
WHERE cp.coin_id = 'bitcoin'
AND YEAR(cp.date) = 2025;
SELECT 
cp.date,
cp.price_usd AS bitcoin_price,
sp.close AS sp500_close
FROM crypto_prices cp
JOIN stock_prices sp ON cp.date = sp.date
WHERE cp.coin_id = 'bitcoin'
AND sp.ticker = '^GSPC'
ORDER BY cp.date;
SELECT 
cp.date,
cp.price_usd AS ethereum_price,
sp.close AS nasdaq_close
FROM crypto_prices cp
JOIN stock_prices sp ON cp.date = sp.date
WHERE cp.coin_id = 'ethereum'
AND sp.ticker = '^IXIC'
AND YEAR(cp.date) = 2025;
SELECT 
cp.date,
cp.price_usd AS bitcoin_price,
op.price_usd AS oil_price,
sp.close AS sp500_close
FROM crypto_prices cp
JOIN oil_prices op ON cp.date = op.date
JOIN stock_prices sp ON cp.date = sp.date
WHERE cp.coin_id = 'bitcoin'
AND sp.ticker = '^GSPC'
ORDER BY cp.date;
DESCRIBE cryptocurrencies;
SHOW COLUMNS FROM cryptocurrencies;
USE cross_market;
SHOW COLUMNS FROM cryptocurrencies;
SHOW COLUMNS FROM oil_prices;
SHOW COLUMNS FROM stock_prices;