# Task 12 – Titanic Dataset Data Quality Analysis

**Objective:**  
Evaluate the quality of `titanic.csv`, identify errors (missing/invalid data), and describe how to fix them.

---

## Steps

1. Loaded dataset from `data/titanic/titanic.csv`
2. Analyzed structure, summary statistics, and missing values using Pandas  
3. Ran rule-based checks for invalid categories and numeric ranges  
4. Identified incorrect values in `Survived`, `Pclass`, `Sex`, and `Fare`

Script used:  
`scripts/task12_data_quality_titanic.py`

---

## Findings

### Missing values
- Survived: 1  
- Pclass: 3  
- Name: 1  
- Sex: 3  
- Age: 3  
- Parents/Children Aboard: 5  
- Fare: 4  

### Invalid values detected

#### Survived  
Contains invalid values: `-1`, `3`, `10`

#### Pclass  
Contains invalid values: `0`, `6`, `22`, `33`  
Also has missing values.

#### Sex  
Invalid entries:
`F`, `Male`, `Female`, `emale`, `boy`, `fem`, `M`, blank, NaN  
Allowed values: `male`, `female`

#### Fare  
One negative entry: `-20.525`

#### Parents/Children Aboard  
Unrealistic high value: `13`

#### Name  
One blank/missing name

---

## Proposed Fixes

- Replace invalid `Survived` values with `NaN` → then impute or drop
- Standardize `Sex` to lowercase → map misspellings to correct values or set as missing
- Replace invalid `Pclass` values with mode (3)
- Replace negative `Fare` with `NaN` → impute with median fare per class
- Correct extreme `Parents/Children Aboard` values or set to `NaN`
- Drop or investigate blank `Name` row

---

## Result

All major quality issues identified:
- Missing values
- Incorrect category entries
- Impossible numeric value
- Spelling inconsistencies

---
