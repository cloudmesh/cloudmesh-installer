"""Usage: cloudmesh-installer clone
          cloudmesh-installer pull
          cloudmesh-installer install
          cloudmesh-installer purge [-f]
          cloudmesh-installer list
          cloudmesh-installer info

Download and install cloudmesh.

Options:
  -h --help
  -f       executes the purge

"""
from docopt import docopt

def main():
    arguments = docopt(__doc__)
    print(arguments)

    if arguments["clone"]:
        print("clone")

    elif arguments["pull"]:
        print("purge")

    elif arguments["install"]:
        print("install")

    elif arguments["purge"]:
        print("purge")

    elif arguments["list"]:
        print("list")

    elif arguments["info"]:
        print("info")


if __name__ == '__main__':
    main()
