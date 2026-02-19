import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
@st.cache_data
def load_data():
    cryptos = pd.read_csv("cryptocurrencies.csv", parse_dates=["date"])
    crypto_prices = pd.read_csv("crypto_prices.csv", parse_dates=["date"])
    oil = pd.read_csv("oil_prices.csv", parse_dates=["date"])
    stocks = pd.read_csv("stock_prices.csv", parse_dates=["date"])
    return cryptos, crypto_prices, oil, stocks

cryptos, crypto_prices, oil, stocks = load_data()

# --- Sidebar Pages ---
page = st.sidebar.radio("Navigation", ["Filters & Data Exploration", "Comparison Charts", "Insights"])

# --- Sidebar Selections ---
# Crypto coin selection
top_coins = crypto_prices.groupby("coin_name")["price_usd"].mean().sort_values(ascending=False).head(10).index.tolist()
selected_coin = st.sidebar.selectbox("Select Coin", top_coins)

# Stock index selection
selected_ticker = st.sidebar.selectbox("Select Stock Index", stocks["ticker"].unique())

# --- Pages ---
if page == "Filters & Data Exploration":
    st.header("Cryptocurrency Price Trend")
    df_coin = crypto_prices[crypto_prices["coin_name"] == selected_coin]
    fig1 = px.line(df_coin, x="date", y="price_usd", title=f"{selected_coin} Price Trend")
    st.plotly_chart(fig1, use_container_width=True)

    st.header("Oil Price Trend")
    fig2 = px.line(oil, x="date", y="price_usd", title="Crude Oil Price Trend")
    st.plotly_chart(fig2, use_container_width=True)

    st.header(f"Stock Price Trend: {selected_ticker}")
    df_stock = stocks[stocks["ticker"] == selected_ticker]
    fig3 = px.line(df_stock, x="date", y="close", title=f"{selected_ticker} Closing Prices")
    st.plotly_chart(fig3, use_container_width=True)

elif page == "Comparison Charts":
    st.header("Top 3 Coins vs Nifty Index")
    top3 = crypto_prices.groupby("coin_name")["price_usd"].mean().sort_values(ascending=False).head(3).index.tolist()
    for coin in top3:
        df = crypto_prices[crypto_prices["coin_name"] == coin]
        fig = px.line(df, x="date", y="price_usd", title=f"{coin} Price Trend")
        st.plotly_chart(fig, use_container_width=True)

    st.header("Stock vs Oil Price Comparison")
    st.write("Select Stock and Oil for comparison")
    fig4 = px.line(df_stock, x="date", y="close", title=f"{selected_ticker} vs Oil")
    fig4.add_scatter(x=oil["date"], y=oil["price_usd"], mode="lines", name="Oil Price")
    st.plotly_chart(fig4, use_container_width=True)

elif page == "Insights":
    st.header("Insights")
    st.write("Provide key analysis and insights based on the trends.")