import pandas as pd
import sqlite3

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

print(df.head())
print(df.dtypes)
