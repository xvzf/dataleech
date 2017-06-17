#!/bin/python3
"""
dataleech - a backup plan using zfs... 
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from zfs import ZFS
from datetime import datetime

# Manages snapshots created by dataleech
class LocalSnapManager(object):

    datasets = []

    dailysnaps = []
    shortsnaps = []

    def __init__(self, datasets, keep=5):
        super(LocalSnapManager, self).__init__()
        self.localzfs = ZFS()
        self.datasets = datasets
        self.keep = keep

        for i in self.datasets:
            self._importsnaps_dataset(i)
    
    
    def gentimestamp(self):
        return datetime.now().strftime('%Y-%m-%d_%H-%M')


    def _importsnaps_dataset(self, dataset):
        for i in self.localzfs.getsnaplist(dataset):
            if "dataleech-daily-" in i:
                if i not in self.dailysnaps:
                    self.dailysnaps.append(i)

            if "dataleech-short-" in i:
                if i not in self.shortsnaps:
                    self.shortsnaps.append(i)
       
    
    def snapshot(self, name):
        status = True

        for i in self.datasets:
            if not self.localzfs.snapshot(name, i):
                status = False

        if not status:
            for i in self.datasets:
                self.localzfs.destroysnapshot(name, i)

        return status


    def newshortsnap(self):
        snapname = "dataleech-short-" + self.gentimestamp()
        
        status = self.snapshot(snapname)

        if status:
            self.shortsnaps.append(snapname)

            while len(self.shortsnaps) > self.keep:
                delname = self.shortsnaps.pop(0)
                for i in self.datasets:
                    self.localzfs.destroysnapshot(delname, i)
            
        return status 


    def newdailysnap(self):
        snapname = "dataleech-daily-" + self.gentimestamp()

        return self.snapshot(snapname)


    def newcustomsnap(self, name):
        snapname = "dataleech-custom-" + name + "-" +  self.gentimestamp()

        return self.snapshot(snapname)

