<!--
//////////////////////////////////////////////////////////////////////////
/
/   MOLEX Ltd. Test Spec
/   developed by Raman Brar
/   raman.brar@molex.com
/
/  Managed-Switch Sanity Test for Test Automation
/
//////////////////////////////////////////////////////////////////////////
-->

<!--
//////////////////////////////////////////////////////////////////////////
/ spec definition
///
-->
# Managed-switch

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