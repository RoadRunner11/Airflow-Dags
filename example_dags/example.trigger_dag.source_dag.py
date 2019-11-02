import airflow
from airflow.models import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator


dag = DAG(
    dag_id='example.trigger_dag.source_dag',
    default_args={'start_date': airflow.utils.dates.days_ago(2), 'owner': 'ngu.truong'},
    schedule_interval='@once',
)


def trigger(context, dag_run_obj):
    dag_run_obj.payload = {'message': context['params']['message']}
    return dag_run_obj


trigger = TriggerDagRunOperator(
    dag=dag,
    task_id='test_trigger_dagrun',
    trigger_dag_id="example.trigger_dag.target_dag",
    python_callable=trigger,
    params={'message': 'Hello World'}
)
