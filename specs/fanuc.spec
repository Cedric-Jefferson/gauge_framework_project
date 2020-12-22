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
# Fanuc

<!--
//////////////////////////////////////////////////////////////////////////
/ cycle power scenario f-host
///
-->
## Cycle Power Fanuc

Tags: f-host, fanuc, cycle-power

Power cycle and verify the device is connected to the PC

* Hard reset device
* Verify device is connected to PC

<!--
//////////////////////////////////////////////////////////////////////////
/ configure card scenario f-host
///
-->
## Configure Card F-Host Profinet1

Tags: f-host, fanuc, config, port-25, profinet1

The card needs the current configuration removed and a new configuration to be downloaded

* Connect to device "0"
* Download configuration "f-host_port-25.bin"
* Verify configuration

<!--
//////////////////////////////////////////////////////////////////////////
/ configure card scenario f-host
///
-->
## Configure Card F-Host Profinet2

Tags: f-host, fanuc, config, port-26, profinet2

The card needs the current configuration removed and a new configuration to be downloaded

* Connect to device "0"
* Download configuration "f-host_port-26.bin"
* Verify configuration

<!--
//////////////////////////////////////////////////////////////////////////
/ factory flash scenario f-host
///
-->
## Connect And Verify Fanuc

Tags: f-host, fanuc, verify-connect

Connect to the card and verify the IP, Name, and Firmware version

* Connect to device "0"
* Get card info
* Verify "fanuc-cnc-ctrl" card name
* Verify "192.168.1.10" ip address
* Verify firmware version

<!--
//////////////////////////////////////////////////////////////////////////
/ scan network scenario f-host
///
-->
## Scan Network F-Host Profinet1

Tags: f-host, fanuc, scan-network, profinet1

The card will need to scan the network and verify IO is active

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Verify "2" connections
* Verify "2" active connections

<!--
//////////////////////////////////////////////////////////////////////////
/ scan network scenario f-host
///
-->
## Scan Network F-Host Profinet2

Tags: f-host, fanuc, scan-network, profinet2

The card will need to scan the network and verify IO is active

* Reserve "profinet2"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Verify "2" connections
* Verify "2" active connections

<!--
//////////////////////////////////////////////////////////////////////////
/ io verification scenario f-host
///
-->
## IO Status Test F-Host Profinet1

Tags: f-host, fanuc, io-status, profinet1

This test verifys getting io status and enabling/disabling io

* Reserve "profinet1"
* Connect to device "0"
* Get IO status "0"
* Get safe IO status "0"
* Start protocol
* Start standard connections "0"
* Get IO status "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get safe IO status "0"
* Get state
* Get connection info
* Verify "2" connections
* Verify "2" active connections
* Get IO status "0"
* Get safe IO status "0"
* Test IO "1"
* Test safe IO "1"
* Change connection state "0" "0"
* Get IO status "0"
* Get safe IO status "0"
* Change connection state "0" "1"
* Get IO status "0"
* Get safe IO status "0"
* Start protocol
* Start standard connections "0"
* Get IO status "0"
* Get safe IO status "0"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ io verification scenario f-host
///
-->
## IO Verification F-Host Profinet1

Tags: f-host, fanuc, io-verify, profinet1

Will need to connect and verify connection, then toggle output and read input

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Verify "2" connections
* Verify "2" active connections
* Test IO "1"
* Test safe IO "1"

<!--
//////////////////////////////////////////////////////////////////////////
/ io verification scenario f-host
///
-->
## IO Verification F-Host Profinet2

Tags: f-host, fanuc, io-verify, profinet2

Will need to connect and verify connection, then toggle output and read input

* Reserve "profinet2"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Verify "2" connections
* Verify "2" active connections
* Test IO "1"
* Test safe IO "1"

<!--
//////////////////////////////////////////////////////////////////////////
/ loop test scenario f-host
///
-->
## Looping Test F-Host Profinet1 test1

Tags: f-host, fanuc, loop-test, profinet1, test1

Loop through test on timeout until fail

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Test IO "1"
* Test safe IO "1"
* Verify "2" connections
* Verify "2" active connections
* Test IO "1" test safe IO "1" loop "120"

<!--
//////////////////////////////////////////////////////////////////////////
/ loop test scenario f-host
///
-->
## Looping Test F-Host Profinet1 test2

Tags: f-host, fanuc, loop-test, profinet1, test2

Loop through test on timeout until fail

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Test IO "1"
* Test safe IO "1"
* Verify "2" connections
* Verify "2" active connections
* Test IO "1" test safe IO "1" loop "240"

<!--
//////////////////////////////////////////////////////////////////////////
/ loop test scenario f-host
///
-->
## Looping Test F-Host Profinet1 test3

Tags: f-host, fanuc, loop-test, profinet1, test3

Loop through test on timeout until fail

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Test IO "1"
* Test safe IO "1"
* Verify "2" connections
* Verify "2" active connections
* Test IO "1" test safe IO "1" loop "60"

<!--
//////////////////////////////////////////////////////////////////////////
/ loop test scenario f-host
///
-->
## Looping Test F-Host Profinet2

Tags: f-host, fanuc, loop-test, profinet2

Loop through test on timeout until fail

* Reserve "profinet2"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Connect to safe device "0"
* Start safe connections "0"
* Get state
* Get connection info
* Test IO "1"
* Test safe IO "1"
* Verify "2" connections
* Verify "2" active connections
* Test IO "1" test safe IO "1" loop "120"

<!--
//////////////////////////////////////////////////////////////////////////
/ arp scenario f-host
///
-->
## ARP Test F-Host Profinet1

Tags: f-host, fanuc, arp-test, profinet1

The card will run an arp test

* Wireshark start
* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* ARP register
* ARP use "192.168.1.12"
* ARP start "192.168.1.12" "0" "0" "0"
* Wait "30"
* ARP unregister
* Wait "1"
* Wireshark stop
* Wireshark generate json "./wireshark.cap"
* Wireshark arp count "5" "192.168.1.10" "192.168.1.12"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ arp scenario f-host case7
///
-->
## ARP Test F-Host-case7

Tags: f-host, fanuc, arp-test, profinet1, case7

The card will run an arp test

* Reserve "profinet1"
* Wireshark start
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* ARP register
* ARP use "192.168.1.12"
* ARP start "192.168.1.12" "10" "1000" "10000"
* Wait "15"
* ARP unregister
* Wait "1"
* Wireshark stop
* Wireshark generate json "./wireshark.cap"
* Wireshark arp count "10" "192.168.1.10" "192.168.1.12"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ arp scenario f-host case1
/ with parameters: 
/ Probes=4 
/ Interval = 2000  ms
/ Timeout=0 (which means 4*2000=8000ms)
///
-->
## ARP Test F-Host 4-2000-0 N5 totestextraarps

Tags:  f-host, fanuc, arp-test, profinet1, f-host-fullrun, PCT_95794

The card will run an arp test

* Wireshark start
* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* ARP register
* ARP use "192.168.1.12"
* ARP start "192.168.1.12" "4" "2000" "0"
* Wait "15"
* ARP unregister
* Wireshark stop
* Wireshark generate json "./wireshark.cap"
* Wireshark arp count "4" "192.168.1.10" "192.168.1.12"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ arp scenario f-host 
///
-->
## ARP Test F-Host test2

Tags:  f-host, fanuc, arp-test, f-host-fullrun, PCT_95794

The card will run an arp test

* Wireshark start
* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* ARP register
* ARP use "192.168.1.12"
* ARP start "192.168.1.12" "10" "2000" "0"
* Wait "25"
* ARP unregister
* Wireshark stop
* Wireshark generate json "./wireshark.cap"
* Wireshark arp count "10" "192.168.1.10" "192.168.1.12"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ arp scenario f-host 
///
-->
## ARP Test F-Host test3

Tags: f-host, fanuc, arp-test, f-host-fullrun, PCT_95794

The card will run an arp test

* Wireshark start
* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* ARP register
* ARP use "192.168.1.12"
* ARP start "192.168.1.12" "10" "2000" "20000"
* Wait "25"
* ARP unregister
* Wireshark stop
* Wireshark generate json "./wireshark.cap"
* Wireshark arp count "10" "192.168.1.10" "192.168.1.12"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ arp scenario f-host 
///
-->
## ARP Test F-Host test4

Tags: f-host, fanuc, arp-test, f-host-fullrun, PCT_95794

The card will run an arp test

* Wireshark start
* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* ARP register
* ARP use "192.168.1.12"
* ARP start "192.168.1.12" "10" "2000" "8000"
* Wait "30"
* ARP unregister
* Wireshark stop
* Wireshark generate json "./wireshark.cap"
* Wireshark arp count "10" "192.168.1.10" "192.168.1.12"
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ ping scenario f-host
///
-->
## Ping Test F-Host

Tags: f-host, fanuc, ping-test, profinet1

The card will run a ping test

* Reserve "profinet1"
* Wireshark start
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get state
* Get connection info
* Ping open "192.168.1.12" "0" "0"
* Wait "30"
* Get ping stats
* Get ping error no
* Ping close
* Wireshark stop
* Unreserve "profinet1"

<!--
//////////////////////////////////////////////////////////////////////////
/ hb scenario f-host
///
-->
## HB Test F-Host

Tags: f-host, fanuc, hb-test, profinet1

The card will run the hb test

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get connection info
* Get state
* HB start "500"
* Wait "10"
* HB stop
* Wait "2"
* Get state
<!-- * Unreserve "profinet1" -->

<!--
//////////////////////////////////////////////////////////////////////////
/ hb scenario f-host
///
-->
## HB Fail Test F-Host

Tags: f-host, fanuc, hb-test, hb-fail

The card will run the hb test

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get connection info
* Get state
* HB start "500"
* Wait "10"
* HB fail
* Wait "2"
* Get state
<!-- * Unreserve "profinet1" -->

<!--
//////////////////////////////////////////////////////////////////////////
/ poll scenario f-host
///
-->
## Poll Test F-Host

Tags: f-host, fanuc, hb-test, poll

The card will run the hb test

* Reserve "profinet1"
* Connect to device "0"
* Start protocol
* Start standard connections "0"
* Get connection info
* Get state
* Poll start "500"
* Wait "10"
* Poll stop
<!-- * Unreserve "profinet1" -->

<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Blink Test
///
-->
## Messaging Blink Test 1

Tags: f-host, fanuc, message, blink, profinet1

Call CAPI Send Message with Service ID for Blink

* Reserve "profinet1"
* Connect to device "0"
* Send message blink "00:A0:91:30:4B:29" "254"
* Send message blink "00:0F:9E:ED:E2:C4" "254"

<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Set IP Test
///
-->
## Messaging Set IP Test 1

Tags: f-host, fanuc, message, set-ip, profinet1

Call CAPI Send Message with Service ID for Set IP

* Reserve "profinet1"
* Connect to device "0"
* Send message set ip "1" "1" "192.168.1.13" "255.255.255.0" "0.0.0.0" "00:A0:91:30:4B:29" "254"
* Wait "2"
* Ping "192.168.1.13"
* Send message set ip "1" "1" "192.168.1.12" "255.255.255.0" "0.0.0.0" "00:A0:91:30:4B:29" "254"
* Wait "2"
* Ping "192.168.1.12"

<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Set Name Test
///
-->
## Messaging Set Name Test 1

Tags: f-host, fanuc, message, set-name, profinet1

Call CAPI Send Message with Service ID for Set Name

* Reserve "profinet1"
* Connect to device "0"
* Send message set name "1" "14" "harshio600-epn" "00:A0:91:30:4B:29" "254"

<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Factory Reset Profinet 1 Safety Block
///
-->
## Messaging Factory Reset Safety Block 1

Tags: f-host, fanuc, message, factory-reset, safety, profinet1

Factory reset the Murr safety block

* Reserve "profinet1"
* Connect to device "0"
* Send message factory reset "00:0F:9E:ED:E2:C4" "254"
* Wait "30"
* Send message set ip "1" "1" "192.168.1.31" "255.255.255.0" "0.0.0.0" "00:0F:9E:ED:E2:C4" "254"
* Wait "2"
* Ping "192.168.1.31"
* Send message set name "1" "5" "murr2" "00:0F:9E:ED:E2:C4" "254"


<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Blink Test
///
-->
## Messaging Blink Test 2

Tags: f-host, fanuc, message, blink, profinet2

Call CAPI Send Message with Service ID for Blink

* Reserve "profinet2"
* Connect to device "0"
* Send message blink "00:A0:91:31:B5:09" "254"
* Send message blink "00:0F:9E:F7:51:0C" "254"

<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Set IP Test
///
-->
## Messaging Set IP Test 2

Tags: f-host, fanuc, message, set-ip, profinet2

Call CAPI Send Message with Service ID for Set IP

* Reserve "profinet2"
* Connect to device "0"
* Send message set ip "1" "1" "192.168.1.13" "255.255.255.0" "0.0.0.0" "00:A0:91:31:B5:09" "254"
* Wait "2"
* Ping "192.168.1.13"
* Send message set ip "1" "1" "192.168.1.12" "255.255.255.0" "0.0.0.0" "00:A0:91:31:B5:09" "254"
* Wait "2"
* Ping "192.168.1.12"

<!--
//////////////////////////////////////////////////////////////////////////
/ Messaging Set Name Test
///
-->
## Messaging Set Name Test 2

Tags: f-host, fanuc, message, set-name, profinet2

Call CAPI Send Message with Service ID for Set Name

* Reserve "profinet2"
* Connect to device "0"
* Send message set name "1" "14" "harshio600-epn" "00:A0:91:31:B5:09" "254"