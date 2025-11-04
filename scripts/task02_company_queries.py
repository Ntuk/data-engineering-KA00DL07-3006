import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

db_path = "data/company_data/company_database.db"
conn = sqlite3.connect(db_path)

# Output directory for reports
report_dir = "reports/task02_company_data"
os.makedirs(report_dir, exist_ok=True)

# Query to join employee_projects and employees_realistic
query_join = """
SELECT 
    ep.project_id,
    ep.employee_id,
    ep.hours_worked,
    er.salary
FROM employee_projects AS ep
JOIN employees_realistic AS er
    ON ep.employee_id = er.employee_id;
"""

df_join = pd.read_sql_query(query_join, conn)
print(df_join.head())

# Query to calculate total salary costs per project
query_salary_costs = """
SELECT
    ep.project_id,
    SUM((er.salary / 1900.0) * ep.hours_worked) AS salary_costs
FROM employee_projects AS ep
JOIN employees_realistic AS er
    ON ep.employee_id = er.employee_id
GROUP BY ep.project_id;
"""

df_costs = pd.read_sql_query(query_salary_costs, conn)
print(df_costs.head())

# Join salary costs per project with project budgets
query_join_budget = """
SELECT
    p.project_id,
    p.budget,
    sc.salary_costs
FROM projects AS p
JOIN (
    SELECT
        ep.project_id,
        SUM((er.salary / 1900.0) * ep.hours_worked) AS salary_costs
    FROM employee_projects AS ep
    JOIN employees_realistic AS er
        ON ep.employee_id = er.employee_id
    GROUP BY ep.project_id
) AS sc
    ON p.project_id = sc.project_id;
"""

df_budget = pd.read_sql_query(query_join_budget, conn)
print("\nJoined with budgets:")
print(df_budget.head())

# Calculate what fraction (%) of each project budget is used for salaries
query_fraction = """
SELECT
    p.project_id,
    p.budget,
    sc.salary_costs,
    ROUND((sc.salary_costs / p.budget) * 100, 2) AS salary_cost_percent
FROM projects AS p
JOIN (
    SELECT
        ep.project_id,
        SUM((er.salary / 1900.0) * ep.hours_worked) AS salary_costs
    FROM employee_projects AS ep
    JOIN employees_realistic AS er
        ON ep.employee_id = er.employee_id
    GROUP BY ep.project_id
) AS sc
    ON p.project_id = sc.project_id
ORDER BY salary_cost_percent DESC;
"""

df_fraction = pd.read_sql_query(query_fraction, conn)

print("\nSalary cost as % of budget:")
print(df_fraction.head())

# Visualize the salary cost percentage per project
plt.figure(figsize=(10, 6))
plt.bar(df_fraction["project_id"].astype(str), df_fraction["salary_cost_percent"])
plt.title("Salary Cost as % of Project Budget")
plt.xlabel("Project ID")
plt.ylabel("Salary Cost (%) of Budget")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(report_dir, "salary_cost_fraction.png"))
plt.show()

conn.close()
