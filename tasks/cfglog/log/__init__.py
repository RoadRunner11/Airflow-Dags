''' Setup a nice formatter, configurable level, and syslog handler for logging.
    https://github.com/mitodl/flask-log/blob/master/flask_log.py
'''
import sys
import logging
import platform

from tasks.cfglog.cfg import getConfig, config


def __sif__():
    LOGGERS = dict()

    class NoConfigValue(Exception):
        pass

    def getLoggerHandler(logspec=None):
        def parse_spec(prefix, cls, defport=None):
            if not logspec.startswith(prefix):
                return None

            hostname, _, port = logspec[len(prefix):].partition(':')
            hostname = hostname or 'localhost'
            port = int(port) if port else defport
            return cls(hostname, port)

        def wrap_syslog(host, port):
            return logging.handlers.SysLogHandler(
                address=(host, port),
                facility=logging.handlers.SysLogHandler.LOG_LOCAL0
            )

        if logspec == 'stderr' or logspec is None:
            return logging.StreamHandler(sys.stderr)

        if logspec == 'stdout':
            return logging.StreamHandler(sys.stdout)

        for prefix, wrapper, defport in (
            ('syslog://', wrap_syslog, 514)
            ('udp://', logging.handlers.DataGramHandler, None),
            ('tcp://', logging.handlers.SocketHandler, None),
            ('unix://', logging.handlers.SocketHandler, None)
        ):
            handler = parse_spec(prefix, wrapper, defport)
            if handler is not None:
                return handler

        if logspec.startswith('file://'):
            return logging.FileHandler(logspec[7:])

        raise ValueError('Cannot parse logging spec: %s' % logspec)

    def setupLogger(module_name, log_config):
        ''' Setup the logging handlers, level and formatters.
        '''
        module_logger = logging.getLogger(module_name)

        if log_config is None:
            return module_logger

        def get_config_value(name):
            value = getattr(log_config, name, None)
            if isinstance(value, str):
                return value

            raise NoConfigValue('Invalid log config value: {} = {}'.format(name, value))

        try:
            log_level = get_config_value('LOG_LEVEL')
            log_level = getattr(logging, log_level.upper(), None)

            if not isinstance(log_level, int):
                raise ValueError('Invalid log level: {0}'.format(log_level))
        except (ValueError, NoConfigValue):
            log_level = None
        finally:
            module_logger.setLevel(log_level if log_level else logging.NOTSET)

        try:
            module_logger.propagate = get_config_value('LOG_PROPAGATE') == 'True'
        except NoConfigValue:
            module_logger.propagate = True

        log_handlers = []
        try:
            log_output = get_config_value('LOG_OUTPUT')
        except NoConfigValue:
            log_output = None

        try:
            log_output_secondary = get_config_value('LOG_OUTPUT_SECONDARY')
        except NoConfigValue:
            log_output_secondary = None

        if log_output:
            log_handlers.append(getLoggerHandler(log_output))
        elif module_name is None:
            # Setup root logger if no output specified.
            log_handlers.append(getLoggerHandler())

        if log_output_secondary:
            log_handlers.append(getLoggerHandler(log_output_secondary))

        try:
            log_formatter = get_config_value('LOG_FORMATTER')
        except NoConfigValue:
            pass
        else:
            # Set up format for default logging
            hostname = platform.node().split('.')[0]
            formatter = log_formatter.format(hostname=hostname)

            ''' Override the default log formatter with your own.
            '''
            # Add our formatter to all the handlers
            for handler in log_handlers:
                handler.setFormatter(logging.Formatter(formatter))

        # Special case for the root logger
        if module_name is None:
            # Setup basic StreamHandler logging with format and level (do
            # setup in case we are main, or change root logger if we aren't.
            logging.basicConfig(handlers=log_handlers)
        else:
            for handler in log_handlers:
                module_logger.addHandler(handler)

        LOGGERS[module_name] = module_logger
        return module_logger

    def getLogger(module_name, log_config=None):
        if module_name in LOGGERS:
            return LOGGERS[module_name]

        log_config = log_config or getConfig(module_name)
        return setupLogger(module_name, log_config)

    return getLogger, setupLogger(None, config)


getLogger, logger = __sif__()
