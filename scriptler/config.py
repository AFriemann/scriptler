# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<aljosha.friemann@gmail.com> wrote this file.  As long as you retain this
notice you can do whatever you want with this stuff. If we meet some day,
and you think this stuff is worth it, you can buy me a beer in return.
----------------------------------------------------------------------------

"""

import logging

# F*** configparser and everybody who wrote it..

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

from simple_model import Model, Attribute, AttributeList

logging.getLogger('simple_model').setLevel(logging.WARNING)

class Source(Model):
    name   = Attribute(str)
    url = Attribute(str)
    user = Attribute(str, optional=True)
    password = Attribute(str, optional=True)
    branch = Attribute(str, optional=True)

class Script(Model):
    name   = Attribute(str)
    path   = Attribute(str)
    source = Attribute(Source, optional=True)

class Config(Model):
    path       = Attribute(str)
    script_dir = Attribute(str)
    scripts    = AttributeList(Script, fallback=[])

def parse_config(config_path, defaults = {}):
    config = ConfigParser()
    config.read([ config_path ])

    scriptler = defaults
    scripts = []

    if 'scripts' in config:
        for key, value in dict(config['scripts']).items():
            if ':' in value:
                source_name, path = value.split(':', 1)

                assert source_name in config, "source %s is not defined" % source_name

                source = Source(name = source_name, **dict(config[source_name]))
            else:
                path = value
                source = None

            scripts.append(Script(name = key, path = path, source = source))

    if 'scriptler' in config:
        scriptler.update(config['scriptler'])

    del config

    return Config(path = config_path, scripts = scripts, **scriptler)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
