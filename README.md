
# Cloudmesh Installer 

This is an experimental installer that is most usefull during the development of
cloudmesh components form source. Once cloudmehs is released, you can use the
packages hosted at pypi.

This command can be installed with 

```bash
$ pip install cloudmesh-installer
```

## Usage
```
Usage:
  cloudmesh-installer git key [LOCATION]
  cloudmesh-installer git [clone|pull|status] [BUNDLE]
  cloudmesh-installer install [BUNDLE] [-e]
  cloudmesh-installer local purge [DIR] [-f]
  cloudmesh-installer list
  cloudmesh-installer info
  cloudmesh-installer pyenv purge ENV [-f]

A convenient program called `cloudmesh-installer` to ownload and install cloudmesh
from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos
  ENV         the name of the pyenv

Options:
  -h --help
  -f       executes the purge

Description:


    cloudmesh-installer list

        Bundles

        Cloudmesh has a number of bundels. Bundels are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer local purge [DIR] [-f]

        This command should not be used in general. It is for the most
        experienced user and allows to identify eggs in your directory
        recursively. The -f option allows to delete the egg, but it may be a
        better strategy to just list the egs without th -f and than delete the
        files you do not want.

    Example:

        let us assume you like to work on storage, than you need to do the following

            mkdir cm
            cd cm
            cloudmesh-installer git clone storage
            cloudmesh-installer install storage -e
            cloudmesh-installer info
```
