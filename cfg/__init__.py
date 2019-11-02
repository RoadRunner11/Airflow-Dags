from tasks.cfglog import setupLibrary

config, logger = setupLibrary(__name__)
__all__ = ('config', 'logger')
