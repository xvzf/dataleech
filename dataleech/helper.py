""" Contains helper functions used in various parts of dataleech """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.


def get_dataleech_snapshots(_zfs, dataset):
    """
    Returns a dict containing short, daily and weekly snapshots

    `syncsnaps` are ordered and also contain custom snapshots

    :param _zfs: ZFS instance
    :param dataset: Dataset
    :returns: {"short": [..], "daily": [..], "weekly": [..], "syncsnaps": [..]}
    """
    toreturn = {
        "short": [],
        "daily": [],
        "weekly": [],
        "syncsnaps": []
    }

    # Go through all snapshots
    for snapshot in _zfs.get_snapshot_list(dataset):

        if "dataleech-short-" in snapshot:
            # Don't sync shortterm snapshots
            toreturn["short"].append(snapshot)

        elif "dataleech-daily-" in snapshot:
            toreturn["daily"].append(snapshot)
            toreturn["syncsnaps"].append(snapshot)

        elif "dataleech-weekly-" in snapshot:
            toreturn["weekly"].append(snapshot)
            toreturn["syncsnaps"].append(snapshot)

        elif "dataleech-custom-" in snapshot:
            # Only add custom snapshots to the sync target
            toreturn["syncsnaps"].append(snapshot)

    return toreturn
