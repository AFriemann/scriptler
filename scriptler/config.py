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

import logging, json, subprocess, os

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

    if config.has_section('scripts'):
        for key in config.options('scripts'):
            value = config.get('scripts', key)
            if ':' in value:
                source_name, path = value.split(':', 1)

                assert config.has_section(source_name), "source %s is not defined" % source_name

                source = Source(name = source_name, **dict(config.items(source_name)))
            else:
                path = value
                source = None

            scripts.append(Script(name = key, path = path, source = source))

    if config.has_section('scriptler'):
        scriptler.update(config.items('scriptler'))

    del config

    return Config(path = config_path, scripts = scripts, **scriptler)

def pretty_print(config):
    print(json.dumps(dict(config), sort_keys=True, indent=4))

def edit(config):
    editor = os.environ.get('EDITOR')

    if editor is None:
        raise RuntimeError('Environment variable EDITOR is not set.')

    return subprocess.call([editor, config.path])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
