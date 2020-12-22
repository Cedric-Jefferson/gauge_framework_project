##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   CAPI Test Functions for Test Automation in Gauge Framework
#
##########################################################################

##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, after_scenario, before_scenario
import time
import os
import json
import sys
import struct
import pickle
import grpc
sys.path.append(r"../grpc_library")
import embedded_automation_pb2
import embedded_automation_pb2_grpc

##########################################################################
# constants
###
CMTP_BUFFER_LEN = 1024

##########################################################################
# before scenario setup
###
@before_scenario
def beforeScenarioHook():
    data_store.scenario["init"] = False
    data_store.scenario["openInterface"] = False
    data_store.scenario["startProtocol"] = False
    data_store.scenario["safeInit"] = False
    data_store.scenario["safeOpenInterface"] = False
    data_store.scenario["safeEnabled"] = False
    data_store.scenario["pingOpen"] = False
    data_store.scenario["arpRegistered"] = False
    data_store.scenario["capiServerAddress"] = "localhost:4502"
    data_store.scenario["capiRPCChannel"] = grpc.insecure_channel(data_store.scenario["capiServerAddress"])
    data_store.scenario["capiRPCStub"] = embedded_automation_pb2_grpc.embeddedAutomationServiceStub(data_store.scenario["capiRPCChannel"])
    Messages.write_message("capi before scenario completed")

##########################################################################
# standard card methods
###
# init step
###
@step("Init")
def init():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi init request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIInit(request)
    Messages.write_message("capi init returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Init failed"
    data_store.scenario["init"] = True
###
# enum drivers
###
@step("Enum drivers <index>")
def enumDrivers(index):
    dataStr = json.dumps({"index": index})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi enum drivers request",
        data = dataStr
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIEnumDrivers(request)
    Messages.write_message("enum drivers returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Enum drivers failed"
###
# open interface at index
###
@step("Open interface <index>")
def openInterface(index):
    dataStr = json.dumps({"index": index})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi open interface request",
        data = dataStr
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIOpenInterface(request)
    Messages.write_message("open interface returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Open interface failed"
    data_store.scenario["openInterface"] = True
###
# get card info
###
@step("Get card info")
def getCardInfo():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get card info request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetCardInfo(request)
    Messages.write_message("open interface returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Open interface failed"
    responseData = json.loads(response.data)
    data_store.scenario["productName"] = str(responseData["productName"])
    Messages.write_message("Product name: {}".format(data_store.scenario["productName"]))
    data_store.scenario["ipAddr"] = str(responseData["ipAddr"])
    Messages.write_message("IP addr: {}".format(data_store.scenario["ipAddr"]))
    data_store.scenario["firmwareVersion"] = str(responseData["firmwareVersion"])
    Messages.write_message("Firmware version: {}".format(data_store.scenario["firmwareVersion"]))
###
# soft reset
###
@step("Soft reset device")
def softResetDevice():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi soft reset request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISoftReset(request)
    Messages.write_message("capi soft reset returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Soft reset failed"
###
# start standard connections
###
@step("Start standard connections <index>")
def startStandardConnection(index):
    # refresh IO
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi refresh io request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIRefreshIO(request)
    Messages.write_message("capi refresh io returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Refresh IO failed"
    # start all connections
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi start all connections request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIStartAllConnections(request)
    Messages.write_message("capi Start all connections returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Start all connections failed"
    # start produce
    requestData = json.dumps({"index": int(index)})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi start produce request",
        data = requestData
    )
    produceResponse = data_store.scenario["capiRPCStub"].rpcCAPIStartProduce(request)
    produceResponseData = json.loads(produceResponse.data)
    assert produceResponseData["produceFunctionStop"] == False
    # start consume
    requestData = json.dumps({"index": int(index)})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi start consume request",
        data = requestData
    )
    consumeResponse = data_store.scenario["capiRPCStub"].rpcCAPIStartConsume(request)
    consumeResponseData = json.loads(consumeResponse.data)
    assert consumeResponseData["consumeFunctionStop"] == False
    time.sleep(consumeResponseData["consumeFunctionDuty"])
###
# start protocol
###
@step("Start protocol")
def startProtocol():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi start protocol request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIStartProtocol(request)
    Messages.write_message("start protocol returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Start protocol failed"
    data_store.scenario["startProtocol"] = False
###
# stop protocol
###
@step("Stop protocol")
def stopProtocol():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi stop protocol request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIStopProtocol(request)
    Messages.write_message("stop protocol returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Stop protocol failed"
###
# get connection info
###
@step("Get connection info")
def getConnectionInfo():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get connection info request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetConnectionInfo(request)
    Messages.write_message("get connection info returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Get connection info failed"
    responseData = json.loads(response.data)
    data_store.scenario["numConnections"] = responseData["numConnections"]
    Messages.write_message("Number of connections: {}".format(data_store.scenario["numConnections"]))
    data_store.scenario["numActConnections"] = responseData["numActConnections"]
    Messages.write_message("Active connections: {}".format(data_store.scenario["numActConnections"]))
###
# get state
###
@step("Get state")
def getState():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get state request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIReadState(request)
    Messages.write_message("get state returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Get state failed"
    responseData = json.loads(response.data)
    Messages.write_message("State: {}".format(responseData["state"]))
    Messages.write_message("IO State: {}".format(responseData["ioState"]))
    Messages.write_message("Ch1 State: {}".format(responseData["ch1State"]))
    Messages.write_message("Ch2 State: {}".format(responseData["ch2State"]))
    Messages.write_message("Ch1 IO State: {}".format(responseData["ch1IOState"]))
    Messages.write_message("Ch2 IO State: {}".format(responseData["ch2IOState"]))
    Messages.write_message("Ch2 IO State: {}".format(responseData["ch2IOState"]))
###
# read io
###
@step("Read IO")
def readIO():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi read IO request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIReadIO(request)
    Messages.write_message("read IO returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "read IO failed"
    responseData = json.loads(response.data)
    data_store.scenario["producedIO"] = responseData["produced"]
    Messages.write_message("Produced: {}".format(data_store.scenario["producedIO"]))
    data_store.scenario["consumedIO"] = responseData["consumed"]
    Messages.write_message("Consumed: {}".format(data_store.scenario["consumedIO"]))
###
# write io
###
@step("Write IO <value>")
def writeIO(value):
    newProduceData = list(data_store.scenario["producedIO"])
    newProduceData[0] = int(value)
    newProduceData = tuple(newProduceData)
    requestData = pickle.dumps(newProduceData)
    request = embedded_automation_pb2.bytesRequest(
        result = 0,
        description = "capi write IO request",
        bytesData = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIWriteIO(request)
    Messages.write_message("write IO returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "write IO failed"
    Messages.write_message("Write: {}".format(newProduceData))
    responseData = json.loads(response.data)
    time.sleep(responseData["produceFunctionDuty"])
###
# start all connections
###
@step("Start all connections")
def startAllConnections():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi Start all connections request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcStartAllConnections(request)
    Messages.write_message("start all connections exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Start all connections failed"
###
# refresh io
###
@step("Refresh IO")
def refreshIO():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi refresh IO request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIRefreshIO(request)
    Messages.write_message("refresh IO returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Refresh IO failed"
###
# ping open
###
@step("Ping open <ip> <interval> <length>")
def pingOpen(ip, interval, length):
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address format is wrong"
    interval = int(interval)
    length = int(length)
    if interval == 0:
        interval = 15
    if length == 0:
        length = 10
    requestData = json.dumps({
        "ip": ip,
        "interval": interval,
        "length": length
    })
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ping open request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIPingOpen(request)
    Messages.write_message("ping open returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ping open failed"
    data_store.scenario["pingOpen"] = True
###
# ping close
###
@step("Ping close")
def pingClose():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ping close request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIPingClose(request)
    Messages.write_message("ping close returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ping close failed"
    data_store.scenario["pingOpen"] = False
###
# get ping stats
###
@step("Get ping stats")
def getPingStats():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ping get stats request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetPingStats(request)
    Messages.write_message("ping get stats returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ping get stats failed"
    responseData = json.loads(response.data)
    if responseData != "":
        data_store.scenario["transmitted"] = str(responseData["transmitted"])
        Messages.write_message("Number of transmitted PING requests: {}".format(data_store.scenario["transmitted"]))
        data_store.scenario["received"] = str(responseData["received"])
        Messages.write_message("Number of received PING reply packets: {}".format(data_store.scenario["received"]))
        data_store.scenario["duplicated"] = str(responseData["duplicated"])
        Messages.write_message("Number of duplicated PING reply packets: {}".format(data_store.scenario["duplicated"]))
        data_store.scenario["lastRTT"] = str(responseData["lastRTT"])
        Messages.write_message("Round trip time of the last PING in millisec: {}".format(data_store.scenario["lastRTT"]))
        data_store.scenario["maxRTT"] = str(responseData["maxRTT"])
        Messages.write_message("Maximum round trip time in millisec: {}".format(data_store.scenario["maxRTT"]))
        data_store.scenario["minRTT"] = str(responseData["minRTT"])
        Messages.write_message("Minimum round trip time in millisec: {}".format(data_store.scenario["minRTT"]))
        data_store.scenario["avrRTT"] = str(responseData["avrRTT"])
        Messages.write_message("Average round trip time in millisec: {}".format(data_store.scenario["avrRTT"]))
        data_store.scenario["sumRTT"] = str(responseData["sumRTT"])
        Messages.write_message("Sum of all round trip time in millisec: {}".format(data_store.scenario["sumRTT"]))
        data_store.scenario["sendErrorCode"] = str(responseData["sendErrorCode"])
        Messages.write_message("PING send request error code if any: {}".format(data_store.scenario["sendErrorCode"]))
        data_store.scenario["recvErrorCode"] = str(responseData["recvErrorCode"])
        Messages.write_message("PING recv error code if any: {}".format(data_store.scenario["recvErrorCode"]))
    else:
        assert False, "Returned with empty data"
###
# get ping error no
###
@step("Get ping error no")
def getPingErrorNo():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get ping error-no request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetPingErrorNo(request)
    Messages.write_message("ping get error no returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Get ping error-no failed"
    responseData = json.loads(response.data)
    if responseData != "":
        data_store.scenario["pingErrNo"] = hex(responseData["pingErrNo"])
        Messages.write_message("Last error Number: {}".format(data_store.scenario["pingErrNo"]))
    else:
        assert False, "Returned with empty data"
###
# arp register
###
@step("ARP register")
def arpRegister():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ARP register request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIArpRegister(request)
    Messages.write_message("ARP register returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ARP register failed"
    data_store.scenario["arpRegistered"] = True
###
# arp use
###
@step("ARP use <ip>")
def arpUse(ip):
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address is wrong"
    requestData = json.dumps({"ip": ip})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ARP use IP request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIArpUseIP(request)
    Messages.write_message("ARP use IP returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ARP use IP failed"
###
# arp start
###
@step("ARP start <ip> <probe> <interval> <timeout>")
def arpStart(ip, probe, interval, timeout):
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address format is wrong"
    probe = int(probe)
    interval = int(interval)
    timeout = int(timeout)
    data_store.scenario["arpStartTime"] = time.time()
    requestData = json.dumps({
        "ip": ip,
        "probe": probe,
        "interval": interval,
        "timeout": timeout
    })
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ARP start request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIArpStart(request)
    Messages.write_message("ARP start returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ARP start failed"
###
# arp cancel
###
@step("ARP cancel <ip>")
def arpCancel(ip):
    ip = list(map(int, ip.split(".")))
    assert len(ip) == 4, "IP address format is wrong"
    requestData = json.dumps({"ip": ip})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ARP cancel request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIArpCancel(request)
    Messages.write_message("ARP cancel returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ARP cancel failed"
###
# arp unregister
###
@step("ARP unregister")
def arpUnregister():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi ARP unregister request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIArpUnregister(request)
    Messages.write_message("ARP register unreturned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "ARP unregister failed"
    data_store.scenario["arpRegistered"] = False
###
# hb start
###
@step("HB start <heartBeat>")
def hbStart(heartBeat):
    heartBeat = int(heartBeat)
    requestData = json.dumps({"heartBeat": heartBeat})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi heartbeat start request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIHbStart(request)
    Messages.write_message("heartbeat start returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "heartbeat start failed"
###
# hb stop
###
@step("HB stop")
def hbStop():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi heartbeat stop request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIHbStop(request)
    Messages.write_message("heartbeat stop returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "heartbeat stop failed"
###
# hb fail
###
@step("HB fail")
def hbFail():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi fail heartbeat request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIHbFail(request)
    Messages.write_message("fail heartbeat returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "fail heartbeat failed"
###
# poll start
###
@step("Poll start <dutyCycle>")
def pollStart(dutyCycle):
    dutyCycle = int(dutyCycle)
    requestData = json.dumps({"dutyCycle": dutyCycle})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi poll start request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIPollStart(request)
    Messages.write_message("poll start returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "poll start failed"
###
# poll stop
###
@step("Poll stop")
def pollStop():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi poll stop request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIPollStop(request)
    Messages.write_message("poll stop returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "poll stop failed"
###
# change connection state
###
@step("Change connection state <index> <state>")
def changeConnectionState(index, state):
    index = int(index)
    state = bool(int(state))

    requestData = json.dumps({
        "index": index,
        "state": state
    })
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi change connection state request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIChangeConnectionState(request)
    Messages.write_message("change connection state returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "change connection state failed"
###
# get io status
###
@step("Get IO status <index>")
def getIOStatus(index):
    index = int(index)
    requestData = json.dumps({"index": index})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get io status request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetIOStatus(request)
    Messages.write_message("get io status returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Get IO status failed"
    responseData = json.loads(response.data)
    data_store.scenario["producedStatus"] = responseData["producedStatus"]
    Messages.write_message("Produced Status: {}".format(data_store.scenario["producedStatus"]))
    data_store.scenario["consumedStatus"] = responseData["consumedStatus"]
    Messages.write_message("Consumed Status: {}".format(data_store.scenario["consumedStatus"]))
###
# send blink message
###
@step("Send message blink <byMac> <dataLength>")
def sendMessageBlink(byMac, dataLength):
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message blink request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message blink returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message blink failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send set ip message
###
@step("Send message set name <dwRemanent> <dwNameLength> <szName> <byMac> <dataLength>")
def sendMessageSetName(dwRemanent, dwNameLength, szName, byMac, dataLength):
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message set name request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message set name returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message set name failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send set ip message
###
@step("Send message set ip <dwRemanent> <dwIPMode> <byIPAddr> <byIPMask> <byIPGateway> <byMac> <dataLength>")
def sendMessageSetIP(dwRemanent, dwIPMode, byIPAddr, byIPMask, byIPGateway, byMac, dataLength):
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message set ip request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message set ip returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message set ip failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send read explicit message
###
@step("Send message read explicit <dwConfID> <dwCrc32> <wDeviceNumber> <dwApi> <wSlotNumber> <wSubSlotNumber> <wIndex> <wLengthDataToRead> <dataLength>")
def sendMessageReadExplicit(dwRemanent, dwIPMode, byIPAddr, byIPMask, byIPGateway, byMac, dataLength):
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message read explicit request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message set name returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message read explicit failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    assert responseData.result == 0, "read explicit failed"
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send write explicit message
###
@step("Send message write explicit <dwConfID> <dwCrc32> <wDeviceNumber> <dwApi> <wSlotNumber> <wSubSlotNumber> <wIndex> <dataToWrite> <dataLength>")
def sendMessageWriteExplicit(dwRemanent, dwIPMode, byIPAddr, byIPMask, byIPGateway, byMac, dataLength):
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message write explicit request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message write explicit returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message write explicit failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send identify message
###
@step("Send message identify")
def sendMessageIdentify():
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message identify request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message identify returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message identify failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send get device detected message
###
@step("Send message get device detected")
def sendMessageGetDeviceDetected():
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message get device request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message get device returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message get device failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
###
# send blink message
###
@step("Send message factory reset <byMac> <dataLength>")
def sendMessageFactoryReset(byMac, dataLength):
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
    # serialize data to bytes-like object for gRPC transmission
    serializedData = pickle.dumps(data)
    request = embedded_automation_pb2.capiMessageRequest(
        result = 0,
        description = "capi send message factory reset request",
        bytesData = serializedData,
        serviceID = serviceID,
        dataLength = dataLength
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISendMessage(request)
    Messages.write_message("send message factory reset returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Send message factory reset failed"
    # load the stringified response data into a dictionary object
    responseData = json.loads(response.data)
    Messages.write_message("Received Status: {}".format(responseData["status"]))
    Messages.write_message("Received Service: {}".format(responseData["service"]))
    Messages.write_message("Received Size: {}".format(responseData["size"]))
    dataString = ""
    for i, resultData in enumerate(responseData["data"]):
        if i % 4 == 0:
            dataString += "\n"
            dataString += "{0:0{1}X}: ".format(i, 4)
            dataString += "{0:0{1}X} ".format(resultData, 2)
        else:
            dataString += "{0:0{1}X} ".format(resultData, 2)
    Messages.write_message("Received Data: \n{}".format(dataString))
    assert responseData["status"] == 0, "Status from response is non-zero - {}".format(responseData["status"])
    
##########################################################################
# safe card steps
###
# safe init
###
@step("Safe init")
def safeInit():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi safe init request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPISafeInit(request)
    Messages.write_message("safe init returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Safe init failed"
###
# open safe interface
###
@step("Open safe interface <index>")
def openSafeInterface(index):
    requestData = json.dumps({"index": int(index)})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi open safe interface request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIOpenSafeInterface(request)
    Messages.write_message("open safe interface exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Open safe interface failed"
    data_store.scenario["safeOpenInterface"] = True
###
# read safe config
###
@step("Read safe config")
def readSafeConfig():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi read safe config request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIReadSafeConfig(request)
    Messages.write_message("read safe config returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Read safe config failed"
###
# enable safe connection
###
@step("Enable safe connection")
def enableSafeConnection():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi enable safe connection request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIEnableSafeConnection(request)
    Messages.write_message("enable safe connection returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Enable safe connection failed"
    data_store.scenario["safeEnabled"] = True
###
# start safe connections
###
@step("Start safe connections <index>")
def startSafeConnections(index):
    # refresh Safe IO
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi refresh safe io request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIRefreshSafeIO(request)
    Messages.write_message("capi refresh safe io returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Refresh safe IO failed"
    # start safe produce
    requestData = json.dumps({"index": int(index)})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi start safe produce request",
        data = requestData
    )
    produceResponse = data_store.scenario["capiRPCStub"].rpcCAPIStartSafeProduce(request)
    produceResponseData = json.loads(produceResponse.data)
    assert produceResponseData["produceSafeFunctionStop"] == False
    # start consume
    requestData = json.dumps({"index": int(index)})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi start safe consume request",
        data = requestData
    )
    consumeResponse = data_store.scenario["capiRPCStub"].rpcCAPIStartSafeConsume(request)
    consumeResponseData = json.loads(consumeResponse.data)
    assert consumeResponseData["consumeSafeFunctionStop"] == False
    time.sleep(consumeResponseData["consumeSafeFunctionDuty"])
###
# read safe io
###
@step("Read safe IO")
def readSafeIO():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi read safe IO request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIReadSafeIO(request)
    Messages.write_message("read IO returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "read safe IO failed"
    responseData = json.loads(response.data)
    data_store.scenario["producedSafeIO"] = responseData["produced"]
    Messages.write_message("Safe Produced: {}".format(data_store.scenario["producedSafeIO"]))
    data_store.scenario["consumedSafeIO"] = responseData["consumed"]
    Messages.write_message("Safe Consumed: {}".format(data_store.scenario["consumedSafeIO"]))
###
# write safe io
###
@step("Write safe IO <value>")
def writeSafeIO(value):
    newProduceData = list(data_store.scenario["producedSafeIO"])
    newProduceData[0] = int(value)
    newProduceData = tuple(newProduceData)
    requestData = pickle.dumps(newProduceData)
    request = embedded_automation_pb2.bytesRequest(
        result = 0,
        description = "capi write safe IO request",
        bytesData = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIWriteSafeIO(request)
    Messages.write_message("write safe IO returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "write safe IO failed"
    Messages.write_message("Write: {}".format(newProduceData))
    Messages.write_message("Response data: {}".format(response.data))
    responseData = json.loads(response.data)
    time.sleep(responseData["produceSafeFunctionDuty"])
###
# change ncs
###
@step("Change NCS <value>")
def changeNCS(value):
    requestData = json.dumps({"ncsStatus": int(value)})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi change NCS connection request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIChangeNCS(request)
    Messages.write_message("change NCS returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "change NCS failed"
###
# get ncs
###
@step("Get NCS")
def getNCS():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get NCS request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetNCS(request)
    Messages.write_message("capi get NCS returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "get NCS failed"
    responseData = json.loads(response.data)
    data_store.scenario["producedNSC"] = responseData["producedNSC"]
    Messages.write_message("Produced NCS: {}".format(data_store.scenario["producedNSC"]))
    data_store.scenario["consumedNSC"] = responseData["consumedNSC"]
    Messages.write_message("Consumed NCS: {}".format(data_store.scenario["consumedNSC"]))
###
# ncs loop
###
@step("Get NCS loop <value>")
def getNCSLoop(value):
    timeout = time.time() + float(value)
    while (time.time() < timeout):
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi get NCS request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIGetNCS(request)
        responseData = json.loads(response.data) 
        Messages.write_message(response.description)
        Messages.write_message("Produced NCS: {}".format(responseData["producedNSC"]))
        Messages.write_message("Produced NCS: {}".format(responseData["consumedNSC"]))
        time.sleep(0.5)
###
# get safe io status
###
@step("Get safe IO status <index>")
def getIOStatus(index):
    index = int(index)
    requestData = json.dumps({"index": index})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi get safe io status request",
        data = requestData
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIGetSafeIOStatus(request)
    Messages.write_message("get io safe status returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Get safe IO status failed"
    responseData = json.loads(response.data)
    data_store.scenario["producedSafeStatus"] = responseData["producedStatus"]
    Messages.write_message("Produced Safe Status: {}".format(data_store.scenario["producedSafeStatus"]))
    data_store.scenario["consumedSafeStatus"] = responseData["consumedStatus"]
    Messages.write_message("Consumed Safe Status: {}".format(data_store.scenario["consumedSafeStatus"]))

##########################################################################
# configuration steps
###
# register
###
@step("Config register")
def configRegister():
    request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi config register request",
        flag = True
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPINotifyReq(request)
    Messages.write_message("capi configure register returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Register failed"
###
# unregister
###
@step("Config unregister")
def configUnregister():
    request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi config unregister request",
        flag = False
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPINotifyReq(request)
    Messages.write_message("capi configure unregister returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Unregister failed"
###
# lock
###
@step("Config lock")
def configLock():
    request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi config lock request",
        flag = True
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIConfigLockReq(request)
    Messages.write_message("capi config lock returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Config lock failed"
###
# unlock
###
@step("Config unlock")
def configUnlock():
    request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi config unlock request",
        flag = False
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIConfigLockReq(request)
    Messages.write_message("capi config unlock returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Config unlock failed"
###
# config mode
###
@step("Config mode")
def configMode():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi config mode request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIConfigMode(request)
    Messages.write_message("capi config mode returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Config mode failed"
###
# config reset
###
@step("Config reset")
def configReset():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi config reset request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIConfigReset(request)
    Messages.write_message("capi config reset returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Config reset failed"
    timeout = time.time() + 30
    configRead = False
    id_request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi read config ID request",
        flag = True
    )
    while (time.time() < timeout and configRead == False):
        x = data_store.scenario["capiRPCStub"].rpcCAPIReadConfigID(id_request)
        if (x.result == 0):
            configRead = True
    assert configRead == True, "Unable to confirm config was reset"
###
# write block - network config
###
@step("Write block network config")
def writeBlockNetworkConfig():
    try:
        dataString = json.dumps({"fileType": 10, "fileName":data_store.suite["configFile"]})
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi write block request",
            data = dataString
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIWriteBlock(request)
        Messages.write_message("capi write block returned exit code " + str(response.result) + ": " + response.description)
        assert response.result == 0, "Write block network config failed"
    except NameError:
        Messages.write_message("Load config was not called, there is no config to load")
        assert False, "NameError when trying to write configFile"
###
# write block - network config compressed
###
@step("Write block network config compressed")
def writeBlockNetworkConfigCompressed():
    try:
        dataString = json.dumps({"fileType": 11, "fileName":data_store.suite["configFile"]})
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi write block compressed request",
            data = dataString
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIWriteBlock(request)
        Messages.write_message("capi write block returned exit code " + str(response.result) + ": " + response.description)
        assert response.result == 0, "Write file to device failed"
    except NameError:
        Messages.write_message("Load config was not called, there is no config to load")
        assert False, "NameError when trying to write configFile"
###
# config validate
###
@step("Config validate")
def configValidate():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi config validate request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIConfigValidate(request)
    Messages.write_message("capi config validate returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Config validate failed"
###
# config apply
###
@step("Config apply")
def configApply():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "capi config apply compressed request",
        data = ""
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIConfigApply(request)
    Messages.write_message("capi config apply returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Config apply failed"
    timeout = time.time() + 30
    configRead = False
    id_request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi read config ID request",
        flag = True
    )
    while (time.time() < timeout and configRead == False):
        x = data_store.scenario["capiRPCStub"].rpcCAPIReadConfigID(id_request)
        if (x.result == 0):
            configRead = True
    assert configRead == True, "Cannot verify config"
##########################################################################
# verify steps
###
# verify config
###
@step("Verify configuration")
def verifyConfiguration():
    request = embedded_automation_pb2.flagRequest(
        result = 0,
        description = "capi read config ID request",
        flag = True
    )
    response = data_store.scenario["capiRPCStub"].rpcCAPIReadConfigID(request)
    Messages.write_message("capi verify config returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "Read config failed"
    responseData = json.loads(response.data)
    Messages.write_message("Device CRC: {}".format(hex(int(responseData["configDataCRC"]))))
    Messages.write_message("Database CRC: {}".format(data_store.suite["configCRC"]))
    Messages.write_message("{}".format(responseData))
    assert data_store.suite["configCRC"] == hex(int(responseData["configDataCRC"])), "Cannot verify config, database CRC: {}".format(data_store.suite["configCRC"])
###
# verify card name
###
@step("Verify <name> card name")
def verifyCardName(name):
    assert name == data_store.scenario["productName"], "{} != {}".format(name, data_store.scenario["productName"])
###
# verify ip address
###
@step("Verify <address> ip address")
def verifyIPAddress(address):
    assert address == data_store.scenario["ipAddr"], "{} != {}".format(address, data_store.scenario["ipAddr"])
###
# verify firmware version
###
@step("Verify firmware version")
def verifyFirmwareVersion():
    assert os.getenv("firmware_version") == data_store.scenario["firmwareVersion"], "{} != {}".format(os.getenv("firmware_version"), data_store.scenario["firmwareVersion"])
###
# verify number connections
###
@step("Verify <num> connections")
def verifyConnections(num):
    assert data_store.scenario["numConnections"] == int(num), "{} != {}".format(int(num), data_store.scenario["numConnections"])
###
# verify number active connections
###
@step("Verify <num> active connections")
def verifyActiveConnections(num):
    assert data_store.scenario["numActConnections"] == int(num), "{} != {}".format(int(num), data_store.scenario["numActConnections"])
###
# verify input
###
@step("Verify input <value>")
def verifyInput(value):
    assert data_store.scenario["consumedIO"][0] == int(value), "{} != {}".format(int(value), data_store.scenario["consumedIO"][0])
###
# verify safe output
###
@step("Verify safe output <value>")
def verifySafeOutput(value):
    assert data_store.scenario["producedSafeIO"][0] == int(value), "{} != {}".format(int(value), data_store.scenario["producedSafeIO"][0])
###
# verify ncs
###
@step("Verify NCS <val1> or <val2>")
def verifyNCS(val1, val2):
    assert data_store.scenario["consumedNSC"] == int(val1) or data_store.scenario["consumedNSC"] == int(val2), "{} != {} or {}".format(data_store.scenario["consumedNSC"], int(val1), int(val2))

##########################################################################
# automation steps
###
# io test loop
###
@step("Test IO <standardValue> test safe IO <safeValue> loop <timeoutSeconds>")
def testIOTestSafeIOLoop(standardValue, safeValue, timeoutSeconds):
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
    if data_store.scenario["safeEnabled"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi disable safe connection request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIDisableSafeConnection(request)
        Messages.write_message("capi disable safe connection returned exit code " + str(response.result) + ": " + response.description)
    if data_store.scenario["safeOpenInterface"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi close safe interface request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPICloseSafeInterface(request)
        Messages.write_message("capi close safe interface returned exit code " + str(response.result) + ": " + response.description)
    if data_store.scenario["safeInit"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi safe exit request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPISafeExit(request)
        Messages.write_message("capi safe exit returned exit code " + str(response.result) + ": " + response.description)
    if data_store.scenario["pingOpen"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi ping close request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIPingClose(request)
        Messages.write_message(response.description)
    if data_store.scenario["arpRegistered"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi ARP unregister request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIArpUnregister(request)
        Messages.write_message(response.description)
    if data_store.scenario["startProtocol"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi stop protocol request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIStopProtocol(request)
        Messages.write_message(response.description)
    if data_store.scenario["openInterface"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi close interface request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPICloseInterface(request)
        Messages.write_message("close interface returned exit code " + str(response.result) + ": " + response.description)
    if data_store.scenario["init"]:
        request = embedded_automation_pb2.basicRequest(
            result = 0,
            description = "capi exit request",
            data = ""
        )
        response = data_store.scenario["capiRPCStub"].rpcCAPIExit(request)
        Messages.write_message("capi exit returned exit code " + str(response.result) + ": " + response.description)
    Messages.write_message("capi after scenario completed")
