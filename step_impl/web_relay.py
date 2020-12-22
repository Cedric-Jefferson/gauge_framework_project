##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   Web Relay Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``kmtronic_web_relay_library`` is used for this Step Implementation file. All Steps are in the ``web_relay.py`` file.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
import json
import os
import requests
import sys
import time
from getgauge.python import step, Messages, before_suite, data_store
sys.path.append(r"../kmtronic_web_relay_library")
from KMTronicWebRelayLibrary import WebRelayController

##########################################################################
# before suite setup
###
@before_suite
def beforeSuiteHook():
    """
    Uses the Dynamic Variable ``os.getenv("automation_index")`` to determine which Web Relay Controller classes to make and saves them to the related ``data_store.suite.``
    """
    print("automation index: {}".format(os.getenv("automation_index")))
    data_store.suite["addressMap"], data_store.suite["relayIndexLists"] = getRelayInfo(os.getenv("automation_index"))
    data_store.suite["webControllers"] = []
    for address in data_store.suite["addressMap"].keys():
        data_store.suite["webControllers"].append(WebRelayController(address))
    Messages.write_message("web relay before suite complete")

##########################################################################
# methods
###
# retrieve relay addresses and indices
# param automationIndex: index of the automation node
# return addressMap: Key is IP of relay controller, value is position in list of
#   relayIndexLists which that relay controller is responsible for
# return relayIndexLists: list of lists of relay indexes separated by controller responsibility
###
def getRelayInfo(automationIndex, timeout=15):
    # send request
    try:
        datas = json.dumps({"automation_index": automationIndex})
        response = requests.post(
            url="http://10.10.1.100:5000/api/v2/lookup-relay-info",
            data=datas
        )
        if response.status_code == 200:
            results = json.loads(response.text)
        else:
            Messages.write_message(response.text)
            Messages.write_message(response.request.body)
            assert False, "error returned from server"
    except:
        Messages.write_message(response.text)
        Messages.write_message(response.request.body)
        assert False, "error while sending request"
    Messages.write_message("Response data: {}".format(results["data"]))
    # organize data
    responseData = json.loads(results["data"])
    if len(responseData["addresses"]) == 0:
        assert False, "address list in response was empty"
    elif len(responseData["indices"]) == 0:
        assert False, "relay index list in response was empty"
    relayIndexLists = [None]*len(responseData["addresses"])
    addressMap = {}
    for i, (address, index) in enumerate(zip(responseData["addresses"], responseData["indices"])):
        if address in addressMap:
            relayIndexLists[addressMap[address]].append(index)
        else:
            addressMap[address] = i
            relayIndexLists[i] = [index]
    return addressMap, relayIndexLists
###
# set web relay step
###
@step("Set web relay <relayList>")
def setWebRelay(relayList):
    """
    Set the web relays set in the Before Suite Hook to the given list of values.

    Args:
        relayList (string): List of 8 relay values.

    Step and function definition::

        @step("Set web relay <relayList>")
        def setWebRelay(relayList):

    Example usage:
        * Set web relay "0,0,0,0,0,0,1,1"
    """
    for controller in data_store.suite["webControllers"]:
        relayList = list(relayList)
        results = controller.setRelays(relayList)
        Messages.write_message(results["description"])
        assert results["result"] == 0, "Set web relay failed"
###
# verify web relay status
###
@step("Verify web relay status <relayStatus>")
def verifyWebRelayStatus(relayStatus):
    """
    Verify the given status of the Web Relay Controller(s) at the ``os.getenv("automation_index")`` index.

    Args:
        relayStatus (int): Value to verify (0 for OFF or 1 for ON).

    Step and function definition::

        @step("Verify web relay status <relayStatus>")
        def verifyWebRelayStatus(relayStatus):

    Example usage:
        * Verify web relay status "0"
    """
    for controller in data_store.suite["webControllers"]:
        Messages.write_message("Verifying status of web relay at {}.".format(controller.ip))
        results = controller._getStatus()
        assert results["result"] == 0, "Get status failed"
        relayIndices = data_store.suite["relayIndexLists"][data_store.suite["addressMap"][controller.ip]]
        for relayIndex in relayIndices:
            assert relayStatus == controller.status[relayIndex], "Verify {} != Result {}".format(relayStatus, controller.status[relayIndex-1])
###
# set web relay power
###
@step("Set web relay power <relayToggle>")
def setWebRelayPower(relayToggle):
    """
    Set the power (ON or OFF) of the Web Relay Controller(s) at the ``os.getenv("automation_index")`` index.

    Args:
        relayToggle (int): Value to set (0 for OFF or 1 for ON).

    Step and function definition::

        @step("Set web relay power <relayToggle>")
        def setWebRelayPower(relayToggle):

    Example usage:
        * Set web relay power "0"
    """
    relayToggle = int(relayToggle)
    for controller in data_store.suite["webControllers"]:
        Messages.write_message("Setting power for web relay at {}.".format(controller.ip))
        relayIndices = data_store.suite["relayIndexLists"][data_store.suite["addressMap"][controller.ip]]
        for relayIndex in relayIndices:
            if (relayToggle == 0):
                results = controller.relayOn(relayIndex)
                assert results["result"] == 0, "Failed to turn on web relay at index {}".format(relayIndex)
            else:
                results = controller.relayOff(relayIndex)
                assert results["result"] == 0, "Failed to turn on web relay at index {}".format(relayIndex)
        Messages.write_message("Successfully toggled relay index/indices: {}.".format(relayIndices))
###
# factory flash set web relay
###
@step("Factory flash set web relay power <relayToggle>")
def factoryFlashSetWebRelayPower(relayToggle):
    """
    Set the power (ON or OFF) of the Web Relay Controller(s) at the ``os.getenv("automation_index")`` index if the variable ``data_store.scenario["factoryFlashRestart"]`` is True. This is used on the MUX when the DUT is bricked.

    Args:
        relayToggle (int): Value to set (0 for OFF or 1 for ON).

    Step and function definition::

        @step("Factory flash set web relay power <relayToggle>")
        def factoryFlashSetWebRelayPower(relayToggle):

    Example usage:
        * Factory flash set web relay power "0"
    """
    relayToggle = int(relayToggle)
    if data_store.scenario["factoryFlashRestart"]:
        for controller in data_store.suite["webControllers"]:
            Messages.write_message("Setting power (factory flash) for web relay at {}.".format(controller.ip))
            relayIndices = data_store.suite["relayIndexLists"][data_store.suite["addressMap"][controller.ip]]
            for relayIndex in relayIndices:
                if (relayToggle == 0):
                    results = controller.relayOn(relayIndex)
                    assert results["result"] == 0, "Failed to turn on web relay at index {}".format(relayIndex)
                else:
                    results = controller.relayOff(relayIndex)
                    assert results["result"] == 0, "Failed to turn on web relay at index {}".format(relayIndex)
            Messages.write_message("Successfully toggled relay index/indices: {}.".format(relayIndices))
    else:
        Messages.write_message("Don't need restart")
###
# reset trace32 device
###
@step("Reset trace32 device")
def resetTrace32Device():
    """
    Used on the Automation Lab only. This will cycle the power on the Lauterbach and the DUT.

    Step and function definition::

        @step("Reset trace32 device")
        def resetTrace32Device():

    Example usage:
        * Reset trace32 device
    """
    if os.getenv("automation_index") == "99":
        for controller in data_store.suite["webControllers"]:
            results = controller.relayOff(4)
            Messages.write_message(results["description"])
            time.sleep(5)
            results = controller.relayOn(4)
            Messages.write_message(results["description"])
            time.sleep(10)
            assert True
