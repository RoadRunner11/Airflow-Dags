__version__ = '1.0.0'


def setupLibrary(name):
    from .log import getLogger
    from .cfg import getConfig
    config = getConfig(name)
    logger = getLogger(name, config)
    return config, logger
