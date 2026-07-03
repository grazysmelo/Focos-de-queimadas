from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'Graziele_Melo',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
        dag_id='pipeline_inpe_queimadas',
        default_args=default_args,
        description='Pipeline de focos de incêndio',
        schedule_interval='@daily',
        catchup=True,
        max_active_runs=1
        tags=['etl', 'inpe']
) as dag: