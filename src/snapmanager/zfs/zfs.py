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

        return (cp_out.stdout.decode('UTF-8'), cp_out.returncode)


    # ZFS Utils need superuser privileges
    def checkrequirements(self):
        if os.getuid() != 0:
            return False
        return True


    # Get list of datasets
    def getdatasets(self):

        if not self.checkrequirements:
            return None

        out, ecode = self._exec("zfs", "list")

        if ecode == 0:

            datasetlist = []

            for i in out.split("\n")[1:(len(out.split("\n"))-1)]:

                datasetlist.append(i.split(" ")[0])

            return datasetlist

        return None


    # Returns a list of all snapshots for a defined dataset/subdataset
    def getsnaplist(self, dataset, subdataset=None):

        if not self.checkrequirements:
            return None

        if subdataset:
            dataset = dataset + "/" + subdataset

        ssnaplist, ecode = self._exec("zfs", "list -r -t snapshot " + dataset)

        if ecode < 0:
            return []

        dirtysnaplist = ssnaplist.split("\n")[1:(len(ssnaplist.split("\n")) - 1)]

        snaplist = []

        for i in dirtysnaplist:
            snaplist.append(i.split(" ")[0].split("@")[1])

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


    def send(self, ip, name, origin=None):
        sarr = []
        sarr.append("/usr/libexec/dataleech/snapsend")
        sarr.append(ip)
        if origin:
            sarr.append("-i")
            sarr.append(origin)
        sarr.append(name)

        cp_out = subprocess.run(sarr, stdout=subprocess.PIPE)

        return cp_out.returncode

    def receive(self, targetdataset, force=False):
        sarr = []
        sarr.append("/usr/libexec/dataleech/snapreceive")
        if force:
            sarr.append("-F")
        sarr.append(targetdataset)

        cp_out = subprocess.run(sarr, stdout=subprocess.PIPE)

        return cp_out.returncode
