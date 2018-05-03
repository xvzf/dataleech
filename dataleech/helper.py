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

    :param _zfs: ZFS instance
    :param dataset: Dataset
    :returns: {"short": [..], "daily": [..], "weekly": [..]}
    """
    toreturn = {
        "short": [],
        "daily": [],
        "weekly": []
    }

    # Go through all snapshots
    for snapshot in _zfs.get_snapshot_list(dataset):

        if "dataleech-short-" in snapshot:
            if snapshot not in toreturn["short"]:
                toreturn["short"].append(snapshot)

        if "dataleech-daily-" in snapshot:
            if snapshot not in toreturn["daily"]:
                toreturn["daily"].append(snapshot)

        if "dataleech-weekly-" in snapshot:
            if snapshot not in toreturn["weekly"]:
                toreturn["weekly"].append(snapshot)

    return toreturn
