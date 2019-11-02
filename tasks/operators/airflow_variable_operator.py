from airflow import models
from airflow.utils.decorators import apply_defaults
import logging as logger


class AirflowVariableOperator(models.BaseOperator):

    """Set an airflow variable. Assumning this is the last step of a signal DAG

    Attributes:
        variable_name (str): name of the variable
        variable_value: value of the variable
    """

    @apply_defaults
    def __init__(self, variable_name: str, variable_value, *args, **kwargs) -> None:
        self.variable_name = variable_name
        self.variable_value = variable_value
        super().__init__(*args, **kwargs)

    def execute(self, context):
        try:
            models.Variable.set(self.variable_name, self.variable_value)
        except Exception as e:
            logger.error('Cannot set Airflow Variable. Please check the data type of variable.')
            raise e
