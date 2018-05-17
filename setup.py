from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dataleech",
    version="1.0.2",
    description="ZFS Backup Strategy - short term local backups and long term\
                 remote sync. ",
    long_description=long_description,
    url="https://github.com/xvzf/dataleech",
    author="Matthias Riegler",
    author_email="matthias@xvzf.tech",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
    ],

    keywords="backup zfs",
    packages=["dataleech"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "dataleech = dataleech.__main__:dataleech_cli"
        ]
    },
    setup_requires=[],
    tests_require=[],

    project_urls={  # Optional
        "Bug Reports": "https://github.com/xvzf/dataleech/issues",
        "Source": "https://github.com/xvzf/dataleech/",
    },

)
