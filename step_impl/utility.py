##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   Automation Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
No Automation Libraries are used in this Step Implementation file. All Steps are in the utility.py file. This file is for general utilities that might be needed during a test.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, after_suite, before_suite
import os
import requests
import time
import json
import sys
import subprocess
from opcua import Client
from opcua import ua

##########################################################################
# before suite setup
###
@before_suite
def beforeSuite():
    """
    Sets the ``data_store.suite["reservedList"]`` to an empty list.
    """
    data_store.suite["reservedList"] = []
    Messages.write_message("utility before suite complete")

##########################################################################
# steps
###
###
# wait step
###
@step("Wait <timeout>")
def wait(timeout):
    """
    Wait for given time in seconds

    Args:
        timeout (int): Time in seconds.

    Step and function definition::

        @step("Wait <timeout>")
        def wait(timeout):

    Example usage:
        * Wait "10"
    """
    time.sleep(float(timeout))
    assert True
###
# ping step
###
@step("Ping <ipAddr>")
def ping(ipAddr):
    """
    Ping the given IP Address 4 tries.

    Args:
        ipAddr (string): IP address.

    Step and function definition::

        @step("Ping <ipAddr>")
        def ping(ipAddr):

    Example usage:
        * Ping "192.168.1.12"
    """
    assert len(ipAddr.split(".")) == 4, "IP address not proper"
    command = ["ping", "-c", "4", ipAddr]
    result = subprocess.run(args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    Messages.write_message("{}".format(result.stdout.decode("utf-8")))
    Messages.write_message("{}".format(result.stderr.decode("utf-8")))
    assert result.returncode == 0, "Ping failed"
###
# send shell command
###
@step("Send shell command <cmd> <check>")
def sendShellCommand(cmd, check):
    """
    Send the given shell command and check returncode or ignore it.

    Args:
        cmd (string): Command to execute.
        check (bool): True will check returncode.

    Step and function definition::

        @step("Send shell command <cmd> <check>")
        def sendShellCommand(cmd, check):

    Example usage:
        * Send shell command "ls -la" "False"
        * Send shell command "echo 404 > /sys/class/gpio/export" "False"
    """
    if check.lower() == "true":
        check = True
    else:
        check = False
    try:
        process = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check, shell=True)
    except subprocess.CalledProcessError:
        assert False, "call retruned non-zero"
    except Exception as exc:
        assert False, "error during call {}".format(exc)
    Messages.write_message(process)
###
# force fail
###
@step("Force fail")
def forceFail():
    """
    Force the Gauge Step to fail.

    Step and function definition::

        @step("Force fail")
        def forceFail():

    Example usage:
        * Force fail
    """
    assert False, "Force failure"
###
# force pass
###
@step("Force pass")
def forcePass():
    """
    Force the Gauge Step to pass.

    Step and function definition::

        @step("Force pass")
        def forcePass():

    Example usage:
        * Force pass
    """
    assert True
###
# reserve tool
###
@step("Reserve <toolname>")
def reserve(toolname, timeout=300):
    """
    Reserve a specific tool from the tool resources on a timeout of 300 seconds.

    Args:
        toolname (string): Tool name to reserve.
        timeout (int, optional): Timeout. Defaults to 300.

    Step and function definition::

        @step("Reserve <toolname>")
        def reserve(toolname, timeout=300):

    Example usage:
        * Reserve "profinet1"
    """
    if not toolname in data_store.suite["reservedList"]:  
        results = {}
        results["result"] = 1
        timeout = time.time() + timeout
        vlanId = int(os.getenv("vlan_id"))
        nodename = os.getenv("nodename")
        datas = json.dumps({"node": nodename, "toolname": toolname})
        while (timeout > time.time()) and (results["result"] == 1):
            try:
                response = requests.post(
                    url="http://10.10.1.100:5000/api/v2/reserve",
                    params={"vlan_id": vlanId},
                    data=datas
                )
                if response.status_code == 200:
                    results = response.json()
                else:
                    Messages.write_message(response.text)
                    Messages.write_message(response.request.body)
                    assert False, "error returned from server"
            except:
                Messages.write_message(response.text)
                Messages.write_message(response.request.body)
                assert False, "error while sending request"
            time.sleep(15)
        Messages.write_message(results)
        assert results["result"] == 0, "was unable to reserve within timeout period"
        data_store.suite["reservedList"].append(toolname)
    else:
        Messages.write_message("tool is already reserved")
###
# unreserve
###
@step("Unreserve <toolname>")
def unreserve(toolname):
    """
    Unreserve a specific tool from the current node.

    Args:
        toolname (string): Tool name to unreserve.

    Step and function definition::

        @step("Unreserve <toolname>")
        def unreserve(toolname):

    Example usage:
        * Unreserve "profinet1"
    """
    nodename = os.getenv("nodename")
    datas = json.dumps({"node": nodename, "toolname": toolname})
    try:
        response = requests.post(
            url="http://10.10.1.100:5000/api/v2/unreserve",
            data=datas
        )
        if response.status_code == 200:
            results = response.json()
        else:
            Messages.write_message(response.text)
            Messages.write_message(response.request.body)
            assert False, "error returned from server"
    except:
        Messages.write_message(response.text)
        Messages.write_message(response.request.body)
        assert False, "error while sending request"
    Messages.write_message(results)
    assert results["result"] == 0, "was unable to unreserve"
    data_store.suite["reservedList"].remove(toolname)
###
# get config crc
###
@step("Get config crc <configFilename>")
def getConfigCRC(configFilename):
    """
    Request the CRC from the specific configuration file, located in the ``configurations`` repo.

    Args:
        configFilename (string): Config filename.

    Step and function definition::

        @step("Get config crc <configFilename>")
        def getConfigCRC(configFilename):

    Example usage:
        * Get config crc "f-host_port-25.bin"
    """
    datas = json.dumps({"filename": configFilename})
    try:
        response = requests.post(
            url="http://10.10.1.100:5000/api/v2/lookup/config-crc",
            data=datas
        )
        if response.status_code == 200:
            results = response.json()
            data_store.suite["configCRC"] = results["data"]["crc"]
        else:
            Messages.write_message(response.text)
            Messages.write_message(response.request.body)
            assert False, "error returned from server"
    except:
        Messages.write_message(response.text)
        Messages.write_message(response.request.body)
        assert False, "error while sending request"
    Messages.write_message(results)
    assert results["result"] == 0, "was unable to get crc from {} file".format(configFilename)
###
# load config
###
@step("Load config <configFilename>")
def loadConfig(configFilename):
    """
    Load the configuration file path into ``data_store.suite["configFile"]`` variable.

    Args:
        configFilename (string): Config filename.

    Step and function definition::

        @step("Load config <configFilename>")
        def loadConfig(configFilename):

    Example usage:
        * Load config "f-host_port-25.bin"
    """    
    configFilepath = os.getenv("config_filepath")
    Messages.write_message(configFilepath)
    Messages.write_message(configFilename)
    data_store.suite["configFile"] = configFilepath + configFilename
    assert os.path.exists(data_store.suite["configFile"]), "config file does not exist"
###
# lookup tool
###
@step("Lookup protocol standard <standardProtocol> safe <safeProtocol>")
def lookupProtocol(standardProtocol, safeProtocol):
    """
    Lookup a specific tool name from the tool resources pool based on standard and safe protocol. Leaving one protocol empty will then only search based on the one specified. The result will be stored in the ``data_store.suite["lookupToolname"]`` variable to be used in Reserve Lookup Tool.

    Args:
        standardProtocol (string): Standard protocol to search for.
        safeProtocol (string): Safe protocol to search for.

    Step and function definition::

        @step("Lookup protocol standard <standardProtocol> safe <safeProtocol>")
        def lookupProtocol(standardProtocol, safeProtocol):

    Example usage:
        * Lookup protocol standard "profinet" safe ""
        * Lookup protocol standard "profinet" safe "profisafe"
        * Lookup protocol standard "ethernetip" safe ""

    """
    if safeProtocol == "":
        datas = json.dumps({"standard": standardProtocol})
    else:
        datas = json.dumps({"standard": standardProtocol, "safe": safeProtocol})
    try:
        response = requests.post(
            url="http://10.10.1.100:5000/api/v2/lookup",
            data=datas
        )
        if response.status_code == 200:
            results = response.json()
            data_store.suite["lookupPort"] = results["data"]["port"]
            data_store.suite["lookupToolname"] = results["data"]["toolname"]
        else:
            Messages.write_message(response.text)
            Messages.write_message(response.request.body)
            assert False, "error returned from server"
    except:
        Messages.write_message(response.text)
        Messages.write_message(response.request.body)
        assert False, "error while sending request"
    Messages.write_message(results)
    assert results["result"] == 0, "was unable to get a return for the lookup with data: {}".format(datas)
###
# reserve lookup
###
@step("Reserve lookup tool")
def reserveLookupTool(timeout=300):
    """
    Try to reserve the tool name from Lookup Protocol on a timeout of 300 seconds.

    Args:
        timeout (int, optional): Timeout value. Defaults to 300.

    Step and function definition::

        @step("Reserve lookup tool")
        def reserveLookupTool(timeout=300):

    Example usage:
        * Reserve lookup tool
    """
    if not data_store.suite["lookupToolname"] in data_store.suite["reservedList"]:  
        results = {}
        results["result"] = 1
        timeout = time.time() + timeout
        vlanId = int(os.getenv("vlan_id"))
        nodename = os.getenv("nodename")
        datas = json.dumps({"node": nodename, "toolname": data_store.suite["lookupToolname"]})
        while (timeout > time.time()) and (results["result"] == 1):
            try:
                response = requests.post(
                    url="http://10.10.1.100:5000/api/v2/reserve",
                    params={"vlan_id": vlanId},
                    data=datas
                )
                if response.status_code == 200:
                    results = response.json()
                else:
                    Messages.write_message(response.text)
                    Messages.write_message(response.request.body)
                    assert False, "error returned from server"
            except:
                Messages.write_message(response.text)
                Messages.write_message(response.request.body)
                assert False, "error while sending request"
            time.sleep(15)
        Messages.write_message(results)
        assert results["result"] == 0, "was unable to reserve within timeout period"
        data_store.suite["reservedList"].append(data_store.suite["lookupToolname"])
    else:
        Messages.write_message("tool is already reserved")
###
# unreserve lookup tool
###
@step("Unreserve lookup tool")
def unreserveLookupTool():
    """
    Try to unreserve the tool name from Lookup Protocol on a timeout of 300 seconds.

    Step and function definition::

        @step("Unreserve lookup tool")
        def unreserveLookupTool():

    Example usage:
        * Unreserve lookup tool
    """
    nodename = os.getenv("nodename")
    datas = json.dumps({"node": nodename, "toolname": data_store.suite["lookupToolname"]})
    try:
        response = requests.post(
            url="http://10.10.1.100:5000/api/v2/unreserve",
            data=datas
        )
        if response.status_code == 200:
            results = response.json()
        else:
            Messages.write_message(response.text)
            Messages.write_message(response.request.body)
            assert False, "error returned from server"
    except:
        Messages.write_message(response.text)
        Messages.write_message(response.request.body)
        assert False, "error while sending request"
    Messages.write_message(results)
    assert results["result"] == 0, "was unable to unreserve"
    data_store.suite["reservedList"].remove(data_store.suite["lookupToolname"])
###
# config lookup tool
###
@step("Config lookup tool <hardware>")
def configLookuptool(hardware):
    """
    Get the default configuration filename for the specific tool name that was returned from Lookup Protocol.

    Args:
        hardware (string): Hardware to look up config for (ie. f-host, osprey).

    Step and function definition::

        @step("Config lookup tool <hardware>")
        def configLookuptool(hardware):

    Example usage:
        * Config lookup tool "f-host"
    """
    filename = "{}_port-{}.bin".format(hardware, data_store.suite["lookupPort"])
    getConfigCRC(filename)
    loadConfig(filename)
###
# execute windows subsystems
###
@step("Startup windows subsystems")
def startupWindowsSubsystems():
    """
    Start the Windows executables in the windows_subsystem_list environment variable. This variable is created in Jenkins based on the product definition.

    Step and function definition::

        @step("Startup windows subsystems")
        def startupWindowsSubsystems():

    Example usage:
        * Startup windows subsystems
    """
    subsystemJson = json.loads(os.getenv("windows_subsystem_list"))
    Messages.write_message("Subsystem list: {}".format(subsystemJson))
    for key in subsystemJson:
        filepath = os.path.join(os.getenv("workspace_path").strip(), subsystemJson[key])
        Messages.write_message("Filepath: {}".format(filepath))
        data_store.suite[key] = subprocess.Popen(filepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
###
# stop windows subsystems
###
@step("Stop windows subsystems")
def stopWindowsSubsystems():
    """
    Stop the Windows executables in the windows_subsystem_list environment variable. This variable is created in Jenkins based on the product definition.

    Step and function definition::

        @step("Stop windows subsystems")
        def stopWindowsSubsystems():

    Example usage:
        * Stop windows subsystems
    """
    subsystemJson = json.loads(os.getenv("windows_subsystem_list"))
    for key in subsystemJson:
        data_store.suite[key].kill()

##########################################################################
# after suite setup
###
@after_suite
def afterSuite():
    """
    If the ``data_store.suite["reservedList"]`` has items in it this Hook will unreserve them.
    """
    for toolname in data_store.suite["reservedList"]:
        unreserve(toolname)
    Messages.write_message("utility after suite complete")
