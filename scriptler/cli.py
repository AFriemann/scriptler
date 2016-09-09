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

import click, os, logging

from tabulate import tabulate

from .config import Config, parse_config, pretty_print, edit
from . import scripts, __version__

logger = logging.getLogger(__name__)

def pretty_path(path):
    HOME = os.environ.get('HOME')
    return path.replace(HOME, '~')

pass_config = click.make_pass_decorator(Config)

@click.group()
@click.option('-d', '--debug/--no-debug', default=False)
@click.option('-c', '--config', type=click.Path(dir_okay=False, exists=True), default=os.path.expanduser('~/.config/scriptler/config.ini'))
@click.option('-s', '--script-dir', type=click.Path(file_okay=False), default=os.path.expanduser('~/.local/share/scriptler'))
@click.pass_context
def main(ctx, debug, config, script_dir):
    logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING)
    ctx.obj = parse_config(config, defaults={'script_dir': script_dir})

@main.command()
def version():
    print('Scriptler %s' % __version__)

@main.command()
@pass_config
def remove(config):
    for script in scripts.get_all(config.script_dir):
        print('removing %s' % os.path.basename(script))
        scripts.remove(script)

@main.command()
@pass_config
def update(config):
    for script in config.scripts:
        print('installing %s' % script.name)
        scripts.install(script, config.script_dir)

    for script in scripts.get_unmanaged(config.script_dir, config.scripts):
        print('removing unmanaged file %s' % os.path.basename(script))
        scripts.remove(script)

table_formats = [
    'plain',
    'simple',
    'grid',
    'fancy_grid',
    'pipe',
    'orgtbl',
    'rst',
    'mediawiki',
    'html',
    'latex',
    'latex_booktabs',
]

@main.command()
@click.option('-f', '--table-format', type=click.Choice(table_formats), default='simple')
@pass_config
def status(config, table_format):
    config_table = [
        ['config file', pretty_path(config.path)],
        ['script dir', pretty_path(config.script_dir)]
    ]

    print(tabulate(config_table, tablefmt='plain') + '\n')

    all_scripts = list(scripts.get_all(config.script_dir))
    unmanaged_scripts = list(scripts.get_unmanaged(config.script_dir, config.scripts))

    script_table = [ (os.path.basename(s), s not in unmanaged_scripts) for s in all_scripts ]

    print(tabulate(script_table, headers=['script', 'managed'], tablefmt=table_format))

@main.group()
def config():
    pass

@config.command()
@pass_config
def view(config):
    pretty_print(config)

@config.command(name='edit')
@pass_config
def config_edit(config):
    return edit(config)

def run():
    try:
        return main()
    except AssertionError as e:
        raise RuntimeError(str(e))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
