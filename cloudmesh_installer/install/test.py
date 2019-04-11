import subprocess
import os

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
