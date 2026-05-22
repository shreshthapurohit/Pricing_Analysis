import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Data
data = {
    "Price": [10, 15, 20, 25, 30, 35, 40],
    "Units_Sold": [100, 90, 80, 60, 50, 30, 20]
}

# Step 2: DataFrame
df = pd.DataFrame(data)

# Step 3: Revenue (IMPORTANT LINE)
df["Revenue"] = df["Price"] * df["Units_Sold"]

optimal = df.loc[df["Revenue"].idxmax()]

print("\nBest Price (Optimal):")
print(optimal)

# Step 4: Print full table
print(df)
# Calculate percentage change
df["Price_Change"] = df["Price"].pct_change()
df["Demand_Change"] = df["Units_Sold"].pct_change()

# Elasticity
df["Elasticity"] = df["Demand_Change"] / df["Price_Change"]

print("\nElasticity Table:")
print(df[["Price", "Units_Sold", "Elasticity"]])

# Step 5: Graph
plt.scatter(df["Price"], df["Units_Sold"],label="All Data")
plt.scatter(optimal["Price"], optimal["Units_Sold"], color="red",s=200, label="Optimal Price ")
plt.xlabel("Price")
plt.ylabel("Units Sold")
plt.title("optimal pricing point")
plt.legend()
plt.show()