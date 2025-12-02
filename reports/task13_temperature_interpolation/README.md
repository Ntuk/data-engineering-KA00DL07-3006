# Task 13 – Temperature Data Gap Analysis & Interpolation

**Objective:**  
Investigate missing values in global temperature observations, fill the gaps using several interpolation methods, and compare the results both visually and statistically.

---

## Steps

1. Loaded dataset from  
   `data/temperature_observations/Temperature_data_with_gaps.csv`

2. Converted the `Time` column to `datetime` and set it as the DataFrame index

3. Calculated number of missing values and missing value percentage

4. Applied multiple Pandas interpolation methods:
   - **linear**
   - **index**
   - **nearest**
   - **spline**

5. Plotted all interpolated series on the same graph for visual comparison

6. Compared statistical summaries (mean, std, min, max) for each interpolation method.

Script used:  
`scripts/task13_temperature_interpolation.py`

Plot saved to:  
`reports/task13_temperature_interpolation/interpolation_comparison.png`

---

## Findings

### Missing data
- `Temperature`: 758 missing values  
- Missing fraction: ~3.16%

### Interpolation Behavior
All interpolation methods produced curves that almost completely overlap. This is expected because:

- Missing values are short and scattered, not long continuous gaps.
- The temperature data shows a smooth, seasonal pattern, making interpolation reliable

**Method observations:**

- Linear** and Index interpolation produce identical results.
- Nearest interpolation introduces small step-like sections but follows the trend closely.
- Spline interpolation is smooth and does not overshoot, indicating stable data.

### Recommended Method
For this dataset, linear interpolation is the most practical and stable choice due to its simplicity and accuracy.

---

## Result
All missing temperature values were successfully filled using multiple interpolation approaches.
Visual and statistical comparisons showed no significant artifacts or deviations.

This task demonstrates effective handling of missing data in time series and highlights how interpolation methods behave with small, scattered gaps in well-structured climate data.

---