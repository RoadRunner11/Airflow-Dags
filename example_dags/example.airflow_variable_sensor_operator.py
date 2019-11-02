"""Example DAG demonstrating the usage of the AirflowVariableSensorOperator."""
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from tasks.operators.airflow_variable_sensor_operator import AirflowVariableSensorOperator
import airflow

# Define the DAG
with DAG(
    dag_id='example.airflow_variable_sensor_operator',
    default_args={"owner": "ngu.truong", "start_date": airflow.utils.dates.days_ago(2)},
    schedule_interval=None
) as dag:

    def variable_checker() -> bool:
        signal_match = Variable.get('signal_match', default_var=0)
        if signal_match:  # pass
            return True
        return False

    set_airflow_variable_op = AirflowVariableSensorOperator(
        task_id='set_airflow_variable',
        variable_checker=variable_checker
    )

    run_this_op = BashOperator(
        task_id='run_this',
        bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"'
    )

    set_airflow_variable_op >> run_this_op
