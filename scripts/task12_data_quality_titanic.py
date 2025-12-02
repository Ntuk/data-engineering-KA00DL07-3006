import pandas as pd

df = pd.read_csv("data/titanic/titanic.csv")

print("\n=== BASIC INFO ===")
print(df.info())

print("\n=== SUMMARY STATISTICS ===")
print(df.describe(include="all"))

print("\n=== MISSING VALUES ===")
print(df.isna().sum())

print("\n=== INVALID VALUES CHECK ===")

# Survived must be 0 or 1
print("\nInvalid Survived values:")
print(df[~df["Survived"].isin([0,1])])

# Pclass must be 1, 2, 3
print("\nInvalid Pclass values:")
print(df[~df["Pclass"].isin([1,2,3]) | df["Pclass"].isna()])

# Sex must be 'male' or 'female'
print("\nInvalid Sex values:")
print(df[~df["Sex"].isin(["male","female"]) | df["Sex"].isna()])

# Age must be 0–100
print("\nInvalid Age values:")
print(df[(df["Age"] < 0) | (df["Age"] > 100)])

# Fare must be >= 0
print("\nInvalid Fare values:")
print(df[df["Fare"] < 0])
