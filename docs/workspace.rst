===============
About workspace
===============

Workspace is user directory to manage all data of Gears.

Structure
=========

Default files.

* ``settings.toml``
* ``bin/`` (installed executable files)
* ``cache``
* ``logs/``
* ``repos/`` (Items repository contents)


Rule of finding workspace
=========================

#. Passed ``--workspace`` argument by calling CLI.
#. Passed environment variable ``GEARS_HOME``.
#. ``${USER_HOME}/.gears`` (ex: ``/home/USER/.gears`` )
