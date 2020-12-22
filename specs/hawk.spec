<!--
//////////////////////////////////////////////////////////////////////////
/
/   MOLEX Ltd. Test Spec
/   developed by Steve Korber
/   Steve.Korber@molex.com
/
/   Hawk F-Host Sanity Test for Test Automation
/
//////////////////////////////////////////////////////////////////////////
-->

<!--
//////////////////////////////////////////////////////////////////////////
/ spec definition
///
-->
# Hawk

<!--
//////////////////////////////////////////////////////////////////////////
/ cycle power scenario hawk
///
-->
## Cycle Power Hawk

Tags: f-host, hawk, cycle-power

Power cycle and verify the device is connected to the PC

* Hard reset device
* Wait "60"

<!--
//////////////////////////////////////////////////////////////////////////
/ factory flash scenario f-host
///
-->
## Connect And Verify Hawk

Tags: f-host, hawk, verify-connect

Connect to the card and verify the IP, Name, and Firmware version

* Connect to device "0"
* Get card info