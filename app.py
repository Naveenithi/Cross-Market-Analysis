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
# Sidebar: Market selection
# -------------------------
market = st.sidebar.selectbox("Select Market", ["Cryptocurrency", "Oil Prices", "Stock Index"])

# -------------------------
# Queries & data fetch
# -------------------------
if market == "Cryptocurrency":
    coin_query = "SELECT DISTINCT name FROM cryptocurrencies"
    coins = pd.read_sql(coin_query, conn)["name"].tolist()
    selected_coin = st.sidebar.selectbox("Select Coin", coins)

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
    # Get available tickers
    ticker_query = "SELECT DISTINCT ticker FROM stock_prices"
    tickers = pd.read_sql(ticker_query, conn)["ticker"].tolist()
    selected_ticker = st.sidebar.selectbox("Select Stock Index", tickers)

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