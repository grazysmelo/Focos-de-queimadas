from airflow.providers.amazon.aws.operators.emr import EmrServerlessStartJobOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator

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
        schedule_interval='@daily',
        catchup=False,
        tags=['etl', 'nasa']
) as dag:

    process_silver=EmrServerlessStartJobOperator(
        task_id='process_raw_to_silver',
        application_id='YOUR_EMR_APPLICATION_ID',
        execution_role_arn='YOUR_EMR_ROLE_ARN',
        job_driver={
            'sparkSubmit': {
                'entryPoint': 's3://seu-bucket-scripts/scripts/silver_processing.py',
            }
        }
    )


    processo_gold=EmrServerlessStartJobOperator(

    )


    processo_gold_repair=AthenaOperator(

    )


    processo_silver >> processo_gold >> processo_gold_repair




















