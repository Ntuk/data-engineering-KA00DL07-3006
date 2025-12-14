from __future__ import annotations

import os
from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import bigquery

GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
BQ_DATASET = os.environ.get("BQ_DATASET", "de_exercise17_us")

RAW_LOCAL = "/opt/airflow/reports/task17_bigquery_etl_elt/task17_usa_names_raw.csv"
XFORM_LOCAL = "/opt/airflow/reports/task17_bigquery_etl_elt/task17_usa_names_top20.csv"

DEST_TABLE_LOCAL_LOAD = f"{GCP_PROJECT_ID}.{BQ_DATASET}.names_top20_local"
DEST_TABLE_ACTION = f"{GCP_PROJECT_ID}.{BQ_DATASET}.names_yearly_gender_summary"


def extract_from_bigquery_to_local_csv():
    client = bigquery.Client(project=GCP_PROJECT_ID)

    sql = """
    SELECT year, name, gender, number
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year BETWEEN 2000 AND 2020
    """
    df = client.query(sql).to_dataframe()

    os.makedirs(os.path.dirname(RAW_LOCAL), exist_ok=True)
    df.to_csv(RAW_LOCAL, index=False)


def transform_locally_with_pandas():
    df = pd.read_csv(RAW_LOCAL)

    grouped = (
        df.groupby(["year", "gender", "name"], as_index=False)["number"]
          .sum()
    )

    grouped["rank"] = grouped.groupby(["year", "gender"])["number"].rank(
        method="first", ascending=False
    )

    top20 = grouped[grouped["rank"] <= 20].copy()
    top20 = top20.sort_values(["year", "gender", "rank"])

    top20.to_csv(XFORM_LOCAL, index=False)


def load_local_csv_to_bigquery():
    client = bigquery.Client(project=GCP_PROJECT_ID)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(XFORM_LOCAL, "rb") as f:
        job = client.load_table_from_file(
            f,
            DEST_TABLE_LOCAL_LOAD,
            job_config=job_config,
        )
    job.result()


def action_query_in_bigquery():
    client = bigquery.Client(project=GCP_PROJECT_ID)

    sql = f"""
    CREATE OR REPLACE TABLE `{DEST_TABLE_ACTION}` AS
    SELECT
      year,
      gender,
      COUNT(DISTINCT name) AS distinct_names,
      SUM(number) AS total_babies,
      AVG(number) AS avg_babies_per_name
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year BETWEEN 2000 AND 2020
    GROUP BY year, gender
    ORDER BY year, gender
    """

    job = client.query(sql, location="US")
    job.result()


with DAG(
    dag_id="task17_bigquery_etl_elt",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["course17"],
) as dag:
    t1 = PythonOperator(
        task_id="extract_bigquery_to_local_csv",
        python_callable=extract_from_bigquery_to_local_csv,
    )

    t2 = PythonOperator(
        task_id="transform_locally_with_pandas",
        python_callable=transform_locally_with_pandas,
    )

    t3 = PythonOperator(
        task_id="load_local_csv_to_bigquery",
        python_callable=load_local_csv_to_bigquery,
    )

    t4 = PythonOperator(
        task_id="action_query_in_bigquery",
        python_callable=action_query_in_bigquery,
    )

    t1 >> t2 >> t3 >> t4
