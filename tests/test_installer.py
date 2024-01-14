###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_installer..py::Test_installer.test_001
# pytest -v --capture=no tests/test_installer.py
# pytest -v  tests/test_installer.py
###############################################################

import shutil

import os
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import banner


@pytest.mark.incremental
class Test_installer:

    def test_create_dir(self):
        banner("test_create_dir")
        path = "tmp"
        try:
            os.mkdir(path)
        except OSError:
            print(f"Creation of the directory {path} failed")
        else:
            print(f"Successfully created the directory {path}")
        os.chdir(path)
        assert True

    def test_version(self):
        banner("test_version")

        cmd = "cmsi version"
        result = Shell.run(cmd)
        print(result)
        print()
        assert True

    def test_info(self):
        banner("test_info")
        print("PWD:", os.getcwd())

        cmd = "cmsi info"
        result = Shell.run(cmd)
        print(result)
        print()
        assert "We found python in" in str(result)

    def test_list(self):
        banner("list")

        cmd = "cmsi list"
        result = Shell.run(cmd)
        print(result)
        assert "cloudmesh-common" in result

    def test_non_existing(self):
        banner("test_non_existing")
        print("PWD:", os.getcwd())

        cmd = "cmsi git clone WRONG"
        try:
            result = Shell.run(cmd)
            assert False
        except RuntimeError:
            assert True

    def test_clone_community(self):
        banner("test_clone_community")
        print("PWD:", os.getcwd())

        cmd = "cmsi git clone community"
        result = Shell.run(cmd)
        print(result)
        assert os.path.isdir("cloudmesh-community.github.io")

    def test_clone_cms(self):
        banner("test_clone_cms")
        print("PWD:", os.getcwd())

        cmd = "cmsi git clone cms"
        result = Shell.run(cmd)
        print("RESULT:", result)

        assert os.path.isdir("cloudmesh-cmd5")

    def test_clone_ls(self):
        banner("test_clone_ls")
        print("PWD:", os.getcwd())
        banner("ls")

        cmd = "ls"
        result = Shell.run(cmd)
        print(result)


    def test_install_cms(self):
        banner("test_install_cms")
        print("PWD:", os.getcwd())

        cmd = "cmsi install cms"
        result = Shell.run(cmd)
        print("RESULT:", result)
        # Try to import the module and check if it raises an ImportError
        try:
            import cloudmesh.shell
            assert True
        except ImportError:
            assert False

    def test_cms_help(self):
        banner("test_cms_help")
        print("PWD:", os.getcwd())

        cmd = "cms help"
        result = Shell.run(cmd)
        print(result)
        assert "quit" in result

    def test_cms_info(self):
        banner("test_cms_info")
        print("PWD:", os.getcwd())

        cmd = "cms info"
        result = Shell.run(cmd)
        print(result)
        assert "cloudmesh.common" in result

    def test_cms_verion(self):
        banner("test_cms_version")
        print("PWD:", os.getcwd())

        cmd = "cms version"
        result = Shell.run(cmd)
        print(result)
        assert "cloudmesh.common" in result


class other:
    def test_delete_dir(self):
        path = "tmp"
        shutil.rmtree(path)
        assert True
