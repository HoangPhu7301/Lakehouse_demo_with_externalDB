from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="lakehouse_spark_etl_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["lakehouse", "spark", "example"],
    description=(
        "Example DAG placeholder for orchestrating the lakehouse Spark ETL "
        "(Spark + Hudi + Trino)."
    ),
) as dag:
    extract = BashOperator(
        task_id="extract_from_external_db",
        bash_command=(
            'echo "TODO: run spark-submit inside the spark container to pull '
            'from external PostgreSQL";'
        ),
    )

    load = BashOperator(
        task_id="load_to_lakehouse",
        bash_command=(
            'echo "TODO: write Hudi tables to MinIO / lakehouse bucket";'
        ),
    )

    query = BashOperator(
        task_id="query_with_trino",
        bash_command=(
            'echo "TODO: run Trino queries or materializations over the lake";'
        ),
    )

    extract >> load >> query
