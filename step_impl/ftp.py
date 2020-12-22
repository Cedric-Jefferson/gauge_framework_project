##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   FTP Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``ftp_library`` is used for this Step Implementation file. All Steps are in the ``ftp.py`` file.

Go to the Concepts to see any concepts that simplify the steps.

"""

##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, before_suite
import os
import sys
sys.path.append(r"../ftp_library")
from FTPLibrary import FTPController

##########################################################################
# methods
###
# connect
###
@step("FTP connect <host>")
def ftpConnect(host):
    """
    Connect to given host address.

    Args:
        host (string): IP address of host

    Step and function definition::

        @step("FTP connect <host>")
        def ftpConnect(host):

    Example usage:
        * FTP connect "192.168.1.10"
    """
    try:
        data_store.suite["ftpController"] = FTPController()
        Messages.write_message("create ftp object successful")
    except:
        Messages.write_message("error creating ftp object")
        assert False
    results = data_store.suite["ftpController"].connect(host)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
    assert results["result"] == 0, "ftp connect failed"
###
# login
###
@step("FTP login <user> <password>")
def ftpLogin(user, password):
    """
    Login to connected host with given username and password.

    Args:
        user (string): Username to login with.
        password (string): Password to login with.

    Step and function definition::

        @step("FTP login <user> <password>")
        def ftpLogin(user, password):

    Example usage:
        * FTP login "root" "root"
    """
    results = data_store.suite["ftpController"].login(user, password)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
    assert results["result"] == 0, "ftp login failed"
###
# change work dir
###
@step("FTP cwd <newDir>")
def ftpChangeWorkDir(newDir):
    """
    Change working directory to given directory.

    Args:
        newDir (string): New directory.

    Step and function definition::

        @step("FTP cwd <newDir>")
        def ftpChangeWorkDir(newDir):

    Example usage:
        * FTP cwd "/molex_fs"

    """
    results = data_store.suite["ftpController"].cwd(newDir)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
    assert results["result"] == 0, "ftp cwd failed"
###
# make new dir
###
@step("FTP mkd <newDir>")
def ftpMakeDir(newDir):
    """
    Make new given directory.

    Args:
        newDir (string): New directory.

    Step and function definition::

        @step("FTP mkd <newDir>")
        def ftpMakeDir(newDir):

    Example usage:
        * FTP mkd "bin"
    """
    results = data_store.suite["ftpController"].mkd(newDir)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
    assert results["result"] == 0, "ftp mkd failed"
###
# list files in cwd
###
@step("FTP nlst")
def ftpListFiles():
    """
    Print contents in current working directory.

    Step and function definition::

        @step("FTP nlst")
        def ftpListFiles():

    Example usage:
        * FTP nlst
    """
    results = data_store.suite["ftpController"].nlst()
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
    assert results["result"] == 0, "ftp nlst failed"
###
# store binary
###
@step("FTP storebinary <filename>")
def ftpStoreBinary(filename):
    """
    Store given file on FTP.

    Args:
        filename (string): Name of file.

    Step and function definition::

        @step("FTP storebinary <filename>")
        def ftpStoreBinary(filename):

    Example usage:
        * FTP storebinary "sup"
    """
    results = data_store.suite["ftpController"].storbinary(filename)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
    assert results["result"] == 0, "ftp storebinary failed"
###
# store binary
###
@step("FTP exit")
def ftpExit():
    """
    Close FTP connection.

    Step and function definition::

        @step("FTP exit")
        def ftpExit():

    Example usage:
        * FTP exit
    """
    results = data_store.suite["ftpController"].exit()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "ftp exit failed"