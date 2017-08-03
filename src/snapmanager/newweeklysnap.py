#!/bin/python3
"""
dataleech - a backup plan using zfs...
Copyright (C) 2017 Matthias Riegler <matthias@xvzf.tech>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import argparse
from snapmanager import LocalSnapManager
from confreader import ConfReader
import sys

def main():
    parser = argparse.ArgumentParser(description="DATALEECH - A ZFS BACKUP SOLUTION FOR DESKTOP COMPUTERS")

    args = parser.parse_args()

    if not LocalSnapManager(ConfReader().getweeklysnapdatasets()).newweeklysnap():
        sys.exit(-1)

if __name__ == '__main__':
    main()
