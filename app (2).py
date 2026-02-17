import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Cross-Market Analysis", layout="wide")

# -------------------------------
# Path to CSV files (update if needed)
# -------------------------------
DATA_PATH = "/content/drive/MyDrive/market_data"  # your mounted Drive folder

csv_files = {
    "Bitcoin": "bitcoin.csv",
    "Nifty": "nifty.csv",
    "Oil": "oil.csv",
    "S&P 500": "sp500.csv"
}

# -------------------------------
# Page Navigation
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Data Viewer", "Charts"])

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":
    st.title("📊 Cross-Market Analysis")
    st.write("""
    Welcome to the Cross-Market Analysis App!  

    Use the sidebar to navigate between pages:  

    - **Data Viewer**: View your CSV datasets.  
    - **Charts**: Visualize trends from your datasets.
    """)

# -------------------------------
# Data Viewer Page
# -------------------------------
elif page == "Data Viewer":
    st.title("📂 Data Viewer")

    selected_datasets = st.multiselect(
        "Select datasets to view",
        options=list(csv_files.keys()),
        default=list(csv_files.keys())
    )

    @st.cache_data
    def load_data(filename):
        path = os.path.join(DATA_PATH, filename)
        df = pd.read_csv(path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df

    for dataset_name in selected_datasets:
        df = load_data(csv_files[dataset_name])
        st.subheader(dataset_name)
        st.dataframe(df)

# -------------------------------
# Charts Page
# -------------------------------
elif page == "Charts":
    st.title("📈 Market Charts")

    selected_datasets = st.multiselect(
        "Select datasets for charts",
        options=list(csv_files.keys()),
        default=list(csv_files.keys())
    )

    @st.cache_data
    def load_data(filename):
        path = os.path.join(DATA_PATH, filename)
        df = pd.read_csv(path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df

    for dataset_name in selected_datasets:
        df = load_data(csv_files[dataset_name])
        st.subheader(dataset_name)
        numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
        if 'date' in df.columns and numeric_cols:
            st.line_chart(df.set_index('date')[numeric_cols[0]])
