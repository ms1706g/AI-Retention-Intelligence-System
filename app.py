import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="AI Retention Intelligence System",
    layout="wide"
)

st.title("📊 AI-Powered User Retention Intelligence System")

conn = sqlite3.connect("retention.db")

# KPI Query
summary_query = """
SELECT
COUNT(*) AS total_users,
SUM(churn) AS churned_users,
ROUND(AVG(subscription_months),2) AS avg_subscription
FROM users
"""

summary_df = pd.read_sql_query(summary_query, conn)

total_users = int(summary_df["total_users"][0])
churned_users = int(summary_df["churned_users"][0])
avg_subscription = float(summary_df["avg_subscription"][0])

churn_rate = round(
    (churned_users / total_users) * 100,
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Users", total_users)
col2.metric("Churned Users", churned_users)
col3.metric("Churn Rate", f"{churn_rate}%")
col4.metric("Avg Subscription", avg_subscription)

import plotly.express as px

reason_query = """
SELECT cancel_reason,
COUNT(*) AS users
FROM users
WHERE churn = 1
GROUP BY cancel_reason
"""

reason_df = pd.read_sql_query(reason_query, conn)

fig = px.bar(
    reason_df,
    x="cancel_reason",
    y="users",
    title="Top Churn Reasons"
)

st.plotly_chart(fig, width="stretch")

plan_query = """
SELECT
plan_type,
ROUND(AVG(churn)*100,2) AS churn_rate
FROM users
GROUP BY plan_type
"""

plan_df = pd.read_sql_query(plan_query, conn)

fig2 = px.pie(
    plan_df,
    values="churn_rate",
    names="plan_type",
    title="Plan Wise Churn"
)

st.plotly_chart(fig2, width="stretch")

st.header("🤖 AI Generated Retention Recommendations")

with open(
    "retention_report.txt",
    "r",
    encoding="utf-8"
) as f:
    report = f.read()

st.markdown(report)

conn.close()