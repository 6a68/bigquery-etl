# Generated via https://github.com/mozilla/bigquery-etl/blob/master/bigquery_etl/query_scheduling/generate_airflow_dags.py

from airflow import DAG
from airflow.operators.sensors import ExternalTaskSensor
import datetime
from utils.gcp import bigquery_etl_query

default_args = {
    "owner": "jklukas@mozilla.com",
    "start_date": datetime.datetime(2019, 7, 25, 0, 0),
    "email": ["telemetry-alerts@mozilla.com", "jklukas@mozilla.com"],
    "depends_on_past": False,
    "retry_delay": datetime.timedelta(seconds=300),
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
}

with DAG("bqetl_core", default_args=default_args, schedule_interval="0 1 * * *") as dag:

    telemetry_derived__core_clients_daily__v1 = bigquery_etl_query(
        task_id="telemetry_derived__core_clients_daily__v1",
        destination_table="core_clients_daily_v1",
        dataset_id="telemetry_derived",
        project_id="moz-fx-data-shared-prod",
        owner="jklukas@mozilla.com",
        email=["jklukas@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=False,
        dag=dag,
    )

    telemetry_derived__core_clients_last_seen__v1 = bigquery_etl_query(
        task_id="telemetry_derived__core_clients_last_seen__v1",
        destination_table="core_clients_last_seen_v1",
        dataset_id="telemetry_derived",
        project_id="moz-fx-data-shared-prod",
        owner="jklukas@mozilla.com",
        email=["jklukas@mozilla.com"],
        date_partition_parameter="submission_date",
        depends_on_past=True,
        dag=dag,
    )

    wait_for_copy_deduplicate_copy_deduplicate_all = ExternalTaskSensor(
        task_id="wait_for_copy_deduplicate_copy_deduplicate_all",
        external_dag_id="copy_deduplicate",
        external_task_id="copy_deduplicate_all",
        check_existence=True,
        mode="reschedule",
        dag=dag,
    )

    telemetry_derived__core_clients_daily__v1.set_upstream(
        wait_for_copy_deduplicate_copy_deduplicate_all
    )

    telemetry_derived__core_clients_last_seen__v1.set_upstream(
        telemetry_derived__core_clients_daily__v1
    )
