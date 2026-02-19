import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from datetime import date, timedelta

# -------------------------------
# TiDB / MySQL Connection
# -------------------------------
conn = mysql.connector.connect(
    host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="2E7RXmh1PwAwo6G.root",
    password="7oxoP3UUnvifoJrR",
    database="cross_market"
)

# -------------------------------
# Sidebar: Pages
# -------------------------------
st.sidebar.title("📊 Cross-Market Analysis")
page = st.sidebar.radio("Select Page", ["Crypto", "Oil", "Stock Index"])

# -------------------------------
# Cached Query Function
# -------------------------------
@st.cache_data
def run_query(query):
    return pd.read_sql(query, conn)

# -------------------------------
# Common Date Filter: Last 1 Year
# -------------------------------
today = date.today()
last_year = today - timedelta(days=365)

# -------------------------------
# Page 1: Crypto
# -------------------------------
if page == "Crypto":
    st.header("💰 Cryptocurrency Price Trends")

    # Top 3 coins
    top_coins = ["Bitcoin", "Ethereum", "BNB"]
    coin = st.selectbox("Select Coin", top_coins)

    query = f"""
        SELECT date, current_price
        FROM cryptocurrencies
        WHERE name = '{coin}'
          AND date >= '{last_year}'
        ORDER BY date
    """
    df = run_query(query)

    st.line_chart(df.set_index("date")["current_price"])
    st.dataframe(df)

# -------------------------------
# Page 2: Oil
# -------------------------------
elif page == "Oil":
    st.header("🛢 Oil Prices (USD)")

    query = f"""
        SELECT date, price_usd
        FROM oil_prices
        WHERE date >= '{last_year}'
        ORDER BY date
    """
    df = run_query(query)

    fig = px.line(df, x="date", y="price_usd", title="Oil Prices Last 1 Year")
    st.plotly_chart(fig)
    st.dataframe(df)

# -------------------------------
# Page 3: Stock Index
# -------------------------------
elif page == "Stock Index":
    st.header("📈 Stock Index Prices")

    # Get available tickers
    tickers_query = "SELECT DISTINCT ticker FROM stock_prices"
    tickers = run_query(tickers_query)["ticker"].tolist()
    ticker = st.selectbox("Select Stock Index", tickers)

    query = f"""
        SELECT date, close
        FROM stock_prices
        WHERE ticker = '{ticker}'
          AND date >= '{last_year}'
        ORDER BY date
    """
    df = run_query(query)

    fig = px.line(df, x="date", y="close", title=f"{ticker} Last 1 Year")
    st.plotly_chart(fig)
    st.dataframe(df)