"""Usage: cloudmesh-installer clone [BUNDLE]
          cloudmesh-installer pull [BUNDLE]
          cloudmesh-installer install [BUNDLE]
          cloudmesh-installer purge [-f]
          cloudmesh-installer list
          cloudmesh-installer info

Download and install cloudmesh.

Arguments:
  BUNDLE      the bundle [default: cms]

Options:
  -h --help
  -f       executes the purge

"""
from docopt import docopt
import subprocess
import sys
from pprint import pprint
import oyaml as yaml
import requests
import re
import os

repos = dict({

    'cms': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-inventory',
        'cloudmesh-cloud'
    ],

    'source': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-inventory',
        'cloudmesh-cloud',
        'cloudmesh-storage',
        'cloudmesh-emr',
        'cloudmesh-comet',
        'cloudmesh-openapi',
        'cloudmesh-nn',
        'cloudmesh-nist',
        'cloudmesh-conda',
    ],

    'web': [
        'about',
        'get',
        'cloudmesh-github.io',
    ],

    'community': [
        'cloudmesh-community.github.io'
    ],

    'spring19': [
         'fa18-516-22',
         'fa18-516-26',
         'fa18-516-29',
         'hid-sample',
         'hid-sp18-407',
         'hid-sp18-512',
         'hid-sp18-519',
         'hid-sp18-520',
         'hid-sp18-522',
         'hid-sp18-523',
         'hid-sp18-602',
         'hid-sp18-701',
         'hid-sp18-704',
         'hid-sp18-709',
         'hid-sp18-710',
         'sp19-222-100',
         'sp19-222-101',
         'sp19-222-102',
         'sp19-222-89',
         'sp19-222-90',
         'sp19-222-91',
         'sp19-222-92',
         'sp19-222-93',
         'sp19-222-94',
         'sp19-222-96',
         'sp19-222-97',
         'sp19-222-98',
         'sp19-222-99',
         'sp19-516-121',
         'sp19-516-122',
         'sp19-516-123',
         'sp19-516-124',
         'sp19-516-125',
         'sp19-516-126',
         'sp19-516-127',
         'sp19-516-128',
         'sp19-516-129',
         'sp19-516-130',
         'sp19-516-131',
         'sp19-516-132',
         'sp19-516-133',
         'sp19-516-134',
         'sp19-516-135',
         'sp19-516-136',
         'sp19-516-137',
         'sp19-516-138',
         'sp19-516-139',
         'sp19-616-111',
         'sp19-616-112'
    ]
})


# git clone git@github.com:cloudmesh-community/$f.git


#git clone https://github.com/cloudmesh/get.git

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


class Git(object):

    @staticmethod
    def url(repo):
        if repo in repos['community']:
            return f"https://github.com/cloudmesh-community/{repo}"
        else:
            return f"https://github.com/cloudmesh/{repo}"

    @staticmethod
    def clone(repos):
        for repo in repos:
            print(f"clone -> {repo}")
            if not os.path.isdir(repo):
                try:
                    location = Git.url(repo)
                    r = run(f"git clone {location}.git")
                    print (r)
                except Exception as e:
                    print (e)
            else:
                print ("         ERROR: not downlaoded as repo already exists.")

    @staticmethod
    def status(repos):
        for repo in repos:
            print ("status", repo)

    # git clone https://github.com/cloudmesh/get.git

    @staticmethod
    def pull(repos):
        for repo in repos:
            print ("status", repo)


#git clone https://github.com/cloudmesh/get.git


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



def main():
    arguments = docopt(__doc__)
    bundle = arguments["BUNDLE"] = arguments.get("BUNDLE") or 'cms'
    print(arguments)

    if arguments["clone"]:
        result = Git.clone(repos[bundle])

    elif arguments["pull"]:
        print("purge")

    elif arguments["install"]:
        print("install")

    elif arguments["purge"]:
        print("purge")

    elif arguments["list"]:
        print("list")
        lines = yaml.dump(repos, default_flow_style=False).split("\n")
        for line in lines:
            if ":" in line:
                print()
            print(line)


    elif arguments["info"]:
        print("info")
        packages = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]
        for package in packages:
            print ("\nVersion info for package <{package}>".format(
                package=package))
            installed = run("pip freeze | grep {package}".format(
                package=package)).strip()
            print ("\t---Installed---")
            print(installed)
            v = requests.get("https://raw.githubusercontent.com/cloudmesh"
                             "/{package}/master/VERSION".format(
                                package=package)).text
            print ("\t---In git---")
            print (v)
            v = requests.get("https://pypi.org/project/{package}/".format(
                package=package)).text
            pat_str = '(.*)<h1 class="package-header__name">(.+?)</h1>(.*)'
            pattern = re.compile(pat_str, re.M | re.I | re.S)
            groups = re.match(pattern, v)
            #print (groups)
            v = (groups.group(2)).strip().split(package)[1].strip()
            print ("\t---In pypi---")
            print (v)


if __name__ == '__main__':
    main()
