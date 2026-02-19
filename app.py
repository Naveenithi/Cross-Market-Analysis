import pandas as pd
import streamlit as st

# -----------------------------
# Cached CSV loader
# -----------------------------
@st.cache_data
def load_csv(file_path, usecols=None, rename_map=None):
    """
    Load CSV and optionally select columns and rename them.

    Parameters:
    - file_path (str): Path to the CSV file
    - usecols (list of str): Columns to read
    - rename_map (dict): Columns to rename, e.g., {"coin_id": "symbol"}

    Returns:
    - pd.DataFrame: Loaded DataFrame
    """
    try:
        df = pd.read_csv(file_path, usecols=usecols)
    except ValueError as e:
        st.warning(f"Column mismatch detected: {e}\nLoading all columns instead.")
        df = pd.read_csv(file_path)  # fallback to full CSV

    if rename_map:
        df = df.rename(columns=rename_map)

    return df

# -----------------------------
# Sidebar Pages
# -----------------------------
st.sidebar.title("Cross-Market Analysis")
page = st.sidebar.radio("Select Page:", ["Crypto Prices", "Oil Prices", "Stocks vs Oil"])

# -----------------------------
# Page: Crypto Prices
# -----------------------------
if page == "Crypto Prices":
    st.header("Cryptocurrency Prices")
    
    crypto_df = load_csv(
        "crypto_prices.csv",
        usecols=["date", "coin_id", "price_usd"],
        rename_map={"coin_id": "symbol"}
    )
    
    st.dataframe(crypto_df.head())
    st.line_chart(crypto_df.set_index("date")["price_usd"])

# -----------------------------
# Page: Oil Prices
# -----------------------------
elif page == "Oil Prices":
    st.header("Crude Oil Prices")
    
    oil_df = load_csv(
        "oil_prices.csv",
        usecols=["date", "close"],
        rename_map={"close": "oil_close"}
    )
    
    st.dataframe(oil_df.head())
    st.line_chart(oil_df.set_index("date")["oil_close"])

# -----------------------------
# Page: Stocks vs Oil
# -----------------------------
elif page == "Stocks vs Oil":
    st.header("Stock Prices vs Crude Oil")
    
    stock_df = load_csv(
        "stocks.csv",
        usecols=["date", "close"],
        rename_map={"close": "stock_close"}
    )
    
    oil_df = load_csv(
        "oil_prices.csv",
        usecols=["date", "close"],
        rename_map={"close": "oil_close"}
    )
    
    # Merge on date
    merged_df = pd.merge(stock_df, oil_df, on="date", how="inner")
    
    st.dataframe(merged_df.head())
    st.line_chart(merged_df.set_index("date"))

# -----------------------------
# Footer
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("📊 Cross-Market Analysis App")