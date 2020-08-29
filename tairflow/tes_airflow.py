from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
default_args = {
    'owner': 'tairflow',
    'email': ['fali@ampath.or.ke'],
    'email_on_failure': True,
    'email_on_retry': True,
    'email_on_success': False,
    'start_date': datetime(2020, 8, 17)
}
from cachelib import BaseCache
dag = DAG(
    dag_id='hello_world_dag',
    default_args=default_args,
    schedule_interval='*/10 * * * *')
task1 = BashOperator(task_id="echo_hello_world", bash_command='echo Hello World!', dag=dag)
