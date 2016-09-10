scriptler
=========

Scriptler allows you to manage scripts from different sources in one place with a simple configuration file.

installation
------------

As usual, use pip to install::

    $ pip install --user scriptler

usage
-----

First off, create a configuration file in ~/.config/scriptler/config::

    [scriptler]
    script_dir = ~/.local/share/scriptler

    [afriemann/scripts.git]
    url = github.com/AFriemann/scripts
    branch = master

    [scripts]
    socksme = ~/git/scripts/bash/socksme
    proxy-foxy = ~/git/scripts/bash/proxy-foxy
    swap = afriemann/scripts.git:bin/swap

The only thing of note is that the section scripts is reserved for the actual scripts. Repository sections may be
named however you please.
The `scriptler` section is not required (~/.local/share/scriptler is the default) but should be something you have
write access to and can add to your $PATH.

To install the scripts, simply run::

    $ scriptler update
    installing socksme
    installing swap
    installing proxy-foxy
    removing unmanaged file foobar

This will also remove unmanaged files (those that you removed from your configuration file/never added).

And to remove them again::

    $ scriptler remove
    removing swap
    removing proxy-foxy
    removing socksme

To get a nice list of currently installed scripts::

    $ scriptler status
    config file  ~/.config/scriptler/config
    script dir   ~/.local/share/scriptler

    script     managed    installed
    ---------  ---------  -----------
    swap       yes        no
    proxy-foxy yes        yes
    socksme    yes        yes
    foobar     no         yes

todo
----

* scriptler will ruthlessly reinstall files. Right now I don't care, but it would probably be better to change that
* the only sources supported right now are github and local files
* write some tests to ensure functionality

license
-------

"THE BEER-WARE LICENSE" (Revision 42)::

    <aljosha.friemann@gmail.com> wrote this file.  As long as you retain this
    notice you can do whatever you want with this stuff. If we meet some day,
    and you think this stuff is worth it, you can buy me a beer in return.

