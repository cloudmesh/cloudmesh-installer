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
Command bar
===========

::

  Usage:
        bar --file=FILE
        bar list
        bar [--parameter=PARAMETER] [--experiment=EXPERIMENT] [COMMAND...]

  This command does some useful things.

  Arguments:
      FILE   a file name
      PARAMETER  a parameterized parameter of the form "a[0-3],a5"

  Options:
      -f      specify the file

  Description:

    > cms bar --parameter="a[1-2,5],a10"
    >    example on how to use Parameter.expand. See source code at
    >      https://github.com/cloudmesh/cloudmesh-bar/blob/main/cloudmesh/bar/command/bar.py
    >    prints the expanded parameter as a list
    >    ['a1', 'a2', 'a3', 'a4', 'a5', 'a10']

    > bar exp --experiment=a=b,c=d
    > example on how to use Parameter.arguments_to_dict. See source code at
    >      https://github.com/cloudmesh/cloudmesh-bar/blob/main/cloudmesh/bar/command/bar.py
    > prints the parameter as dict
    >   {'a': 'b', 'c': 'd'}

```
<!-- STOP-MANUAL -->