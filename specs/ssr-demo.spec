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
# SSR

<!--
//////////////////////////////////////////////////////////////////////////
/ ssr f-host scenario f-host
///
-->
## SSR F-Host Cycle Power

Tags: f-host, ssr, cycle-power

Will need to connect and verify connection, then toggle output and read input

* Hard reset device ssr
* Wait "60"

<!--
//////////////////////////////////////////////////////////////////////////
/ nab scenario f-host
///
-->
## NAB F-Host Echo Data

Tags: f-host, ssr, nab-test, echo-data

Verify NAB Agent Echo Data with F-Host

* NAB connect
* NAB echo data "" "zero"
* NAB echo data "1, 1, 3, 51" "zero"
* NAB echo data "1, 2, 3, 4, 5, 6" "zero"

<!--
//////////////////////////////////////////////////////////////////////////
/ nab scenario f-host
///
-->
## NAB F-Host Inverse Data

Tags: f-host, ssr, nab-test, inverse-data

Verify NAB Agent Inverse Data with F-Host

* NAB connect
* NAB inverse data "" "zero"
* NAB inverse data "1, 1, 3, 51" "zero"
* NAB inverse data "1, 2, 3, 4, 5, 6" "zero"