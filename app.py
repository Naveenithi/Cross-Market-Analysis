import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cross-Market Analysis", layout="wide")

# -----------------------------
# Cached CSV loading functions
# -----------------------------
@st.cache_data
def load_csv(file_path, usecols=None):
    df = pd.read_csv(file_path, usecols=usecols)
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_data
def preprocess_crypto(df):
    df = df.sort_values(['symbol', 'date'])
    df['daily_change'] = df.groupby('symbol')['price_usd'].pct_change()
    return df

@st.cache_data
def preprocess_stock(df):
    df = df.sort_values(['ticker', 'date'])
    df['daily_change'] = df.groupby('ticker')['close'].pct_change()
    return df

@st.cache_data
def preprocess_oil(df):
    df = df.sort_values('date')
    df['daily_change'] = df['close'].pct_change()
    return df

# -----------------------------
# Load all CSVs
# -----------------------------
crypto_df = load_csv("crypto_prices.csv", usecols=["date", "symbol", "price_usd"])
crypto_df = preprocess_crypto(crypto_df)

stocks_df = load_csv("stock_prices.csv", usecols=["date", "ticker", "close"])
stocks_df = preprocess_stock(stocks_df)

oil_df = load_csv("oil_prices.csv", usecols=["date", "close"])
oil_df = preprocess_oil(oil_df)

# -----------------------------
# Sidebar - Page selection
# -----------------------------
page = st.sidebar.selectbox("Select Page", [
    "Filters & Data Exploration",
    "Comparison Charts",
    "Top Coins vs Stocks"
])

# -----------------------------
# Page 1 - Filters & Exploration
# -----------------------------
if page == "Filters & Data Exploration":
    st.header("Page 1: Filters & Data Exploration")

    st.subheader("Cryptocurrency Price Trend")
    coins = crypto_df['symbol'].unique().tolist()
    selected_coin = st.selectbox("Select Coin", coins)
    filtered_crypto = crypto_df[crypto_df['symbol'] == selected_coin]

    fig1 = px.line(filtered_crypto, x='date', y='price_usd',
                   title=f"{selected_coin} Price Trend",
                   labels={"price_usd": "Price (USD)"})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Stock Price Trend")
    tickers = stocks_df['ticker'].unique().tolist()
    selected_ticker = st.selectbox("Select Stock", tickers)
    filtered_stock = stocks_df[stocks_df['ticker'] == selected_ticker]

    fig2 = px.line(filtered_stock, x='date', y='close',
                   title=f"{selected_ticker} Stock Price Trend",
                   labels={"close": "Close Price"})
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Page 2 - Comparison Charts
# -----------------------------
elif page == "Comparison Charts":
    st.header("Page 2: Comparison Charts")

    st.subheader("Crypto vs Oil")
    selected_coin = st.selectbox("Select Coin for Comparison", crypto_df['symbol'].unique())
    crypto_filtered = crypto_df[crypto_df['symbol'] == selected_coin]

    merged_df = pd.merge(crypto_filtered, oil_df, on='date', how='inner', suffixes=('_crypto', '_oil'))

    fig3 = px.line(merged_df, x='date', y=['price_usd', 'close'],
                   labels={"value": "Price", "variable": "Asset"},
                   title=f"{selected_coin} vs Crude Oil")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Stock vs Oil")
    selected_stock = st.selectbox("Select Stock for Comparison", stocks_df['ticker'].unique())
    stock_filtered = stocks_df[stocks_df['ticker'] == selected_stock]

    merged_stock_oil = pd.merge(stock_filtered, oil_df, on='date', how='inner', suffixes=('_stock', '_oil'))
    fig4 = px.line(merged_stock_oil, x='date', y=['close', 'close_oil'],
                   labels={"value": "Price", "variable": "Asset"},
                   title=f"{selected_stock} vs Crude Oil")
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Page 3 - Top Coins vs Stocks
# -----------------------------
elif page == "Top Coins vs Stocks":
    st.header("Page 3: Top Coins vs Stocks")

    st.subheader("Top 3 Coins by Latest Price")
    latest_prices = crypto_df.groupby('symbol').last().reset_index()
    top3_coins = latest_prices.nlargest(3, 'price_usd')['symbol'].tolist()
    top3_df = crypto_df[crypto_df['symbol'].isin(top3_coins)]
    fig5 = px.line(top3_df, x='date', y='price_usd', color='symbol', title="Top 3 Coins Price Trend")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Compare Stock vs Oil Prices")
    selected_stock = st.selectbox("Select Stock for Trend Comparison", stocks_df['ticker'].unique())
    stock_filtered = stocks_df[stocks_df['ticker'] == selected_stock]
    merged_stock_oil = pd.merge(stock_filtered, oil_df, on='date', how='inner', suffixes=('_stock', '_oil'))
    fig6 = px.line(merged_stock_oil, x='date', y=['close', 'close_oil'],
                   labels={"value": "Price", "variable": "Asset"},
                   title=f"{selected_stock} vs Crude Oil")
    st.plotly_chart(fig6, use_container_width=True)