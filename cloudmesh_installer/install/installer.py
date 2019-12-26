"""cloudmesh-installer -- a helper to install cloudmesh from source for developers.

Usage:
  cloudmesh-installer git key [LOCATION] [--benchmark]
  cloudmesh-installer git [clone|pull|status] [BUNDLE] [--benchmark]
  cloudmesh-installer install [BUNDLE] [--venv=ENV | -e] [--benchmark]
  cloudmesh-installer list [BUNDLE] [--short | --git]
  cloudmesh-installer version
  cloudmesh-installer info [BUNDLE] [--verbose]
  cloudmesh-installer clean --dir=DIR [--force]
  cloudmesh-installer clean --venv=ENV [--force]



A convenient program called `cloudmesh-installer` to download and install
cloudmesh from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos
  ENV         the name of the venv
  DIR         the directory form where to start the search

Options:
  -h --help
  --force   force the execution of the command. This command could delete files.

Description:

    cloudmesh-installer list

        Cloudmesh has a number of bundles. Bundles are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

        This command lists all available bundles

    cloudmesh-installer list bundle

        lists the information about a particular bundle.

    cloudmesh-installer list [BUNDLE] --git

        Shows the location of the repositories in a bundle.

    cloudmesh-installer info

        The info command gives some very basic information about the version
        numbers of cloudmesh on your system, github, and pypi. THis helps
        identifying if you may run an odlder version.

        In addition we try to check if you do use venv

    cloudmesh-installer git key [LOCATION]

        This command only works if you use ssh keys to authenticate with github.
        This command makes uploading the key easy as it checks for your key and
        provides via the web browser automatic pageloads to github for the
        key upload. You do not have tou use this command. It is intenden for
        novice users.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer clean --dir=. --force

       removes the egs in the current directory tree

    cloudmesh-installer clean --venv=ENV --force

        removes the venv in ~/ENV

    Examples:

        let us assume you like to work on storage, than you need to do the following

            mkdir cm
            cd cm
            cloudmesh-installer git clone storage
            cloudmesh-installer install storage
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
import hostlist

import oyaml as yaml
import requests
from docopt import docopt
import colorama
from colorama import Fore, Style
from venv import EnvBuilder
import pip
import os
from cloudmesh_installer.install.util import banner

from cloudmesh_installer.install.StopWatch import StopWatch

from cloudmesh_installer.install.__version__ import version as insatller_version

debug = False
benchmark = False

# 'cloudmesh-azure',
# 'cloudmesh-aws'

cms = [
    'cloudmesh-common',
    'cloudmesh-cmd5',
    'cloudmesh-sys',
    'cloudmesh-configuration',
    'cloudmesh-manual'
]

cloud = cms + [
    'cloudmesh-cloud',
    'cloudmesh-openstack',
    'cloudmesh-inventory',
]

repos = dict({

    'cms': cms,

    'cloud': cloud,

    'inventory': cms + [
        'cloudmesh-inventory',
    ],

    'cmsd': ['cloudmesh-cmsd'],

    'docker': ['cloudmesh-cmsd'],

    'iu': cloud + [
        'cloudmesh-iu'
    ],

    'batch': cloud + [
        'cloudmesh-batch',
    ],

    'storage': cloud + [
        'cloudmesh-storage',
        'cloudmesh-box',
    ],

    'oracle': cloud + [
        'cloudmesh-storage',
        'cloudmesh-oracle',
    ],

    'openstack': cloud + [
        'cloudmesh-openstack',
    ],

    'google': cloud + [
        'cloudmesh-storage',
        'cloudmesh-google',
    ],

    'frugal': cloud + [
        'cloudmesh-frugal',
    ],

    'analytics': cms + [
        'cloudmesh-analytics'
    ],

    'source': cloud + [
        'cloudmesh-analytics',
        'cloudmesh-aws',
        'cloudmesh-azure',
        'cloudmesh-bar',
        'cloudmesh-batch',
        'cloudmesh-box',
        'cloudmesh-cmsd',
        'cloudmesh-comet',
        'cloudmesh-conda',
        'cloudmesh-docker',
        'cloudmesh-emr',
        'cloudmesh-flow',
        'cloudmesh-flow2',
        'cloudmesh-git',
        'cloudmesh-google',
        'cloudmesh-gui',
        'cloudmesh-iu',
        'cloudmesh-nist',
        'cloudmesh-nn',
        'cloudmesh-notebooks',
        'cloudmesh-openapi',
        'cloudmesh-oracle',
        'cloudmesh-redshift',
        'cloudmesh-stopwatch',
        'cloudmesh-storage',
        'cloudmesh-workflow',
        'cloudmesh-storagelifecycle',
        'cloudmesh-oracle',
        'cloudmesh-frugal',
        'cloudmesh-analytics'
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

    'flow': cloud + [
        'cloudmesh-flow',
    ],

    'emr': cloud + [
        'cloudmesh-emr',
    ],

    'conda': [
        'cloudmesh-conda'
    ],

    '516': hostlist.expand_hostlist("fa19-516-[140-172,174]"),

    '523': hostlist.expand_hostlist("fa19-523-[180-196,198-212]"),

    'spring19': [
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
                    'sp19-616-111',
                    'sp19-616-112'
                ] + hostlist.expand_hostlist(
        "sp19-516-[22,26,29,121-125,127-139]")
                + hostlist.expand_hostlist("sp19-222-[89-94,96-102]")
})


def run(command, verbose=True):
    global benchmark
    if verbose:
        print(command)
    try:
        StopWatch.start(command)
        output = subprocess.check_output(command,
                                         shell=True,
                                         stderr=subprocess.STDOUT,
                                         )
        StopWatch.stop(command)
    except subprocess.CalledProcessError as err:
        if verbose:
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
        if repo in repos['community'] or \
            repo in repos['spring19'] or \
            repo in repos['523'] or \
            repo in repos['516']:
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
                print(Fore.RED + "         ERROR: not downloaded as repo "
                                 "already exists.")

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
                print()
                print(Fore.RED + result)
            os.chdir("../")

    @staticmethod
    def status(repos):
        Git.command(repos, "status",
                    ok_msg="nothing to commit, working tree clean")

    @staticmethod
    def pull(repos):
        Git.command(repos, "pull", ok_msg="Already up to date.")

    @staticmethod
    def install(repos, dev=False):
        for repo in repos:
            StopWatch.start("install " + repo)
            print("install ->", repo)
            if dev:
                os.chdir(repo)
                os.system("pip install -e .")
                os.chdir("../")
            else:
                os.system("pip install {repo}".format(repo=repo))
            StopWatch.stop("install " + repo)


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


def RED(msg):
    print(Fore.RED + msg + Fore.RESET)


def ERROR(msg):
    RED("ERROR: " + msg)


def WARNING(msg):
    RED("WARNING: " + msg)




def remove(location):
    print("delete", location)
    try:
        shutil.rmtree(location)
        print("removing:", location)
    except Exception as e:
        print("Removing failed, file removal")
    try:
        os.remove(location)
        print("removing:", location)
    except Exception as e:
        print("Removing failed, not sure what to do next")
        print(e)


def get_all_repos():
    path = Path(".").resolve()
    gits = list(path.glob("*/.git"))
    names = []
    for repo in gits:
        names.append(os.path.basename(os.path.dirname(repo.resolve())))
    return names


def check_for_bundle(bundle):
    if bundle is None:
        ERROR(f"No  bundle specified.")
        sys.exit(1)
    elif not ((bundle in repos) or (bundle in ["cloudmesh", "all"])):
        ERROR(f"The bundle `{bundle}` does not exist")
        sys.exit(1)

def bundle_list(repos):
    names = []
    for bundle in repos:
        names.append(f'"{bundle}"')
    result = "[" + ", ".join(names) + "]"
    return result

def bundle_elements(bundle):
    block = Fore.BLUE + f"\n{bundle}:\n" + Fore.RESET
    elements = ' '.join(repos[bundle])
    block = block + \
        textwrap.indent(
            textwrap.fill(elements , 70, break_on_hyphens=False),"    ")
    return block

def main():
    arguments = docopt(__doc__)

    bundle = arguments["BUNDLE"]
    benchmark = arguments["--benchmark"]

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

    WARNING = "WARNING WARNING WARNING WARNING WARNING"

    #
    # FIND ALL GIT REPOS IN cwd
    #
    repos["all"] = get_all_repos()

    #
    # FIND ALL GIT REPOS that start with cloudmesh
    #
    repos["cloudmesh"] = []
    for repo in repos["all"]:
        if repo.startswith("cloudmesh-"):
            repos["cloudmesh"].append(repo)

    if arguments["version"]:

        print(insatller_version)

    elif arguments["list"] and not arguments["BUNDLE"] and not arguments["--git"]:

        if not arguments["--short"]:
            banner("Cloudmesh Bundles")
            block = ""
            for bundle in repos:
                block = block + bundle_elements(bundle)

            print(block)
        else:
            print(bundle_list(repos))


    elif arguments["list"] and arguments["--git"]:
        check_for_bundle(bundle)
        print(bundle)
        banner(f" {bundle}")
        for entry in repos[bundle]:
            location = Git.url(entry)
            print(f"{location}.git")


    elif arguments["info"]:

        verbose = arguments["--verbose"]
        native = hasattr(sys, 'real_prefix')
        executable = sys.executable
        if native:
            banner(WARNING, c=Fore.RED)
            print()
            RED("You are likely not running in a venv. "
                "Please remember that for "
                "development purposes we recommend you run in a venv. "
                "Please consult with our handbook on how to set one up")

        print()
        print("We found python in:")
        print(executable)
        print()
        print(70 * '-')
        print()

        # print("info")
        # packages = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]

        bundle = arguments["BUNDLE"] or "cms"

        data = [["Package", "Git", "Pypi", "Installed"]]
        packages = repos[bundle]

        for package in packages:

            undefined = Fore.RED + "not found" + Style.RESET_ALL
            entry = [
                package,
                undefined,  # "git":
                undefined,  # "PYPI"
                undefined,  # "installed"
            ]
            if verbose:
                print(f"\nVersion -> {package}")

            #
            # GIT
            #
            try:
                v = requests.get("https://raw.githubusercontent.com/cloudmesh"
                                 "/{package}/master/VERSION".format(
                    package=package)).text
                entry[1] = v
            except:
                v = "ERROR: can not find git version"
            finally:
                if '404' in v:
                    v = "ERROR: can not find git version"
            if verbose:
                print("... Github Version ->", v)

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
                v = "ERROR: can not find pypi version"
            data.append(entry)
            if verbose:
                print("... Pypi Version ->", v)

            #
            # INSTALLED
            #
            try:
                installed = run(f"pip freeze | grep {package}",
                                verbose=False).strip()
                entry[3] = installed
            except:
                installed = "ERROR: can not find installed version"
            if verbose:
                print("... Installed Version ->", installed)

        if verbose:
            print(70 * "-")
            print()

        print(tabulate(data, headers="firstrow"))
        print()

    elif arguments["status"] and arguments["git"]:
        check_for_bundle(bundle)
        # repos = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]
        Git.status(repos[bundle])
        # if benchmark:
        #    StopWatch.benchmark(sysinfo=True)

    elif arguments["clone"] and arguments["git"]:
        check_for_bundle(bundle)
        result = Git.clone(repos[bundle])
        # if benchmark:
        #    StopWatch.benchmark(sysinfo=True)


    elif arguments["pull"] and arguments["git"]:
        check_for_bundle(bundle)
        Git.pull(repos[bundle])
        # if benchmark:
        #    StopWatch.benchmark(sysinfo=True)


    elif arguments["key"] and arguments["git"]:

        try:
            location = arguments["LOCATION"]
            print("Key location:", location)
            if not location.endswith(".pub"):
                ERROR("make sure you specify a public key")
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
            print("To avoid typing in the password all the time, use ssh-add")

    elif arguments["install"]:
        banner(f"Installing bundle {bundle}")
        print ('\n'.join(repos[bundle]))
        print()
        if arguments["--venv"]:
            result = Git.install(repos[bundle])
        else:
            result = Git.install(repos[bundle], dev=True)

        StopWatch.benchmark(sysinfo=True)


    elif arguments["--venv"] and arguments["clean"]:
        environment = arguments["--venv"]

        print()
        banner(WARNING, c=Fore.RED)

        RED(textwrap.dedent("""
            Please notice that executing this command can do harm to your
            installation. 
            
            Make sure that you also check your 
            .bashrc, .bash_profile or .zprofile files as appropriately to remove 
            aliasses or path variables pointing to your venv."""))

        print()

        print(70 * '-')
        banner(f"Removing {environment}")
        print(70 * '-')
        print()

        commands = [f'rm -rf "~/{environment}"']
        print("\n".join(commands))
        print()

        if arguments["--force"] and \
            yn_question("Would you like us to execute them (yes/n)? "):

            print(70 * '-')
            for command in commands:
                print("Executing:", command)
                print()
                os.system(command)
            print(70 * '-')
            print()

    elif arguments["clean"] and arguments["--dir"]:
        dryrun = not arguments['--force']

        directory = arguments["--dir"]

        eggs = list(Path(directory).glob("**/cloudmesh*egg*"))

        if dryrun:
            banner("Dryrun directory clean")
            for egg in eggs:
                print(f" found -> {egg}")
        else:

            print()
            banner(WARNING, c=Fore.RED)

            RED(textwrap.dedent("""
                Please notice that executing this command can do harm to your
                installation. If you delete files with this command it is on your
                own risk. The deletion may have bad effects on your python
                environment. So please only use it if you know what it effects.
                """))
            print()

            for egg in eggs:
                print(f" found -> {egg}")
            print()

            if not yn_question(
                Fore.RED + f"WARNING: Removing listed files. Do you really want to continue. yes/n)? "):
                sys.exit(1)

            for egg in eggs:
                remove(egg)

    elif arguments["venv"] and arguments["purge"]:

        is_venv = sys.hasattr(sys, 'real_prefix')
        python_path = sys.executable

        name = arguments["ENV"]
        force = arguments["--force"]
        if force and name.startswith("ENV") and yn_question(
            f"Would you like reinstall the venv {name} (yes/n)? "):
            os.system(f"rm -rf  ~/{name}")
            os.system(f"python3 -m venv  ~/{name}")
            os.system(
                "source ~/ENV3/bin/activate; pip install -U pip ; pip install cloudmesh-installer")

            print()
            print(
                "You can add the following to your .bashrc or .bash_profile" or ".zprofile")
            print()
            print("    source ~/ENV3/bin/activate")
            print()


if __name__ == '__main__':
    main()
