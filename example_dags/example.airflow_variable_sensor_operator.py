"""Example DAG demonstrating the usage of the AirflowVariableSensorOperator."""
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from tasks.operators.airflow_variable_sensor_operator import AirflowVariableSensorOperator
import airflow
from dateutil import parser

# Define the DAG
with DAG(
    dag_id='example.airflow_variable_sensor_operator',
    default_args={"owner": "ngu.truong", "start_date": airflow.utils.dates.days_ago(2)},
    schedule_interval=None
) as dag:

    def variable_checker(**kwargs) -> bool:
        execution_time = (parser
                          .parse(kwargs['ts'])
                          .replace(tzinfo=None, hour=0, minute=0)
                          .strftime('%Y%m%d_%H%M'))
        signal_match = Variable.get('example.airflow_variable_operator', default_var='')
        if signal_match:
            if execution_time <= signal_match:  # pass
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
