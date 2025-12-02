import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/temperature_observations/Temperature_data_with_gaps.csv")

print("=== Missing Values ===")
print(df.isna().sum())

missing_fraction = df.isna().mean() * 100
print("\n=== Missing Fraction (%) ===")
print(missing_fraction)

methods = ['linear', 'index', 'nearest', 'spline']
results = {}

for m in methods:
    df_interp = df.copy()
    
    try:
        if m == "spline":
            df_interp["Temperature"] = df_interp["Temperature"].interpolate(method="spline", order=3)
        else:
            df_interp["Temperature"] = df_interp["Temperature"].interpolate(method=m)

        results[m] = df_interp
        print(f"Interpolation '{m}' completed.")

    except Exception as e:
        print(f"Interpolation '{m}' failed: {e}")

plt.figure(figsize=(12, 6))
for m, data in results.items():
    plt.plot(data.index, data["Temperature"], label=m, alpha=0.7)

plt.title("Temperature Interpolation Comparison")
plt.legend()
plt.tight_layout()
plt.savefig("reports/task13_temperature_interpolation/interpolation_comparison.png", dpi=200)
plt.show()

print("\n=== Statistical Comparison ===")
for m, d in results.items():
    print(f"\nMethod: {m}")
    print(d["Temperature"].describe())