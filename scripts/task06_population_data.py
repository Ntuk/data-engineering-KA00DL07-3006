from google.cloud import bigquery
import pandas as pd
import os

# BigQuery setup
project_id = "oamk-476515"
client = bigquery.Client(project=project_id)

# Query full dataset
query = """
SELECT *
FROM `bigquery-public-data.world_bank_global_population.population_by_country`
"""
df = client.query(query).to_dataframe()


# Transform
df_long = df.melt(
    id_vars=["country", "country_code"],
    var_name="year",
    value_name="population"
)

# Clean up values
df_long["year"] = df_long["year"].str.replace("year_", "").astype(int)

# Filter for Nordics
nordics = ["Finland", "Sweden", "Norway", "Denmark", "Iceland"]
df_nordic = df_long[df_long["country"].isin(nordics)]

# Pivot to have one column per country
pivoted = df_nordic.pivot(index="year", columns="country", values="population").reset_index()
pivoted = pivoted[["year"] + nordics]

# Save
os.makedirs("reports/task06_population", exist_ok=True)
pivoted.to_csv("reports/task06_population/nordic_population.csv", index=False)

# Upload to BigQuery
table_id = f"{project_id}.population_analysis.nordic_population"
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE", autodetect=True)

job = client.load_table_from_dataframe(pivoted, table_id, job_config=job_config)
job.result()

print(f"Uploaded {len(pivoted)} rows to {table_id}")