""" Syncronize two datasets, either local->local or local->remote """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

from .zfs import ZFS, RemoteZFS
from .helper import get_dataleech_snapshots
import os
import sys


class SnapSync(object):
    """
    Syncronizes two datasets, either local->local or local->remote

    :param src: Source dataset
    :param dst: Destination dataset
    :param sshopts: If set, it uses the parameters to syncronize to a remote
                    dataset
    """

    def __init__(self, src, dst, sshopts=None):
        """
        Syncs one dataset to another
        """
        self.src = src
        self.dst = dst
        self.sshopts = sshopts

    def sync(self):
        # Check if destination pool exists
        if not self.sshopts:
            if not ZFS().check_pool_exists(self.dst.split("/")[0]):
                return
        else:
            if not RemoteZFS(
                    self.sshopts).check_pool_exists(
                    self.dst.split("/")[0]):
                return

        # Update snapshots
        self.update_snaps()

        while True:
            tosync = self.next_sync_snapshot
            print(tosync)
            if not tosync:
                print("Synced {} to {} -> DONE".format(self.src, self.dst))
                break
            elif tosync == self.src_snaps[0]:
                print("Initial send, forcing")
                self.initial_send(tosync)
            else:
                lastsynced = self.src_snaps[self.src_snaps.index(tosync) - 1]
                print("Incremental send, {} -> {}".format(lastsynced, tosync))
                self.incremental_send(lastsynced, tosync)

    def update_snaps(self):
        """
        Updates the source and destination snapshots
        """
        self.src_snaps = get_dataleech_snapshots(ZFS(), self.src)["syncsnaps"]
        self.dst_snaps = []

        if not self.sshopts:
            # Local destination snapshots
            self.dst_snaps = get_dataleech_snapshots(ZFS(),
                                                     self.dst)["syncsnaps"]
        else:
            # Remote destination snapshots
            self.dst_snaps = get_dataleech_snapshots(RemoteZFS(self.sshopts),
                                                     self.dst)["syncsnaps"]

    @property
    def next_sync_snapshot(self):
        """
        Next snapshot which should be synced
        """
        self.update_snaps()
        for i in self.src_snaps:
            if i not in self.dst_snaps:
                return i

        return None

    def initial_send(self, tosync):
        """
        Initial transmission of a snapshot, zfs needs the `-F` flag in that
        case.

        :param tosync: The snapshot that should be send
        :returns: Success
        """
        if not self.sshopts:
            # Local -> Local
            command = "zfs send {} | pv | zfs receive -F {}".format(
                                "@".join([self.src, tosync]),
                                self.dst)
        else:
            # Local -> Remote
            command = "zfs send {} | pv | ssh {} zfs receive -F {}".format(
                                "@".join([self.src, tosync]),
                                self.sshopts,
                                self.dst)
        status = os.system(command)
        if status != 0:
            sys.exit(-1)

    def incremental_send(self, lastsynced, tosync):
        """
        Incremental transmission of a snapshot

        :param lastsynced: Snapshot on target and destination
        :param tosync: Snapshot that should be send to the destination
        :returns: Success
        """
        if not self.sshopts:
            # Local -> Local
            command = "zfs send -i {} {} | pv | zfs receive {}".format(
                                "@".join([self.src, lastsynced]),
                                "@".join([self.src, tosync]),
                                self.dst)
        else:
            # Local -> Remote
            command = "zfs send -i {} {} | pv | ssh {} zfs receive {}".format(
                                "@".join([self.src, lastsynced]),
                                "@".join([self.src, tosync]),
                                self.sshopts,
                                self.dst)

        status = os.system(command)
        if status != 0:
            sys.exit(-1)
