#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

from scriptler import __version__

setup(name             = "scriptler",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      description      = "manage scripts from different sources",
      license          = read('LICENSE.txt'),
      long_description = read('README.rst'),
      url              = "https://www.github.com/afriemann/scriptler",
      keywords         = ['scripts'],
      version          = __version__,
      install_requires = requirements,
      classifiers      = [],
      packages         = ["scriptler"],
      package_data     = { 'scriptler': ['VERSION'] },
      entry_points     = { 'console_scripts': ['scriptler=scriptler.cli:run'] },
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
