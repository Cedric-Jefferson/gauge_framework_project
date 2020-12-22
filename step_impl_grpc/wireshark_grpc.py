##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   Wireshark Test Functions for Test Automation in Gauge Framework
#
##########################################################################

##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, after_scenario, before_scenario
import time
import json
import os
import sys
import grpc
sys.path.append(r"../grpc_library")
import embedded_automation_pb2
import embedded_automation_pb2_grpc

##########################################################################
# before suite
###
@before_scenario
def beforeScenarioHook():
    data_store.suite["wiresharkCount"] = 0
    data_store.scenario["wiresharkServerAddress"] = "localhost:4504"
    data_store.scenario["wiresharkRPCChannel"] = grpc.insecure_channel(data_store.scenario["wiresharkServerAddress"])
    data_store.scenario["wiresharkRPCStub"] = embedded_automation_pb2_grpc.embeddedAutomationServiceStub(data_store.scenario["wiresharkRPCChannel"])

##########################################################################
# methods
###
# wireshark start
###
@step("Wireshark start")
def wiresharkStart():
    requestData = json.dumps({"interface": os.getenv("wireshark_interface")})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "wireshark start request",
        data = requestData
    )
    response = data_store.scenario["wiresharkRPCStub"].rpcWiresharkStart(request)
    Messages.write_message("wireshark start returned exit code " + str(response.result) + ": " + response.description)
    data_store.scenario["wiresharkEnabled"] = True
    time.sleep(2) # let tshark start
###
# wireshark stop
###
@step("Wireshark stop")
def wiresharkStop():
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "wireshark stop request",
        data = ""
    )
    response = data_store.scenario["wiresharkRPCStub"].rpcWiresharkStop(request)
    Messages.write_message("wireshark stop returned exit code " + str(response.result) + ": " + response.description)
    data_store.scenario["wiresharkEnabled"] = False
###
# wireshark generate json
###
@step("Wireshark generate json <filename>")
def wiresharkGenerateJson(filename):
    # for gRPC implementation, wireshark lib makes the capture file in its own automation-lib dir
    plainFilename = filename.replace("./", "")
    workspacePath = os.getenv("workspace_path")
    filename = os.path.join(workspacePath,"wireshark_library", plainFilename)
    assert os.path.exists(filename), "wireshark capture file does not exist"
    requestData = json.dumps({"filename": filename})
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "wireshark generate json request",
        data = requestData
    )
    response = data_store.scenario["wiresharkRPCStub"].rpcWiresharkGenerateJson(request)
    Messages.write_message("wireshark generate JSON returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "wireshark generate json failed"
###
# arp count
###
@step("Wireshark arp count <count> <srcAddr> <dstAddr>")
def wiresharkArpCount(count, srcAddr, dstAddr):
    ip = list(map(int, srcAddr.split(".")))
    assert len(ip) == 4, "src IP address format is wrong"
    ip = list(map(int, dstAddr.split(".")))
    assert len(ip) == 4, "dst IP address format is wrong"
    count = int(count)
    requestData = json.dumps({
        "srcAddr": srcAddr,
        "dstAddr": dstAddr,
        "startTime": data_store.scenario["arpStartTime"]
    })
    request = embedded_automation_pb2.basicRequest(
        result = 0,
        description = "wireshark arp count request",
        data = requestData
    ) 
    response = data_store.scenario["wiresharkRPCStub"].rpcWiresharkArpCount(request)
    Messages.write_message("wireshark arp count returned exit code " + str(response.result) + ": " + response.description)
    assert response.result == 0, "wireshark arp count failed"
    responseData = json.loads(response.data)
    Messages.write_message("ARPs counted: {}".format(responseData["arpCount"]))
    assert (responseData["arpCount"] == count) or (responseData["arpCount"] == (count + 1)), "ARPs counted: {}, ARPs requested: {}".format(responseData["arpCount"], count)

##########################################################################
# after scenario
###
@after_scenario
def afterScenarioHook():
    if "wiresharkEnabled" in data_store.scenario:
        if data_store.scenario["wiresharkEnabled"]:
            request = embedded_automation_pb2.basicRequest(
                result = 0,
                description = "wireshark stop request",
                data = ""
            )
            response = data_store.scenario["wiresharkRPCStub"].rpcWiresharkStop(request)
            Messages.write_message("wireshark stop returned exit code " + str(response.result) + ": " + response.description)
            Messages.write_message("wireshark after scenario complete")
        else:
            Messages.write_message("wireshark already stopped")
        workspacePath = os.getenv("workspace_path")
        filename = os.path.join(workspacePath,"wireshark_library/wireshark.cap")
        if os.path.exists(filename):
            newFilename = os.path.join(workspacePath,"wireshark_library/wireshark_{}.cap".format(data_store.suite["wiresharkCount"]))
            data_store.suite["wiresharkCount"] += 1
            os.rename(filename, newFilename)