import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

# Output directory for data
data_dir = "./data/global_temp"
os.makedirs(data_dir, exist_ok=True)

# Output directory for reports
report_dir = "./reports/task01_global_temp"
os.makedirs(report_dir, exist_ok=True)

url = "https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv"
df = pd.read_csv(url)

# Save to CSV
csv_path = os.path.join(data_dir, "global_temp.csv")
df.to_csv(csv_path, index=False)

# Save to SQLite db
db_path = os.path.join(data_dir, "global_temp.db")
conn = sqlite3.connect(db_path)
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
plt.ylabel("Temperature Anomaly °C")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(report_dir, "temperature_trends.png"))
plt.close()

# Interpolate missing values
df_interp = df_pivot.interpolate(method="linear")

# Using GCAG for forecasting
y = df_interp["gcag"].values
x = np.arange(len(y))

# Fit a linear trend model: y = m*x + b
coef = np.polyfit(x, y, 1)
trend = np.poly1d(coef)

# Project the next 120 months (10 years)
future_months = 120
x_future = np.arange(len(y) + future_months)
y_future = trend(x_future)

# Create corresponding future dates
last_date = df_interp.index.max()
future_dates = pd.date_range(last_date, periods=future_months + 1, freq="ME")[1:]

# Plot observed + projected
plt.figure(figsize=(10, 6))
plt.plot(df_interp.index, y, label="Observed (GCAG)", color="orange")
plt.plot(future_dates, y_future[-future_months:], "--", label="Projected (Next 10 Years)", color="red")
plt.title("Global Temperature Projection (GCAG)")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(report_dir, "temperature_projection.png"))
plt.close()

# Display estimated anomaly in 10 years
print(f"\nEstimated anomaly in 10 years (GCAG): {y_future[-1]:.3f} °C")
