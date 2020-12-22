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
# EIP

<!--
//////////////////////////////////////////////////////////////////////////
/ eip f-host scenario f-host
///
-->
## Cycle Power EIP F-Host

Tags: f-host, eip, cycle-power

Will need to connect and verify connection, then toggle output and read input

* Hard reset device
* Wait "30"

<!--
//////////////////////////////////////////////////////////////////////////
/ cycle power scenario f-host
///
-->
## Cycle Power F-Host EIP Conformance

Tags: f-host, eip, conformance, cycle-power

Power cycle and verify the device is connected to the PC

* Connect to serial ports
* Clear "SS1" serial port
* Hard reset device
* Find "netbc_init SUCCESS" on "SS1" serial port "120"
* Wait "10"

<!--
//////////////////////////////////////////////////////////////////////////
/ configure card scenario f-host eip
///
-->
## Configure Card F-Host EIP

Tags: f-host, eip, config

The card needs the current configuration removed and a new configuration to be downloaded

* Connect to device "0"
* Download configuration "SSREIP_ssr1_1_81_start_yes.bin"
* Verify configuration
* Wait "30"

<!--
//////////////////////////////////////////////////////////////////////////
/ configure card scenario f-host eip
///
-->
## Configure Card F-Host EIP Conformance

Tags: f-host, eip, config, conformance

The card needs the current configuration removed and a new configuration to be downloaded

* Connect to device "0"
* Download configuration "SSREIP.bin"
* Verify configuration
* Wait "30"

<!--
//////////////////////////////////////////////////////////////////////////
/ conformance test f-host
///
-->
## EIP Conformance Test F-Host

Tags: f-host, eip, conformance-test

This will run an EIP conformance test

* Run conformance tests

