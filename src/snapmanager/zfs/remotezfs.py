#!/bin/python3
"""
dataleech - a backup plan using zfs...
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from .zfs import ZFS
import subprocess

class remoteZFS(ZFS):

    def __init__(self, sshopts):
        super(remoteZFS,self).__init__()
        self.sshopts =sshopts

    def _exec(self, cmdname, args):
        print("cmdname: %s, args: %s" % (cmdname,args))

        if cmdname not in ["zfs", "zpool"]:
            return (None, None)

        sarr = []
        sarr.append("ssh")

        for i in self.sshopts.split(" "):
            sarr.append(i)

        sarr.append(cmdname + " " + args)

        cp_out = subprocess.run(sarr, stdout=subprocess.PIPE)

        return (cp_out.stdout.decode('UTF-8')[0:len(cp_out.stdout.decode('UTF-8'))-1], cp_out.returncode)

