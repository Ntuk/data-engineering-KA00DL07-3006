import pandas as pd
import sqlite3

url = "https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv"
df = pd.read_csv(url)

print(df.head())

# Save to CSV
df.to_csv("global_temp.csv", index=False)

# Save to SQLite db
conn = sqlite3.connect("global_temp.db")
df.to_sql("global_temperature", conn, if_exists="replace", index=False)
conn.close()