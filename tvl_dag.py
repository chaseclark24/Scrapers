from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from tvlScraper import tvlScrape

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 3, 11),
    'email': ['chase24@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'tvl_dag',
    default_args=default_args,
    description='Defi Llama TVL Data',
    schedule_interval='@daily',
)

run_etl = PythonOperator(
    task_id='tvlScraper',
    python_callable=tvlScrape,
    dag=dag,
)

run_etl