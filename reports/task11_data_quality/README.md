# Task 11 – Data Quality Assessment (cars.csv)

**Objective:**
Examine the quality of the `cars.csv` dataset, identify issues, and propose/implement fixes using profiling and validation tools.

---

### Tools Used
1.  **YData-Profiling**: For comprehensive data inspection and discovery (Part **b**).
2.  **Great Expectations (GE)**: For programmatic data validation against defined rules (Part **b**).

---

### C. Quality Issues Identified
The profiling report highlighted several critical data quality issues (Part **c**):

| Variable | Issue Type | Detail |
| :--- | :--- | :--- |
| **Cylinders** | Missing/Outliers | 4.3% missing. Extreme outlier Max value (1798) is a clear error. |
| **EngineVolume** | Missing/Outliers | 4.0% missing. Extreme outlier Max value (1,353,000) is a clear error. |
| **VehicleClass** | Zero Variance | Only one distinct value (`M1`), uninformative for analysis. |
| **Year** | Zero Variance | Only one distinct value (`2020.0`), uninformative for analysis. |
| **Transmission** | Missing Values | 0.5% missing. |

---

### D. Proposed & Implemented Fixes
The following fixes were implemented in `task11_data_quality.py` (Part **d**):

1.  **Outlier & Imputation:** For `Cylinders` and `EngineVolume`, impossible values were set to `NaN`, and all missing values were then filled using the **column median**.
2.  **Missing Categorical Data:** Missing values in `Transmission` were filled using the **mode** (most frequent value).
3.  **Feature Elimination:** The uninformative columns (`VehicleClass`, `Year`) were **dropped** from the DataFrame.

---

### B. Validation (Great Expectations)
The cleaned data was successfully validated using Great Expectations:

| Expectation | Status | Notes |
| :--- | :--- | :--- |
| `expect_column_values_to_not_be_null(column='EngineVolume')` | **PASS** | Passed after median imputation. |
| `expect_column_values_to_be_between(column='Cylinders', ...)` | **PASS** | Passed after outlier correction and imputation. |

**Script:** `scripts/task11_data_quality.py`
**Report:** `reports/task11_cars_profile_report.html`