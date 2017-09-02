#!/bin/python3
"""
dataleech - a backup plan using zfs...
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import os
import subprocess

# Interface class for ZFS. I don't like existing libarys and don't want
# to implement a native interface. Subprocess works just fine
# Only needed functions implemented!
class ZFS(object):
    """TODO for ZFS"""

    def __init__(self):
        super(ZFS, self).__init__()


    # internal util function
    def _exec(self, cmdname, args):
        if cmdname not in ["zfs", "zpool"]:
            return (None, None)

        sarr = []
        sarr.append(cmdname)
        for i in args.split(" "):
            sarr.append(i)

        cp_out = subprocess.run(sarr, stdout=subprocess.PIPE)

        return (cp_out.stdout.decode('UTF-8')[0:(len(cp_out.stdout.decode('UTF-8'))-1)], cp_out.returncode)


    # ZFS Utils need superuser privileges
    def checkrequirements(self):
        if os.getuid() != 0:
            return False
        return True

    # Check if a pool exists
    def check_pool_exists(self, poolname):
        out, ecode = self._exec("zpool", "status %s -x" % poolname)

        if ecode ==0:
            return True
        return False


    # Get list of datasets
    def getdatasets(self):

        out, ecode = self._exec("zfs", "list -H -o name")

        if ecode == 0:
            datasetlist = out.split("\n")

            return datasetlist

        return None


    # Returns a list of all snapshots for a defined dataset/subdataset
    def getsnaplist(self, dataset, subdataset=None):

        if subdataset:
            dataset = dataset + "/" + subdataset

        ssnaplist, ecode = self._exec("zfs", "list -H -t snapshot -o name -s creation -r " + dataset)

        if ecode < 0:
            return []

        if len(ssnaplist) == 0:
            return []

        snaplist = []
        for i in ssnaplist.split("\n"): snaplist.append(i.split("@")[1])

        return snaplist


    def snapshot(self, name, dataset):

        if not self.checkrequirements:
            return False

        if not name:
            return

        if not dataset:
            return

        snapname = dataset + "@" + name

        out, ecode = self._exec("zfs", "snapshot " + snapname)

        if ecode == 0:
            return True

        return False


    def destroysnapshot(self, name, dataset):

        if not self.checkrequirements:
            return False

        out, ecode = self._exec("zfs", "destroy " + dataset  + "@" + name)

        if ecode == 0:
            return True

        return False
