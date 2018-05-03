""" ZFS interface class for a remote ZFS installation """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

from .zfs import ZFS
import subprocess


class RemoteZFS(ZFS):
    """
    Wrapper for the ZFS class so it can access file systems over ssh
    """

    def __init__(self, sshopts):
        """
        Initialize
        """
        super().__init__()
        self.sshopts = sshopts

    def _exec(self, cmdname, args):
        """
        Executes a command on a remote target and returns the output
        For a security measure, `cmdname` has to be either in `zfs` or `zpool`

        :param cmdname: Command to execute, has to be out of ["zfs", "zpool"]
        :param args: Arguments (normal string form as it would be in the
                     console)
        :returns: output, returncode
        """

        if cmdname not in ["zfs", "zpool"]:
            return (None, None)

        sarr = []
        sarr.append("ssh")

        for i in self.sshopts.split(" "):
            sarr.append(i)

        sarr.append(cmdname + " " + args)

        cp_out = subprocess.run(sarr, stdout=subprocess.PIPE)

        return (cp_out.stdout.decode('UTF-8')
                [0:len(cp_out.stdout.decode('UTF-8')) - 1], cp_out.returncode)
