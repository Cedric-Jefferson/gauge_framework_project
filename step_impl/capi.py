##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   CAPI Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The capi_library is used for this Step Implementation file. All Steps are in the ``capi.py`` file.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, after_scenario, before_scenario
import time
import os
import sys
import struct
sys.path.append(r"../capi_library")
try:
    from CAPILibrary import CAPIController
except Exception as exc:
    print("import capi:: {} occured: {}".format(type(exc).__name__, exc))

##########################################################################
# constants
###
CMTP_BUFFER_LEN = 1024

##########################################################################
# before scenario setup
###
@before_scenario
def beforeScenarioHook():
    """
    Initializes boolean variables for CAPI features:
        * data_store.scenario["capiController"] is set to None so the CAPIController class contructor can be called again
        * data_store.scenario["init"] is set to know to call Exit in the After Scenario if it wasn't called
        * data_store.scenario["openInterface"] is set to know to call Close Interface in the After Scenario if it wasn't called
        * data_store.scenario["startProtocol"] is set to know to call Stop Protocol in the After Scenario if it wasn't called
        * data_store.scenario["safeInit"] is set to know to call Safe Exit in the After Scenario if it wasn't called
        * data_store.scenario["safeOpenInterface"] is set to know to call Safe Close Interface in the After Scenario if it wasn't called
        * data_store.scenario["safeEnabled"] is set to know to call Safe Disabled in the After Scenario if it wasn't called
        * data_store.scenario["pingOpen"] is set to know to call Ping Close in the After Scenario if it wasn't called
        * data_store.scenario["arpRegistered"] is set to know to call ARP Unregister in the After Scenario if it wasn't called
    """
    data_store.scenario["capiController"] = None
    data_store.scenario["init"] = False
    data_store.scenario["openInterface"] = False
    data_store.scenario["startProtocol"] = False
    data_store.scenario["safeInit"] = False
    data_store.scenario["safeOpenInterface"] = False
    data_store.scenario["safeEnabled"] = False
    data_store.scenario["pingOpen"] = False
    data_store.scenario["arpRegistered"] = False
    Messages.write_message("capi before scenario completed")

##########################################################################
# standard card methods
###
# init step
###
@step("Init")
def init():
    """
    Call CAPI Init method.

    Step and function definition::

        @step("Init")
        def init():

    Example usage:
        * Init
    """
    data_store.scenario["capiController"] = CAPIController()
    results = data_store.scenario["capiController"].init()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Init failed"
    data_store.scenario["init"] = True
###
# enum drivers
###
@step("Enum drivers <index>")
def enumDrivers(index):
    """
    Call CAPI Enum Drivers method.

    Args:
        index (int): Card index.

    Step and function definition::

        @step("Enum drivers <index>")
        def enumDrivers(index):

    Example usage:
        * Enum drivers "0"
    """
    results = data_store.scenario["capiController"].enumDrivers(int(index))
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Enum drivers failed"
###
# open interface at index
###
@step("Open interface <index>")
def openInterface(index):
    """
    Call CAPI Open Interface method.

    Args:
        index (int): Card index.

    Step and function definition::

        @step("Open interface <index>")
        def openInterface(index):

    Example usage:
        * Open interface "0"
    """
    results = data_store.scenario["capiController"].openInterface(int(index))
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Open interface failed"
    data_store.scenario["openInterface"] = True
###
# get card info
###
@step("Get card info")
def getCardInfo():
    """
    Call CAPI Get Card Info method. This method will store results in:
        * data_store.scenario["productName"] stores the name of the product
        * data_store.scenario["ipAddr"] stores the ip address
        * data_store.scenario["firmwareVersion"] stores the firmware version

    Step and function definition::

        @step("Get card info")
        def getCardInfo():

    Example usage:
        * Get card info
    """
    results = data_store.scenario["capiController"].getCardInfo()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get card info failed"
    data_store.scenario["productName"] = str(results["data"]["productName"])
    Messages.write_message("Product name: {}".format(data_store.scenario["productName"]))
    data_store.scenario["ipAddr"] = str(results["data"]["ipAddr"])
    Messages.write_message("IP addr: {}".format(data_store.scenario["ipAddr"]))
    data_store.scenario["firmwareVersion"] = str(results["data"]["firmwareVersion"])
    Messages.write_message("Firmware version: {}".format(data_store.scenario["firmwareVersion"]))
###
# soft reset
###
@step("Soft reset device")
def softResetDevice():
    """
    Calls CAPI method to soft reset the DUT device.

    Step and function definition::

        @step("Soft reset device")
        def softResetDevice():

    Example usage:
        * Soft reset device
    """
    results = data_store.scenario["capiController"].softReset()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Soft reset failed"
###
# start standard connections
###
@step("Start standard connections <index>")
def startStandardConnection(index):
    """
    This method runs: refresh IO, start all connections, start produced and start consumed threads on the given index.

    Args:
        index (int): Field bus module index.

    Step and function definition::

        @step("Start standard connections <index>")
        def startStandardConnection(index):

    Example usage:
        * Start standard connections "0"
    """
    results = data_store.scenario["capiController"].refreshIO()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Refresh io failed"
    results = data_store.scenario["capiController"].startAllConnections()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Start all connections failed"
    data_store.scenario["capiController"].startProduce(int(index))
    assert data_store.scenario["capiController"].produceFunctionStop == False
    data_store.scenario["capiController"].startConsume(int(index))
    assert data_store.scenario["capiController"].consumeFunctionStop == False
    time.sleep(data_store.scenario["capiController"].consumeFunctionDuty)
###
# start protocol
###
@step("Start protocol")
def startProtocol():
    """
    Calls the CAPI Start Protocol method.

    Step and function definition::

        @step("Start protocol")
        def startProtocol():

    Example usage:
        * Start protocol
    """
    results = data_store.scenario["capiController"].startProtocol()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Start protocol failed"
    data_store.scenario["startProtocol"] = False
###
# stop protocol
###
@step("Stop protocol")
def stopProtocol():
    """
    Calls the CAPI Stop Protocol method.

    Step and function definition::

        @step("Stop protocol")
        def stopProtocol():

    Example usage:
        * Stop protocol
    """
    results = data_store.scenario["capiController"].stopProtocol()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Stop protocol failed"
###
# get connection info
###
@step("Get connection info")
def getConnectionInfo():
    """
    Calls the CAPI Get Connection Info method and stores the values in the following variables:
        * ``data_store.scenario["numConnections"]`` the total number of connections
        * ``data_store.scenario["numActConnections"]`` the number of connections that are active

    Step and function definition::

        @step("Get connection info")
        def getConnectionInfo():

    Example usage:
        * Get connection info
    """
    results = data_store.scenario["capiController"].getConnectionInfo()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get connection info failed"
    data_store.scenario["numConnections"] = results["data"]["numConnections"]
    Messages.write_message("Number of connections: {}".format(data_store.scenario["numConnections"]))
    data_store.scenario["numActConnections"] = results["data"]["numActConnections"]
    Messages.write_message("Active connections: {}".format(data_store.scenario["numActConnections"]))
###
# get state
###
@step("Get state")
def getState():
    """
    Calls the CAPI Read Sate method and prints the following information:
        * State of CAPI
        * IO State of the standard connections
        * Ch1 State of Safe CAPI
        * Ch2 State of Safe CAPI
        * Ch1 IO State of the safe connections
        * Ch2 IO State of the safe connections

    Step and function definition::

        @step("Get state")
        def getState():

    Example usage:
        * Get state
    """
    results = data_store.scenario["capiController"].readState()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get state info failed"
    Messages.write_message("State: {}".format(results["data"]["state"]))
    Messages.write_message("IO State: {}".format(results["data"]["ioState"]))
    Messages.write_message("Ch1 State: {}".format(results["data"]["ch1State"]))
    Messages.write_message("Ch2 State: {}".format(results["data"]["ch2State"]))
    Messages.write_message("Ch1 IO State: {}".format(results["data"]["ch1IOState"]))
    Messages.write_message("Ch2 IO State: {}".format(results["data"]["ch2IOState"]))
###
# read io
###
@step("Read IO")
def readIO():
    """
    Calls the CAPI Read IO method and stores the values in the following variables:
        * ``data_store.scenario["producedIO"]`` value of the produced IO from the opened connection
        * ``data_store.scenario["consumedIO"]`` value of the consumed IO from the opened connection

    Step and function definition::

        @step("Read IO")
        def readIO():

    Example usage:
        * Read IO
    """
    results = data_store.scenario["capiController"].readIO()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Read io failed"
    data_store.scenario["producedIO"] = results["data"]["produced"]
    Messages.write_message("Produced: {}".format(data_store.scenario["producedIO"]))
    data_store.scenario["consumedIO"] = results["data"]["consumed"]
    Messages.write_message("Consumed: {}".format(data_store.scenario["consumedIO"]))
###
# write io
###
@step("Write IO <value>")
def writeIO(value):
    """
    Calls the CAPI Write IO method and sets the produced data to the value given.

    Args:
        value (int): Value to set IO.

    Step and function definition::

        @step("Write IO <value>")
        def writeIO(value):

    Example usage:
        * Write IO "1"
    """
    newProduceData = list(data_store.scenario["producedIO"])
    newProduceData[0] = int(value)
    newProduceData = tuple(newProduceData)
    results = data_store.scenario["capiController"].writeProducedIO(newProduceData)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Write io failed"
    Messages.write_message("Write: {}".format(newProduceData))
    time.sleep(data_store.scenario["capiController"].produceFunctionDuty)
###
# start all connections
###
@step("Start all connections")
def startAllConnections():
    """
    Calls the CAPI Start All Connections method. This will set the header data of all IO found in Refresh IO.

    Step and function definition::

        @step("Start all connections")
        def startAllConnections():

    Example usage:
        * Start all connections
    """
    results = data_store.scenario["capiController"].startAllConnections()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Start all connections failed"
###
# refresh io
###
@step("Refresh IO")
def refreshIO():
    """
    Calls the CAPI Refresh IO method.

    Step and function definition::

        @step("Refresh IO")
        def refreshIO():

    Example usage:
        * Refresh IO
    """
    results = data_store.scenario["capiController"].refreshIO()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Refresh io failed"
###
# ping open
###
@step("Ping open <ip> <interval> <length>")
def pingOpen(ip, interval, length):
    """
    Calls the CAPI Ping Open method with the given IP Address, Interval, and Data Length.

    Args:
        ip (string): IP of target.
        interval (int): Time between ping (0 is default).
        length (int): Length of data sent (0 is default).

    Step and function definition::

        @step("Ping open <ip> <interval> <length>")
        def pingOpen(ip, interval, length):

    Example usage:
        * Ping open "192.168.1.12" "0" "0"
        * Ping open "192.168.1.12" "5" "1024"
    """
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address format is wrong"
    interval = int(interval)
    length = int(length)
    if interval == 0:
        interval = 15
    if length == 0:
        length = 10
    results = data_store.scenario["capiController"].pingOpen(ip, interval, length)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Ping open failed"
    data_store.scenario["pingOpen"] = True
###
# ping close
###
@step("Ping close")
def pingClose():
    """
    Calls the CAPI Ping Close method.

    Step and function definition::

        @step("Ping close")
        def pingClose():

    Example usage:
        * Ping close
    """
    results = data_store.scenario["capiController"].pingClose()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Ping close failed"
    data_store.scenario["pingOpen"] = False
###
# get ping stats
###
@step("Get ping stats")
def getPingStats():
    """
    Calls the CAPI Ping Get Stats method and stores the results in the following variables:
        * ``data_store.scenario["transmitted"]``
        * ``data_store.scenario["received"]``
        * ``data_store.scenario["duplicated"]``
        * ``data_store.scenario["lastRTT"]``
        * ``data_store.scenario["maxRTT"]``
        * ``data_store.scenario["minRTT"]``
        * ``data_store.scenario["avrRTT"]``
        * ``data_store.scenario["sumRTT"]``
        * ``data_store.scenario["sendErrorCode"]``
        * ``data_store.scenario["recvErrorCode"]``

    Step and function definition::

        @step("Get ping stats")
        def getPingStats():

    Example usage:
        * Get ping stats
    """
    results = data_store.scenario["capiController"].pingGetStats()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get ping stats failed"
    if results["data"] != "":
        data_store.scenario["transmitted"] = str(results["data"]["transmitted"])
        Messages.write_message("Number of transmitted PING requests: {}".format(data_store.scenario["transmitted"]))
        data_store.scenario["received"] = str(results["data"]["received"])
        Messages.write_message("Number of received PING reply packets: {}".format(data_store.scenario["received"]))
        data_store.scenario["duplicated"] = str(results["data"]["duplicated"])
        Messages.write_message("Number of duplicated PING reply packets: {}".format(data_store.scenario["duplicated"]))
        data_store.scenario["lastRTT"] = str(results["data"]["lastRTT"])
        Messages.write_message("Round trip time of the last PING in millisec: {}".format(data_store.scenario["lastRTT"]))
        data_store.scenario["maxRTT"] = str(results["data"]["maxRTT"])
        Messages.write_message("Maximum round trip time in millisec: {}".format(data_store.scenario["maxRTT"]))
        data_store.scenario["minRTT"] = str(results["data"]["minRTT"])
        Messages.write_message("Minimum round trip time in millisec: {}".format(data_store.scenario["minRTT"]))
        data_store.scenario["avrRTT"] = str(results["data"]["avrRTT"])
        Messages.write_message("Average round trip time in millisec: {}".format(data_store.scenario["avrRTT"]))
        data_store.scenario["sumRTT"] = str(results["data"]["sumRTT"])
        Messages.write_message("Sum of all round trip time in millisec: {}".format(data_store.scenario["sumRTT"]))
        data_store.scenario["sendErrorCode"] = str(results["data"]["sendErrorCode"])
        Messages.write_message("PING send request error code if any: {}".format(data_store.scenario["sendErrorCode"]))
        data_store.scenario["recvErrorCode"] = str(results["data"]["recvErrorCode"])
        Messages.write_message("PING recv error code if any: {}".format(data_store.scenario["recvErrorCode"]))
    else:
        assert False, "Returned with empty data"
###
# get ping error no
###
@step("Get ping error no")
def getPingErrorNo():
    """
    Calls the CAPI Ping Get Error No method and stores the result in the ``data_store.scenario["pingErrNo"]`` variable.

    Step and function definition::

        @step("Get ping error no")
        def getPingErrorNo():

    Example usage:
        * Get ping error no
    """
    results = data_store.scenario["capiController"].pingGetErrNo()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get ping error no failed"
    if results["data"] != "":
        data_store.scenario["pingErrNo"] = hex(results["data"]["pingErrNo"])
        Messages.write_message("Last error Number: {}".format(data_store.scenario["pingErrNo"]))
    else:
        assert False, "Returned with empty data"
###
# arp register
###
@step("ARP register")
def arpRegister():
    """
    Calls the CAPI ARP Register method.

    Step and function definition::

        @step("ARP register")
        def arpRegister():

    Example usage:
        * ARP register
    """
    results = data_store.scenario["capiController"].arpRegister()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "ARP register failed"
    data_store.scenario["arpRegistered"] = True
###
# arp use
###
@step("ARP use <ip>")
def arpUse(ip):
    """
    Calls the CAPI ARP Use method and sets the destination IP.

    Args:
        ip (string): IP of target.

    Step and function definition::

        @step("ARP use <ip>")
        def arpUse(ip):

    Example usage:
        * ARP use "192.168.1.12"
    """
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address is wrong"
    results = data_store.scenario["capiController"].arpUse(ip)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "ARP use failed"
###
# arp start
###
@step("ARP start <ip> <probe> <interval> <timeout>")
def arpStart(ip, probe, interval, timeout):
    """
    Calls the CAPI ARP Start method and takes in IP, Probe, Interval, and Timeout.

    Args:
        ip (string): IP of target.
        probe (int): Number of ARP's to send (0 is deafult).
        interval (int): Time in ms between ARPs (0 is deafult).
        timeout (int): Max time of ARP request (0 is default).

    Step and function definition::

        @step("ARP start <ip> <probe> <interval> <timeout>")
        def arpStart(ip, probe, interval, timeout):

    Example usage:
        * ARP start "192.168.1.12" "0" "0" "0"
        * ARP start "192.168.1.12" "4" "2000" "0"
        * ARP start "192.168.1.12" "4" "2000" "8000"
    """
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address format is wrong"
    probe = int(probe)
    interval = int(interval)
    timeout = int(timeout)
    data_store.scenario["arpStartTime"] = time.time()
    results = data_store.scenario["capiController"].arpStart(ip, probe, interval, timeout)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "ARP start failed"
###
# arp cancel
###
@step("ARP cancel <ip>")
def arpCancel(ip):
    """
    Calls the CAPI ARP Cancel method and takes in IP.

    Args:
        ip (string): IP of target.

    Step and function definition::

        @step("ARP cancel <ip>")
        def arpCancel(ip):

    Example usage:
        * ARP cancel "192.168.1.12"
    """
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address formar is wrong"
    results = data_store.scenario["capiController"].arpCancel(ip)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "ARP cancel failed"
###
# arp unregister
###
@step("ARP unregister")
def arpUnregister():
    """
    Calls the CAPI ARP Unregister method.

    Step and function definition::

        @step("ARP unregister")
        def arpUnregister():

    Example usage:
        * ARP unregister
    """
    results = data_store.scenario["capiController"].arpUnregister()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "ARP unregister failed"
    data_store.scenario["arpRegistered"] = False
###
# hb start
###
@step("HB start <heartBeat>")
def hbStart(heartBeat):
    """
    Calls the CAPI HB Start method with a heartbeat interval as input.

    Args:
        heartBeat (int): Interval of heartbeat.

    Step and function definition::

        @step("HB start <heartBeat>")
        def hbStart(heartBeat):

    Example usage:
        * HB start "500"
     """
    heartBeat = int(heartBeat)
    results = data_store.scenario["capiController"].startHeartBeatHC(heartBeat)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "HB start failed"
###
# hb stop
###
@step("HB stop")
def hbStop():
    """
    Calls the CAPI HB Stop method.

    Step and function definition::

        @step("HB stop")
        def hbStop():

    Example usage:
        * HB stop
     """
    results = data_store.scenario["capiController"].stopHeartBeatHC()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "HB stop failed"
###
# hb fail
###
@step("HB fail")
def hbFail():
    """
    Calls the CAPI HB Fail method.

    Step and function definition::

        @step("HB fail")
        def hbFail():

    Example usage:
        * HB fail
     """
    results = data_store.scenario["capiController"].failHeartBeatHC()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "HB fail failed"
###
# poll start
###
@step("Poll start <dutyCycle>")
def pollStart(dutyCycle):
    """
    Calls the CAPI Poll Start method with given duty cycle.

    Args:
        dutyCycle (int): Interval of poll.

    Step and function definition::

        @step("Poll start <dutyCycle>")
        def pollStart(dutyCycle):

    Example usage:
        * Poll start "500"
     """
    dutyCycle = int(dutyCycle)
    results = data_store.scenario["capiController"].startPollCH(dutyCycle)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Poll start failed"
###
# poll stop
###
@step("Poll stop")
def pollStop():
    """
    Calls the CAPI Poll Stop method.

    Step and function definition::

        @step("Poll stop")
        def pollStop():

    Example usage:
        * Poll stop
     """
    results = data_store.scenario["capiController"].stopPollCH()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Poll stop failed"
###
# change connection state
###
@step("Change connection state <index> <state>")
def changeConnectionState(index, state):
    """
    Calls the CAPI Change Connection State method. This is used to Enable/Disbale IO.

    Args:
        index (int): Index of IO.
        state (int): State to set IO (0 for False, 1 for True).


    Step and function definition::

        @step("Change connection state <index> <state>")
        def changeConnectionState(index, state):

    Example usage:
        * Change connection state "0" "0"
        * Change connection state "0" "1"
     """
    index = int(index)
    state = bool(int(state))
    results = data_store.scenario["capiController"].changeConnectionState(index, state)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Change connection state"
###
# get io status
###
@step("Get IO status <index>")
def getIOStatus(index):
    """
    Calls the CAPI Get IO Status method and saves the results in the following variables:
        * ``data_store.scenario["producedStatus"]``
        * ``data_store.scenario["consumedStatus"]``

    Args:
        index (int): Index of IO.

    Step and function definition::

        @step("Get IO status <index>")
        def getIOStatus(index):

    Example usage:
        * Get IO status "0"
     """
    index = int(index)
    results = data_store.scenario["capiController"].getIOStatus(index)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get IO status failed"
    data_store.scenario["producedStatus"] = results["data"]["producedStatus"]
    Messages.write_message("Produced Status: {}".format(data_store.scenario["producedStatus"]))
    data_store.scenario["consumedStatus"] = results["data"]["consumedStatus"]
    Messages.write_message("Consumed Status: {}".format(data_store.scenario["consumedStatus"]))
###
# send blink message
###
@step("Send message blink <byMac> <dataLength>")
def sendMessageBlink(byMac, dataLength):
    """
    Calls the CAPI Send Message method and invokes the blink request given MAC Address and Data Length.

    Args:
        byMac (string): MAC address of target.
        dataLength (int): Length of data to send.

    Step and function definition::

        @step("Send message blink <byMac> <dataLength>")
        def sendMessageBlink(byMac, dataLength):

    Example usage:
        * Send message blink "00:A0:91:30:4B:29" "6"
     """
    assert len(byMac.split(":")) == 6, "MAC Address not correct format"
    assert int(dataLength) < 255, "dataLength is too large, needs to be less than 254"
    data = [0] * CMTP_BUFFER_LEN
    dataLength = int(dataLength)
    serviceID = 20
    for i, mac in enumerate(byMac.split(":")):
        data[i] = int("0x{}".format(mac), 0)
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send set ip message
###
@step("Send message set name <dwRemanent> <dwNameLength> <szName> <byMac> <dataLength>")
def sendMessageSetName(dwRemanent, dwNameLength, szName, byMac, dataLength):
    """
    Calls the CAPI Send Message method and invokes the set name request given Remanent, Name Length, Name, MAC Address, and Data Length.

    Args:
        dwRemanent (int): Non-volatile for 1, volatile for 0.	
        dwNameLength (int): Length of the name.
        szName (string): Name to set target.
        byMac (string): MAC address of target.
        dataLength (int): 	Length of data to send.

    Step and function definition::

        @step("Send message set name <dwRemanent> <dwNameLength> <szName> <byMac> <dataLength>")
        def sendMessageSetName(dwRemanent, dwNameLength, szName, byMac, dataLength):

    Example usage:
        * Send message set name "1" "14" "harshio600-epn" "00:A0:91:30:4B:29" "254"
 """
    assert len(byMac.split(":")) == 6, "MAC Address not correct format"
    assert int(dwNameLength) < 240, "Name length must be less than 240"
    assert int(dwNameLength) == len(szName), "szName and dwNameLength are not equal in size"
    assert int(dwRemanent) < 4294967296, "dwRemanent is too large, needs to be less than 4294967296"
    assert int(dataLength) < 255, "dataLength is too large, needs to be less than 254"
    data = [0] * CMTP_BUFFER_LEN
    dataLength = int(dataLength)
    serviceID = 22
    # set request type, 0 is volatile 1 is permenant
    dwRemanentOffset = 24 - 24
    for i, num in enumerate(struct.pack('<i', int(dwRemanent))):
        data[i + dwRemanentOffset] = num
    # set name length
    dwNameLengthOffset = 28 - 24
    for i, num in enumerate(struct.pack('<i', int(dwNameLength))):
        data[i + dwNameLengthOffset] = num
    # set name
    szNameOffset = 32 - 24
    for i, stringNum in enumerate(bytes(szName, "utf-8")):
        data[i + szNameOffset] = stringNum
    # set MAC
    byMacOffset = 272 - 24
    for i, mac in enumerate(byMac.split(":")):
        data[i + byMacOffset] = int("0x{}".format(mac), 0)
    # init data string
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send set ip message
###
@step("Send message set ip <dwRemanent> <dwIPMode> <byIPAddr> <byIPMask> <byIPGateway> <byMac> <dataLength>")
def sendMessageSetIP(dwRemanent, dwIPMode, byIPAddr, byIPMask, byIPGateway, byMac, dataLength):
    """
    Calls the CAPI Send Message method and invokes the set ip request given Remanent, IP Mode, IP Address, IP Mask, IP Gateway, MAC Address, and Data Length.

    Args:
        dwRemanent (int): Non-volatile for 1, volatile for 0.
        dwIPMode (int): 1 for static IP.
        byIPAddr (string): IP to set target.
        byIPMask (string): Subnet mask to set target.
        byIPGateway (string): gateway to set target.
        byMac (string): MAC address of target.
        dataLength (int): Length of data to send.

    Step and function definition::

        @step("Send message set ip <dwRemanent> <dwIPMode> <byIPAddr> <byIPMask> <byIPGateway> <byMac> <dataLength>")
        def sendMessageSetIP(dwRemanent, dwIPMode, byIPAddr, byIPMask, byIPGateway, byMac, dataLength):

    Example usage:
        * Send message set ip "1" "1" "192.168.1.12" "255.255.255.0" "0.0.0.0" "00:A0:91:30:4B:29" "254"
     """
    assert len(byIPAddr.split(".")) == 4, "IP Address not correct format"
    assert len(byIPMask.split(".")) == 4, "IP Mask not correct format"
    assert len(byIPGateway.split(".")) == 4, "IP Gateway not correct format"
    assert len(byMac.split(":")) == 6, "MAC Address not correct format"
    assert int(dwRemanent) < 4294967296, "dwRemanent is too large, needs to be less than 4294967296"
    assert int(dwIPMode) < 4294967296, "dwIPMode is too large, needs to be less than 4294967296"
    assert int(dataLength) < 255, "dataLength is too large, needs to be less than 254"
    data = [0] * CMTP_BUFFER_LEN
    dataLength = int(dataLength)
    serviceID = 23
    # set request type, 0 is volatile 1 is permenant
    dwRemanentOffset = 24 - 24
    for i, num in enumerate(struct.pack('<i', int(dwRemanent))):
        data[i + dwRemanentOffset] = num
    # set IP mode, 1 for static
    dwIPModeOffset = 28 - 24
    for i, num in enumerate(struct.pack('<i', int(dwIPMode))):
        data[i + dwIPModeOffset] = num
    # set IP Addr
    byIPAddrOffset = 32 - 24
    for i, ip in enumerate(byIPAddr.split(".")):
        data[i + byIPAddrOffset] = int("{}".format(ip), 0)
    # set IP Mask
    byIPMaskOffset = 36 - 24
    for i, ip in enumerate(byIPMask.split(".")):
        data[i + byIPMaskOffset] = int("{}".format(ip), 0)
    # set IP Gateway
    byIPGatewayOffset = 40 - 24
    for i, ip in enumerate(byIPGateway.split(".")):
        data[i + byIPGatewayOffset] = int("{}".format(ip), 0)
    # set MAC
    byMacOffset = 44 - 24
    for i, mac in enumerate(byMac.split(":")):
        data[i + byMacOffset] = int("0x{}".format(mac), 0)
    # init data string
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send read explicit message
###
@step("Send message read explicit <dwConfID> <dwCrc32> <wDeviceNumber> <dwApi> <wSlotNumber> <wSubSlotNumber> <wIndex> <wLengthDataToRead> <dataLength>")
def sendMessageReadExplicit(dwConfID, dwCrc32, wDeviceNumber, dwApi, wSlotNumber, wSubSlotNumber, wIndex, wLengthDataToRead, dataLength):
    """
    Calls the CAPI Send Message method and invokes the read explicit request given Config ID, CRC, Device Number, API, Slot Number, Subslot Number, Index, Length of Data to Read, and Data Length.

    Args:
        dwConfID (int): Set to 0.
        dwCrc32 (int): Set to 0.
        wDeviceNumber (int): Device number of target.
        dwApi (int): API number of target.
        wSlotNumber (int): Slot number of target.
        wSubSlotNumber (int): Subslot number of target.
        wIndex (int): Index of target.
        wLengthDataToRead (int): Length of data to read.
        dataLength (int): Length of data to send.

    Step and function definition::

        @step("Send message read explicit <dwConfID> <dwCrc32> <wDeviceNumber> <dwApi> <wSlotNumber> <wSubSlotNumber> <wIndex> <wLengthDataToRead> <dataLength>")
        def sendMessageReadExplicit(dwConfID, dwCrc32, wDeviceNumber, dwApi, wSlotNumber, wSubSlotNumber, wIndex, wLengthDataToRead, dataLength):

    Example usage:
        * TBD
    """
    assert len(byMac.split(":")) == 6, "MAC Address not correct format"
    assert int(dataLength) < 255, "dataLength is too large, needs to be less than 254"
    data = [0] * CMTP_BUFFER_LEN
    dataLength = int(dataLength)
    serviceID = 32
    # set configuration ID
    dwConfIDOffset = 24 - 24
    for i, num in enumerate(struct.pack('<i', int(dwConfID))):
        data[i + dwConfIDOffset] = num
    # set crc 32
    dwCrc32Offset = 28 - 24
    for i, num in enumerate(struct.pack('<i', int(dwCrc32))):
        data[i + dwCrc32Offset] = num
    # set device number
    wDeviceNumberOffset = 32 - 24
    for i, num in enumerate(struct.pack('<h', int(wDeviceNumber))):
        data[i + wDeviceNumberOffset] = num
    # set api
    dwApiOffset = 34 - 24
    for i, num in enumerate(struct.pack('<i', int(dwApi))):
        data[i + dwApiOffset] = num
    # set slot number
    wSlotNumberOffset = 38 - 24
    for i, num in enumerate(struct.pack('<h', int(wSlotNumber))):
        data[i + wSlotNumberOffset] = num
    # set sub slot number
    wSubSlotNumberOffset = 40 - 24
    for i, num in enumerate(struct.pack('<h', int(wSubSlotNumber))):
        data[i + wSubSlotNumberOffset] = num
    # set index
    wIndexOffset = 42 - 24
    for i, num in enumerate(struct.pack('<h', int(wIndex))):
        data[i + wSubSlotNumberOffset] = num
    # set length data to read
    wLengthDataToReadOffset = 44 - 24
    for i, num in enumerate(struct.pack('<h', int(wLengthDataToRead))):
        data[i + wLengthDataToReadOffset] = num
    # init data string
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send write explicit message
###
@step("Send message write explicit <dwConfID> <dwCrc32> <wDeviceNumber> <dwApi> <wSlotNumber> <wSubSlotNumber> <wIndex> <dataToWrite> <dataLength>")
def sendMessageWriteExplicit(dwConfID, dwCrc32, wDeviceNumber, dwApi, wSlotNumber, wSubSlotNumber, wIndex, dataToWrite, dataLength):
    """
    Calls the CAPI Send Message method and invokes the write explicit request given Config ID, CRC, Device Number, API, Slot Number, Subslot Number, Index, Data to Write, and Data Length.

    Args:
        dwConfID (int): Set to 0.
        dwCrc32 (int): Set to 0.
        wDeviceNumber (int): Device number of target.
        dwApi (int): API number of target.
        wSlotNumber (int): Slot number of target.
        wSubSlotNumber (int): Subslot number of target.
        wIndex (int): Index of target.
        dataToWrite (string): Data to write to target.
        dataLength (int): Length of data to send.

    Step and function definition::

        @step("Send message write explicit <dwConfID> <dwCrc32> <wDeviceNumber> <dwApi> <wSlotNumber> <wSubSlotNumber> <wIndex> <dataToWrite> <dataLength>")
        def sendMessageWriteExplicit(dwConfID, dwCrc32, wDeviceNumber, dwApi, wSlotNumber, wSubSlotNumber, wIndex, dataToWrite, dataLength):

    Example usage:
        * TBD
    """
    assert len(byMac.split(":")) == 6, "MAC Address not correct format"
    assert int(dataLength) < 255, "dataLength is too large, needs to be less than 254"
    data = [0] * CMTP_BUFFER_LEN
    dataLength = int(dataLength)
    serviceID = 32
    # set configuration ID
    dwConfIDOffset = 24 - 24
    for i, num in enumerate(struct.pack('<i', int(dwConfID))):
        data[i + dwConfIDOffset] = num
    # set crc 32
    dwCrc32Offset = 28 - 24
    for i, num in enumerate(struct.pack('<i', int(dwCrc32))):
        data[i + dwCrc32Offset] = num
    # set device number
    wDeviceNumberOffset = 32 - 24
    for i, num in enumerate(struct.pack('<h', int(wDeviceNumber))):
        data[i + wDeviceNumberOffset] = num
    # set api
    dwApiOffset = 34 - 24
    for i, num in enumerate(struct.pack('<i', int(dwApi))):
        data[i + dwApiOffset] = num
    # set slot number
    wSlotNumberOffset = 38 - 24
    for i, num in enumerate(struct.pack('<h', int(wSlotNumber))):
        data[i + wSlotNumberOffset] = num
    # set sub slot number
    wSubSlotNumberOffset = 40 - 24
    for i, num in enumerate(struct.pack('<h', int(wSubSlotNumber))):
        data[i + wSubSlotNumberOffset] = num
    # set index
    wIndexOffset = 42 - 24
    for i, num in enumerate(struct.pack('<h', int(wIndex))):
        data[i + wSubSlotNumberOffset] = num
    # set data to write
    dataToWriteOffset = 44 - 24
    for i, num in enumerate(dataToWrite.split(",")):
        assert int(num) < 256, "Number in dataToWrite list too large {} at index {}".format(num, i)
        data[i + dataToWriteOffset] = int(num)
    # init data string
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send identify message
###
@step("Send message identify")
def sendMessageIdentify():
    """
    Calls the CAPI Send Message method and invokes the identify request.

    Step and function definition::

        @step("Send message identify")
        def sendMessageIdentify():

    Example usage:
        * Send message identify
    """
    data = [0] * CMTP_BUFFER_LEN
    dataLength = 254
    serviceID = 10
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send get device detected message
###
@step("Send message get device detected")
def sendMessageGetDeviceDetected():
    """
    Calls the CAPI Send Message method and invokes the get device detected request.

    Step and function definition::

        @step("Send message get device detected")
        def sendMessageGetDeviceDetected():

    Example usage:
        * Send message get device detected
    """
    data = [0] * CMTP_BUFFER_LEN
    dataLength = 254
    serviceID = 11
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])
###
# send blink message
###
@step("Send message factory reset <byMac> <dataLength>")
def sendMessageFactoryReset(byMac, dataLength):
    """
    Calls the CAPI Send Message method and invokes the factory reset request given MAC Address and Data Length.

    Args:
        byMac (string): MAC of target.
        dataLength (int): Length of data to send.

    Step and function definition::

        @step("Send message factory reset <byMac> <dataLength>")
        def sendMessageFactoryReset(byMac, dataLength):

    Example usage:
        * Send message factory reset "00:0F:9E:ED:E2:C4" "254"
    """
    assert len(byMac.split(":")) == 6, "MAC Address not correct format"
    assert int(dataLength) < 255, "dataLength is too large, needs to be less than 254"
    data = [0] * CMTP_BUFFER_LEN
    dataLength = int(dataLength)
    serviceID = 21
    for i, mac in enumerate(byMac.split(":")):
        data[i] = int("0x{}".format(mac), 0)
    dataString = ""
    for i, resultData in enumerate(data):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Sending Service: {}".format(serviceID))
    Messages.write_message("Sending Size: {}".format(dataLength))
    Messages.write_message("Sending Data: \n{}".format(dataString))
    results = data_store.scenario["capiController"].sendMessage(data, serviceID, dataLength)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Send message failed"
    Messages.write_message("Received Status: {}".format(results["data"]["status"]))
    Messages.write_message("Received Service: {}".format(results["data"]["service"]))
    Messages.write_message("Received Size: {}".format(results["data"]["size"]))
    dataString = ""
    for i, resultData in enumerate(results["data"]["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert results["data"]["status"] == 0, "Status from response is non-zero - {}".format(results["data"]["status"])

##########################################################################
# safe card steps
###
# safe init
###
@step("Safe init")
def safeInit():
    """
    Calls the CAPI Safe Init method.

    Step and function definition::

        @step("Safe init")
        def safeInit():

    Example usage:
        * Safe init
    """
    results = data_store.scenario["capiController"].safeInit()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Safe init failed"
    data_store.scenario["safeInit"] = True
###
# open safe interface
###
@step("Open safe interface <index>")
def openSafeInterface(index):
    """
    Calls the CAPI Open Safe Interface method at given index.

    Args:
        index (int): Index of card.

    Step and function definition::

        @step("Open safe interface <index>")
        def openSafeInterface(index):

    Example usage:
        * Open safe interface "0"
    """
    results = data_store.scenario["capiController"].openSafeInterface(int(index))
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Open safe interface failed"
    data_store.scenario["safeOpenInterface"] = True
###
# read safe config
###
@step("Read safe config")
def readSafeConfig():
    """
    Calls the CAPI Read Safe Config method.

    Step and function definition::

        @step("Read safe config")
        def readSafeConfig():

    Example usage:
        * Read safe config
    """
    results = data_store.scenario["capiController"].readSafeConfig()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Read safe config failed"
###
# enable safe connection
###
@step("Enable safe connection")
def enableSafeConnection():
    """
    Calls the CAPI Enable Safe Connection method.

    Step and function definition::

        @step("Enable safe connection")
        def enableSafeConnection():

    Example usage:
        * Enable safe connection
    """
    results = data_store.scenario["capiController"].enableSafeConnection()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Enable safe connection failed"
    data_store.scenario["safeEnabled"] = True
###
# start safe connections
###
@step("Start safe connections <index>")
def startSafeConnections(index):
    """
    Calls the CAPI Refresh Safe IO method and then starts the safe produced and safe consumed threads on the given index.

    Args:
        index (int): Index of safe IO.

    Step and function definition::

        @step("Start safe connections <index>")
        def startSafeConnections(index):

    Example usage:
        * Start safe connections "0"
    """
    results = data_store.scenario["capiController"].refreshSafeIO()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Refresh safe io failed"
    data_store.scenario["capiController"].startSafeProduce(0)
    assert data_store.scenario["capiController"].produceSafeFunctionStop == False
    data_store.scenario["capiController"].startSafeConsume(0)
    assert data_store.scenario["capiController"].consumeSafeFunctionStop == False
    time.sleep(data_store.scenario["capiController"].consumeSafeFunctionDuty)
###
# read safe io
###
@step("Read safe IO")
def readSafeIO():
    """
    Calls the CAPI Read Safe IO method for the opened IO index.

    Step and function definition::

        @step("Read safe IO")
        def readSafeIO():

    Example usage:
        * Read safe IO
    """
    results = data_store.scenario["capiController"].readSafeIO()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Read safe io failed"
    data_store.scenario["producedSafeIO"] = results["data"]["produced"]
    Messages.write_message("Safe Produced: {}".format(data_store.scenario["producedSafeIO"]))
    data_store.scenario["consumedSafeIO"] = results["data"]["consumed"]
    Messages.write_message("Safe Consumed: {}".format(data_store.scenario["consumedSafeIO"]))
###
# write safe io
###
@step("Write safe IO <value>")
def writeSafeIO(value):
    """
    Calls the CAPI Write Safe IO method for the opened IO index with given value.

    Args:
        value ([type]): [description]

    Step and function definition::

        @step("Write safe IO <value>")
        def writeSafeIO(value):

    Example usage:
        * Write safe IO "1"
    """
    newProduceData = list(data_store.scenario["producedSafeIO"])
    newProduceData[0] = int(value)
    newProduceData = tuple(newProduceData)
    results = data_store.scenario["capiController"].writeSafeProducedIO(newProduceData)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Write safe io failed"
    Messages.write_message("Write: {}".format(newProduceData))
    time.sleep(data_store.scenario["capiController"].produceSafeFunctionDuty)
###
# change ncs
###
@step("Change NCS <value>")
def changeNCS(value):
    """
    Calls the CAPI Change NCS method with given value.

    Args:
        value (int): Value to write.

    Step and function definition::

        @step("Change NCS <value>")
        def changeNCS(value):

    Example usage:
        * Change NCS "4"
    """
    results = data_store.scenario["capiController"].changeNCS(int(value))
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Change NCS failed"
###
# get ncs
###
@step("Get NCS")
def getNCS():
    """
    Calls the CAPI Get NCS method and stores the result in the following values:
        * data_store.scenario["producedNSC"]
        * data_store.scenario["consumedNSC"]

    Step and function definition::

        @step("Get NCS")
        def getNCS():

    Example usage:
        * Get NCS
    """
    results = data_store.scenario["capiController"].getNCS()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get NCS failed"
    data_store.scenario["producedNSC"] = results["data"]["producedNSC"]
    Messages.write_message("Produced NCS: {}".format(data_store.scenario["producedNSC"]))
    data_store.scenario["consumedNSC"] = results["data"]["consumedNSC"]
    Messages.write_message("Consumed NCS: {}".format(data_store.scenario["consumedNSC"]))
###
# ncs loop
###
@step("Get NCS loop <value>")
def getNCSLoop(value):
    """
    Calls the CAPI Get NCS method on a loop with given timeout value and prints the results to the Gauge report.

    Args:
        value (int): Value for timeout in s.

    Step and function definition::

        @step("Get NCS loop <value>")
        def getNCSLoop(value):

    Example usage:
        * Get NCS loop "10"
    """
    timeout = time.time() + float(value)
    while (time.time() < timeout):
        x = data_store.scenario["capiController"].getNCS()
        Messages.write_message(x["description"])
        Messages.write_message("Produced NCS: {}".format(x["data"]["producedNSC"]))
        Messages.write_message("Produced NCS: {}".format(x["data"]["consumedNSC"]))
        time.sleep(0.5)
###
# get safe io status
###
@step("Get safe IO status <index>")
def getIOStatus(index):
    """
    Calls the CAPI Get Safe IO Status method and saves results to the following:
        * data_store.scenario["producedSafeStatus"]
        * data_store.scenario["consumedSafeStatus"]

    Args:
        index (int): IO index to get status from.

    Step and function definition::

        @step("Get safe IO status <index>")
        def getIOStatus(index):

    Example usage:
        * Get safe IO status "0"
    """
    index = int(index)
    results = data_store.scenario["capiController"].getSafeIOStatus(index)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Get safe IO status failed"
    data_store.scenario["producedSafeStatus"] = results["data"]["producedStatus"]
    Messages.write_message("Produced Safe Status: {}".format(data_store.scenario["producedSafeStatus"]))
    data_store.scenario["consumedSafeStatus"] = results["data"]["consumedStatus"]
    Messages.write_message("Consumed Safe Status: {}".format(data_store.scenario["consumedSafeStatus"]))

##########################################################################
# configuration steps
###
# register
###
@step("Config register")
def configRegister():
    """
    Calls the CAPI Config Register method.

    Step and function definition::

        @step("Config register")
        def configRegister():

    Example usage:
        * Config register
    """
    results = data_store.scenario["capiController"].notifyReq(True)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Register failed"
###
# unregister
###
@step("Config unregister")
def configUnregister():
    """
    Calls the CAPI Config Unregister method.

    Step and function definition::

        @step("Config unregister")
        def configUnregister():

    Example usage:
        * Config unregister
    """
    results = data_store.scenario["capiController"].notifyReq(False)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Unregister failed"
###
# lock
###
@step("Config lock")
def configLock():
    """
    Calls the CAPI Config Lock method.

    Step and function definition::

        @step("Config lock")
        def configLock():

    Example usage:
        * Config lock
    """
    results = data_store.scenario["capiController"].configLockReq(True)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Lock failed"
###
# unlock
###
@step("Config unlock")
def configUnlock():
    """
    Calls the CAPI Config Unlock method.

    Step and function definition::

        @step("Config unlock")
        def configUnlock():

    Example usage:
        * Config unlock
    """
    results = data_store.scenario["capiController"].configLockReq(False)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Unlock failed"
###
# config mode
###
@step("Config mode")
def configMode():
    """
    Calls the CAPI Config Mode method.

    Step and function definition::

        @step("Config mode")
        def configMode():

    Example usage:
        * Config mode
    """
    results = data_store.scenario["capiController"].configMode()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Config mode failed"
###
# config reset
###
@step("Config reset")
def configReset():
    """
    Calls the CAPI Config Reset method.

    Step and function definition::

        @step("Config reset")
        def configReset():

    Example usage:
        * Config reset
    """
    results = data_store.scenario["capiController"].configReset()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Config reset failed"
    timeout = time.time() + 30
    configRead = False
    while (time.time() < timeout and configRead == False):
        x = data_store.scenario["capiController"].readConfigID(True)
        if (x["result"] == 0):
            configRead = True
    assert configRead == True, "Unable to confirm config was reset"
###
# write block - network config
###
@step("Write block network config")
def writeBlockNetworkConfig():
    """
    Calls the CAPI Write Block Network Configuration (Non-compressed) method and it will use the filename saved in ``data_store.suite["configFile"]`` variable.

    Step and function definition::

        @step("Write block network config")
        def writeBlockNetworkConfig():

    Example usage:
        * Write block network config
    """
    try:
        results = data_store.scenario["capiController"].writeBlock(10, data_store.suite["configFile"])
        Messages.write_message(results["description"])
        assert results["result"] == 0, "Write file to device failed"
    except NameError:
        Messages.write_message("Load config was not called, there is no config to load")
        assert False, "NameError when trying to write configFile"
###
# write block - network config compressed
###
@step("Write block network config compressed")
def writeBlockNetworkConfigCompressed():
    """
    Calls the CAPI Write Block Network Configuration Compressed method and it will use the filename saved in ``data_store.suite["configFile"]`` variable.

    Step and function definition::

        @step("Write block network config compressed")
        def writeBlockNetworkConfigCompressed():

    Example usage:
        * Write block network config compressed
    """
    try:
        results = data_store.scenario["capiController"].writeBlock(11, data_store.suite["configFile"])
        Messages.write_message(results["description"])
        assert results["result"] == 0, "Write file to device failed"
    except NameError:
        Messages.write_message("Load config was not called, there is no config to load")
        assert False, "NameError when trying to write configFile"
###
# config validate
###
@step("Config validate")
def configValidate():
    """
    Calls the CAPI Config Validate method.

    Step and function definition::

        @step("Config validate")
        def configValidate():

    Example usage:
        * Config validate
    """
    results = data_store.scenario["capiController"].configValidate()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Config validate failed"
###
# config apply
###
@step("Config apply")
def configApply():
    """
    Calls the CAPI Config Apply method.

    Step and function definition::

        @step("Config apply")
        def configApply():

    Example usage:
        * Config apply
    """
    results = data_store.scenario["capiController"].configApply()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Config apply failed"
    timeout = time.time() + 30
    configRead = False
    while (time.time() < timeout and configRead == False):
        x = data_store.scenario["capiController"].readConfigID(True)
        if (x["result"] == 0):
            configRead = True
    assert configRead == True, "Cannot verify config"

##########################################################################
# verify steps
###
# verify config
###
@step("Verify configuration")
def verifyConfiguration():
    """
    Calls the CAPI Read Config ID method and asserts against the CRC that was stored for the downloaded network configuration file.

    Step and function definition::

        @step("Verify configuration")
        def verifyConfiguration():

    Example usage:
        * Verify configuration
    """
    results = data_store.scenario["capiController"].readConfigID(True)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Read config failed"
    Messages.write_message("Device CRC: {}".format(hex(int(results["data"]["configDataCRC"]))))
    Messages.write_message("Database CRC: {}".format(data_store.suite["configCRC"]))
    Messages.write_message("{}".format(results["data"]))
    assert data_store.suite["configCRC"] == hex(int(results["data"]["configDataCRC"])), "Cannot verify config"
###
# verify card name
###
@step("Verify <name> card name")
def verifyCardName(name):
    """
    Asserts the given name against the stored ``data_store.scenario["productName"]`` variable.

    Args:
        name (string): Name of string to assert.

    Step and function definition::

        @step("Verify <name> card name")
        def verifyCardName(name):

    Example usage:
        * Verify "fanuc-cnc" card name
    """
    assert name == data_store.scenario["productName"], "{} != {}".format(name, data_store.scenario["productName"])
###
# verify ip address
###
@step("Verify <address> ip address")
def verifyIPAddress(address):
    """
    Asserts the given IP Address against the stored data_store.scenario["ipAddr"] variable.

    Args:
        address (string): IP to assert.

    Step and function definition::

        @step("Verify <address> ip address")
        def verifyIPAddress(address):

    Example usage:
        * Verify "192.168.1.10" ip address
    """
    assert address == data_store.scenario["ipAddr"], "{} != {}".format(address, data_store.scenario["ipAddr"])
###
# verify firmware version
###
@step("Verify firmware version")
def verifyFirmwareVersion():
    """
    Asserts the firmware version from Artifactory saved in ``os.getenv("firmware_version")`` against the stored ``data_store.scenario["firmwareVersion"]`` variable.

    Step and function definition::

        @step("Verify firmware version")
        def verifyFirmwareVersion():

    Example usage:
        * Verify firmware version
    """
    assert os.getenv("firmware_version") == data_store.scenario["firmwareVersion"], "{} != {}".format(os.getenv("firmware_version"), data_store.scenario["firmwareVersion"])
###
# verify number connections
###
@step("Verify <num> connections")
def verifyConnections(num):
    """
    Asserts the given num of connections against the stored ``data_store.scenario["numConnections"]`` variable.

    Args:
        num (int): Number of connections.

    Step and function definition::

        @step("Verify <num> connections")
        def verifyConnections(num):

    Example usage:
        * Verify "2" connections
    """
    assert data_store.scenario["numConnections"] == int(num), "{} != {}".format(int(num), data_store.scenario["numConnections"])
###
# verify number active connections
###
@step("Verify <num> active connections")
def verifyActiveConnections(num):
    """
    Asserts the given num of active connections against the stored ``data_store.scenario["numActConnections"]`` variable.

    Args:
        num (int): Number of connections.

    Step and function definition::

        @step("Verify <num> active connections")
        def verifyActiveConnections(num):

    Example usage:
        * Verify "2" active connections
    """
    assert data_store.scenario["numActConnections"] == int(num), "{} != {}".format(int(num), data_store.scenario["numActConnections"])
###
# verify input
###
@step("Verify input <value>")
def verifyInput(value):
    """
    Asserts the given value against the stored ``data_store.scenario["consumedIO"][0]`` variable.

    Args:
        value (int): Value of IO.

    Step and function definition::

        @step("Verify input <value>")
        def verifyInput(value):

    Example usage:
        * Verify input "1"
    """
    assert data_store.scenario["consumedIO"][0] == int(value), "{} != {}".format(int(value), data_store.scenario["consumedIO"][0])
###
# verify safe output
###
@step("Verify safe output <value>")
def verifySafeOutput(value):
    """
    Asserts the given value against the stored ``data_store.scenario["producedSafeIO"][0]`` variable.

    Args:
        value (int): Value of IO

    Step and function definition::

        @step("Verify safe output <value>")
        def verifySafeOutput(value):

    Example usage:
        * Verify safe output "1"
    """
    assert data_store.scenario["producedSafeIO"][0] == int(value), "{} != {}".format(int(value), data_store.scenario["producedSafeIO"][0])
###
# verify ncs
###
@step("Verify NCS <val1> or <val2>")
def verifyNCS(val1, val2):
    """
    Asserts the given val1 or val2 against the stored ``data_store.scenario["consumedNSC"]`` variable.

    Args:
        val1 (int): Value 1 of NCS.
        val2 (int): Value 2 of NCS.

    Step and function definition::

        @step("Verify NCS <val1> or <val2>")
        def verifyNCS(val1, val2):

    Example usage:
        * Verify NCS "0" or "16"
    """
    assert data_store.scenario["consumedNSC"] == int(val1) or data_store.scenario["consumedNSC"] == int(val2), "{} != {} or {}".format(data_store.scenario["consumedNSC"], int(val1), int(val2))

##########################################################################
# automation steps
###
# io test loop
###
@step("Test IO <standardValue> test safe IO <safeValue> loop <timeoutSeconds>")
def testIOTestSafeIOLoop(standardValue, safeValue, timeoutSeconds):
    """
    This method loops through reading/writing standard/safe IO for the timeout given.

    Args:
        standardValue (int): Value to write to standard IO.
        safeValue (int): Value to write to safe IO.
        timeoutSeconds (int): Timeout in seconds.

    Step and function definition::

        @step("Test IO <standardValue> test safe IO <safeValue> loop <timeoutSeconds>")
        def testIOTestSafeIOLoop(standardValue, safeValue, timeoutSeconds):

    Example usage:
        * Test IO "1" test safe IO "1" loop "300"
    """
    timeout = time.time() + int(timeoutSeconds)
    while timeout > time.time():
        readIO()
        writeIO(standardValue)
        time.sleep(0.5)
        readIO()
        verifyInput(standardValue)
        readIO()
        writeIO("0")
        time.sleep(0.5)
        readIO()
        verifyInput("0")
        verifyNCS("0", "16")
        getState()
        readSafeIO()
        writeSafeIO(safeValue)
        time.sleep(0.5)
        readSafeIO()
        verifySafeOutput(safeValue)
        readSafeIO()
        writeSafeIO("0")
        time.sleep(0.5)
        readSafeIO()
        verifySafeOutput("0")
        verifyConnections("2")
        verifyActiveConnections("2")
        Messages.write_message("=============================")
        Messages.write_message("Loop iteration")
        Messages.write_message("=============================")

##########################################################################
# after scenario tasks
###
@after_scenario
def afterScenarioHook():
    """
    Goes through all variables named in the Before Scenario Hook and calls the related method to close CAPI.

    """
    if data_store.scenario["safeEnabled"]:
        results = data_store.scenario["capiController"].disableSafeConnection()
        Messages.write_message(results["description"])
    if data_store.scenario["safeOpenInterface"]:
        results = data_store.scenario["capiController"].closeSafeInterface()
        Messages.write_message(results["description"])
    if data_store.scenario["safeInit"]:
        results = data_store.scenario["capiController"].safeExit()
        Messages.write_message(results["description"])
    if data_store.scenario["pingOpen"]:
        results = data_store.scenario["capiController"].pingClose()
        Messages.write_message(results["description"])
    if data_store.scenario["arpRegistered"]:
        results = data_store.scenario["capiController"].arpUnregister()
        Messages.write_message(results["description"])
    if data_store.scenario["startProtocol"]:
        results = data_store.scenario["capiController"].stopProtocol()
        Messages.write_message(results["description"])
    if data_store.scenario["openInterface"]:
        results = data_store.scenario["capiController"].closeInterface()
        Messages.write_message(results["description"])
    if data_store.scenario["init"]:
        results = data_store.scenario["capiController"].exit()
        Messages.write_message(results["description"])
    Messages.write_message("capi after scenario completed")