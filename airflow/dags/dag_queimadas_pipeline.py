from airflow.providers.standard.operators.bash import BashOperator

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
        dag_id='pipeline_inpe_queimadas',
        default_args=default_args,
        description='Pipeline de focos de incêndio',
        schedule_interval='@daily',
        catchup=True,
        max_active_runs=1,
        tags=['etl', 'inpe']
) as dag:

    ingestao_api_inpe = BashOperator(
        task_id='ingestao_api_inpe',
        bash_command='cd airflow/dags/dag_queimadas_pipeline.py'
    )

    transformacao_dbt = BashOperator(
        task_id='transformacao_dbt',
    # {{ ds }} transforma a data para o formato que a função exec_api espera no bash. ex. 'python opt/airflow/src/csmd_api.py 2026-10-06'
    # o dbt lê a query com os tratamentos, entende as dependências e atualiza o banco com os dados coletados.
        bash_command='python opt/airflow/src/csmd_api.py {{ ds }}'
        )

    ingestao_api_inpe >> transformacao_dbt




















