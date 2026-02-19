import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ------------------------
# Streamlit Page Config
# ------------------------
st.set_page_config(
    page_title="Cross-Market Analysis",
    layout="wide"
)

st.title("📊 Cross-Market Analysis Dashboard")
st.write("Crypto | Oil | Stocks Analysis")

# ------------------------
# Database Connection
# ------------------------
@st.cache_resource
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="2E7RXmh1PwAwo6G.root",
            password="7oxoP3UUnvifoJrR",
            database="cross_market"
        )
        return conn
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None

conn = create_connection()
if not conn:
    st.stop()

# ------------------------
# Cached query function
# ------------------------
@st.cache_data
def run_query(query):
    return pd.read_sql(query, conn)

# ------------------------
# Sidebar: Page Selector
# ------------------------
page = st.sidebar.radio(
    "Select Page",
    ["Crypto Analysis", "Oil Price Analysis", "Stock Index Analysis"]
)

# ------------------------
# Page 1: Crypto Analysis
# ------------------------
if page == "Crypto Analysis":
    st.header("📈 Cryptocurrency Price Trend")

    # Get coin list
    coin_query = "SELECT DISTINCT name FROM cryptocurrencies"
    coins = run_query(coin_query)["name"].tolist()
    selected_coin = st.sidebar.selectbox("Select Coin", coins)

    # Query coin prices
    query = f"""
        SELECT date, current_price
        FROM cryptocurrencies
        WHERE name = '{selected_coin}'
        ORDER BY date
    """
    df = run_query(query)
    if not df.empty:
        st.line_chart(df.rename(columns={"date": "index"}).set_index("index")["current_price"])
    else:
        st.warning("No data available for this coin.")

# ------------------------
# Page 2: Oil Price Analysis
# ------------------------
elif page == "Oil Price Analysis":
    st.header("🛢 Crude Oil Price Trend")

    query = "SELECT date, price_usd FROM oil_prices ORDER BY date"
    df = run_query(query)
    if not df.empty:
        st.line_chart(df.rename(columns={"date": "index"}).set_index("index")["price_usd"])
    else:
        st.warning("No oil price data available.")

# ------------------------
# Page 3: Stock Index Analysis
# ------------------------
elif page == "Stock Index Analysis":
    st.header("📊 Stock Index Price Trend")

    # Get available tickers
    ticker_query = "SELECT DISTINCT ticker FROM stock_prices"
    tickers = run_query(ticker_query)["ticker"].tolist()
    selected_ticker = st.sidebar.selectbox("Select Stock Index", tickers)

    query = f"""
        SELECT date, close
        FROM stock_prices
        WHERE ticker = '{selected_ticker}'
        ORDER BY date
    """
    df = run_query(query)
    if not df.empty:
        st.line_chart(df.rename(columns={"date": "index"}).set_index("index")["close"])
    else:
        st.warning("No data available for this stock index.")