Filters & Data Exploration (Page 1)

SQL Query Runner (Page 2)

Top 3 Crypto Analysis (Page 3)

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# -------------------------
# Streamlit page config
# -------------------------
st.set_page_config(page_title="Cross-Market Analysis", layout="wide")
st.title("📊 Cross-Market Analysis Dashboard")
st.write("Crypto | Oil | Stocks Analysis")
st.success("Streamlit is working successfully!")

# -------------------------
# Database connection
# -------------------------
conn = mysql.connector.connect(
    host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="2E7RXmh1PwAwo6G.root",
    password="7oxoP3UUnvifoJrR",
    database="cross_market"  # Change if needed
)

# -------------------------
# Tabs for pages
# -------------------------
tab1, tab2, tab3 = st.tabs(["Market Snapshot", "SQL Query Runner", "Top 3 Crypto Analysis"])

# -------------------------
# Page 1: Market Snapshot
# -------------------------
with tab1:
    st.header("📈 Market Snapshot")
    market = st.selectbox("Select Market", ["Cryptocurrency", "Oil Prices", "Stock Index"])

    if market == "Cryptocurrency":
        coin_query = "SELECT DISTINCT name FROM cryptocurrencies"
        coins = pd.read_sql(coin_query, conn)["name"].tolist()
        selected_coin = st.selectbox("Select Coin", coins)

        query = f"""
            SELECT date, current_price
            FROM cryptocurrencies
            WHERE name = '{selected_coin}'
            ORDER BY date
        """
        df = pd.read_sql(query, conn)
        st.subheader(f"{selected_coin} Price Trend")
        fig = px.line(df, x="date", y="current_price", title=f"{selected_coin} Daily Price")
        st.plotly_chart(fig, use_container_width=True)

    elif market == "Oil Prices":
        query = "SELECT date, price_usd FROM oil_prices ORDER BY date"
        df = pd.read_sql(query, conn)
        st.subheader("WTI Crude Oil Price Trend")
        fig = px.line(df, x="date", y="price_usd", title="Oil Prices (USD)")
        st.plotly_chart(fig, use_container_width=True)

    elif market == "Stock Index":
        ticker_query = "SELECT DISTINCT ticker FROM stock_prices"
        tickers = pd.read_sql(ticker_query, conn)["ticker"].tolist()
        selected_ticker = st.selectbox("Select Stock Index", tickers)

        query = f"""
            SELECT date, close
            FROM stock_prices
            WHERE ticker = '{selected_ticker}'
            ORDER BY date
        """
        df = pd.read_sql(query, conn)
        st.subheader(f"{selected_ticker} Closing Price Trend")
        fig = px.line(df, x="date", y="close", title=f"{selected_ticker} Daily Closing Price")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Page 2: SQL Query Runner
# -------------------------
with tab2:
    st.header("💻 SQL Query Runner")
    queries = {
        "Top 3 Cryptocurrencies by Market Cap": "SELECT name, market_cap FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3",
        "Average Oil Price per Year": "SELECT YEAR(date) AS yr, AVG(price_usd) AS avg_price FROM oil_prices GROUP BY yr ORDER BY yr",
        "Highest Closing Price of NASDAQ": "SELECT MAX(close) AS max_close FROM stock_prices WHERE ticker='^IXIC'"
    }

    selected_query = st.selectbox("Select a Query", list(queries.keys()))
    if st.button("Run Query"):
        df = pd.read_sql(queries[selected_query], conn)
        st.dataframe(df)

# -------------------------
# Page 3: Top 3 Crypto Analysis
# -------------------------
with tab3:
    st.header("🔝 Top 3 Cryptocurrencies Analysis")

    # Get top 3 coins by market cap
    top3_query = "SELECT name FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3"
    top3_coins = pd.read_sql(top3_query, conn)["name"].tolist()
    selected_coin = st.selectbox("Select Top Coin", top3_coins)

    start_date = st.date_input("Start Date", pd.to_datetime("2025-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2025-12-31"))

    query = f"""
        SELECT date, current_price
        FROM cryptocurrencies
        WHERE name = '{selected_coin}' AND date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date
    """
    df = pd.read_sql(query, conn)

    st.subheader(f"{selected_coin} Price Trend (Top 3)")
    fig = px.line(df, x="date", y="current_price", title=f"{selected_coin} Daily Price Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Prices Table")
    st.dataframe(df)