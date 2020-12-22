<!--
//////////////////////////////////////////////////////////////////////////
/
/   MOLEX Ltd. Test Spec
/   developed by Steve Korber
/   Steve.Korber@molex.com
/
/   Osprey Sanity Test for Test Automation
/
//////////////////////////////////////////////////////////////////////////
-->

<!--
//////////////////////////////////////////////////////////////////////////
/ spec definition
///
-->
# Osprey

<!--
//////////////////////////////////////////////////////////////////////////
/ confirm boot scenario
///
-->
## Cycle Power Osprey

Tags: osprey, io, cycle-power

Verify boot of device

* Hard reset device
* Find "Initialize safety layer" on "SS1" serial port "120"

<!--
//////////////////////////////////////////////////////////////////////////
/ verify plc connection scenario
///
-->
## Verify PLC Connection

Tags: osprey, io, verify-plc

Verify device can connect to Allen Bradley PLC

* Reserve "ab_plc1"
* Wireshark start
* Wait "10"
* PyLogix connect
* Wait "5"
* PyLogix read tag "Osprey_MVP_2:I.ConnectionFaulted" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].4" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].5" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].6" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].7" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].4" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].5" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].6" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].7" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].4" value "1" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].5" value "1" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].6" value "1" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].7" value "1" check "False"
* Wait "2"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].4" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].5" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].6" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].7" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].4" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].5" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].6" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].7" check "False"
* Wait "2"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].4" value "0" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].5" value "0" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].6" value "0" check "False"
* PyLogix write tag "Osprey_MVP_2:O.Data[0].7" value "0" check "False"
* Wait "2"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].4" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].5" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].6" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[0].7" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].4" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].5" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].6" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0].7" check "False"
* Wait "2"
* PyLogix read tag "Osprey_MVP_2:O.Data[0]" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[1]" check "False"
* PyLogix read tag "Osprey_MVP_2:O.Data[2]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[0]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[1]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[2]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[3]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[4]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[5]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[6]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[7]" check "False"
* PyLogix read tag "Osprey_MVP_2:I.Data[8]" check "False"
* PyLogix disconnect
* Wireshark stop

<!--
//////////////////////////////////////////////////////////////////////////
/ verify plc connection scenario
///
-->
## Verify Config Webpage

Tags: osprey, io, verify-config

Verify config.html can be changed

* Send shell command "apk update && apk add font-noto libwmf libexif udev chromium chromium-chromedriver xvfb" "False"
* Selenium connect "chrome"
* Selenium navigate "http://192.168.1.10:8081/usr/config.html"
* Wait "3"
* Selenium save screenshot
* Wait "3"
* Selenium select by value "ID" "item1_on_off_filter_time" "10"
* Selenium select by value "ID" "item2_on_off_filter_time" "10"
* Selenium select by value "ID" "item3_on_off_filter_time" "10"
* Selenium select by value "ID" "item4_on_off_filter_time" "10"
* Selenium select by value "ID" "item5_on_off_filter_time" "10"
* Selenium select by value "ID" "item6_on_off_filter_time" "10"
* Selenium select by value "ID" "item7_on_off_filter_time" "10"
* Selenium select by value "ID" "item8_on_off_filter_time" "10"
* Selenium select by value "ID" "item9_on_off_filter_time" "10"
* Selenium select by value "ID" "item10_on_off_filter_time" "10"
* Selenium select by value "ID" "item11_on_off_filter_time" "10"
* Selenium select by value "ID" "item12_on_off_filter_time" "10"
* Selenium select by value "ID" "item1_off_on_filter_time" "10"
* Selenium select by value "ID" "item2_off_on_filter_time" "10"
* Selenium select by value "ID" "item3_off_on_filter_time" "10"
* Selenium select by value "ID" "item4_off_on_filter_time" "10"
* Selenium select by value "ID" "item5_off_on_filter_time" "10"
* Selenium select by value "ID" "item6_off_on_filter_time" "10"
* Selenium select by value "ID" "item7_off_on_filter_time" "10"
* Selenium select by value "ID" "item8_off_on_filter_time" "10"
* Selenium select by value "ID" "item9_off_on_filter_time" "10"
* Selenium select by value "ID" "item10_off_on_filter_time" "10"
* Selenium select by value "ID" "item11_off_on_filter_time" "10"
* Selenium select by value "ID" "item12_off_on_filter_time" "10"
* Selenium select by value "ID" "item9_port_direction" "1"
* Selenium select by value "ID" "item10_port_direction" "1"
* Selenium select by value "ID" "item11_port_direction" "1"
* Selenium select by value "ID" "item12_port_direction" "1"
* Selenium select by value "ID" "item9_output_source" "0"
* Selenium select by value "ID" "item10_output_source" "0"
* Selenium select by value "ID" "item11_output_source" "0"
* Selenium select by value "ID" "item12_output_source" "0"
* Selenium select by value "ID" "item13_output_source" "0"
* Selenium select by value "ID" "item14_output_source" "0"
* Selenium select by value "ID" "item15_output_source" "0"
* Selenium select by value "ID" "item16_output_source" "0"
* Selenium click "Class" "btn-apply"
* Selenium save screenshot
* Wait "30"
* Selenium save screenshot
* Wait "3"
* Selenium get text "ID" "config_status_p" "Download successful. Please power-cycle the system for the changes to take effect."
* Hard reset device
* Find "Initialize safety layer" on "SS1" serial port "120"
* Selenium navigate "http://192.168.1.10:8081/usr/config.html"
* Wait "3"
* Selenium save screenshot
* Wait "3"
* Selenium disconnect