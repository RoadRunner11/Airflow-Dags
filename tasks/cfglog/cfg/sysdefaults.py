''' When all lookups failed. This module provides a last chance to get a config value.
    i.e. A system level default values for Config variables.

    If a variable is not defined in this file, it will throw an error if the following
    checks failed:
        - a configuration in the default configuration file (in the correct section)
        - a default value in `defaults.py`
'''

LOG_LEVEL = 'debug'
LOG_FORMATTER_LONG = ('[%(asctime)s] [{hostname}] '
                      '%(process)d %(levelname)-8s '
                      '[%(name)16.16s - %(filename)-16.16s:%(lineno)3d] '
                      '%(message)s')
LOG_FORMATTER_SHORT = ('[%(asctime).10s]  '
                       '%(process)d %(levelname)-8s '
                       '[%(name)16.16s - %(filename)-16.16s:%(lineno)3d] '
                       '%(message)s')
LOG_FORMATTER = LOG_FORMATTER_SHORT
LOG_OUTPUT = None
LOG_OUTPUT_SECONDARY = None

MONGO_HOST = 'mongo.service'
MONGO_PORT = 27017
REDIS_HOST = 'redis.service'
REDIS_PORT = 6379
EXCHANGE_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

ENABLE_CONTRACT = False
