##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   OPC UA Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``opcua_client_library`` is used for this Step Implementation file. All Steps are in the ``opcua_client.py`` file.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
import sys
from getgauge.python import step, Messages, data_store, before_suite, after_suite
sys.path.append(r"../opcua_client_library")
from OPCUAClientLibrary import OPCUAClientController

##########################################################################
# methods
###
# connect
###
@step("OPC UA Client connect <url>")
def opcUaClientConnect(url):
    """
    Create the NAB Agent Contoller class using the ``data_store.suite["opcUaClientController"]`` variable.

    Args:
        url (string): Url of OPC UA Server.

    Step and function definition::

        @step("OPC UA Client connect <url>")
        def opcUaClientConnect(url):

    Example Usage:
        * OPC UA Client connect "opc.tcp://192.168.1.10:48020"
    """
    data_store.suite["opcUaClientController"] = OPCUAClientController(url)
    Messages.write_message("Create OPC UA Client object successful")
###
# get node
###
@step("OPC UA Client get node <nodeId> <keyName>")
def opcUaClientGetNode(nodeId, keyName):
    """
    Get and set the node based on given string to variable in data_store object.

    Args:
        nodeId (string): ID of the node in OPC UA Server.
        keyName (string): Key name to save the variable as.

    Step and function definition::

        @step("OPC UA Client get node <nodeId> <keyName>")
        def opcUaClientGetNode(nodeId, keyName):

    Example usage:
        * OPC UA Client get node "ns=4;i=6001" "IN0"
        * OPC UA Client get node "ns=4;i=6005" "OUT0"
    """
    results = data_store.suite["opcUaClientController"].getNode(nodeId)
    assert results["result"] == 0, "Error getting node, check log"
    data_store.suite[keyName] = results["data"]["node"]
    Messages.write_message("Stored node in {} key".format(keyName))
###
# get browse name
###
@step("OPC UA Client get browse name <keyName>")
def opcUaClientGetBrowseName(keyName):
    """
    Get the node's browse based on given string from variable in data_store object.

    Args:
        keyName (string): Key name to save the variable as.

    Step and function definition::

        @step("OPC UA Client get browse name <keyName>")
        def opcUaClientGetBrowseName(keyName):

    Example usage:
        * OPC UA Client get browse name "IN0"
        * OPC UA Client get browse name "OUT0"
    """
    results = data_store.suite["opcUaClientController"].getBrowseName(data_store.suite[keyName])
    assert results["result"] == 0, "Error getting browse name, check log"
    Messages.write_message("Browse name: {}".format(results["data"]["name"]))
###
# get value
###
@step("OPC UA Client get value <keyName>")
def opcUaClientGetValue(keyName):
    """
    Get the node's value based on given string from variable in data_store object.

    Args:
        keyName (string): Key name to save the variable as.

    Step and function definition::

        @step("OPC UA Client get value <keyName>")
        def opcUaClientGetValue(keyName):

    Example usage:
        * OPC UA Client get value "IN0"
        * OPC UA Client get value "OUT0"
    """
    results = data_store.suite["opcUaClientController"].getValue(data_store.suite[keyName])
    assert results["result"] == 0, "Error getting value, check log"
    Messages.write_message("Value: {}".format(results["data"]["value"]))
###
# set value
###
@step("OPC UA Client set value <keyName> <value> <valueType>")
def opcUaClientSetValue(keyName, value, valueType):
    """
    Set the node's value based on given string from variable in data_store object and value.

    Args:
        keyName (string): Key name to save the variable as.
        value (str/bool/int/float): Value to send to node.
        valueType (string): Type that the value is (ie. str, float, int, bool).

    Step and function definition::

        @step("OPC UA Client set value <keyName> <value> <valueType>")
        def opcUaClientSetValue(keyName, value, valueType):

    Example usage:
        * OPC UA Client set value "IN0" "2.2" "float"
    """
    if valueType == "str":
        value = str(value)
    elif valueType == "int":
        value = int(value)
    elif valueType == "float":
        value = float(value)
    elif valueType == "bool":
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        else:
            value = bool(value)
    else:
        raise Exception("Type given is not supported, only bool, int, float, and str are supported")
    results = data_store.suite["opcUaClientController"].setValue(data_store.suite[keyName], value)
    assert results["result"] == 0, "Error setting value, check log"
    Messages.write_message("Set value to: {}".format(value))