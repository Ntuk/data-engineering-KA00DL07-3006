import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

db_path = "data/company_data/company_database.db"
conn = sqlite3.connect(db_path)

# Output directory for reports
report_dir = "reports/task03_daily_sales"
os.makedirs(report_dir, exist_ok=True)

# Query daily total sales
query_sales = """
SELECT
    DATE(order_date) AS order_day,
    SUM(amount) AS daily_sales
FROM orders
GROUP BY order_day
ORDER BY order_day;
"""

# Read into DataFrame
df_sales = pd.read_sql_query(query_sales, conn)
conn.close()

# Convert order_day column to proper datetime
df_sales["order_day"] = pd.to_datetime(df_sales["order_day"])

print(df_sales.head())

# Plot daily total sales
plt.figure(figsize=(10, 6))
plt.plot(df_sales["order_day"], df_sales["daily_sales"], marker="o", linestyle="-", color="teal")
plt.title("Daily Total Sales")
plt.xlabel("Date")
plt.ylabel("Total Sales (€)")

# Format the x-axis for better readability
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.gcf().autofmt_xdate()

plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.tight_layout()

# Save the figure
plt.savefig(os.path.join(report_dir, "daily_total_sales.png"))
plt.show()
