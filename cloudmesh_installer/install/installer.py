"""cloudmesh-installer -- a helper to install cloudmesh from source for developers.

Usage:
  cloudmesh-installer git key [LOCATION]
  cloudmesh-installer git [clone|pull|status] [BUNDLE]
  cloudmesh-installer install [BUNDLE] [-e]
  cloudmesh-installer list [BUNDLE] [--short]
  cloudmesh-installer git list BUNDLE
  cloudmesh-installer bundles
  cloudmesh-installer version
  cloudmesh-installer info
  cloudmesh-installer local purge DIR [--force]
  cloudmesh-installer pyenv purge ENV [--force]
  cloudmesh-installer venv purge ENV [--force]



A convenient program called `cloudmesh-installer` to ownload and install cloudmesh
from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos
  ENV         the name of the pyenv
  DIR         the directory form where to start the search

Options:
  -h --help
  --force   force the execution of the command. This command could delete files.

Description:

    cloudmesh-installer bundles

        Cloudmesh has a number of bundels. Bundels are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

        This command lists all available bundles

    cloudmesh-installer list bundle

        list sthe information about a particular bundle.

    cloudmesh-installer git list [BUNDLE]

        Shows the location of the repositories in a bundle.

    cloudmesh-installer info

        The info command gives some very basic information about the version
        numbers of cloudmesh on your system, github, and pypi. THis helps
        identifying if you may run an odlder version.

        In addition we try to check if you do use pyenv

    cloudmesh-installer git key [LOCATION]

        This command only works if you use ssh keys to authenticate with github.
        This command makes uploading the key easy as it checks for your key and
        provides via the web browser automatic pageloads to github for the
        keyupload. YOu do not have tou use this command. It is intenden for
        novice users.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer local purge [DIR] [--force]

        THIS IS A DANGEROUS COMMAND AND YOU SHOULD PROBABLY NOT USE IT


        This command should not be used in general. It is for the most
        experienced user and allows to identify eggs in your directory
        recursively. The --force option allows to delete the egg, but it may be a
        better strategy to just list the egs without the --force and than delete the
        files you do not want.

        One test that you may want to do is to just call the command without the
        force option as to see possible eggs that you forgot and may need to be
        deleted.

    cloudmesh-installer pyenv purge ENV [--force]

        THIS IS A DANGEROUS COMMAND AND YOU SHOULD PROBABLY NOT USE IT

        THis command removes the specified virtual envireonment and reinstalls
        it with python 3.7.3. It will erase it entirely, thus make sure you know
        what this command does. YOu will have to reinstall all packages.

    Example:

        let us assume you like to work on storage, than you need to do the following

            mkdir cm
            cd cm
            cloudmesh-installer git clone storage
            cloudmesh-installer install storage -e
            cloudmesh-installer info

"""
import os
import re
import shutil
import subprocess
import sys
import textwrap
import webbrowser
from pathlib import Path
from pprint import pprint
from tabulate import tabulate
import shlex

import oyaml as yaml
import requests
from docopt import docopt
import colorama
from colorama import Fore, Style
from venv import EnvBuilder
import pip
import os

from cloudmesh_installer.install.__version__ import version as insatller_version
debug = False

# 'cloudmesh-azure',
# 'cloudmesh-aws'

repos = dict({

    'cms': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-manual'
    ],

    'cloud': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-cloud',
        'cloudmesh-inventory',
        'cloudmesh-manual'
    ],

    'batch': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-cloud',
        'cloudmesh-inventory',
        'cloudmesh-batch',
        'cloudmesh-manual'
    ],

    'storage': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-cloud',
        'cloudmesh-storage',
        'cloudmesh-inventory',
        'cloudmesh-box',
        'cloudmesh-manual'
    ],

    'source': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-cloud',
        'cloudmesh-storage',
        'cloudmesh-inventory',
        'cloudmesh-emr',
        'cloudmesh-comet',
        'cloudmesh-openapi',
        'cloudmesh-nn',
        'cloudmesh-nist',
        'cloudmesh-conda',
        'cloudmesh-azure',
        'cloudmesh-aws',
        'cloudmesh-box',
        'cloudmesh-redshift',
        'cloudmesh-manual'
    ],

    'web': [
        'about',
        'get',
        'cloudmesh-github.io',
        'cloudmesh-manual'
    ],

    'community': [
        'cloudmesh-community.github.io'
    ],

    'flow': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-cloud',
        'cloudmesh-inventory',
        'cloudmesh-flow',
        'cloudmesh-manual'
    ],

    'emr': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-cloud',
        'cloudmesh-inventory',
        'cloudmesh-emr',
        'cloudmesh-manual'
    ],

    'conda': [
        'cloudmesh-conda'
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


# git clone https://github.com/cloudmesh/get.git

pyenv_purge = [
    'rm -f ~/.pyenv/shims/cms',
    'pyenv deactivate',
    'pyenv uninstall -f {env}',
    'pyenv virtualenv 3.7.3 {env}',
    'pyenv activate {env}',
    "pip install pip -U"
]


def run(command, verbose=True):
    if verbose:
        print(command)
    try:
        output = subprocess.check_output(command,
                                         shell=True,
                                         stderr=subprocess.STDOUT,
                                         )
    except subprocess.CalledProcessError as err:
        print()
        print(Fore.RED + f"ERROR: {err}")
        sys.exit(1)

    return output.decode('utf-8')


def script(commands, environment):
    for command in commands:
        result = run(command.format(env=environment))
        print(result)


class Git(object):

    @staticmethod
    def url(repo):
        global repos
        if repo in repos['community'] or repo in repos['spring19']:
            return f"https://github.com/cloudmesh-community/{repo}"
        else:
            return f"https://github.com/cloudmesh/{repo}"

    @staticmethod
    def clone(repos):
        for repo in repos:
            print(f"clone -> {repo}")

            if not os.path.isdir(Path(f"./{repo}")):
                try:
                    location = Git.url(repo)
                    command = f"git clone {location}.git"
                    r = run(command)
                    print(f"         {r}")
                except Exception as e:
                    print(e)
            else:
                print(Fore.RED + "         ERROR: not downlaoded as repo already exists.")

    @staticmethod
    def command(repos, name, ok_msg="nothing to commit, working tree clean"):
        for repo in repos:
            print("status ->", f"{repo:25}", end=" ")

            try:
                os.chdir(repo)
            except FileNotFoundError:
                print(Fore.RED + "ERROR:", repo, "not found")

            result = run(f"git {name}", verbose=False)
            if ok_msg in result:
                print(Fore.GREEN + f"... ok")
            else:
                print ()
                print(Fore.RED + result)
            os.chdir("../")

    @staticmethod
    def status(repos):
        Git.command(repos, "status", ok_msg="nothing to commit, working tree clean")

    @staticmethod
    def pull(repos):
        Git.command(repos, "pull", ok_msg="Already up to date.")

    @staticmethod
    def install(repos, dev=False):
        for repo in repos:
            print("install ->", repo)
            if dev:
                os.chdir(repo)
                os.system("pip install -e .")
                os.chdir("../")
            else:
                os.system("pip install {repo}".format(repo=repo))


# git clone https://github.com/cloudmesh/get.git

def yn_question(msg):
    while True:
        query = input(Fore.RED + msg)
        answer = query.lower().strip()
        if query == '' or answer not in ['yes', 'n']:
            print('Please answer with yes/n!')
        else:
            break
    print(Fore.RESET)
    return answer == 'yes'


def banner(txt, c=Fore.BLUE):
    """prints a banner of the form with a frame of # around the txt::

      ############################
      # txt
      ############################

    :param txt: a text message to be printed
    :type txt: string
    """
    print(c + "#" * 70)
    print(c + f"#{txt}")
    print(c + "#" * 70)


def remove(location):
    print("delete", location)
    try:
        shutil.rmtree(location)
        print("removing:", location)
    except Exception as e:
        print("Removing faild, tring file removal")
    try:
        os.remove(location)
        print("removing:", location)
    except Exception as e:
        print("Removing faild, not sure what to do next")
        print(e)

def gett_all_repos():
    path = Path(".").resolve()
    gits = list(path.glob("*/.git"))
    names = []
    for repo in gits:
        names.append(os.path.basename(os.path.dirname(repo.resolve())))
    return names

def check_for_bundle(bundle):
    if not ((bundle in repos)  or (bundle in ["cloudmesh", "all"])):
        print(Fore.RED + f"ERROR: The `bundle` {bundle} does not exist" + Fore.RESET)
        sys.exit(1)

def main():
    arguments = docopt(__doc__)
    bundle = arguments["BUNDLE"] = arguments.get("BUNDLE") or 'cms'
    check_for_bundle(bundle)

    arguments["DIR"] = \
        os.path.expandvars(os.path.expanduser(arguments.get("DIR") or '.'))
    arguments["LOCATION"] = \
        os.path.expandvars(os.path.expanduser(
            arguments.get("LOCATION") or '~/.ssh/id_rsa.pub'))

    colorama.init(autoreset=True)

    if debug:
        banner("BEGIN ARGUMENTS")
        pprint(arguments)
        banner("END ARGUMENTS")

    WARNING = "WARNNING WARNNING WARNNING WARNNING WARNNING"


    #
    # FIND ALL GIT REPOS IN cwd
    #
    repos["all"] = gett_all_repos()

    #
    # FIND ALL GIT REPOS that start with cloudmes-
    #
    repos["cloudmesh"] = []
    for repo in repos["all"]:
        if repo.startswith("cloudmesh-"):
            repos["cloudmesh"].append(repo)


    if arguments["purge"] and arguments["local"]:
        dryrun = not arguments['--force']

        eggs = list(Path(arguments["DIR"]).glob("**/cloudmesh*egg*"))

        if dryrun:
            banner("Dryrun purge")
            for egg in eggs:
                print(f" found -> {egg}")
        else:

            print()
            banner(WARNING, c=Fore.RED)

            print(textwrap.dedent(Fore.RED + """
                Please notice that executing this command can do harm to your
                instalation. If you delete files with this command it is on your
                own risk. The deletion may have bad effects on your python
                environment. So please only use it if you know what it effects.
                """))
            print()
            if not yn_question(
                Fore.RED + f"WARNING: Do you realy want to continue. This is DANGEROUS (yes/n)? "):
                sys.exit(1)

            for egg in eggs:
                print()
                if yn_question(
                    Fore.RED + f"WARNING: Do you want to delete the egg '{egg}' (yes/n)? "):
                    remove(egg)

    elif arguments["venv"] and arguments["purge"]:

        name = arguments["ENV"]
        force = arguments["--force"]
        if force and name.startswith("ENV") and yn_question(f"Would you like reinstall the venv {name} (yes/n)? "):
            os.system(f"rm -rf  ~/{name}")
            os.system(f"python3 -m venv  ~/{name}")
            os.system("source ~/ENV3/bin/activate; pip install -U pip ; pip install cloudmesh-installer")

            print()
            print ("You can add the following to your .bashrc or .bash_profile")
            print ()
            print ("    source ~/ENV3/bin/activate")
            print ()

    elif arguments["bundles"]:

        for bundle in repos:
            print(Fore.BLUE + f"{bundle}:" + Fore.RESET)
            elements = ' '.join(repos[bundle])
            block = textwrap.fill(elements, 70, break_on_hyphens=False)

            print(textwrap.indent(block, "        "))

    elif arguments["list"] and arguments["git"]:
        print (bundle)
        banner(f" {bundle}")
        for entry in repos[bundle]:
            location = Git.url(entry)
            print (f"{location}.git")


    elif arguments["list"]:
        banner(f" {bundle}")

        if not arguments["--short"]:
            print('\n'.join(repos[bundle]))
        else:
            print (' '.join(repos[bundle]))

    elif arguments["version"]:

        print (insatller_version)

    elif arguments["info"]:

        executable = sys.executable
        if "pyenv" not in executable:
            banner(WARNING, c=Fore.RED)
            print()
            print(Fore.RED + "You are likely not running pyenv, please remember that for "
                  "development purpuses we recommend you run in a virtual env. "
                  "Please consult with our handbook on how to set one up")
        print()
        print ("We found your executable in:")
        print(executable)
        print()
        print (70 * '-')
        print ()

        # print("info")
        # packages = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]

        data = [["Package", "Git", "Pypi", "Installed"]]
        packages = repos[bundle]

        for package in packages:

            undefined = Fore.RED + "not found" + Style.RESET_ALL
            entry = [
                package,
                undefined, # "git":
                undefined, # "PYPI"
                undefined,  # "installed"
            ]
            print("\nVersion -> {package}".format(
                package=package))


            #
            # GIT
            #
            try:
                v = requests.get("https://raw.githubusercontent.com/cloudmesh"
                                 "/{package}/master/VERSION".format(
                    package=package)).text
                entry[1] = v
            except:
                v = "!CANNOT FIND GIT VERSION INFO"
            finally:
                if '404' in v:
                    v = "!CANNOT FIND GIT VERSION INFO"
            print("...Github Version ->", v)

            #
            # PYPI
            #
            try:
                v = requests.get("https://pypi.org/project/{package}/".format(
                    package=package)).text
                pat_str = '(.*)<h1 class="package-header__name">(.+?)</h1>(.*)'
                pattern = re.compile(pat_str, re.M | re.I | re.S)
                groups = re.match(pattern, v)
                # print (groups)
                v = (groups.group(2)).strip().split(package)[1].strip()
                entry[2] = v
            except:
                v = "!CANNOT FIND PYPI VERSION INFO"
            print("...Pypi Version ->", v)
            data.append(entry)

            #
            # INSTALLED
            #
            try:
                installed = run("pip freeze | grep {package}".format(
                    package=package)).strip()
                entry[3] = installed
            except:
                installed = "!CANNOT FIND INSTALLED VERSION"
            print("...Installed Version ->", installed)


        print (70 * "-")
        print()
        print(tabulate(data, headers="firstrow"))
        print()



    if arguments["status"] and arguments["git"]:
        # repos = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]
        Git.status(repos[bundle])

    elif arguments["clone"] and arguments["git"]:
        result = Git.clone(repos[bundle])

    elif arguments["pull"] and arguments["git"]:

        Git.pull(repos[bundle])

    elif arguments["key"] and arguments["git"]:

        try:
            location = arguments["LOCATION"]
            print("Key location:", location)
            if not location.endswith(".pub"):
                print(Fore.RED + "ERROR: make sure you specify a public key")
                sys.exit(1)
            key_contents = open(location).read()
            print()
            print("Make sure you copy the content between the lines to github")
            print(70 * "-")
            print(key_contents.strip())
            print(70 * "-")
            print(
                "Please copy the content now, so you can use it in the browser.")
            print()
            if yn_question(
                "would you like to open a web page to github to upload the key (yes/n)? "):
                webbrowser.open_new("https://github.com/settings/keys")
                if yn_question("Is the key missing (yes/n)? "):
                    print("Paste the key in the next window and submit.")
                    webbrowser.open_new("https://github.com/settings/ssh/new")

        except:
            print(" you must have a key and upload it to github.")
            print("To generate the key use ssh-keygen")
            print("To avoid typing in the password all the time, usee ssh-add")

    elif arguments["install"]:
        if arguments["-e"]:
            result = Git.install(repos[bundle], dev=True)
        else:
            result = Git.install(repos[bundle])

    elif arguments["pyenv"] and arguments["purge"]:
        environment = arguments["ENV"]

        print()
        banner(WARNING, c=Fore.RED)

        print(Fore.RED + textwrap.dedent("""
        Please notice that executing this command can do harm to your
        instalation. This command also does not work if you are not setting up
        the pyenv as we discussed in our handbook. YOu must make sure that your
        .bashrc or .bash_profile files are properly configured for pyenv
        
        If you use venv please do not use this command.
        
        If you do not use pyenv or do not know what it is, you for sure do not
        want to executethis command.
        
        """))
        print()
        print(
            "next you need to activate your pyenv, use the following commands")
        print()

        print(70 * '-')
        for line in pyenv_purge:
            print(line.format(env=environment))
        print(70 * '-')
        print()
        if arguments["--force"] and \
            yn_question("Would you like us to execute them (yes/n)? ") and \
            yn_question(
                "Last warning, do you realy want to do it (yes/n)? ") and \
            yn_question(
                "Now the real last warning, do you realy want to do it (yes/n)? "):

            print(70 * '-')
            for line in pyenv_purge:
                command = line.format(env=environment)
                print("Executing:", command)
                print()
                os.system(command)
            print(70 * '-')
            print()



if __name__ == '__main__':
    main()
