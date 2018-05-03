""" Heart of dataleech """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

import sys
import click
from .cli_helper import (new_snapshot, snapsync_local, snapsync_remote,
                         snapsync_custom)


@click.option("-l", "--local", count=True,
              help="Snyc snapshots to the local backup target")
@click.option("-r", "--remote", count=True,
              help="Snyc snapshots to the remote backup target")
@click.option("-c", "--custom", count=True,
              help="Custom source and target, please specify")
@click.option("--custom-src",
              help="Custom source")
@click.option("--custom-dst",
              help="Custom destination")
@click.command()
def sync(local, remote, custom, custom_src, custom_dst):
    """
    Syncs snapshots to a local or remote backup target
    """
    # Check if there is anything to sync
    if not local and not remote:
        sys.exit(1)

    # Sync local
    if local:
        snapsync_local()

    # Sync remote
    if remote:
        snapsync_remote()

    # Custom snapsync
    if custom:
        snapsync_custom(custom_src, custom_dst)


@click.command()
@click.argument("name")
@click.option("--custom-dataset", default=None,
              help="Custom dataset")
@click.option("--custom-name", default=None,
              help="Custom snapshot name")
def snapshot(name, custom_dataset, custom_name):
    """
    Creates a snapshot, either short, daily, weekly or custom
    """
    # Check if the name is set or a valid value
    if not name or name not in ["short", "daily", "weekly", "custom"]:
        click.echo("[-] This script can only create short, daily, weekly\
                    or custom snapshots")
        sys.exit(1)

    if new_snapshot(name,
                    custom_dataset=custom_dataset,
                    custom_name=custom_name):
        click.echo("[+] Created new  {} snapshot".format(name))

    else:
        click.echo("[-] Failed to create new {} snapshot".format(name))
        sys.exit(1)


@click.group()
def cli():
    """
    Commandline interface for dataleech
    """
    pass


def dataleech_cli():
    cli.add_command(snapshot)
    cli.add_command(sync)
    cli()
