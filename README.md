# 💰🛢️📈 Cross-Market Analysis: Crypto, Oil & Stocks

A full-stack data analytics project that analyzes relationships between Cryptocurrency, Crude Oil, and Stock Market indices using SQL and Streamlit.

---

## 🚀 Live Application

🔗 Live App: [https://your-app-name.streamlit.app](https://cross-market-analysis-l6blposhge5nfjzugvb4xr.streamlit.app/)

---

## 📖 Project Overview

This project performs cross-market analysis between:

- 📈 Cryptocurrencies (Top Coins)
- 🛢️ Crude Oil Prices
- 📊 Stock Market Indices (e.g., S&P 500, NIFTY)

The system extracts financial data, stores it in a SQL database, performs analytical queries, and visualizes insights using an interactive Streamlit dashboard.

---

## 🛠️ Tech Stack

### Programming & Analysis
- Python
- Pandas
- SQL

### Database
- MySQL / TiDB Cloud

### Data Visualization
- Streamlit
- Plotly

### Deployment
- GitHub
- Streamlit Community Cloud

---

## 🏗️ Architecture Diagram

    APIs / CSV Data
           │
           ▼
    Google Colab (ETL)
           │
           ▼
    MySQL / TiDB Cloud
           │
    (SQL Analytics Queries)
           │
           ▼
    Streamlit Dashboard
           │
           ▼
    Streamlit Cloud (Live App)


---

## ⚙️ Features

- ✅ API-based financial data collection
- ✅ ETL pipeline using Pandas
- ✅ Structured SQL database design
- ✅ Cross-market comparison (Crypto vs Oil vs Stocks)
- ✅ Date-based filtering
- ✅ Interactive charts & trend analysis
- ✅ Cloud database integration
- ✅ Live deployed dashboard

---

## 📊 Key Analysis Performed

- Daily price comparison across markets
- Cross-asset trend alignment
- Market movement visualization
- Multi-asset data merging using SQL + Pandas

---

## 📁 Project Structure

Cross-Market-Analysis/
│
├── app.py
├── requirements.txt
├── Cross Market Data.sql
├── README.md

---

## 🔐 Environment Variables (Streamlit Secrets)

The app securely connects to TiDB Cloud using:
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME


These credentials are stored in Streamlit Secrets and not exposed in the code.

---

## 👨‍💻 Author

**Naveen Kumar**

Data Analytics | SQL | Python | Streamlit | Cloud Deployment

---

## ⭐ Future Improvements

- Correlation heatmap
- Moving averages
- Volatility analysis
- Downloadable reports
- Advanced filtering options

