import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="AI Retention Intelligence System",
    layout="wide"
)

st.title("📊 AI-Powered User Retention Intelligence System")
st.write("SQL Analytics + Gemini AI + Automated Retention Recommendations")

# Database Connection
conn = sqlite3.connect("retention.db")

# KPI Data
kpi_query = """
SELECT
    COUNT(*) AS total_users,
    SUM(churn) AS churned_users,
    ROUND(AVG(subscription_months), 2) AS avg_subscription
FROM users
"""

kpi_df = pd.read_sql_query(kpi_query, conn)

total_users = int(kpi_df.loc[0, "total_users"])
churned_users = int(kpi_df.loc[0, "churned_users"])
avg_subscription = float(kpi_df.loc[0, "avg_subscription"])

churn_rate = round((churned_users / total_users) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Users", total_users)
col2.metric("Churned Users", churned_users)
col3.metric("Churn Rate", f"{churn_rate}%")
col4.metric("Avg Subscription (Months)", avg_subscription)

st.divider()

# Churn Reasons
reason_query = """
SELECT
    cancel_reason,
    COUNT(*) AS users
FROM users
WHERE churn = 1
GROUP BY cancel_reason
ORDER BY users DESC
"""

reason_df = pd.read_sql_query(reason_query, conn)

reason_chart = px.bar(
    reason_df,
    x="cancel_reason",
    y="users",
    title="Top Churn Reasons"
)

st.plotly_chart(reason_chart, use_container_width=True)

# Plan-wise Churn
plan_query = """
SELECT
    plan_type,
    ROUND(AVG(churn) * 100, 2) AS churn_rate
FROM users
GROUP BY plan_type
"""

plan_df = pd.read_sql_query(plan_query, conn)

plan_chart = px.pie(
    plan_df,
    values="churn_rate",
    names="plan_type",
    title="Plan-wise Churn Rate"
)

st.plotly_chart(plan_chart, use_container_width=True)

# Data Table
st.subheader("📋 Churn Reason Breakdown")
st.dataframe(reason_df, use_container_width=True)

st.divider()

# AI Report
st.header("🤖 AI Generated Retention Recommendations")

try:
    with open("retention_report.txt", "r", encoding="utf-8") as file:
        report_text = file.read()

    st.markdown(report_text)

except FileNotFoundError:
    st.warning("retention_report.txt not found. Generate AI report first.")

# Footer
st.divider()
st.caption(
    "Built using Python, SQLite, SQL Analytics, Streamlit and Gemini AI"
)

conn.close()