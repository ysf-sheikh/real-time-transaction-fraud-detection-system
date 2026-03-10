import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Setup page
st.set_page_config(
    page_title="Real-Time Fraud Detection",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💳 Real-Time Transaction Fraud Detection Dashboard")
st.markdown("Monitor alerts and per-account stats live from the data stream.")

# Define paths relative to the project root
ALERTS_CSV = Path("data/alerts.csv")
TRANS_CSV = Path("data/transactions.csv")

# Sidebar for manual or auto refresh
st.sidebar.header("Controls")
if st.sidebar.button("Manual Refresh"):
    st.rerun()

# --- Data Loading ---
def load_data():
    df_alerts = pd.read_csv(ALERTS_CSV) if ALERTS_CSV.exists() else pd.DataFrame()
    df_trans = pd.read_csv(TRANS_CSV) if TRANS_CSV.exists() else pd.DataFrame()
    return df_alerts, df_trans

df_alerts, df_trans = load_data()

# --- Metrics ---
total_alerts = len(df_alerts) if not df_alerts.empty else 0
active_accounts = df_trans["account_id"].nunique() if not df_trans.empty else 0

st.sidebar.metric("Total Alerts", total_alerts)
st.sidebar.metric("Active Accounts", active_accounts)

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚨 Live Alerts")
    if not df_alerts.empty:
        # Sort by timestamp (assuming standard format)
        st.dataframe(df_alerts.sort_values(by="timestamp", ascending=False), width="stretch")
    else:
        st.info("No alerts detected in data/alerts.csv")

with col2:
    st.subheader("📊 Transaction Summary")
    if not df_trans.empty:
        stats = df_trans.groupby("account_id").agg({
            "amount": "sum",
            "transaction_id": "count"
        }).rename(columns={"amount": "Total Spent", "transaction_id": "Txn Count"})
        st.dataframe(stats, width="stretch")
    else:
        st.info("No transaction data found.")

# --- Visualizations ---
st.subheader("📈 Visualizations")
c1, c2 = st.columns(2)

with c1:
    if not df_alerts.empty:
        fig_alerts = px.histogram(df_alerts, x="account_id", title="Alerts per Account", color_discrete_sequence=['red'])
        st.plotly_chart(fig_alerts, use_container_width=True)

with c2:
    if not df_trans.empty:
        fig_trans = px.bar(df_trans.groupby("account_id").size().reset_index(name='counts'), 
                           x="account_id", y="counts", title="Transactions per Account")
        st.plotly_chart(fig_trans, use_container_width=True)

# Auto-refresh every 5 seconds
st.empty()
import time
time.sleep(5)
st.rerun()