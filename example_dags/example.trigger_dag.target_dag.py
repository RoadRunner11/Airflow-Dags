import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator


dag = DAG(
    dag_id='example.trigger_dag.target_dag',
    default_args={'start_date': airflow.utils.dates.days_ago(2), 'owner': 'ngu.truong'},
    schedule_interval=None,
)


def run_this_func(*args, **kwargs):
    print("Remotely received a message: {}".
          format(kwargs['dag_run'].conf['message']))


run_this = PythonOperator(
    task_id='run_this',
    python_callable=run_this_func,
    provide_context=True,
    dag=dag,
)
