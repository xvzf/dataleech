#!/usr/bin/env python3
""" ZFS Submodule based on the zfs commandline interface and subprocess """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

__all__ = ["zfs"]
from .zfs import ZFS
from .remote_zfs import RemoteZFS
