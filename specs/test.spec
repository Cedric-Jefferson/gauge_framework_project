<!--
//////////////////////////////////////////////////////////////////////////
/
/   MOLEX Ltd. Test Spec
/   developed by Steve Korber
/   Steve.Korber@molex.com
/
/   Fanuc F-Host Sanity Test for Test Automation
/
//////////////////////////////////////////////////////////////////////////
-->

<!--
//////////////////////////////////////////////////////////////////////////
/ spec definition
///
-->
# Test

<!--
//////////////////////////////////////////////////////////////////////////
/ run-all test scenario f-host
///
-->
## Force Fail Test

Tags: test1, fail

* Force fail

<!--
//////////////////////////////////////////////////////////////////////////
/ run-all test scenario f-host
///
-->
## Force Pass Test

Tags: test2, pass

* Force pass

<!--
//////////////////////////////////////////////////////////////////////////
/ skip test scenario f-host
///
-->
## Force Skip Test

Tags: test3, skip

This spec will fail bacause it will force a skip

* Force skip

<!--
//////////////////////////////////////////////////////////////////////////
/ automation test 1
///
-->
## Automation Test 1

Tags: automation, test1

Test lookup

* Lookup protocol standard "profinet" safe ""
* Lookup protocol standard "profinet" safe "profisafe"
* Reserve "profinet1"
* Lookup protocol standard "profinet" safe ""
* Lookup protocol standard "profinet" safe "profisafe"
* Reserve "profinet2"
* Lookup protocol standard "profinet" safe ""
* Lookup protocol standard "profinet" safe "profisafe"
* Unreserve "profinet1"
* Lookup protocol standard "profinet" safe ""
* Lookup protocol standard "profinet" safe "profisafe"

<!--
//////////////////////////////////////////////////////////////////////////
/ automation test 2
///
-->
## Automation Test 2

Tags: automation, test2

Test lookup

* Lookup protocol standard "profinet" safe ""
* Reserve lookup tool
* Connect to device "0"
* Download lookup configuration "f-host"
* Verify configuration
* Get card info
* Verify "fanuc-cnc-ctrl" card name
* Verify "192.168.1.10" ip address
* Verify firmware version
* Unreserve lookup tool

<!--
//////////////////////////////////////////////////////////////////////////
/ check numato ethernet relay
///
-->
## Check Numato Ethernet Relay

Tags: check-relay

Verify Ethernet Relay

* Numato eth relay connect to "relay-1" at "192.168.1.201"
* Numato eth relay connect to "relay-2" at "192.168.1.202"
* Numato eth relay version at "relay-1"
* Numato eth relay version at "relay-2"
* Numato eth relay reset at "relay-1"
* Numato eth relay reset at "relay-2"
* Wait "2"
* Numato eth relay read all at "relay-1"
* Numato eth relay read all at "relay-2"
* Numato eth relay write all at "relay-1" with "1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0"
* Numato eth relay write all at "relay-2" with "1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0"
* Wait "2"
* Numato eth relay read all at "relay-1"
* Numato eth relay read all at "relay-2"
* Numato eth relay reset at "relay-1"
* Numato eth relay reset at "relay-2"

<!--
//////////////////////////////////////////////////////////////////////////
/ ixia Library Port 1 to port 2 data transfer
///
-->
## ixnetwork connectivity

tags: managed-switch

* Connect to ixia "192.168.0.200" "TX_to_RX" "True"
* Configure ports "1, 2" "True"
* Configure topology and device group "Ethernet Topology 1" "Ethernet Device Group 1" "1" "1"
* Configure topology and device group "Ethernet Topology 2" "Ethernet Device Group 2" "2" "1"
* Configure protocol interface "Ethernet Device Group 1" "Ethernet 1" "1500"
* Configure protocol interface "Ethernet Device Group 2" "Ethernet 2" "1500"
* Create traffic item "Traffic Test" "Ethernet" "True" "1" "2"
* Configure traffic item "245" "100" "ffff"
* Start traffic
* Print statistics
* Stop traffic

<!--
//////////////////////////////////////////////////////////////////////////
/ GPIO library testing
///
-->
## gpio

tags: gpio

* GPIO connect
* Init GPIO "329" "out"
* Read pin level "329"
* Set pin level "329" "False"
* Read pin level "329"
* Set pin level "329" "True"
* Read pin level "329"
* Set pin level "329" "False"
* Read pin level "329"
* Close sysfs GPIO "329"