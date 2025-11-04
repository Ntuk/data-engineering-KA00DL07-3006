import sqlite3
import pandas as pd

db_path = "data/company_data/company_database.db"
conn = sqlite3.connect(db_path)

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

conn.close()
