import json
import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("data/polar")
OUTPUT_FILE = Path("data/polar_summary.csv")

def extract_summary(json_data: dict):
    """Extract general info from one Polar JSON training file."""

    # Top-level values
    start = json_data.get("startTime")
    stop = json_data.get("stopTime")
    duration = json_data.get("duration")
    distance = json_data.get("distance")
    calories = json_data.get("calories")
    avg_hr = json_data.get("averageHeartRate")
    max_hr = json_data.get("maxHeartRate")

    # First exercise block
    exercises = json_data.get("exercises", [])
    ex = exercises[0] if exercises else {}

    sport = ex.get("sport")
    ex_duration = ex.get("duration")
    ex_distance = ex.get("distance")

    hr = ex.get("heartRate", {})
    ex_hr_min = hr.get("min")
    ex_hr_avg = hr.get("avg")
    ex_hr_max = hr.get("max")

    speed = ex.get("speed", {})
    speed_min = speed.get("min")
    speed_avg = speed.get("avg")
    speed_max = speed.get("max")

    return {
        "start_time": start,
        "stop_time": stop,
        "duration_total": duration,
        "duration_exercise": ex_duration,
        "distance_total": distance,
        "distance_exercise": ex_distance,
        "calories": calories,
        "avg_hr_total": avg_hr,
        "max_hr_total": max_hr,
        "hr_min_exercise": ex_hr_min,
        "hr_avg_exercise": ex_hr_avg,
        "hr_max_exercise": ex_hr_max,
        "speed_min": speed_min,
        "speed_avg": speed_avg,
        "speed_max": speed_max,
        "sport": sport
    }

def main():
    records = []

    for file in DATA_FOLDER.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            records.append(extract_summary(data))

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved CSV: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
