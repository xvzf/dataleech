""" Helper functions for the commandline interface """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

import sys
from .snapsync import SnapSync
from .confreader import ConfReader
from .snapmanager import SnapManager


def new_snapshot(snapshot_type, custom_dataset, custom_name=None):
    """
    Creates a new snapshot

    :param snapshot_type: short, daily or weekly
    :returns: Success
    """

    if snapshot_type == "short":
        return SnapManager(ConfReader().shortsnapdatasets).newshortsnap()
    elif snapshot_type == "daily":
        return SnapManager(ConfReader().dailysnapdatasets).newdailysnap()
    elif snapshot_type == "weekly":
        return SnapManager(ConfReader().weeklysnapdatasets).newweeklysnap()
    elif snapshot_type == "custom":
        return SnapManager([custom_dataset]).newcustomsnap(custom_name)
    else:
        return False


def snapsync_local():
    """
    Syncronize snapshots to local backup target
    """
    for src, dst in ConfReader().localsyncdatasets:
        SnapSync(src, dst).sync()


def snapsync_remote():
    """
    Syncronize snapshots to remote backup target
    """
    sshopts = ConfReader().sshopts
    if not sshopts:
        print("[-] SSH options needed for remote sync")
        sys.exit(1)

    for src, dst in ConfReader().remotesyncdatasets:
        SnapSync(src, dst, sshopts).sync()


def snapsync_custom(src, dst):
    """
    Syncronizes dataleech snapshots from a custom source to a custom target
    """
    if not src or not dst:
        print("[-] Invalid source or destination")
        sys.exit(1)

    SnapSync(src, dst).sync()
