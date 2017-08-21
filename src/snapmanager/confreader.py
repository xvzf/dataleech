#!/bin/python3
"""
dataleech - a backup plan using zfs...
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import json
import re
import argparse
import sys

class ConfReader(object):

    confdict = {}

    def __init__(self, configfilepath="/etc/dataleech/datasets"):
        try:
            with open(configfilepath, 'r') as file:
                self.confdict = json.loads(re.sub('#.*?\r?\n', '', file.read()))
        except IOError:
            print("[-] Could not open config file, exiting")
            sys.exit(1)
        except json.decoder.JSONDecodeError:
            print("[-] Invalid config file, fix config")
            sys.exit(1)
        except UnicodeDecodeError:
            print("[-] Invalid formating, fix config")
        except Exception as e:
            print("[-] Unknown exception, please report as an issue on github:\n" + str(e))

    def getshortsnapdatasets(self):
        return list(set(self.confdict["short"].keys()))

    def getdailysnapdatasets(self):
        return list(set(self.confdict["daily"].keys()))

    def getweeklysnapdatasets(self):
        return list(set(self.confdict["weekly"].keys()))

    def getsyncdatasets(self):
        related_datasets = []

        for src, dest in self.confdict["daily"].items():
            related_datasets.append((src, dest))

        for src, dest in self.confdict["weekly"].items():
            related_datasets.append((src, dest))

        return_datasets = []

        for src, dest in  list(set(related_datasets)):
            if dest != "none":
                return_datasets.append((src,dest))

        return return_datasets



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--open', help='specify the path', nargs=1)

    args = parser.parse_args()

    cfgpath = "/etc/dataleech/datasets"
    if args.open:
        cfgpath = args.open[0]

    c = ConfReader(cfgpath)

    for i in c.getsyncdatasets():
        print("%s:%s" % i)
