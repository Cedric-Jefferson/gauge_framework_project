##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Raman Brar
#   raman.brar@molex.com
#
#   General Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``ixnetwork_library`` is used for this Step Implementation file. All Steps are in the ``ixnetwork.py`` file.
Go to the Concepts to see any concepts that simplify the steps.
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, after_step, data_store, after_scenario, before_scenario
import sys
import json

sys.path.append(r"../ixnetwork_library")

try:
    from  IxnetworkLibrary import IxnetworkController
except Exception as exc:
    print("import IxnetworkLibrary:: {} occured: {}".format(type(exc).__name__, exc))

##########################################################################
# before scenario setup
###
@before_scenario
def beforeScenarioHook():
    """
    Initializes variables:
        * ``data_store.scenario["ixiaConnected"]`` is set to ``False`` so that no Step can be run unless the PyLogix Controller class is created.
        * ``data_store.scenario["IxnetworkController"]``  is set to None so the IxnetworkController class constructor can be called again.
        * ``data_store.scenario["ixiaPortsConfigured"]`` is set to false so that ports are configured before configuring the topology.
        * ``data_store.scenario["configureTopologyAndDeviceGroup"]`` is set to false so that toplogy and device groups are configured before configuring protocol.
        * ``data_store.scenario["configureProtocolInterfaces"]`` is set to false so that protocol interface is configured before creating the traffic item.
        * ``data_store.scenario["createTrafficItem"]`` is set to false so that traffic item is created before creating the traffic.
        * ``data_store.scenario["startTraffic"]`` is set to false so that traffic is started before stoping and reading the statistics of traffic.
    """
    data_store.scenario["IxnetworkController"] = None
    data_store.scenario["ixiaConnected"] = False
    data_store.scenario["ixiaPortsConfigured"] = False
    data_store.scenario["configureTopologyAndDeviceGroup"] = False
    data_store.scenario["configureProtocolInterfaces"] = False
    data_store.scenario["createTrafficItem"] = False
    data_store.scenario["startTraffic"] = False
    Messages.write_message("Ixnetwork before scenario completed")

##########################################################################
# methods
###
# Connect to IXIA
###
@step("Connect to ixia <ipAddress> <sessionName> <clearConfig>")
def connectToIxia(ipAddress, sessionName, clearConfig):
    """
    Connects to the chassis of ixia.

    Args:
        ipAddress (str, optional): IP address of ixia device. Defaults to '192.168.0.200'.
        sessionName (str, optional): Name of the ixia session. Defaults to 'TX_to_RX'.
        clearConfig (bool, optional): Clear the configuration of previous session if there is a sessions with the same name. Defaults to True.

    Step and function definition::

        @step("Connect to ixia")
        def connectToIxia():

    Example usage:
        * Connect to ixia  "192.168.0.200" "TX_to_RX" "True"
    """
    clearConfig = json.loads(clearConfig.lower())

    if ipAddress == "":
        ipAddress = '192.168.0.200'
    if sessionName == "":
        sessionName = 'TX_to_RX'
    if clearConfig == "":
        clearConfig = True
    elif isinstance(clearConfig, bool) == False:
        assert False, "clearConfig can only take the value True or False please set the values accordingly"

    data_store.scenario["IxnetworkController"] = IxnetworkController()
    results = data_store.scenario["IxnetworkController"].connectToChassis(ipAddress = ipAddress,
                                                                          sessionName = sessionName,
                                                                          clearConfig = clearConfig)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Connect to ixia failed"
    data_store.scenario["ixiaConnected"] = True

@step("Configure ports <portIds> <forceOwnership>")
def configurePorts(portIds, forceOwnership):
    """
     Create port resources and connect to the hardware ports.

    Args:
        portIds (list, optional): Ports number of ixia ports which you wanna connect to. Defaults to [1,2].
        forceOwnership (bool, optional): Forcefully connect to the ports. Defaults to True.

    Step and function definition::

        @step("Configure ports <portIds>")
        def configurePorts(portIds):

    Example usage:
        * Configure ports "1, 2" "True"
    """
    assert data_store.scenario["ixiaConnected"] == True, "ixia chassis is not connected"
    if portIds != "":
        portIdList = [int(x) for x in portIds.split(",")]
        Messages.write_message("data to echo: {}".format("".join("0x{:02X} ".format(x) for x in portIdList)))
    else:
        portIdList = [1, 2]
        Messages.write_message("PortIds are not given, it will take the default values")
    assert len(portIdList) == 2, "port ID list should have two ports, one as source and other as destination."

    forceOwnership = json.loads(forceOwnership.lower())
    if forceOwnership == "":
        forceOwnership = True
    elif isinstance(forceOwnership, bool) == False:
        assert False, "forceOwnership can only take the value True or False please set the values accordingly"

    results = data_store.scenario["IxnetworkController"].configurePorts(portIdList = portIdList,
                                                                        forceOwnership = forceOwnership)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Configure ports failed"
    data_store.scenario["ixiaPortsConfigured"] = True

@step("Configure topology and device group <topologyName> <deviceGroupName> <portId> <multiplier>")
def configureTopologyAndDeviceGroup(topologyName, deviceGroupName, portId, multiplier):
    """
    Configure topology and device group.

    Args:
        topologyName (string): Name of the topology.
        deviceGroupName (string): Name of the device group.
        portIdList (int): PortId for the topology.
        multiplier (str, optional): multiplier. Defaults to '1'.

    Step and function definition::

        @step("Configure topology and device group <topologyName> <deviceGroupName> <portId> <multiplier>")
        def configureTopologyAndDeviceGroup(topologyName, deviceGroupName, portId, multiplier):

    Example Usage:
        * Configure topology and device group "Ethernet Topology 1" "Ethernet Device Group 1" "1" "1"
    """
    assert data_store.scenario["ixiaPortsConfigured"] == True, "ixia ports are not configured"
    assert topologyName != "", "Please provide the topology name."
    assert deviceGroupName != "", "Please provide the device group name."
    assert portId != "", "Please don't leave the port ID empty"
    if multiplier == "":
        multiplier = '1'
        Messages.write_message("multiplier value is not given, it will use the default value '1' ")

    results = data_store.scenario["IxnetworkController"].configureTopology(topologyName = topologyName,
                                                                           portId = int(portId),
                                                                           multiplier = multiplier)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Configure topology failed"
    results = data_store.scenario["IxnetworkController"].configureDeviceGroup(topologyName = topologyName,
                                                                              deviceGroupName = deviceGroupName,
                                                                              multiplier = multiplier)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Configure device group failed"
    data_store.scenario["configureTopologyAndDeviceGroup"] = True

@step("Configure protocol interface <deviceGroupName> <protocolName> <mtuValue>")
def configureProtocolInterfaces(deviceGroupName, protocolName, mtuValue):
    """
    Configure protocol interfaces.

    Args:
        deviceGroupName (string): Name of the device group.
        protocolName (string): Name of the protocol.
        mtuValue (int, optional): Maximum Transmission Unit. Defaults to 1500.

    Step and function definition::

        @step("Configure protocol interface <deviceGroupName> <protocolName> <mtuValue>")
        def configureProtocolInterfaces(deviceGroupName, protocolName, mtuValue):

    Example Usage:
        * Configure protocol interface "Ethernet Device Group 1" "Ethernet 1" "1500"
    """
    assert data_store.scenario["configureTopologyAndDeviceGroup"] == True, "Topology and device group is not configured"
    assert deviceGroupName != "", "Please provide the device group name."
    assert protocolName != "", "Please provide the protocol name."

    if mtuValue == "":
        mtuValue = "1500"
        Messages.write_message("mtuValue value is not given, it will use the default value '1500' ")

    results = data_store.scenario["IxnetworkController"].configureProtocolInterfaces(deviceGroupName = deviceGroupName,
                                                                                     protocolName = protocolName,
                                                                                     mtuValue = mtuValue)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Configure Protocol Interface failed"
    data_store.scenario["configureProtocolInterfaces"] = True

@step("Create traffic item <trafficItemName> <trafficType> <biDirectional> <sourcePortId> <destPortId>")
def createTrafficItem(trafficItemName, trafficType, biDirectional, sourcePortId, destPortId):
    """
    Create traffic item.

    Args:
        trafficItemName (str): Name of the traffic item.e.g. value 'Traffic Test'.
        trafficType (str): Type of traffic. e.g. value 'Ethernet'.
        sourcePortId (int): Port ID of traffic source. e.g. value 1.
        destPortId (int): Port ID of traffic destination. e.g. value 2.
        biDirectional(bool): Traffic is unidirectional or bidirectional. Defaults to True.

    Step and function definition::

        @step("Create traffic item <trafficItemName> <trafficType> <biDirectional> <sourcePortId> <destPortId>")
        def createTrafficItem(trafficItemName, trafficType, biDirectional, sourcePortId, destPortId):

    Example Usage:
        * Create traffic item "Traffic Test" "Ethernet" "True" "1" "2"
    """
    biDirectional = json.loads(biDirectional.lower())
    assert trafficItemName != "", "Please provide name for traffic item."
    assert sourcePortId != "", "Please provide value for source port ID."
    assert destPortId != "", "Please provide value for destination port ID."
    sourcePortId = int(sourcePortId)
    destPortId   = int(destPortId)

    if isinstance(biDirectional, bool) == False:
        assert False, "biDirectional can only take the value True or False please set the values accordingly"

    if trafficType != "Ethernet":
        assert False, "Presently, only Ethernet traffic type is supported please set trafficType to Ethernet"

    results = data_store.scenario["IxnetworkController"].createTrafficItem(trafficItemName = trafficItemName,
                                                                           trafficType = trafficType,
                                                                           biDirectional = biDirectional,
                                                                           sourcePortId = sourcePortId,
                                                                           destPortId = destPortId)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Create traffic item failed"
    data_store.scenario["createTrafficItem"] = True

@step("Configure traffic item <frameSize> <percentLineRate> <etherTypeValue>")
def configTrafficItem(frameSize, percentLineRate, etherTypeValue):
    """
    Configure the traffic item parameters.

    Args:
        frameSize (int, optional): Size of the frame. Defaults to 245.
        percentLineRate (str, optional): Line rate of traffic. Defaults to '100'.
        etherTypeValue (str, optional): Specify protocol of ethernet. Value is in hexadecimal. defaults to 'ffff'

    Step and function definition::

        @step("Configure traffic item <frameSize> <percentLineRate> <etherTypeValue>")
        def configTrafficItem(frameSize, percentLineRate, etherTypeValue):

    Example Usage:
        * Configure traffic item "245" "100" "ffff"
    """
    assert data_store.scenario["createTrafficItem"] == True, "Traffic item is not created"

    if percentLineRate == "":
        percentLineRate = '100'
        Messages.write_message("percentLineRate value is not given, it will use the default value '100' ")

    if etherTypeValue == "":
        etherTypeValue = "ffff"
        Messages.write_message("etherTypeValue value is not given, it will use the default value 'ffff' ")

    if frameSize == "":
        frameSize = 245
        Messages.write_message("frameSize value is not given, it will use the default value 245 ")

    frameSize = int(frameSize)
    results = data_store.scenario["IxnetworkController"].configTrafficItem(frameSize = frameSize,
                                                                           percentLineRate = percentLineRate,
                                                                           etherTypeValue = etherTypeValue)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Configure traffic item failed"

@step("Start traffic")
def startTraffic():
    """
    Push ConfigElement settings down to HighLevelStream resources.
    Apply traffic to hardware and start traffic.

    Step and function definition::

        @step("Start traffic")
        def startTraffic():

    Example Usage:
        * Start traffic
    """
    assert data_store.scenario["createTrafficItem"] == True, "Traffic item is not created"

    results = data_store.scenario["IxnetworkController"].startTraffic()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Start traffic failed"
    data_store.scenario["startTraffic"] = True

@step ("Print statistics")
def printStatistics():
    """
    Print Statistics of traffic.

    Step and function definition::

        @step("Start traffic")
        def startTraffic():

    Example Usage:
        * Print statistics
    """
    assert data_store.scenario["startTraffic"] == True, "Traffic is not started"
    results = data_store.scenario["IxnetworkController"].printStatistics()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Print statistics failed"

@step ("Stop traffic")
def stopTraffic():
    """
    Stop traffic.

    Step and function definition::

        @step ("Stop traffic")
        def stopTraffic():

    Example Usage:
        * Stop traffic
    """
    assert data_store.scenario["startTraffic"] == True, "Traffic is not started"
    results = data_store.scenario["IxnetworkController"].stopTraffic()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Stop traffic failed"