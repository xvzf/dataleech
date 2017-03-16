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
class LocalSnapManager(object):

    datasets = []

    dailysnaps = []
    shortsnaps = []

    def __init__(self, datasets):
        super(LocalSnapManager, self).__init__()
        self.localzfs = ZFS()
        self.datasets = datasets

        for i in self.datasets:
            self._importsnaps_dataset(i)
    
    
    def gentimestamp(self):
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


    def _importsnaps_dataset(self, dataset):
        for i in self.localzfs.getsnaplist(dataset):
            if "dataleech-daily-" in i:
                if i not in self.dailysnaps:
                    self.dailysnaps.append(i)

            if "dataleech-short-" in i:
                if i not in self.shortsnaps:
                    self.shortsnaps.append(i)
       

    def newshortsnap(self):
        snapname = "dataleech-short-" + self.gentimestamp()
        
        for i in self.datasets:
            self.localzfs.snapshot(snapname, i)

        self.shortsnaps.append(snapname)

        while len(self.shortsnaps) > 5:
            delname = self.shortsnaps.pop(0)
            print (delname)
            for i in self.datasets:
                self.localzfs.deletesnapshot(i + "@" + delname)

    def newdailysnap(self):
        snapname = "dataleech-daily-" + self.gentimestamp()

        for i in self.datasets:
            self.localzfs.snapshot(snapname, i)