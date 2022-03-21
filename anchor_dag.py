from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from anchorScraper import anchorScrape

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 3, 21),
    'email': ['chase24@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'anchor_dag',
    default_args=default_args,
    description='Predict when Anchor reserves will run out',
    schedule_interval='@daily',
)

run_etl = PythonOperator(
    task_id='anchorScraper',
    python_callable=anchorScrape,
    dag=dag,
)

run_etl