# Cloudmehs Installer 

[![Version](https://img.shields.io/pypi/v/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cloudmesh/cloudmesh-installer/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![Format](https://img.shields.io/pypi/format/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![Status](https://img.shields.io/pypi/status/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![Travis](https://travis-ci.com/cloudmesh/cloudmesh-installer.svg?branch=master)](https://travis-ci.com/cloudmesh/cloudmesh-installer)

This is an experimental installer that is most usefull during the
development of cloudmesh components form source. Once cloudmehs is
released, you can use the packages hosted at pypi.

This command can be installed with 

```bash
$ pip install cloudmesh-installer
```

an FAQ is available at

* <https://github.com/cloudmesh/cloudmesh-installer/blob/master/FAQ.md>

## Usage
```
cloudmesh-installer -- a helper to install cloudmesh from source for developers.

Usage:
  cloudmesh-installer git key [LOCATION] [--benchmark]
  cloudmesh-installer git [clone|pull|status] [BUNDLE] [--benchmark]
  cloudmesh-installer install [BUNDLE] [--venv=ENV | -e] [--benchmark]
  cloudmesh-installer list [BUNDLE] [--short | --git]
  cloudmesh-installer version
  cloudmesh-installer info [BUNDLE] [--verbose]
  cloudmesh-installer clean --dir=DIR [--force]
  cloudmesh-installer clean --venv=ENV [--force]

A convenient program called `cloudmesh-installer` to download and install
cloudmesh from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos
  ENV         the name of the venv
  DIR         the directory form where to start the search

Options:
  -h --help
  --force   force the execution of the command. This command could delete files.

Description:

    cloudmesh-installer list

        Cloudmesh has a number of bundles. Bundles are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

        This command lists all available bundles

    cloudmesh-installer list bundle

        lists the information about a particular bundle.

    cloudmesh-installer list [BUNDLE] --git

        Shows the location of the repositories in a bundle.

    cloudmesh-installer info

        The info command gives some very basic information about the version
        numbers of cloudmesh on your system, github, and pypi. THis helps
        identifying if you may run an odlder version.

        In addition we try to check if you do use venv

    cloudmesh-installer git key [LOCATION]

        This command only works if you use ssh keys to authenticate with github.
        This command makes uploading the key easy as it checks for your key and
        provides via the web browser automatic pageloads to github for the
        key upload. You do not have tou use this command. It is intenden for
        novice users.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer clean --dir=. --force

       removes the egs in the current directory tree

    cloudmesh-installer clean --venv=ENV --force

        removes the venv in ~/ENV

    Examples:

        let us assume you like to work on storage, than you need to do the following

            mkdir cm
            cd cm
            cloudmesh-installer git clone storage
            cloudmesh-installer install storage
            cloudmesh-installer info

```
## Appendix

Timings

| Command | Time |
| --- | --- |
| `pip install cloudmesh-installer` | 	0m4.558s |
| `time cloudmesh-installer install cms`| 0m18.288s |
| `time cloudmesh-installer git clone storage` | 	0m4.926s |


