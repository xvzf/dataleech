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
from datetime import datetime
import json

# Manages snapshots created by dataleech
class RemoteSnapManager(object):

    datasets = []

    dailysnaps = []


    def __init__(self, datasets):
        super(LocalSnapManager, self).__init__()
        self.localzfs = ZFS()
        self.datasets = datasets

        for i in self.datasets:
            self._importsnaps_dataset(i)
    

    def _importsnaps_dataset(self, dataset):
        for i in self.localzfs.getsnaplist(dataset):
            if "dataleech-daily-" in i:
                if i not in self.dailysnaps:
                    self.dailysnaps.append(i)

            if "dataleech-short-" in i:
                if i not in self.shortsnaps:
                    self.shortsnaps.append(i)