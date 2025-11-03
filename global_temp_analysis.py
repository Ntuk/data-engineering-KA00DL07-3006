import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv"
df = pd.read_csv(url)

# Save to CSV
df.to_csv("global_temp.csv", index=False)

# Save to SQLite db
conn = sqlite3.connect("global_temp.db")
df.to_sql("global_temperature", conn, if_exists="replace", index=False)
conn.close()

# Convert 'Year' column to datetime format
df["Date"] = pd.to_datetime(df["Year"], format="%Y-%m")

# Convert to Unix epoch
df["UnixEpoch"] = df["Date"].astype("int64") // 10**9

# Pivot so that each source is a column, using 'Date' as index
df_pivot = df.pivot(index="Date", columns="Source", values="Mean")

# Drop rows with NaN values & calculate the diff between gcac and GISTEMP
comparison = df_pivot.dropna().copy()
comparison["Difference"] = comparison["gcag"] - comparison["GISTEMP"]

# Display summary statistics
print("\nComparison summary:")
print(comparison.describe())

# Show the first few difference values
print("\nSample differences:")
print(comparison.head())

# Plot temperature trends from both sources
plt.figure(figsize=(10, 6))
plt.plot(df_pivot.index, df_pivot["gcag"], label="GCAG", color="orange")
plt.plot(df_pivot.index, df_pivot["GISTEMP"], label="GISTEMP", color="blue")
plt.title("Global Temperature Trends")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly °c")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()