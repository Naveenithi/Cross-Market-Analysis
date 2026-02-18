import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Cross-Market Analysis", layout="wide")
st.title("📊 Cross-Market Analysis Dashboard")
st.write("Crypto | Oil | Stocks Analysis")

# -------------------- DATABASE CONNECTION --------------------
conn = mysql.connector.connect(
    host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="2E7RXmh1PwAwo6G.root",
    password="7oxoP3UUnvifoJrR",
    database="cross_market"
)

# -------------------- PAGE NAVIGATION --------------------
page = st.sidebar.radio("Select Page", ["Market Snapshot", "SQL Query Runner", "Top Crypto Analysis"])

# ==================== PAGE 1: MARKET SNAPSHOT ====================
if page == "Market Snapshot":
    st.header("📊 Market Snapshot")

    # Date range
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-12-31"))

    # -------------------- LOAD CRYPTO (Bitcoin) --------------------
    crypto_df = pd.read_sql("""
        SELECT date, price_usd
        FROM crypto_prices
        WHERE coin_id = 'bitcoin'
    """, conn)
    crypto_df["date"] = pd.to_datetime(crypto_df["date"])
    crypto_df = crypto_df[(crypto_df["date"] >= pd.to_datetime(start_date)) & 
                          (crypto_df["date"] <= pd.to_datetime(end_date))]
    
    st.subheader("Bitcoin Price Trend")
    fig = px.line(crypto_df, x="date", y="price_usd", title="Bitcoin Daily Price")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------- LOAD OIL --------------------
    oil_df = pd.read_sql("SELECT date, price_usd FROM oil_prices", conn)
    oil_df["date"] = pd.to_datetime(oil_df["date"])
    oil_df = oil_df[(oil_df["date"] >= pd.to_datetime(start_date)) & 
                    (oil_df["date"] <= pd.to_datetime(end_date))]

    st.subheader("Oil Price Trend")
    fig = px.line(oil_df, x="date", y="price_usd", title="Oil Daily Price")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------- LOAD STOCKS --------------------
    stock_query = "SELECT DISTINCT ticker FROM stock_prices"
    tickers = pd.read_sql(stock_query, conn)["ticker"].tolist()
    selected_ticker = st.sidebar.selectbox("Select Stock Index", tickers)

    stock_df = pd.read_sql(f"""
        SELECT date, close
        FROM stock_prices
        WHERE ticker = '{selected_ticker}'
    """, conn)
    stock_df["date"] = pd.to_datetime(stock_df["date"])
    stock_df = stock_df[(stock_df["date"] >= pd.to_datetime(start_date)) & 
                        (stock_df["date"] <= pd.to_datetime(end_date))]

    st.subheader(f"{selected_ticker} Price Trend")
    fig = px.line(stock_df, x="date", y="close", title=f"{selected_ticker} Daily Price")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------- SNAPSHOT TABLE --------------------
    snapshot_df = crypto_df.rename(columns={"price_usd": "Bitcoin"}).merge(
        oil_df.rename(columns={"price_usd": "Oil"}), on="date", how="inner"
    ).merge(
        stock_df.rename(columns={"close": selected_ticker}), on="date", how="inner"
    )

    st.subheader("Daily Market Snapshot")
    st.dataframe(snapshot_df.head(50))

    st.success("Market snapshot loaded successfully!")

# ==================== PAGE 2: SQL QUERY RUNNER ====================
elif page == "SQL Query Runner":
    st.header("💻 SQL Query Runner")

    # Predefined queries
    query_list = {
        "Top 3 Cryptos by Market Cap": "SELECT * FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3",
        "Coins with Circulating Supply > 90% of Total": "SELECT * FROM cryptocurrencies WHERE circulating_supply/total_supply > 0.9",
        "Highest Oil Price in Last 5 Years": "SELECT MAX(price_usd) as max_price FROM oil_prices",
        "NASDAQ Highest Close": "SELECT MAX(close) as max_close FROM stock_prices WHERE ticker='^IXIC'"
    }

    query_name = st.selectbox("Select Query", list(query_list.keys()))
    if st.button("Run Query"):
        sql = query_list[query_name]
        df = pd.read_sql(sql, conn)
        st.dataframe(df)
        st.success("Query executed successfully!")

# ==================== PAGE 3: TOP CRYPTO ANALYSIS ====================
elif page == "Top Crypto Analysis":
    st.header("📈 Top Cryptocurrencies Analysis")

    # Top 3 coins
    top_coins = pd.read_sql("SELECT coin_id FROM crypto_prices GROUP BY coin_id ORDER BY MAX(price_usd) DESC LIMIT 3", conn)["coin_id"].tolist()
    selected_coin = st.sidebar.selectbox("Select Cryptocurrency", top_coins)

    # Date range
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-12-31"))

    crypto_df = pd.read_sql(f"""
        SELECT date, price_usd
        FROM crypto_prices
        WHERE coin_id = '{selected_coin}'
    """, conn)
    crypto_df["date"] = pd.to_datetime(crypto_df["date"])
    crypto_df = crypto_df[(crypto_df["date"] >= pd.to_datetime(start_date)) & 
                          (crypto_df["date"] <= pd.to_datetime(end_date))]

    st.subheader(f"{selected_coin} Price Trend")
    fig = px.line(crypto_df, x="date", y="price_usd", title=f"{selected_coin} Daily Price")
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.subheader(f"{selected_coin} Daily Price Table")
    st.dataframe(crypto_df.head(50))

    # -------------------- CROSS-MARKET COMPARISON --------------------
    st.sidebar.subheader("Cross-Market Comparison")
    compare_market = st.sidebar.checkbox("Enable Cross-Market Comparison")

    if compare_market:
        # Select stock index
        ticker_query = "SELECT DISTINCT ticker FROM stock_prices"
        tickers = pd.read_sql(ticker_query, conn)["ticker"].tolist()
        selected_ticker = st.sidebar.selectbox("Select Stock Index", tickers, index=0)

        # Load oil and stock
        oil_df = pd.read_sql("SELECT date, price_usd FROM oil_prices", conn)
        oil_df["date"] = pd.to_datetime(oil_df["date"])
        oil_df = oil_df[(oil_df["date"] >= pd.to_datetime(start_date)) & 
                        (oil_df["date"] <= pd.to_datetime(end_date))]
        oil_df = oil_df.rename(columns={"price_usd": "Oil"})

        stock_df = pd.read_sql(f"""
            SELECT date, close
            FROM stock_prices
            WHERE ticker = '{selected_ticker}'
        """, conn)
        stock_df["date"] = pd.to_datetime(stock_df["date"])
        stock_df = stock_df[(stock_df["date"] >= pd.to_datetime(start_date)) & 
                            (stock_df["date"] <= pd.to_datetime(end_date))]
        stock_df = stock_df.rename(columns={"close": selected_ticker})

        # Merge
        combined_df = crypto_df.rename(columns={"price_usd": selected_coin}).merge(
            oil_df, on="date", how="inner"
        ).merge(
            stock_df, on="date", how="inner"
        )

        fig = px.line(combined_df, x="date", y=[selected_coin, "Oil", selected_ticker],
                      title=f"Cross-Market Comparison: {selected_coin} vs Oil vs {selected_ticker}")
        st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard loaded successfully!")