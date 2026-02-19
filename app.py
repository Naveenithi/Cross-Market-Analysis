import pandas as pd
import streamlit as st
import sqlite3

# -----------------------------
# Load CSVs (local, in repo)
# -----------------------------
@st.cache_data
def load_csv(file_path, usecols=None, rename_map=None):
    try:
        df = pd.read_csv(file_path, usecols=usecols)
    except FileNotFoundError:
        st.error(f"CSV not found: {file_path}")
        return pd.DataFrame()
    except ValueError as e:
        st.warning(f"Column mismatch: {e}\nLoading all columns instead.")
        df = pd.read_csv(file_path)
    
    if rename_map:
        df = df.rename(columns=rename_map)
    
    return df

# Load all 4 CSVs
crypto_meta_df = load_csv("cryptocurrencies.csv")
crypto_prices_df = load_csv("crypto_prices.csv")
oil_df = load_csv("oil_prices.csv")
stocks_df = load_csv("stock_prices.csv")

# Merge crypto prices with metadata
if not crypto_prices_df.empty and not crypto_meta_df.empty:
    crypto_df = crypto_prices_df.merge(
        crypto_meta_df[['id', 'symbol', 'name']],
        left_on='coin_id',
        right_on='id',
        how='left'
    )
else:
    crypto_df = pd.DataFrame()

# -----------------------------
# Sidebar Pages
# -----------------------------
st.sidebar.title("Cross-Market Analysis")
page = st.sidebar.radio(
    "Select Page:",
    ["Filters & Data Exploration", "SQL Query Runner", "Top Crypto Analysis"]
)

# -----------------------------
# Page 1: Filters & Cross-Market Chart
# -----------------------------
if page == "Filters & Data Exploration":
    st.header("Filters & Cross-Market Data")

    # Date range picker
    if not crypto_df.empty:
        crypto_df['price_usd'] = pd.to_numeric(crypto_df['price_usd'], errors='coerce')
        date_min = pd.to_datetime(crypto_df['date']).min()
        date_max = pd.to_datetime(crypto_df['date']).max()
        selected_dates = st.date_input("Select Date Range", [date_min, date_max])
        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])

    # Crypto coin selection
    if not crypto_df.empty:
        coins = crypto_df['symbol'].unique()
        selected_coins = st.multiselect("Select Crypto Coins", coins, default=coins[:3])
        crypto_filtered = crypto_df[
            (crypto_df['symbol'].isin(selected_coins)) &
            (pd.to_datetime(crypto_df['date']) >= start_date) &
            (pd.to_datetime(crypto_df['date']) <= end_date)
        ]
        crypto_pivot = crypto_filtered.pivot(index='date', columns='symbol', values='price_usd')

    # Oil price filtering
    if not oil_df.empty:
        oil_filtered = oil_df[
            (pd.to_datetime(oil_df['date']) >= start_date) &
            (pd.to_datetime(oil_df['date']) <= end_date)
        ].rename(columns={'close': 'oil_price'})
        oil_filtered.set_index('date', inplace=True)

    # Stock price filtering
    if not stocks_df.empty:
        stocks_filtered = stocks_df[
            (pd.to_datetime(stocks_df['date']) >= start_date) &
            (pd.to_datetime(stocks_df['date']) <= end_date)
        ].rename(columns={'close': 'stock_price'})
        stocks_filtered.set_index('date', inplace=True)

    # Merge all for cross-market chart
    merged_df = pd.concat([crypto_pivot, oil_filtered, stocks_filtered], axis=1)
    st.subheader("Cross-Market Chart")
    st.dataframe(merged_df.fillna(0))  # show merged table
    st.line_chart(merged_df.fillna(0))  # plot all series

# -----------------------------
# Page 2: SQL Query Runner
# -----------------------------
elif page == "SQL Query Runner":
    st.header("SQL Query Runner")

    conn = sqlite3.connect(":memory:")
    if not crypto_df.empty:
        crypto_df.to_sql("crypto", conn, index=False, if_exists="replace")
    if not oil_df.empty:
        oil_df.to_sql("oil", conn, index=False, if_exists="replace")
    if not stocks_df.empty:
        stocks_df.to_sql("stocks", conn, index=False, if_exists="replace")

    query = st.text_area("Write SQL Query", "SELECT * FROM crypto LIMIT 5")
    if st.button("Run Query"):
        try:
            result = pd.read_sql_query(query, conn)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Query failed: {e}")

# -----------------------------
# Page 3: Top Crypto Analysis
# -----------------------------
elif page == "Top Crypto Analysis":
    st.header("Top Crypto Coins")

    if not crypto_df.empty:
        top_coins = crypto_df.groupby('symbol')['price_usd'].max().sort_values(ascending=False).head(10)
        st.bar_chart(top_coins)

# -----------------------------
# Footer
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("📊 Cross-Market Analysis App")