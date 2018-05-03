""" Config parser for /etc/dataleech/datasets """

#   dataleech - a backup plan using zfs...
#   Copyright (C) 2018 Matthias Riegler <matthias@xvzf.tech>
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

import re
import json
import sys


class ConfReader(object):
    """
    Parses the configuration file for dataleech, default path is

    :param path: Path of the configfile, default is `/etc/dataleech/datasets`
    """

    confdict = {}

    def __init__(self, configfilepath="/etc/dataleech/datasets"):
        """
        Initializes the object and parses the configuration
        """

        try:
            # Try to parse the configuration
            with open(configfilepath, 'r') as file:
                self.confdict = json.loads(
                    ConfReader._remove_comments(file.read())
                )

        # Error handling
        except IOError:
            print("[-] Could not open config file, exiting")
            sys.exit(1)

        except json.decoder.JSONDecodeError:
            print("[-] Invalid config file, fix config")
            sys.exit(1)

        except UnicodeDecodeError:
            print("[-] Invalid formating, fix config")

        except Exception as e:
            print(
                "[-] Unknown exception, please post an issue on github:\n" +
                str(e)
            )

    @staticmethod
    def _remove_comments(config_string):
        return re.sub('#.*?\r?\n', '', config_string)

    @property
    def shortsnapdatasets(self):
        """
        Datasets which should be snapshotted on the `short` interval
        """
        return list(set(self.confdict["short"].keys()))

    @property
    def dailysnapdatasets(self):
        """
        Datasets which should be snapshotted on the `daily` interval
        """
        return list(set(self.confdict["daily"].keys()))

    @property
    def weeklysnapdatasets(self):
        """
        Datasets which should be snapshotted on the `weekly` interval
        """
        return list(set(self.confdict["weekly"].keys()))

    @property
    def syncdatasets(self):
        """
        List of datasets which should be synced
        """
        related_datasets = []

        for src, dest in self.confdict["daily"].items():
            for i in dest.split(";"):
                related_datasets.append((src, i))

        for src, dest in self.confdict["weekly"].items():
            for i in dest.split(";"):
                related_datasets.append((src, i))

        return_datasets = []

        for src, dest in list(set(related_datasets)):
            if dest != "none":
                return_datasets.append((src, dest))

        return return_datasets

    @property
    def localsyncdatasets(self):
        """
        Datasets which should be synced to a another local dataset (can be on a
        different ZFS pool)
        """
        returnlist = []
        for src, dst in self.syncdatasets:
            if "local@" in dst:
                returnlist.append((src, dst[6:]))

        return returnlist

    @property
    def remotesyncdatasets(self):
        """
        Datasets which should be synced to a remote dataset, depends on
        `sshopts` to be set in the configuration
        """
        returnlist = []
        for src, dst in self.syncdatasets:
            if "remote@" in dst:
                returnlist.append((src, dst[7:]))

        return returnlist

    @property
    def sshopts(self):
        """
        parameters for the ssh command when cloning to a remote dataset
        """
        if "sshopts" in self.confdict.keys():
            return self.confdict["sshopts"]
