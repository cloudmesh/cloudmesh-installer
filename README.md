# Cloudmesh Installer 


[![image](https://img.shields.io/pypi/v/cloudmesh-common.svg)](https://pypi.org/project/cloudmesh-common/)
[![Python](https://img.shields.io/pypi/pyversions/cloudmesh-common.svg)](https://pypi.python.org/pypi/cloudmesh-common)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cloudmesh/cloudmesh-common/blob/main/LICENSE)
[![Format](https://img.shields.io/pypi/format/cloudmesh-common.svg)](https://pypi.python.org/pypi/cloudmesh-common)
[![Status](https://img.shields.io/pypi/status/cloudmesh-common.svg)](https://pypi.python.org/pypi/cloudmesh-common)
[![Travis](https://travis-ci.com/cloudmesh/cloudmesh-common.svg?branch=main)](https://travis-ci.com/cloudmesh/cloudmesh-common)



This is an experimental installer that is most usefull during the development of
cloudmesh components form source. Once cloudmehs is released, you can use the
packages hosted at pypi.

This command can be installed with 

```bash
$ pip install cloudmesh-installer
```

an FAQ is available at

* <https://github.com/cloudmesh/cloudmesh-installer/blob/main/FAQ.md>

## Usage

```bash

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

<!-- START-MANUAL -->
```
Usage:
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
<!-- STOP-MANUAL -->