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

    def getrelatedsets(self):
        return self.confdict

    def getlocaldatasets(self):
        return self.confdict.keys()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--open', help='specify the path', nargs=1)

    args = parser.parse_args()

    cfgpath = "/etc/dataleech/datasets"
    if args.open:
        cfgpath = args.open[0]

    c = ConfReader(cfgpath)

    for localdataset, remotedataset in c.getrelatedsets().items():
        print("%s:%s" % (localdataset, remotedataset) )
