#!/bin/python3
"""
dataleech - a backup plan using zfs... 
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

__all__ = ["zfs", "localsnapmanager", "remotesnapmanager"]
from snapmanager.localsnapmanager import LocalSnapManager
from snapmanager.remotesnapmanager import RemoteSnapManager
from snapmanager.zfs import ZFS