import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

# Streamlit title
st.title("💳 Real-Time Credit Card Fraud Dashboard")

# Connect to SQLite DB
conn = sqlite3.connect("fraud_detection.db")
query = "SELECT * FROM fraud_transactions ORDER BY timestamp DESC"
df = pd.read_sql_query(query, conn)
conn.close()

# Count total frauds
fraud_count = len(df)

# Show total number
st.metric("🚨 Total Fraud Transactions", fraud_count)

# 🧪 If frauds exist, show table and chart
if fraud_count > 0:
    st.subheader("📋 Latest Fraud Transactions")
    st.dataframe(df)

    st.subheader("📈 Fraud Amount by Merchant")
    chart = alt.Chart(df).mark_bar().encode(
        x='merchant:N',
        y='amount:Q',
        color='location:N',
        tooltip=['merchant', 'amount', 'location', 'timestamp']
    ).properties(width=700)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No fraud transactions found in the database.")

