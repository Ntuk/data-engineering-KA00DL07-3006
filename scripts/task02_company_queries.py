import sqlite3
import pandas as pd

db_path = "data/company_data/company_database.db"
conn = sqlite3.connect(db_path)

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

conn.close()
