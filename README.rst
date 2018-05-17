=========
DATALEECH
=========

ZFS Backup Strategy - short term local backups and long term remote sync.
Developed to be transparent and easy to use.


Usage
~~~~~

.. code-block::

    Usage: dataleech [OPTIONS] COMMAND [ARGS]...

    Commandline interface for dataleech

    Options:
    --help  Show this message and exit.

    Commands:
    snapshot  Creates a snapshot, either short, daily,...
    sync      Syncs snapshots to a local or remote backup...



Snapshot options
~~~~~~~~~~~~~~~~

.. code-block::

    Usage: dataleech snapshot [OPTIONS] NAME

    Creates a snapshot, either short, daily, weekly or custom

    Options:
    --short-keep INTEGER   How many short term snapshots to keep
    --custom-dataset TEXT  Custom dataset
    --custom-name TEXT     Custom snapshot name
    --help                 Show this message and exit.


Sync options
~~~~~~~~~~~~

.. code-block::

    Usage: dataleech sync [OPTIONS]

    Syncs snapshots to a local or remote backup target

    Options:
    -l, --local        Snyc snapshots to the local backup target
    -r, --remote       Snyc snapshots to the remote backup target
    -c, --custom       Custom source and target, please specify
    --custom-src TEXT  Custom source
    --custom-dst TEXT  Custom destination
    --help             Show this message and exit.

