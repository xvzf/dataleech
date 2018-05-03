""" Snapshot manager for dataleech """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

from datetime import datetime
from .zfs import ZFS
from .helper import get_dataleech_snapshots


class SnapManager(object):
    """
    Manages local snapshots divided into two groups:
        - short: Usually every few minutes, depends on the cronfile
                 (only a few are kept, old ones get deleted using a FIFO queue,
                  set the keep option to the desired size)
        - daily: Daily snapshot
        - weekly: Weekly snapshot


    :param datasets: A list of datasets where the snapshots should be created
    :param keep: How many short term snapshots
    """

    datasets = []

    dailysnaps = []
    shortsnaps = []
    weeklysnaps = []

    def __init__(self, datasets, keep=5):
        """
        Initializes the object and imports the snapshots to the internal
        datastructure
        """
        self.datasets = datasets
        self.keep = keep

        for dataset in self.datasets:
            self._importsnaps_dataset(dataset)

    @property
    def _timestamp(self):
        """
        Timestamp used for daily and weekly snapshots
        """
        return datetime.now().strftime('%Y-%m-%d')

    @property
    def _timestamp_short(self):
        """
        Timestamp used for the short snapshots
        """
        return datetime.now().strftime('%Y-%m-%d_%H-%M')

    def _importsnaps_dataset(self, dataset):
        """
        Imports all snapshots matching `dataleech-(short|daily|weekly)`

        :param dataset: Dataset which contains the snapshot
        """
        tmp = get_dataleech_snapshots(ZFS(), dataset)

        self.shortsnaps = tmp["short"]
        self.dailysnaps = tmp["daily"]
        self.weeklysnaps = tmp["weekly"]

    def snapshot(self, name):
        """
        Tries to create a snapshot on all datasets, if it is not successfull,
        it deletes ALL (!!!) snapshots with this name to be on the same status
        on all datasets.

        :param name: Snapshot name
        :returns: True whenever the snapshot creation was successfull
        """
        status = True

        for i in self.datasets:
            if not ZFS().snapshot(name, i):
                status = False

        if not status:
            for i in self.datasets:
                ZFS().destroy_snapshot(name, i)

        return status

    def newshortsnap(self):
        """
        Creates a new shortterm snapshot

        :returns: Success
        """
        snapname = "dataleech-short-{}".format(self._timestamp_short)
        print(snapname)

        status = self.snapshot(snapname)

        if status:
            self.shortsnaps.append(snapname)
            # Only keep as many shortterm snapshots as requested
            while len(self.shortsnaps) > self.keep:
                delname = self.shortsnaps.pop(0)
                for dataset in self.datasets:
                    # Try to delete the snapshot, if it is not possible, return
                    if not ZFS().destroy_snapshot(delname, dataset):
                        return False

        return status

    def newdailysnap(self):
        """
        Creates a new daily snapshot

        :returns: Success
        """
        snapname = "dataleech-daily-{}".format(self._timestamp)
        print(snapname)
        return self.snapshot(snapname)

    def newweeklysnap(self):
        """
        Creates a new weekly snapshot

        :returns: Success
        """
        snapname = "dataleech-weekly-{}".format(self._timestamp)
        print(snapname)
        return self.snapshot(snapname)

    def newcustomsnap(self, name):
        """
        Creates a new custom snapshot

        :name: Name of the snapshot ("dataleech-weekly-" + name)
        :returns: Success
        """
        snapname = "dataleech-weekly-{}".format(self._timestamp_short)
        print(snapname)
        return self.snapshot(snapname)
