import pandas as pd
import os
from ydata_profiling import ProfileReport

DATA_PATH = 'data/cars/cars.csv'
REPORT_DIR = 'reports/task11_data_quality'
os.makedirs(REPORT_DIR, exist_ok=True)

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Error: File not found at {DATA_PATH}")
    exit()

print("\nGenerating Pandas Profiling Report")
PROFILE_REPORT_PATH = os.path.join(REPORT_DIR, 'task11_cars_profile_report.html')

profile = ProfileReport(
    df,
    title="Cars Data Quality Report (Pandas Profiler)",
    html={'style': {'full_width': True}},
    sort=None
)

profile.to_file(PROFILE_REPORT_PATH)

print(f"Pandas Profiling Report saved to: {os.path.abspath(PROFILE_REPORT_PATH)}")