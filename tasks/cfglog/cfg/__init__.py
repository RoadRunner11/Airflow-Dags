import re
import importlib
import json
import os
from typing import Optional

import configparser

APP_CONFIG_SECTION = os.environ.get('APP_CONFIG_SECTION', 'app')
APP_CONFIG_MODULE = os.environ.get(
    'APP_CONFIG_MODULE', 'tasks.cfglog.cfg.sysdefaults')
RX_INVALID_OPTION = re.compile(r'[^A-Za-z\d_]+')


def __module_config__():
    __parser__ = configparser.ConfigParser()
    __parser__.optionxform = lambda s: RX_INVALID_OPTION.sub(
        '_', s.strip()).upper()

    __config__: dict = {}

    def readfp(fp) -> None:
        __parser__.readfp(fp)

    def getvalue(instance, name, getter=__parser__.get):
        NAME = name.upper()
        try:
            return getter(instance.section, NAME)
        except configparser.NoOptionError:
            return getattr(instance.defaults, NAME)

    class ModuleConfig(object):
        def __init__(self, module_name, defaults=None):
            if module_name in __config__:
                raise ValueError(
                    'Module [{}] configured multiple times'.format(module_name)
                )

            self.section = module_name
            self.defaults = defaults
            if not __parser__.has_section(self.section):
                __parser__.add_section(self.section)

        def __getattr__(self, name):
            return getvalue(self, name)

        def getint(self, name):
            return getvalue(self, name, __parser__.getint)

        def getfloat(self, name):
            return getvalue(self, name, __parser__.getfloat)

        def getboolean(self, name):
            return getvalue(self, name, __parser__.getboolean)

        def getjson(self, name):
            def getter(section, key):
                return json.loads(__parser__.get(section, key))
            return getvalue(self, name, getter)

        def items(self):
            shadowed = set()
            for key, value in __parser__.items(self.section):
                # key = key.upper() is not required due to optionxform function above.
                assert key.isupper(), 'Config key is not transformed to uppercase: %s' % key

                shadowed.add(key)
                yield (key, value)

            try:
                attr_iter = self.defaults.__dict__.items()
            except AttributeError:
                pass
            else:
                for key, value in attr_iter:
                    if key in shadowed or not key.isupper():
                        continue

                    shadowed.add(key)
                    yield (key, value)

    def getConfig(
        module_name: Optional[str],
        defaults: str=None
    ) -> ModuleConfig:
        if module_name in __config__:
            return __config__[module_name]

        try:
            if defaults is None:
                defaults = module_name + '.defaults'
            defmod = importlib.import_module(defaults)
        except ImportError as e:
            import logging
            logging.warning(
                'Cannot import default configuration for: [%s] => %s',
                module_name,
                e
            )
            defmod = None

        __config__[module_name] = ModuleConfig(module_name, defmod)
        return __config__[module_name]

    # makes an instance of the Config helper class available to all the modules
    return ModuleConfig, getConfig, getConfig(
        APP_CONFIG_SECTION, APP_CONFIG_MODULE
    )


ModuleConfig, getConfig, config = __module_config__()
