""" ZFS interface class for local use """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

import os
import subprocess


class ZFS(object):
    """
    Interface class for ZFS based on subprocess (INCOMPLETE!!)
    """

    def _exec(self, cmdname, args):
        """
        Executes a command and returns the output
        For a security measure, `cmdname` has to be either in `zfs` or `zpool`

        :param cmdname: Command to execute, has to be out of ["zfs", "zpool"]
        :param args: Arguments (normal string form as it would be in the
                     console)
        :returns: output, returncode
        """
        if cmdname not in ["zfs", "zpool"]:
            return (None, None)

        sarr = []
        sarr.append(cmdname)
        for i in args.split(" "):
            sarr.append(i)

        cp_out = subprocess.run(sarr, stdout=subprocess.PIPE)
        output = cp_out.stdout.decode('UTF-8')
        return (output[0:-1], cp_out.returncode)

    def checkrequirements(self):
        """
        Checks if the script is run by the root user, not best practice but
        needed in order to destroys/creates a zfs snapshot
        """
        if os.getuid() != 0:
            return False
        return True

    def check_pool_exists(self, poolname):
        """
        Checks if a zfs pool exists

        :param poolname: Poolname
        :returns: Exists or not
        """
        out, ecode = self._exec("zpool", "status {} -x".format(poolname))

        if ecode == 0:
            return True
        return False

    @property
    def datasets(self):
        """
        All available datasets
        """

        out, ecode = self._exec("zfs", "list -H -o name")

        if ecode == 0:
            datasetlist = out.split("\n")

            return datasetlist

        return None

    def get_snapshot_list(self, dataset, subdataset=None):
        """
        Returns a list of all snapshots for a defined dataset/subdataset

        :param dataset: Dataset
        :param subdataset: Subdataset
        :returns: Snapshotlist
        """

        if subdataset:
            dataset = dataset + "/" + subdataset

        ssnaplist, ecode = self._exec(
            "zfs", "list -H -t snapshot -o name -s creation -r " + dataset)

        if ecode < 0:
            return []

        if len(ssnaplist) == 0:
            return []

        snaplist = []
        for i in ssnaplist.split("\n"):
            snaplist.append(i.split("@")[1])

        return snaplist

    def snapshot(self, name, dataset):
        """
        Creates a snapshot

        :param name: Name of the snapshot
        :param dataset: Target dataset
        :returns: True if snapshot was created
        """

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

    def destroy_snapshot(self, name, dataset):
        """
        Destroys a snapshot

        :param name: Name of the snapshot
        :param dataset: Target dataset
        :returns: True if snapshot was destroyed
        """

        if not self.checkrequirements:
            return False

        out, ecode = self._exec("zfs", "destroy " + dataset + "@" + name)

        if ecode == 0:
            return True

        return False
