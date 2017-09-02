#!/bin/python3
"""
dataleech - a backup plan using zfs...
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from confreader import ConfReader
from zfs import ZFS
import os
import sys

class SnapSync(object):
    def __init__(self):
        pass

    def update_snaps(self):
        self.src_snaps = []
        self.dst_snaps = []

        for i in ZFS().getsnaplist(self.src):
            if "dataleech-daily" in i or "dataleech-weekly" in i:
                self.src_snaps.append(i)

        for i in ZFS().getsnaplist(self.dst):
            if "dataleech-daily" in i or "dataleech-weekly" in i:
                self.dst_snaps.append(i)


    def get_next_sync_snapshot(self):
        self.update_snaps()
        for i in self.src_snaps:
            if i not in self.dst_snaps:
                return i


        return None

    def initial_send(self, tosync, remote=None):
        if not remote:
            command = "zfs send %s | pv | zfs receive -F %s" % (self.src + "@" + tosync, self.dst)
            status = os.system(command)
            if status != 0:
                sys.exit(-1)

    def incremental_send(self, lastsynced, tosync, remote=None):
        if not remote:
            command = "zfs send -i %s %s | pv | zfs receive %s" %    (self.src+"@"+lastsynced,\
                                                                self.src+"@"+tosync,self.dst)
            status = os.system(command)
            if status != 0:
                sys.exit(-1)

    def sync_local(self, src, dst):
        self.src = src
        self.dst = dst

        # Check if destination pool exists
        if not ZFS().check_pool_exists(dst.split("/")[0]):
            return

        while True:
            tosync = self.get_next_sync_snapshot()
            if not tosync:
                print("Synced %s to %s -> DONE" % (self.src, self.dst))
                break
            elif tosync == self.src_snaps[0]:
                print("Initial send, forcing")
                self.initial_send(tosync)
            else:
                lastsynced = self.src_snaps[self.src_snaps.index(tosync)-1]
                print("Incremental send, %s -> %s" % (lastsynced, tosync))
                self.incremental_send(lastsynced, tosync)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        SnapSync().sync_local(sys.argv[1], sys.argv[2])
        sys.exit(0)

    for src, dst in ConfReader().getlocalsyncdatasets():
        SnapSync().sync_local(src, dst)

    sys.exit(0)
