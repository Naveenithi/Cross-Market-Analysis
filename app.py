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
# Sidebar Navigation (Pages)
# -------------------------
page = st.sidebar.radio(
    "Select Page",
    ["Filters & Data Exploration", "SQL Query Runner", "Top 3 Crypto Analysis"]
)

# -------------------------
# Page 1: Filters & Data Exploration
# -------------------------
if page == "Filters & Data Exploration":
    st.header("📈 Filters & Data Exploration")

    market = st.selectbox("Select Market", ["Cryptocurrency", "Oil Prices", "Stock Index"])

    if market == "Cryptocurrency":
        # Only Top 3 coins by market_cap
        top3_query = "SELECT name FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3"
        top3_coins = pd.read_sql(top3_query, conn)["name"].tolist()
        selected_coin = st.selectbox("Select Coin (Top 3)", top3_coins)

        # Fetch coin price data
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
elif page == "SQL Query Runner":
    st.header("💻 SQL Query Runner")

    queries = {
        "Top 3 Cryptocurrencies by Market Cap": "SELECT name, market_cap FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3",
        "Coins near ATH": "SELECT name, current_price, ath FROM cryptocurrencies WHERE current_price >= ath * 0.9",
        "Average Market Cap Rank (Volume > $1B)": "SELECT AVG(market_cap_rank) AS avg_rank FROM cryptocurrencies WHERE total_volume > 1000000000",
        "Most Recently Updated Coin": "SELECT name, date FROM cryptocurrencies ORDER BY date DESC LIMIT 1",
        "Highest Bitcoin Price (Last 365 Days)": "SELECT MAX(current_price) AS max_price FROM cryptocurrencies WHERE name='Bitcoin'",
        "Average Ethereum Price (Last 365 Days)": "SELECT AVG(current_price) AS avg_price FROM cryptocurrencies WHERE name='Ethereum'",
        "Oil Highest Price (Last 5 Years)": "SELECT MAX(price_usd) AS max_price FROM oil_prices",
        "Average Oil Price per Year": "SELECT YEAR(date) AS yr, AVG(price_usd) AS avg_price FROM oil_prices GROUP BY yr ORDER BY yr",
        "Highest NASDAQ Close": "SELECT MAX(close) AS max_close FROM stock_prices WHERE ticker='^IXIC'",
        "Top 5 S&P 500 High Difference Days": "SELECT date, (high-low) AS diff FROM stock_prices WHERE ticker='^GSPC' ORDER BY diff DESC LIMIT 5"
    }

    selected_query = st.selectbox("Select a Query", list(queries.keys()))
    if st.button("Run Query"):
        df = pd.read_sql(queries[selected_query], conn)
        st.dataframe(df)

# -------------------------
# Page 3: Top 3 Crypto Analysis
# -------------------------
elif page == "Top 3 Crypto Analysis":
    st.header("🔝 Top 3 Cryptocurrencies Analysis")

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