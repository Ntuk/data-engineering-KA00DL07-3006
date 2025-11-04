import os
import pandas as pd
import sqlite3

folder = "data/company_data"
db_path = os.path.join(folder, "company_database.db")

# Create connection
conn = sqlite3.connect(db_path)

# Loop through all CSVs in the folder
for file in os.listdir(folder):
    if file.endswith(".csv"):
        table_name = file.replace(".csv", "")
        df = pd.read_csv(os.path.join(folder, file))
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Imported {table_name} ({len(df)} rows)")

conn.close()
print("\ncompany_database.db created")
