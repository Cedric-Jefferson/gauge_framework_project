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
# OPC Demo

<!--
//////////////////////////////////////////////////////////////////////////
/ opc demo scenario 
///
-->
## OPC Demo Sanity

Tags: sanity-test

Test for OPC Demo

* Startup windows subsystems
* Wait "5"
* OPC UA Client connect "opc.tcp://192.168.1.10:48020"
* OPC UA Client get node "ns=4;i=6001" "IN0"
* OPC UA Client get node "ns=4;i=6005" "OUT0"
* OPC UA Client get browse name "IN0"
* OPC UA Client get browse name "OUT0"
* OPC UA Client get value "IN0"
* OPC UA Client get value "OUT0"
* OPC UA Client set value "IN0" "2.2" "float"
* Wait "0.5"
* OPC UA Client get value "IN0"
* OPC UA Client get value "OUT0"
* OPC UA Client set value "IN0" "3.3" "float"
* Wait "0.5"
* OPC UA Client get value "IN0"
* OPC UA Client get value "OUT0"
* Stop windows subsystems

<!--
//////////////////////////////////////////////////////////////////////////
/ opc demo scenario 
///
-->
## Web Services/OPC UA Demo Sanity

Tags: osprey

Test for OPC Demo

* Clear "SS1" serial port
* FTP connect "192.168.1.10"
* FTP login "root" "root"
* FTP nlst
* FTP cwd "/dev/shmem"
* Send shell command "cp ../configurations/opc_demo_osprey/config.bin ." "False"
* Send shell command "ls" "False"
* FTP storebinary "config.bin"
* FTP nlst
* Wait "60"
* Hard reset device
* Wait "60"
* OPC UA Client connect "opc.tcp://192.168.1.10:48020"
* OPC UA Client get node "ns=4;i=6001" "IN0"
* OPC UA Client get node "ns=4;i=6005" "OUT0"
* OPC UA Client get browse name "IN0"
* OPC UA Client get browse name "OUT0"
* OPC UA Client get value "IN0"
* OPC UA Client get value "OUT0"
* OPC UA Client set value "IN0" "2.2" "float"
* Wait "0.5"
* OPC UA Client get value "IN0"
* OPC UA Client get value "OUT0"
* OPC UA Client set value "IN0" "3.3" "float"
* Wait "0.5"
* OPC UA Client get value "IN0"
* OPC UA Client get value "OUT0"
