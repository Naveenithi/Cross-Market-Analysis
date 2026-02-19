import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ------------------------
# Streamlit Config
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
# Cached Query Function
# ------------------------
@st.cache_data
def run_query(query):
    return pd.read_sql(query, conn)

# ------------------------
# Sidebar Page Selector
# ------------------------
page = st.sidebar.radio(
    "Select Page",
    ["Crypto Analysis", "Oil Price Analysis", "Stock Index Analysis"]
)

# ------------------------
# Page 1: Crypto Analysis
# ------------------------
if page == "Crypto Analysis":
    st.header("📈 Top 3 Cryptocurrencies Price Trend")

    # Get top 3 coins by market cap
    coin_query = """
        SELECT name
        FROM cryptocurrencies
        ORDER BY market_cap DESC
        LIMIT 3
    """
    coins = run_query(coin_query)["name"].tolist()
    selected_coin = st.sidebar.selectbox("Select Coin", coins)

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
    st.header("📊 Stock Index vs Crude Oil")

    # Get available tickers
    ticker_query = "SELECT DISTINCT ticker FROM stock_prices"
    tickers = run_query(ticker_query)["ticker"].tolist()
    selected_ticker = st.sidebar.selectbox("Select Stock Index", tickers)

    stock_query = f"""
        SELECT date, close
        FROM stock_prices
        WHERE ticker = '{selected_ticker}'
        ORDER BY date
    """
    stock_df = run_query(stock_query)

    oil_query = "SELECT date, price_usd FROM oil_prices ORDER BY date"
    oil_df = run_query(oil_query)

    if not stock_df.empty and not oil_df.empty:
        # Merge on date to compare
        merged_df = pd.merge(stock_df, oil_df, on="date", how="inner")
        merged_df.set_index("date", inplace=True)
        st.line_chart(merged_df.rename(columns={"close": selected_ticker, "price_usd": "Oil Price"}))
    else:
        st.warning("Stock or oil data not available.")