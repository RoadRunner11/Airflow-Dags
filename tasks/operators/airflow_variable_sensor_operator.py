from airflow import sensors
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
from typing import Dict


class AirflowVariableSensorOperator(sensors.BaseSensorOperator):

    @apply_defaults
    def __init__(
        self,
        variable_checker,  # type: Callable
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if not callable(variable_checker):
            raise AirflowException('`variable_checker` param must be callable')
        self.variable_checker = variable_checker

    def poke(self, context: Dict) -> bool:
        """
        Function that the sensors defined while deriving this class should
        override.
        """
        return self.variable_checker(**context)
