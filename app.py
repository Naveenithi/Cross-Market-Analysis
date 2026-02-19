import pandas as pd
import streamlit as st
from urllib.error import URLError

# -----------------------------
# GitHub CSV URLs (raw)
# -----------------------------
GITHUB_BASE = "https://raw.githubusercontent.com/your-username/your-repo/main/"

CSV_PATHS = {
    "crypto": GITHUB_BASE + "crypto_prices.csv",
    "oil": GITHUB_BASE + "oil_prices.csv",
    "stocks": GITHUB_BASE + "stocks.csv"
}

# -----------------------------
# Cached CSV loader
# -----------------------------
@st.cache_data
def load_csv(file_url, local_path=None, usecols=None, rename_map=None):
    """
    Load CSV from URL (GitHub) or local fallback.
    
    Parameters:
    - file_url (str): URL to CSV
    - local_path (str): fallback local path if URL fails
    - usecols (list): columns to read
    - rename_map (dict): columns to rename
    
    Returns:
    - pd.DataFrame
    """
    try:
        df = pd.read_csv(file_url, usecols=usecols)
        st.info(f"Loaded CSV from GitHub URL: {file_url}")
    except (URLError, ValueError) as e:
        st.warning(f"Could not load from GitHub URL: {e}")
        if local_path:
            st.info(f"Falling back to local CSV: {local_path}")
            df = pd.read_csv(local_path, usecols=usecols)
        else:
            raise RuntimeError("No local fallback CSV provided.") from e

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
        CSV_PATHS["crypto"],
        local_path="crypto_prices.csv",
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
        CSV_PATHS["oil"],
        local_path="oil_prices.csv",
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
        CSV_PATHS["stocks"],
        local_path="stocks.csv",
        usecols=["date", "close"],
        rename_map={"close": "stock_close"}
    )
    
    oil_df = load_csv(
        CSV_PATHS["oil"],
        local_path="oil_prices.csv",
        usecols=["date", "close"],
        rename_map={"close": "oil_close"}
    )
    
    merged_df = pd.merge(stock_df, oil_df, on="date", how="inner")
    
    st.dataframe(merged_df.head())
    st.line_chart(merged_df.set_index("date"))

# -----------------------------
# Footer
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("📊 Cross-Market Analysis App")