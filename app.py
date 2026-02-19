import streamlit as st
import pandas as pd
import mysql.connector

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Cross Market Analysis", layout="wide")

st.title("📊 Cross-Market Analysis: Crypto, Oil & Stocks")

# --------------------------------------------------
# DATABASE CONNECTION (TiDB via Streamlit Secrets)
# --------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )

# --------------------------------------------------
# LOAD DATA FROM DATABASE
# --------------------------------------------------
@st.cache_data
def load_data():
    conn = get_connection()

    crypto_query = """
        SELECT coin_id, date, price_usd
        FROM crypto_prices
    """

    oil_query = """
        SELECT date, price_usd
        FROM oil_prices
    """

    stock_query = """
        SELECT date, ticker, close
        FROM stock_prices
    """

    crypto_df = pd.read_sql(crypto_query, conn)
    oil_df = pd.read_sql(oil_query, conn)
    stocks_df = pd.read_sql(stock_query, conn)

    conn.close()

    crypto_df["date"] = pd.to_datetime(crypto_df["date"])
    oil_df["date"] = pd.to_datetime(oil_df["date"])
    stocks_df["date"] = pd.to_datetime(stocks_df["date"])

    return crypto_df, oil_df, stocks_df


crypto_df, oil_df, stocks_df = load_data()

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
page = st.sidebar.selectbox(
    "Select Page",
    [
        "📊 Filters & Data Exploration",
        "🧮 SQL Query Runner",
        "🚀 Top 3 Crypto Analysis"
    ]
)

# ==================================================
# PAGE 1 – FILTERS & DATA EXPLORATION
# ==================================================
if page == "📊 Filters & Data Exploration":

    st.header("Market Snapshot")

    min_date = crypto_df["date"].min()
    max_date = crypto_df["date"].max()

    start_date = st.date_input("Start Date", min_date)
    end_date = st.date_input("End Date", max_date)

    crypto_filtered = crypto_df[
        (crypto_df["date"] >= pd.to_datetime(start_date)) &
        (crypto_df["date"] <= pd.to_datetime(end_date))
    ]

    oil_filtered = oil_df[
        (oil_df["date"] >= pd.to_datetime(start_date)) &
        (oil_df["date"] <= pd.to_datetime(end_date))
    ].drop_duplicates(subset=["date"])

    stocks_filtered = stocks_df[
        (stocks_df["date"] >= pd.to_datetime(start_date)) &
        (stocks_df["date"] <= pd.to_datetime(end_date))
    ]

    # Pivot crypto
    crypto_pivot = crypto_filtered.pivot(
        index="date",
        columns="coin_id",
        values="price_usd"
    )

    # Pivot stocks
    stocks_pivot = stocks_filtered.pivot(
        index="date",
        columns="ticker",
        values="close"
    )

    oil_filtered = oil_filtered.set_index("date")
    oil_filtered.rename(columns={"price_usd": "Oil_Price"}, inplace=True)

    # Join like SQL INNER JOIN
    merged_df = crypto_pivot \
        .join(oil_filtered, how="inner") \
        .join(stocks_pivot, how="inner") \
        .sort_index()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    if "bitcoin" in merged_df.columns:
        col1.metric("Bitcoin Avg",
                    round(merged_df["bitcoin"].mean(), 2))

    if "Oil_Price" in merged_df.columns:
        col2.metric("Oil Avg",
                    round(merged_df["Oil_Price"].mean(), 2))

    if "^GSPC" in merged_df.columns:
        col3.metric("S&P 500 Avg",
                    round(merged_df["^GSPC"].mean(), 2))

    if "^NSEI" in merged_df.columns:
        col4.metric("NIFTY Avg",
                    round(merged_df["^NSEI"].mean(), 2))

    st.subheader("Daily Market Snapshot")
    st.dataframe(merged_df)

# ==================================================
# PAGE 2 – SQL QUERY RUNNER
# ==================================================
elif page == "🧮 SQL Query Runner":

    st.header("Run Predefined SQL Queries")

    queries = {
        "Top 3 Cryptos by Market Cap":
            "SELECT * FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3;",

        "Highest Bitcoin Price":
            """
            SELECT MAX(price_usd) AS highest_bitcoin_price
            FROM crypto_prices
            WHERE coin_id='bitcoin';
            """,

        "Highest Oil Price":
            "SELECT MAX(price_usd) AS highest_oil_price FROM oil_prices;",

        "Highest NASDAQ Close":
            """
            SELECT MAX(close) AS highest_nasdaq
            FROM stock_prices
            WHERE ticker='^IXIC';
            """
    }

    selected_query = st.selectbox("Choose Query", list(queries.keys()))

    if st.button("Run Query"):
        conn = get_connection()
        result_df = pd.read_sql(queries[selected_query], conn)
        conn.close()
        st.dataframe(result_df)

# ==================================================
# PAGE 3 – TOP 3 CRYPTO ANALYSIS
# ==================================================
elif page == "🚀 Top 3 Crypto Analysis":

    st.header("Top 3 Crypto Daily Analysis")

    coins = crypto_df["coin_id"].unique()
    selected_coin = st.selectbox("Select Coin", coins)

    min_date = crypto_df["date"].min()
    max_date = crypto_df["date"].max()

    start_date = st.date_input("Start Date", min_date, key="crypto_start")
    end_date = st.date_input("End Date", max_date, key="crypto_end")

    coin_filtered = crypto_df[
        (crypto_df["coin_id"] == selected_coin) &
        (crypto_df["date"] >= pd.to_datetime(start_date)) &
        (crypto_df["date"] <= pd.to_datetime(end_date))
    ].set_index("date")

    st.subheader("Daily Price Trend")
    st.line_chart(coin_filtered["price_usd"])

    st.subheader("Daily Price Table")
    st.dataframe(coin_filtered)