"""cloudmesh-installer -- a helper to install cloudmesh from source for developers.

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

    cloudmesh-installer update [BUNDLE]
    cloudmesh-installer get [BUNDLE]

        For each repository in the bundle it clones it and also pulls.
        Thus the command can easly be used to get a new bundle element, but
        also get the new code for already existing bundles elements.

        The code is checked out with https

    cloudmesh-installer get -ssh [BUNDLE]

        For each repository in the bundle it clones it and also pulls.
        Thus the command can easly be used to get a new bundle element, but
        also get the new code for already existing bundles elements.

        The code is checked out with ssh

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
import platform

import colorama
import requests
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.console import Console
from cloudmesh.common.util import banner
from cloudmesh_installer.install.__version__ import version as installer_version
from cloudmesh_installer.install.bundle import *
from colorama import Fore, Style
from docopt import docopt
from ordered_set import OrderedSet
from tabulate import tabulate
from cloudmesh.common.Shell import Shell

debug = False
benchmark = False

def os_is_pi():
    """
    Checks if the os is Raspberry OS

    :return: True is Raspberry OS
    :rtype: bool
    """
    try:
        content = readfile('/etc/os-release')
        return platform.system() == "Linux" and "raspbian" in content
    except:  # noqa: E722
        return False

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
        StopWatch.status(command, "error" not in str(output).lower())

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

    # "git@github.com:cloudmesh/cloudmesh-installer.git"

    @staticmethod
    def url(repo, protocol="https"):

        if protocol == "https":
            prefix = "https://github.com/"
        else:
            prefix = "git@github.com:"
        print(repo)
        global repos
        if repo in repos['community'] or 'sp19' in repo or 'fa19' in repo or 'sp20' in repo or 'fa20' in repo:
            return f"{prefix}cloudmesh-community/{repo}"
        elif 'bookmanager' in repo:
            return f"{prefix}cyberaide/{repo}"
        elif 'book' == repo:
            return f"{prefix}cloudmesh-community/{repo}"
        else:
            return f"{prefix}cloudmesh/{repo}"

    @staticmethod
    def error_color(error="ERROR"):
        if error == "ERROR":
            color = Fore.RED
        elif error == "WARNING":
            color = Fore.MAGENTA
        elif error == "INFO":
            color = Fore.MAGENTA
        else:
            color = ""
        return color

    @staticmethod
    def clone(repos, error="INFO", protocol="https"):
        repos = OrderedSet(repos)

        for repo in set(repos):
            print(f"clone -> {repo}")

            if not os.path.isdir(Path(f"./{repo}")):
                try:
                    location = Git.url(repo, protocol=protocol)
                    command = f"git clone {location}.git"
                    r = run(command)
                    print(f"         {r}")
                except Exception as e:
                    print(e)
            else:

                color = Git.error_color(error)

                print(color + f"         {error}: not downloaded as repo already exists.")

    @staticmethod
    def version(repos):
        for repo in repos:
            with open(f"{repo}/VERSION") as f:
                v = f.read().strip()
            print(f"version {repo:30}:", v)

    @staticmethod
    def command(repos, name, ok_msg="nothing to commit, working tree clean", r=False):
        repos = OrderedSet(repos)

        for repo in repos:
            print("status ->", f"{repo:25}", end=" ")

            try:
                os.chdir(repo)
            except FileNotFoundError:
                print(Fore.RED + "ERROR:", repo, "not found")

            result = run(f"git {name}", verbose=False)
            if ok_msg in result:
                print(Fore.GREEN + "... ok")
            else:
                print()
                print(Fore.RED + result)
            os.chdir("../")

    @staticmethod
    def _command(repos, command, ok_msg="Uploading", verbose=False, r=False):
        repos = OrderedSet(repos)

        for repo in repos:
            print(f"{command} -> {repo:25}", end=" ")

            try:
                os.chdir(repo)
            except FileNotFoundError:
                print(Fore.RED + "ERROR:", repo, "not found")

            result = run(f"{command}", verbose=False)

            if ok_msg in result:
                print(Fore.GREEN + "... ok")
            else:
                print()
                print(Fore.RED + result)

            if verbose:
                print()
                print(textwrap.indent(result, "    "))
                print()

            os.chdir("../")

    @staticmethod
    def status(repos):
        Git.command(repos, "status",
                    ok_msg="nothing to commit, working tree clean")

    @staticmethod
    def authors(repos, error="ERROR"):

        command = "shortlog -e -s -n"
        Git.command(repos, command)

    @staticmethod
    def pull(repos):
        Git.command(repos, "pull", ok_msg="Already up to date.")

    @staticmethod
    def get(repos, dev=True, protocol="https"):
        Git.clone(repos, error="WARNING", protocol=protocol)
        Git.pull(repos)
        Git.install(repos, dev=dev)

    @staticmethod
    def install(repos, dev=False, protocol="https"):

        repos = OrderedSet(repos)

        Git.clone(repos, protocol=protocol)

        for repo in repos:

            StopWatch.start("install " + repo)

            if dev:
                banner(f"dev install -> {repo}")

                Console.info(f"pip install -e .: {repo}")
                print()

                os.chdir(repo)
                os.system("pip install -e .")
                os.chdir("../")

            else:
                banner(f"install -> {repo}")

                Console.info(f"pip install: {repo}")
                print()

                os.system("pip install {repo}".format(repo=repo))

            if repo in javascript_repo:
                banner(f"javascript install -> {repo}")

                Console.info(f"pip install -e .: {repo}")
                print()

                os.chdir(repo)
                os.system("yarn")
                os.chdir("../")

            StopWatch.stop("install " + repo)
            StopWatch.status("install " + repo, True)


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
    except Exception as e:  # noqa: F841
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
        ERROR("No  bundle specified.")
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
    block = block + textwrap.indent(textwrap.fill(elements, 70, break_on_hyphens=False), "    ")
    return block


def main():
    arguments = docopt(__doc__)

    bundle = arguments["BUNDLE"]
    benchmark = arguments["--benchmark"]  # noqa: F841

    arguments["DIR"] = \
        os.path.expandvars(os.path.expanduser(arguments.get("DIR") or '.'))
    arguments["LOCATION"] = \
        os.path.expandvars(os.path.expanduser(
            arguments.get("LOCATION") or '~/.ssh/id_rsa.pub'))

    protocol = "https"
    if arguments["--ssh"]:
        protocol = "ssh"

    colorama.init(autoreset=True)

    if debug:
        banner("BEGIN ARGUMENTS")
        pprint(arguments)
        banner("END ARGUMENTS")

    WARNING = "WARNING WARNING WARNING WARNING WARNING"

    #
    # FIND ALL GIT REPOS IN cwd
    #
    global repos
    repos["all"] = get_all_repos()

    #
    # FIND ALL GIT REPOS that start with cloudmesh
    #

    bundles = arguments["BUNDLES"]

    def _get_bundles():
        repositories = []

        bundles = arguments["BUNDLES"]

        for bundle in bundles:
            check_for_bundle(bundle)
            repositories += repos[bundle]

        return repositories

    repos["cloudmesh"] = []
    for repo in repos["all"]:
        if repo.startswith("cloudmesh-"):
            repos["cloudmesh"].append(repo)

    if arguments["version"]:

        print(installer_version)

    elif arguments["burn"] and arguments["--branch"] and arguments["BRANCH"]:
        Console.warning(
            "This command only works if you installed the source version and are standing in the cm directory")
        dirname = os.path.basename(os.getcwd())

        if dirname != 'cm':
            Console.error("you are not in cm")
        else:
            branch = arguments["BRANCH"]
            for repo in ["cloudmesh-pi-burn", "cloudmesh-inventory"]:
                r = Shell.run(f"cd {repo} ; git checkout {branch} ; pip install -e .")
                print(r)
            for repo in ["cloudmesh-pi-burn", "cloudmesh-inventory"]:
                b = Shell.run(f"cd {repo} ; git rev-parse --symbolic-full-name --abbrev-ref HEAD").strip()
                Console.ok(f"{repo} is in branch {b}")

        return ""

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
        protocol = "https"
        check_for_bundle(bundle)
        print(bundle)
        banner(f" {bundle}")
        for entry in repos[bundle]:
            location = Git.url(entry, protocol=protocol)
            print(f"{location}.git")

    elif arguments["list"] and arguments["BUNDLE"]:

        bundle = arguments["BUNDLE"]
        if bundle in repos:
            print(bundle_elements(bundle))
        else:
            print(f"ERROR: could not find bundle {bundle}")
            print("Available bundles: ")
            print(" ".join(repos.keys()))

        return ""

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
                                 f"/{package}/main/VERSION").text
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
        repositories = _get_bundles()
        Git.status(repositories)

    elif arguments["clone"] and arguments["git"]:
        repositories = _get_bundles()
        result = Git.clone(repositories, error="INFO", protocol=protocol)

    elif arguments["pull"] and arguments["git"]:
        repositories = _get_bundles()
        Git.pull(repositories)

    elif arguments["authors"] and arguments["git"]:
        repositories = _get_bundles()
        Git.authors(repositories)

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
            if yn_question("would you like to open a web page to github to upload the key (yes/n)? "):
                webbrowser.open_new("https://github.com/settings/keys")
                if yn_question("Is the key missing (yes/n)? "):
                    print("Paste the key in the next window and submit.")
                    webbrowser.open_new("https://github.com/settings/ssh/new")

        except:
            print(" you must have a key and upload it to github.")
            print("To generate the key use ssh-keygen")
            print("To avoid typing in the password all the time, use ssh-add")

    elif arguments["get"] or arguments["update"]:

        repositories = _get_bundles()

        Git.get(repositories, protocol=protocol)

        # if benchmark:
        #    StopWatch.benchmark(sysinfo=True)

    elif arguments["install"]:
        banner(f"Installing bundles: {bundles}")
        repositories = OrderedSet(_get_bundles())
        print('\n'.join(repositories))
        print()
        if arguments["--venv"]:
            result = Git.install(repositories)
        else:
            result = Git.install(repositories, dev=True)

        StopWatch.benchmark(sysinfo=True)

    elif arguments["release"]:

        testing = "TESTING" in os.environ

        if testing:
            del os.environ["TESTING"]

        os.system("pip install twine")

        repos = arguments["REPOS"]

        repositories = []
        for repository in repos:
            repositories.append(f"cloudmesh-{repository}")

        banner(f"Releasing repositories: {repositories}")
        print('\n'.join(repositories))
        print()

        result = Git._command(repositories, "make patch")  # noqa: F841
        result = Git._command(repositories, "make release")  # noqa: F841

        StopWatch.status("make patch", "released")
        StopWatch.status("make release", "released")

        StopWatch.benchmark(sysinfo=True)

        Git.version(repositories)

        if testing:
            os.environ["TESTING"] = "1"

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

        if arguments["--force"] and yn_question("Would you like us to execute them (yes/n)? "):

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

            if not yn_question(Fore.RED + "WARNING: Removing listed files. Do you really want to continue. yes/n)? "):
                sys.exit(1)

            for egg in eggs:
                remove(egg)

    elif arguments["new"]:

        python = arguments["--python"] or "python3.8"
        venv = arguments["VENV"] or os.path.basename(os.environ("VIRTUAL_ENV")) or "~/ENV3"

        if os.path.basename(venv).startswith("ENV") and \
            yn_question(f"Would you like reinstall the venv {venv} (yes/n)? "):  # noqa: E125

            script = textwrap.dedent(f"""
            rm -rf {venv}
            {python} -m venv {venv}
            source {venv}/bin/activate
            pip install pip -U
            which python
            which pip
            python --version
            pip --version
            pip install cloudmesh-installer
            """).strip()

            script = "; ".join(script.splitlines())

            os.system(script)

            if bundles:
                print()
                print("Installing Bundles")
                print()
                repositories = _get_bundles()
                Git.get(repositories)

            print()
            print(
                "You can add the following to your .bashrc or .bash_profile" or ".zprofile")
            print()
            print("    source ~/ENV3/bin/activate")
            print()

        elif arguments["pi"] and arguments["--dev"]:

            if os_is_pi():
                os.system("curl -Ls https://raw.githubusercontent.com/cloudmesh/get/main/pi/index.html | sh -")
            else:
                Console.error("Command can only be executed on a Pi")
            return ""

        elif arguments["pi"]:

            if os_is_pi():
                os.system("curl -Ls http://cloudmesh.github.io/get/pi | sh -")
            else:
                Console.error("Command can only be executed on a Pi")
            return ""




if __name__ == '__main__':
    main()
