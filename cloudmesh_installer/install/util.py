from colorama import Fore, Style
import subprocess
import os

def banner(txt, c=Fore.BLUE):
    """prints a banner of the form with a frame of # around the txt::

      ############################
      # txt
      ############################

    :param txt: a text message to be printed
    :type txt: string
    """
    print(c + "#" * 70)
    print(c + f"# {txt}")
    print(c + "#" * 70)


def readfile(filename):
    """
    returns the content of a file
    :param filename: the filename
    :return:
    """
    with open(filename, 'r') as f:
        content = f.read()
    return content


#def run(command):
#    #result = subprocess.check_output(command, shell=True)
#
#    result = subprocess.check_output(command)
#
#    return result.decode("utf-8")

def run (command):
    os.system (f"{command} > cmd-output")
    content = readfile("cmd-output")
    return content
