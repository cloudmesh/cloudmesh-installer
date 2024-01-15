# Cloudmesh Installer 


[![image](https://img.shields.io/pypi/v/cloudmesh-installer.svg)](https://pypi.org/project/cloudmesh-installer/)
[![Python](https://img.shields.io/pypi/pyversions/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cloudmesh/cloudmesh-installer/blob/main/LICENSE)
[![Format](https://img.shields.io/pypi/format/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![Status](https://img.shields.io/pypi/status/cloudmesh-installer.svg)](https://pypi.python.org/pypi/cloudmesh-installer)
[![GitHub Actions Status](https://github.com/cloudmesh/cloudmesh-installer/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/cloudmesh/cloudmesh-installer/actions/)


This is an experimental installer that is most useful during the development of
cloudmesh components form source. Once cloudmesh is released, you can use the
packages hosted at pypi.

This command can be installed with 

```bash
$ pip install cloudmesh-installer
```

an FAQ is available at

* <https://github.com/cloudmesh/cloudmesh-installer/blob/main/FAQ.md>

## Usage

```bash
cloudmesh-installer git key [LOCATION] [--benchmark]
cloudmesh-installer [--ssh] git [clone|pull|status|authors] [BUNDLES...] [--benchmark]
cloudmesh-installer [--ssh] get [BUNDLES...] [--benchmark]
cloudmesh-installer update [BUNDLES...] [--benchmark]
cloudmesh-installer install [BUNDLES...] [--venv=ENV | -e] [--benchmark]
cloudmesh-installer list [BUNDLE] [--short | --git]
cloudmesh-installer version
cloudmesh-installer info [BUNDLE] [--verbose]
cloudmesh-installer clean --dir=DIR [--force]
cloudmesh-installer clean --venv=ENV [--force]
cloudmesh-installer new VENV [BUNDLES...] [--python=PYTHON]
cloudmesh-installer release [REPOS...] [--benchmark]
cloudmesh-installer pi [--dev]
cloudmesh-installer burn --branch BRANCH
cloudmesh-installer to5
cloudmesh-installer help
cloudmesh-installer usage
```

## Appendix

Timings

| Command | Time |
| --- | --- |
| `pip install cloudmesh-installer` | 	0m4.558s |
| `time cloudmesh-installer install cms`| 0m18.288s |
| `time cloudmesh-installer git clone storage` | 	0m4.926s |


Tests

 * [test_installer](tests/test_installer.py)
 
## Acknowledgments

This work was in part funded by the NSF
CyberTraining: CIC: CyberTraining for Students and Technologies
from Generation Z with the awadrd numbers 1829704 and 2200409.



## Manual Page

```bash
cloudmesh-installer -- a helper to install cloudmesh from source for 
developers.
Usage:
  cloudmesh-installer git key [LOCATION] [--benchmark]
  cloudmesh-installer [--ssh] git  [BUNDLES...] [--benchmark]
  cloudmesh-installer [--ssh] get [BUNDLES...] [--benchmark]
  cloudmesh-installer update [BUNDLES...] [--benchmark]
  cloudmesh-installer install [BUNDLES...] [--venv=ENV | -e] [--benchmark]
  cloudmesh-installer list [BUNDLE] [--short | --git]
  cloudmesh-installer version
  cloudmesh-installer info [BUNDLE] [--verbose]
  cloudmesh-installer clean --dir=DIR [--force]
  cloudmesh-installer clean --venv=ENV [--force]
  cloudmesh-installer new VENV [BUNDLES...] [--python=PYTHON]
  cloudmesh-installer release [REPOS...] [--benchmark]
  cloudmesh-installer pi [--dev]
  cloudmesh-installer burn --branch BRANCH
  cloudmesh-installer to5
  cloudmesh-installer help
  cloudmesh-installer usage
A convenient program called `cloudmesh-installer` to download and install
cloudmesh from sources published in github.
Arguments:
  BUNDLE      the bundle 
  REPOS       list of git repos
  ENV         the name of the venv
  DIR         the directory form where to start the search
Options:
  -h --help
  --force   force the execution of the command. This command could delete 
files.
Note: you can also use `cmsi` instead of `cloudmesh-installer`
Description:
    cmsi list
    cloudmesh-installer list
        Cloudmesh has a number of bundles. Bundles are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.
        This command lists all available bundles
    cmsi list bundle
    cloudmesh-installer list bundle
        lists the information about a particular bundle.
    cmsi list [BUNDLE] --git
    cloudmesh-installer list [BUNDLE] --git
        Shows the location of the repositories in a bundle.
    cmsi info
    cloudmesh-installer info
        The info command gives some very basic information about the version
        numbers of cloudmesh on your system, github, and pypi. THis helps
        identifying if you may run an odlder version.
        In addition we try to check if you do use venv
    cmsi git key [LOCATION]
    cloudmesh-installer git key [LOCATION]
        This command only works if you use ssh keys to authenticate with 
github.
        This command makes uploading the key easy as it checks for your key and
        provides via the web browser automatic pageloads to github for the
        key upload. You do not have tou use this command. It is intenden for
        novice users.
    cmsi git  [BUNDLE]
    cloudmesh-installer git  [BUNDLE]
        This command executes the given git command on the bundle
    cmsi update [BUNDLE]
    cmsi get [BUNDLE]
    cloudmesh-installer update [BUNDLE]
    cloudmesh-installer get [BUNDLE]
        For each repository in the bundle it clones it and also pulls.
        Thus the command can easly be used to get a new bundle element, but
        also get the new code for already existing bundles elements.
        The code is checked out with https
    cmsi get -ssh [BUNDLE]
    cloudmesh-installer get -ssh [BUNDLE]
        For each repository in the bundle it clones it and also pulls.
        Thus the command can easly be used to get a new bundle element, but
        also get the new code for already existing bundles elements.
        The code is checked out with ssh
    cmsi install [BUNDLE]
    cloudmesh-installer install [BUNDLE]
        This command executes an install on the given bundle
    cmsi info
    cloudmesh-installer info
        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi
    cmsi clean --dir=. --force
    cloudmesh-installer clean --dir=. --force
       removes the egs in the current directory tree
    cmsi clean --venv=ENV --force
    cloudmesh-installer clean --venv=ENV --force
        removes the venv in ~/ENV
    Examples:
        let us assume you like to work on bar, than you need to do the 
following
            mkdir cm
            cd cm
            cmsi git clone bar
            cmsi install bar
            cmsi info
```

