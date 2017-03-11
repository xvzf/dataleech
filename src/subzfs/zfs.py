#!/bin/python3
"""
zbackup - a backup plan using zfs... 
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

		return (stdout.decode('UTF-8'), cp_out.returncode)


	# ZFS Utils need superuser privileges
	def checkrequirements(self):
		if os.getuid() != 0:
			return False
		return True


	# Returns a list of all snapshots
	def getsnaplist(self, dataset, subdataset=None):

		if not self.checkrequirements:
			return None

		if subdataset:
			dataset = dataset + "/" + subdataset

		ssnaplist, ecode = self._exec("zfs", "list -t snapshot " + dataset)

		if ecode < 0:
			return []

		dirtysnaplist = ssnaplist.split("\n")[1:(len(ssnaplist.split("\n")) - 1)]

		snaplist = []

		for i in dirtysnaplist:
			snaplist.append(i.split(" ")[0])

		return snaplist
