##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   Numato Ethernet Relay Automation Tests in Gauge Framework
#
##########################################################################
"""
The ``numato_ethernet_relay_library`` is used for this Step Implementation file. All Steps are in the ``numato_ethernet_relay.py`` file.
Go to the Concepts to see any concepts that simplify the steps.

Below are a list of implemented Steps:
"""

##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, before_suite
import os
import sys
sys.path.append(r"../numato_ethernet_relay_library")
try:
    from NumatoEthernetRelayLibrary import NumatoEthernetRelayController
except Exception as exc:
    print("import numato_ethernet_relay:: {} occured: {}".format(type(exc).__name__, exc))

##########################################################################
# before suite
###
@before_suite
def beforeSuiteHook():
    """
    Initializes variables:
        * ``data_store.suite["numatoEthernetRelayConnected"]`` is set to ``{}`` so that no Step can be run unless the PyLogix Controller class is created
        * ``data_store.suite["numatoEthernetRelayController"]`` is set to ``{}`` so that no Step can be run unless the PyLogix Controller class is created
    """
    data_store.suite["numatoEthernetRelayConnected"] = {}
    data_store.suite["numatoEthernetRelayController"] = {}

##########################################################################
# methods
###
# connect
###
@step("Numato eth relay connect to <name> at <host>")
def numatoEthernetRelayConnect(name, host):
    """
    Create the PyLogix Contoller class using the ``data_store.suite["numatoEthernetRelayController"]`` variable with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.
        host (string): IP address of the relay to connect to.

    Step and function definition::

        @step("Numato eth relay connect to <name> at <host>")
        def numatoEthernetRelayConnect(name, host):

    Example usage:
        * Numato eth relay connect to "relay-1" at "192.168.1.201"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        if data_store.suite["numatoEthernetRelayConnected"][name]:
            Messages.write_message("NAB Agent object already connected")
    try:
        data_store.suite["numatoEthernetRelayController"][name] = NumatoEthernetRelayController(ip=host)
        data_store.suite["numatoEthernetRelayConnected"][name] = True
    except:
        Messages.write_message("Error creating Numato Ethernet Relay object")
        assert False
###
# version
###
@step("Numato eth relay version at <name>")
def numatoEthernetRelayVersion(name):
    """
    Get the firmware version from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.

    Step and function definition::

        @step("Numato eth relay version at <name>")
        def numatoEthernetRelayVersion(name):

    Example usage:
        * Numato eth relay version at "relay-1"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].ver()
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
###
# reset
###
@step("Numato eth relay reset at <name>")
def numatoEthernetRelayReset(name):
    """
    Reset all relays to default state from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.

    Step and function definition::

        @step("Numato eth relay reset at <name>")
        def numatoEthernetRelayReset(name):

    Example usage:
        * Numato eth relay reset at "relay-1"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].reset()
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
###
# read
###
@step("Numato eth relay read at <name> with <index>")
def numatoEthernetRelayRead(name, index):
    """
    Read the state of the relay at the given ``index`` from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.
        index (int): Index of the relay.

    Step and function definition::

        @step("Numato eth relay read at <name> with <index>")
        def numatoEthernetRelayRead(name, index):

    Example usage:
        * Numato eth relay read at "relay-1" with "0"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].relayRead(int(index))
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
###
# read all
###
@step("Numato eth relay read all at <name>")
def numatoEthernetRelayReadAll(name):
    """
    Read all states from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.

    Step and function definition::

        @step("Numato eth relay read all at <name>")
        def numatoEthernetRelayReadAll(name):

    Example usage:
        * Numato eth relay read all at "relay-1"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].relayReadAll()
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
###
# relay on
###
@step("Numato eth relay on at <name> with <index>")
def numatoEthernetRelayOn(name, index):
    """
    Set the state high of the relay at the given ``index`` from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.
        index (int): Index of the relay.

    Step and function definition::

        @step("Numato eth relay on at <name> with <index>")
        def numatoEthernetRelayOn(name, index):

    Example usage:
        * Numato eth relay on at "relay-1" with "0"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].relayOn(int(index))
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
###
# relay off
###
@step("Numato eth relay off at <name> with <index>")
def numatoEthernetRelayOff(name, index):
    """
    Set the state low of the relay at the given ``index`` from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.
        index (int): Index of the relay.

    Step and function definition::

        @step("Numato eth relay off at <name> with <index>")
        def numatoEthernetRelayOff(name, index):

    Example usage:
        * Numato eth relay off at "relay-1" with "0"
    """
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].relayOff(int(index))
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
###
# write all
###
@step("Numato eth relay write all at <name> with <indexList>")
def numatoEthernetRelayWriteAll(name, indexList):
    """
    Set the states of the corresponding relays  from the relay with the given ``name`` key.

    Args:
        name (string): The key used to differentiate the object.
        indexList (list): List of 0 and 1 corresponding to relay state to set.

    Step and function definition::

        @step("Numato eth relay write all at <name> with <indexList>")
        def numatoEthernetRelayWriteAll(name, indexList):

    Example usage:
        * Numato eth relay write all at "relay-1" with "1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0"
    """
    indexList = [int(i) for i in indexList.split(",")]
    assert len(indexList) == 16, "Relay list is not of length 16"
    if name in data_store.suite["numatoEthernetRelayConnected"]:
        assert data_store.suite["numatoEthernetRelayConnected"][name] == True, "Numato web relay is not connected"
    else:
        assert False, "Numato web relay with name ({}) does not exist".format(name)
    results = data_store.suite["numatoEthernetRelayController"][name].relayWriteAll(indexList)
    Messages.write_message(results)
    assert results["result"] == 0, "Error getting results"
