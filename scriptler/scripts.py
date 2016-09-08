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

import os, logging, stat

from . import sources

logger = logging.getLogger(__name__)

def get_all(path, only_executable = True):
    for root,dirs,files in os.walk(path):
        for file in files:
            abspath = os.path.join(root, file)

            if only_executable:
                if os.access(abspath, os.X_OK):
                    yield abspath
            else:
                yield abspath

def get_unmanaged(path, managed_scripts):
    managed_script_names = [ s.name for s in managed_scripts ]
    for script in get_all(path, False):
        if os.path.basename(script) not in managed_script_names:
            yield script

def get_managed(path, managed_scripts):
    managed_script_names = [ s.name for s in managed_scripts ]
    for script in get_all(path, False):
        if os.path.basename(script) in managed_script_names:
            yield script

def make_executable(path):
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)

def install(script, script_dir):
    logger.debug('installing %s to %s', script, script_dir)

    os.makedirs(script_dir, exist_ok=True)

    basepath = os.path.join(script_dir, script.name)

    sources.get(script.path, script.source, basepath)

    make_executable(basepath)

def remove(path):
    logger.debug('deleting %s', path)

    os.remove(path)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
