import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("Nassau Candy Supply Chain Dashboard")
st.markdown("### Supply Chain Performance Analysis Dashboard")
# Load data
df = pd.read_csv("processed_supply_chain.csv")

# Show data
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Metrics
st.subheader("Key Metrics")

st.write("Total Orders:", len(df))
st.write("Average Lead Time:", round(df["Lead Time"].mean(), 2))

# Lead Time by Ship Mode
st.subheader("Lead Time by Ship Mode")

ship_mode = df.groupby("Ship Mode")["Lead Time"].mean()

st.bar_chart(ship_mode)
st.subheader("Lead Time by Region")
region_data = df.groupby("Region")["Lead Time"].mean()

st.bar_chart(region_data)
st.subheader("Orders by Factory")
factory_count = df["Factory"].value_counts()

st.bar_chart(factory_count)
st.subheader("Delay Analysis")

delay_percentage = (df["Lead Time"] > 1000).mean() * 100

st.metric("Delay Percentage", f"{delay_percentage:.2f}%")
st.subheader("Top 10 States by Lead Time")

state_data = (
    df.groupby("State/Province")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(state_data)
st.subheader("Lead Time by Region")

region_data = df.groupby("Region")["Lead Time"].mean()

st.bar_chart(region_data)
st.subheader("Orders by Factory")

factory_count = df["Factory"].value_counts()

st.bar_chart(factory_count)
st.subheader("Top 10 States by Lead Time")

state_data = (
    df.groupby("State/Province")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(state_data)
st.subheader("Sales by Region")

sales_region = df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots()
sales_region.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.subheader("Profit by Factory")

profit_factory = df.groupby("Factory")["Gross Profit"].sum()

fig, ax = plt.subplots()
profit_factory.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.subheader("Top 10 Products")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots()
top_products.plot(kind="bar", ax=ax)
st.pyplot(fig)
st.subheader("Factory Order Count")
st.write(df["Factory"].value_counts())