##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   PyLogix Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``pylogix_library`` is used for this Step Implementation file. All Steps are in the ``pylogix.py`` file.
Go to the Concepts to see any concepts that simplify the steps.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, before_suite, after_suite, before_spec
import os
import sys
sys.path.append(r"../pylogix_library")
try:
    from PyLogixLibrary import PyLogixController
except Exception as exc:
    print("import pylogix:: {} occured: {}".format(type(exc).__name__, exc))

##########################################################################
# before suite
###
@before_suite
def beforeSuiteHook():
    """
    Initializes variables:
        * ``data_store.suite["pyLogixConnected"]`` is set to ``False`` so that no Step can be run unless the PyLogix Controller class is created
    """
    data_store.suite["pyLogixConnected"] = False

##########################################################################
# methods
###
# connect
###
@step("PyLogix connect")
def pyLogixConnect():
    """
    Create the PyLogix Contoller class using the ``data_store.suite["pyLogixController"]`` variable.

    Step and function definition::

        @step("PyLogix connect")
        def pyLogixConnect():

    Example usage:
        * PyLogix connect
    """
    if data_store.suite["pyLogixConnected"]:
        Messages.write_message("PyLogix object already connected")
    else:
        try:
            data_store.suite["pyLogixController"] = PyLogixController()
            Messages.write_message("Created PyLogix object successful")
            data_store.suite["pyLogixConnected"] = True
        except:
            Messages.write_message("Error creating PyLogix object")
            assert False
###
# disconnect
###
@step("PyLogix disconnect")
def pyLogixDisconnect():
    """
    Deconstruct the PyLogix Contoller class variable ``data_store.suite["pyLogixController"]``.

    Step and function definition::

        @step("PyLogix disconnect")
        def pyLogixDisconnect():

    Example usage:
        * PyLogix disconnect
    """
    if data_store.suite["pyLogixConnected"]:
        del(data_store.suite["pyLogixController"])
    else:
        Messages.write_message("PyLogix not connected")
    data_store.suite["pyLogixConnected"] = False
###
# read
###
@step("PyLogix read tag <tagname> check <checkReturn>")
def pyLogixRead(tagname, checkReturn):
    """
    Read tag from the given variable tagname and then assert against the result based on checkReturn variable.

    Args:
        tagname (string): The tagname string.
        checkReturn (bool): True or False.

    Step and function definition::

        @step("PyLogix read tag <tagname> check <checkReturn>")
        def pyLogixRead(tagname, checkReturn):

    Example usage:
        * PyLogix read tag "Osprey:I.ConnectionFaulted" check "True"
        * PyLogix read tag "Osprey:O.Data[0]" check "False"
    """
    assert data_store.suite["pyLogixConnected"] == True, "PyLogix is not connected"
    results = data_store.suite["pyLogixController"].read(tagname)
    Messages.write_message(results["description"])
    Messages.write_message(results)
    if checkReturn.lower() == "true":
        assert results["result"] == 0, "read failed"
###
# write
###
@step("PyLogix write tag <tagname> value <value> check <checkReturn>")
def pyLogixWrite(tagname, value, checkReturn):
    """
    Write tag to the given variable tagname with value and then assert against the result based on checkReturn variable.

    Args:
        tagname (string): The tagname string.
        value (int): Value to write to tag.
        checkReturn (bool): True or False.

    Step and function definition::

        @step("PyLogix write tag <tagname> value <value> check <checkReturn>")
        def pyLogixWrite(tagname, value, checkReturn):

    Example usage:
        * PyLogix write tag "Osprey:O.Data[0].4" value "1" check "False"
    """
    assert data_store.suite["pyLogixConnected"] == True, "PyLogix is not connected"
    results = data_store.suite["pyLogixController"].write(tagname, int(value))
    Messages.write_message(results["description"])
    Messages.write_message(results)
    if checkReturn.lower() == "true":
        assert results["result"] == 0, "write failed"
