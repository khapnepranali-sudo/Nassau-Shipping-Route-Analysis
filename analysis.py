import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# load dataset
df = pd.read_csv("data/Nassau Candy Distributor.csv")
# check dataset
print(df.head())
print(df.shape)
print(df.info())
print(df.isnull().sum())
# Converts Dates
df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    dayfirst=True
)

df['Ship Date'] = pd.to_datetime(
    df['Ship Date'],
    dayfirst=True
)
# Create Lead Time
df['Lead Time'] = (
    df['Ship Date'] - df['Order Date']
).dt.days 

# Remove Invalid Lead Time
df = df[df['Lead Time'] >=0]
df.to_csv(
    "data/cleaned_dataset.csv",
    index=False
)
print(df[['Order Date','Ship Date','Lead Time']].head())
factory_map = {

    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",

    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",

    "Everlasting Gobstopper": "Secret Factory",

    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory",

    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory"
}
df['Factory'] = df['Product Name'].map(factory_map)
print(df[['Product Name', 'Factory']].head())
print(df['Factory'].isnull().sum())
df['Route'] = (
    df['Factory']
    + " -> "
    + df['State/Province']
)
print(df[['Factory', 'State/Province', 'Route']].head())
df.to_csv("data/route_dataset.csv", index=False)
print("Average Lead Time:")
print(df['Lead Time'].mean())
route_volume = df.groupby('Route').size()
print(route_volume.head())
route_leadtime = df.groupby('Route')['Lead Time'].mean()
print(route_leadtime.head())
top_routes = route_leadtime.sort_values().head(10)
print(top_routes)
bottom_routes = route_leadtime.sort_values(
    ascending=False
).head(10)
print(bottom_routes)
route_variability = df.groupby(
    'Route'
)['Lead Time'].std()
print(route_variability.head())
ship_mode = df.groupby(
    'Ship Mode'
)['Lead Time'].mean()
print(ship_mode)
state_analysis = df.groupby(
    'State/Province'
)['Lead Time'].mean()
print(
    state_analysis.sort_values(
        ascending=False
    ).head(10)
)
region_analysis = df.groupby(
    'Region'
)['Lead Time'].mean()

print(region_analysis)
threshold = 910

delay_frequency = (
    (df['Lead Time'] > threshold).mean()
) * 100

print(
    "Delay Frequency:",
    delay_frequency
)
max_lt = df['Lead Time'].max()

df['Efficiency Score'] = (
    1 - (df['Lead Time'] / max_lt)
) * 100

print(
    df[['Lead Time',
        'Efficiency Score']].head()
)
df.to_csv(
    "data/final_analysis.csv",
    index=False
)
print(df[['Order Date','Ship Date']].head(20))
top_routes = route_leadtime.nsmallest(10)

plt.figure(figsize=(10,5))

top_routes.plot(kind='barh')

plt.title("Top 10 Fastest Routes")
plt.xlabel("Average Lead Time")

plt.tight_layout()

plt.savefig("visuals/top_10_fastest_routes.png")

plt.show()
slow_routes = route_leadtime.nlargest(10)

plt.figure(figsize=(10,5))

slow_routes.plot(kind='barh')

plt.title("Top 10 Slowest Routes")
plt.xlabel("Average Lead Time")

plt.tight_layout()

plt.savefig("visuals/top_10_slowest_routes.png")

plt.show()
plt.figure(figsize=(8,5))

ship_mode.plot(kind='bar')

plt.title("Ship Mode Performance")
plt.ylabel("Average Lead Time")

plt.tight_layout()

plt.savefig("visuals/ship_mode_comparison.png")

plt.show()
plt.figure(figsize=(8,5))

region_analysis.plot(kind='bar')

plt.title("Region Performance")
plt.ylabel("Average Lead Time")

plt.tight_layout()

plt.savefig("visuals/region_analysis.png")

plt.show()
# Profit Margin

df["Profit Margin"] = (df["Gross Profit"] / df["Sales"]) * 100

print(df[["Sales", "Gross Profit", "Profit Margin"]].head())
product_profit = df.groupby("Product Name")["Gross Profit"].sum()

print(product_profit.sort_values(ascending=False).head(10))
top_sales = df.groupby("Product Name")["Sales"].sum()

print(top_sales.sort_values(ascending=False).head(10))
factory_sales = df.groupby("Factory")["Sales"].sum()

print(factory_sales)
factory_profit = df.groupby("Factory")["Gross Profit"].sum()

print(factory_profit)
df["Delay Category"] = pd.cut(
    df["Lead Time"],
    bins=[0,1000,1400,2000],
    labels=["Low Delay","Medium Delay","High Delay"]
)

print(df["Delay Category"].value_counts())
df.to_csv("processed_supply_chain.csv", index=False)

print("File Saved Successfully")