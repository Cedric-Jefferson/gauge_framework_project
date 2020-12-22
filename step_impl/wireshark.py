##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   Wireshark Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``wireshark_library`` is used for this Step Implementation file. All Steps are in the ``wireshark.py`` file.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, after_scenario, before_suite
import time
import os
import sys
sys.path.append(r"../wireshark_library")
from WiresharkLibrary import WiresharkController

##########################################################################
# before suite
###
@before_suite
def beforeSuiteHook():
    """
    Initializes boolean variables for CAPI features:
        * ``data_store.suite["wiresharkCount"]`` is set to 0 for the numbering of the wireshark caputures in the After Scenario Hook
    """
    data_store.suite["wiresharkCount"] = 0

##########################################################################
# methods
###
# wireshark start
###
@step("Wireshark start")
def wiresharkStart():
    """
    Starts the wireshark capture by creating the Wireshark Controller class using ``data_store.scenario["wiresharkController"]`` variable.

    Step and function definition::

        @step("Wireshark start")
        def wiresharkStart():

    Example usage:
        * Wireshark start
    """
    data_store.scenario["wiresharkController"] = WiresharkController(os.getenv("wireshark_interface"))
    Messages.write_message("Wireshark started")
    data_store.scenario["wiresharkEnabled"] = True
    time.sleep(2) # let tshark start
###
# wireshark stop
###
@step("Wireshark stop")
def wiresharkStop():
    """
    Stops the wireshark capture.

    Step and function definition::

        @step("Wireshark stop")
        def wiresharkStop():

    Example usage:
        * Wireshark stop
    """
    results = data_store.scenario["wiresharkController"].stopProcess()
    Messages.write_message(results["description"])
    data_store.scenario["wiresharkEnabled"] = False
###
# wireshark generate json
###
@step("Wireshark generate json <filename>")
def wiresharkGenerateJson(filename):
    """
    Generates the given filename in JSON form from the Wireshark capture file.

    Args:
        filename (string): File name to save.

    Step and function definition::

        @step("Wireshark stop")
        def wiresharkStop():

    Example usage:
        *  Wireshark generate json "./wireshark.cap"
    """
    Messages.write_message("Using cap filename: {}".format(filename))
    Messages.write_message("Working in dir: {}".format(os.getcwd()))
    assert os.path.exists(filename), "wireshark capture file does not exist"
    results = data_store.scenario["wiresharkController"].generateJson(filename)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "wireshark generate json failed"
###
# arp count
###
@step("Wireshark arp count <count> <srcAddr> <dstAddr>")
def wiresharkArpCount(count, srcAddr, dstAddr):
    """
    Counts the ARPs in the Wireshark capture given source and destination IP Addresses.

    Args:
        count (int): ARP count to verify.
        srcAddr (string): Source IP address.
        dstAddr (string): Destination IP address.

    Step and function definition::

        @step("Wireshark arp count <count> <srcAddr> <dstAddr>")
        def wiresharkArpCount(count, srcAddr, dstAddr):

    Example usage:
        * Wireshark arp count "10" "192.168.1.10" "192.168.1.12"
    """
    ip = list(map(int, srcAddr.split(".")))
    assert len(ip) == 4, "src IP address format is wrong"
    ip = list(map(int, dstAddr.split(".")))
    assert len(ip) == 4, "dst IP address format is wrong"
    count = int(count)
    results = data_store.scenario["wiresharkController"].arpCount(srcAddr, dstAddr, data_store.scenario["arpStartTime"])
    Messages.write_message(results["description"])
    assert results["result"] == 0, "wireshark arp count failed"
    Messages.write_message("ARPs counted: {}".format(results["data"]["arpCount"]))
    assert (results["data"]["arpCount"] == count) or (results["data"]["arpCount"] == (count + 1)), "ARPs counted: {}, ARPs requested: {}".format(results["data"]["arpCount"], count)

##########################################################################
# after scenario
###
@after_scenario
def afterScenarioHook():
    """
    If the Wireshark Controller class was enabled then the process will be stoped and saved to a file after each Scenario.
    """
    if "wiresharkEnabled" in data_store.scenario:
        if data_store.scenario["wiresharkEnabled"]:
            results = data_store.scenario["wiresharkController"].stopProcess()
            Messages.write_message(results["description"])
            Messages.write_message("wireshark after scenario complete")
        else:
            Messages.write_message("wireshark already stopped")
        if os.path.exists("wireshark.cap"):
            newFilename = "wireshark_{}.cap".format(data_store.suite["wiresharkCount"])
            data_store.suite["wiresharkCount"] += 1
            os.rename("wireshark.cap", newFilename)