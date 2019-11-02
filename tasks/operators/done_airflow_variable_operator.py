from airflow import models
from airflow.models import Variable
from airflow.utils.decorators import apply_defaults
from dateutil import parser
import logging as logger
from cfg import config


class DoneAirflowVariableOperator(models.BaseOperator):

    """Set an airflow variable indicate the timestamp of the latest DAG run.

    Format:
        {
            'dag_id': '%Y%m%d_%H%M'
        }
    """

    @apply_defaults
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def execute(self, context):
        # Timestamp of the latest DAG run
        execution_time = (parser
                          .parse(context['ts'])
                          .replace(tzinfo=None, hour=0, minute=0)
                          .strftime(config.FORMAT_TIME_TEMPLATE))

        try:
            Variable.set(
                context['dag'].dag_id,
                execution_time
            )
        except Exception as e:
            logger.error('Cannot set Airflow Variable. Please check the data type of variable.')
            raise e
        return True
