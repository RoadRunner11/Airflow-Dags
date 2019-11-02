"""Example DAG demonstrating the usage of the AirflowVariableOperator."""

from airflow import DAG
from tasks.operators.airflow_variable_operator import AirflowVariableOperator
from datetime import datetime
import airflow

# Define the DAG
with DAG(
    dag_id='example.airflow_variable_operator',
    default_args={"owner": "ngu.truong", "start_date": airflow.utils.dates.days_ago(2)},
    schedule_interval=None
) as dag:
    set_airflow_variable_op = AirflowVariableOperator(
        task_id='set_airflow_variable',
        variable_name='example.airflow_variable_operator',
        variable_value=datetime.now().strftime('%Y%m%d_%H%M')
    )
