from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'engenharia_dados_etl',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# usando 'with' para criar o container da dag
with DAG(
        dag_id='pipeline_nasa_queimadas',
        default_args=default_args,
        description='Pipeline de focos de incêndio',
        schedule_interval='0 6 * * *',
        catchup=False,
        tags=['etl', 'nasa']
) as dag:

    task_ingestao_api = BashOperator(
        task_id='ingestao_nasa_api',
        bash_command='python /path/to/project/src/csmd_api.py'
    )

    task_dbt_run = BashOperator(
        task_id='dbt_transformacao_lakehouse',
        bash_command='cd /path/to/project/dbt_queimadas && dbt run'
    )

    task_ingestao_api >> task_dbt_run




















