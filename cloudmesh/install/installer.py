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
import subprocess
import sys

def banner(txt):
    """prints a banner of the form with a frame of # around the txt::

      ############################
      # txt
      ############################

    :param txt: a text message to be printed
    :type txt: string
    """
    print("#" * 70)
    print("#", txt)
    print("#" * 70)


def run(command):
    try:
        output = subprocess.check_output(command,
            shell=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        sys.exit(1)

    return output.decode('utf-8')

def main():
    arguments = docopt(__doc__)
    print(arguments)

    if arguments["clone"]:
        print("clone")
        result = run  ("ls -lisa")
        print(result)

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
