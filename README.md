# Embedded Test Automation

* [Gauge Framework Project](#gauge-framework-project)
* [Gauge Framework General](#gauge-framework-general)
* [Test Plan](#test-plan)
* [Dynamic Variables](#dynamic-variables)
* [Gauge Framework API](#gauge-framework-api)

<a name="gauge-framework-project"></a>

## Gauge Framework Project

---

This is the Gauge Framework Project repo which hosts all Specifications used to run automated testing in the Automation Lab.

<br/><br/>

<a name="gauge-framework-general"></a>

## Gauge Framework General

---

There are three file types to be aware of when working with Gauge:

* Specification `.spec`
* Step Implementation `.py`
* Concept `.cpt`

The Specification files exist in the `specs` folder and there can be as many as needed. 

The Step Implementation files exist in the `step_impl` folder and there can be as many as needed.

The Concept files exist in the `specs > concepts` folder and there can be as many as needed.

### Specification Files

The Specification file contains all information that will define the name, tags, and order of the tests.

These files are writen in plain markdown syntax and there are three keys to be aware of:

* `#` is the Specification Header and there is only one per Specification file. This defines the name of the test suite.
* `##` is the Scenario Header and there can be as many as needed. This defines a single test case which consists of tags and steps.
* `*` is the Step Header and there can be as many as needed. This defines the step to be executed and is linked to the Step Implementation files.

Here is an example of a Specification file:

```
# Test Suite

## Test F-Host

This is a test for the F-Host card.

Tags: f-host, tag-a, tag-b

* Step 1
* Step 2

## Test Osprey

This is a test for the Osprey card.

Tags: osprey, tag-a, tag-c

* Step 1
* Step 2
* Concept 1
```

<br/>

### Step Implementation Files

The Step Implementation files are native Python and contain the code to action when the specifc Step or Hook is called.

Step Implementation files have a few key items:

#### Step Definitions

Step will need to be imported at the top of the Step Implementation file.

```python
from getgauge.python import step
```

The step is used to define the steps that can be used in the Specification file. The `@` decorator is used to implement the step in a Python function.

```python
@step("Test step")
def testStep():
    assert True
```

> Note: The string in the `"` is case sensitive.

Variables can be passed into the function by surrounding the string in `<>`. The variable passed will always be of type string. This means you will need to cast it as the specific variable type you want if you do not want a string.

```python
@step("Test step <var1>")
def testStep(var1):
    print(var1)
    assert True
```

The variable is passed into the step from the Specification file like this:

```
## Test

* Test step "variable"
```

#### Before and After Step/Scenario/Suite Hooks

Before and after Hooks are useful to use if there are things that need to be setup/torn down. There are three different types of Hooks: 

* Before/after suite; this will occur only per Specification (ie. `#`)
* Before/after scenario; this will occur once per Scenario (ie. `##`)
* Before/after scenario; this will occur once per Step (ie. `*`)

The hook will need to be imported into the Step Implementation file.

```python
from getgauge.python import before_suite, after_step, before_spec
```

They are used similar to the Steps, using the `@` decorator. Typically a before Hook is used to initialize some booleans in case we need to stop things in the after Hook.

```python
@before_suite
def beforeSuiteHook():
    data_store.suite["nabAgentConnected"] = False
```

#### Messages

Python has the `print` function but when running Gauge this will go to the Jenkins terminal (which can be harder to read/find). The best way to print something in Gauge is to use the built in `Messages` class.

Using the `Messages` class will print to the Gauge report which is attached to the Artifacts section of Jenkins.

Import this into the Step Implementation file before use.

```python
from getgauge.python import Messages
```

Once imported it can be used in the step to print to the report.

```python
@step("Print message <message>")
def printMessage(message):
    Messages.write_message(message)
```

#### Data Store

The `data_store` object is very useful as it can be used across suite/scenarios/specs. Again, this will need to be imported to be used.

```python
from getgauge.python import data_store
```

The `data_store` object can be accessed across Scenarios using `data_store.scenario`, across Specification file using `data_store.spec`, and across test suite using `data_store.suite`.

Typically we use this when we create the automation library controller class object as we typically will use it for the whole test suite.

```python
from getgauge.python import step, data_store, Messages

@step("Connect")
def connect():
    data_store.scenario["testController"] = testController()

@step("Function 1")
def func1():
    results = data_store.scenario["testController"].func1()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Function 1 failed"

@step("Function 2")
def func1():
    results = data_store.scenario["testController"].func2()
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Function 2 failed"
```

### Concepts

Concepts are Step functions, this means that they are a collection of Steps that can be used in a single Step of a Specification file rather then writing each Step everytime.

To create a Concept, add a `.cpt` file to the concepts folder. The Concept has the following structure:

```
# Hard reset device

Cycle power using the web relay

* Set web relay power "0"
* Wait "5"
* Set web relay power "1"
* Verify web relay status "0"
```

Now instead of using the 4 Steps to cycle power on the DUT we can simply use the single line in the Specification file.

```
# Test

## Test Scenario

Showing concepts

* Hard reset device
```

Concepts can also pass variables to be used in other steps. 

```
# Concept with a variable <var1> <var2>

* Print message <var1>
* Print message <var2>
```

This can be used in a Specification file like this:

```
# Test

## Test Scenario

Showing concepts

* Concept with a variable "hello" "world"
```

<br/><br/>

<a name="test-plan"></a>

## Test Plan

---

The test-plan.yml is used by Jenkins to perform the Gauge tests on the DUT. There are two main layers to the test-plan.yml:

### Dev

The `dev` layer is used for testing dummy products in the `Embedded_Automation_Sanity-Automated` pipeline. 

Currently the following products are supported:

* fanuc
* hawk
* eip (aka EIP-Prod)
* ssr (aka SSR-Demo)
* osprey_mvp_1.0

The product and hardware needs to be specified under the `dev` section:

```
dev:
  product: ssr
  ssr:
    bakery:
      - cycle-power: {passive: False, tags: f-host}
```

This is where the tests go, they are structured in the YAML as a list using a newline and `-`. The test case has two main parts: the Specification file name and a JSON object with `passive` and `tags` keys. The `passive` key takes boolean `True` or `False` and will determine whether the test will stop tests or continue to the next test. The `tags` key is used to filter the Scenarios in the Specification file. The `tags` determine the Scenarios based on boolean logic, see the Gauge website for more details.

Here is an example of a test suite in the test-plan.yml:

```
dev:
  product: ssr
  ssr:
    bakery:
      - cycle-power: {passive: False, tags: ssr}
      - nab: {passive: False, tags: f-host}
```

This will complete a factory flash of the latest factory flash images of the product specified on Artifactory, cycle the power on the f-host hardware, verify the boot of the system, and run the NAB agent Specification file with Scenarios that have the f-host tag.

Beyond the test cases there are other keys that can be specified on the `dev` layer to perform specific tasks:

* `latestBinary` can be specified to grab a specific factory image rather then the latest (ie. `latestBinary: /151`)
* `factoryRepo` can be specified to determine a specific repo on Artifactory to pull the latest factory image from (ie. `factoryRepo: ias-pre-prod`)
* `upgradeFirmware` can be specified to grab the latest user image from the same Artifactory repo as the factory image, this can be used to test NAB agent upgrade firmware (ie. `upgradeFirmware: /165`)
* `flashImage` can be specified to generate a factory or user image of the specific dummy product before the Gauge test runs, this will be discussed more below
* `forceFlashing` can be specified to force the bakery to flash factory  or upgrade image
* `conformance` can be specified at the bakery/lab level (specifically under eip) to run the conformance test files, this will be discusses more below
* `third-party` can be specified at the bakery/lab level to run third party test files, this will be discussed more below

> Note: All of these extra options are optional and do not need to be specified.<br/>

#### Flash Image

This key can be specified in the test-plan.yml to generate a factory or user image in the `Embedded_Automation_Sanity-Automated` pipeline. Here is an example:

```
dev:
  version: v0.0.6
  product: ssr
  flashImage:
    generateFlashImage: True
    imageType: factory
    firmwareRepo: ias-development
    firmwareBuildNumber: "591"
    fpgaRepo: ias-prod
    fpgaBuildNumber: ""
  ssr:
    bakery:
      - cycle-power: {passive: False, tags: ssr}
      - nab: {passive: False, tags: f-host}
```

The following keys are needed to successfully create a factory or user image in the test-plan.yml:

* `generateFlashImage` is a boolean value and will only create the image if set to `True`, if an image is not needed set the value to `False`
* `imageType` will determine the type of image created: factory and user are the two options
* `firmwareRepo` determines the repo on Artifactory where to gather the firmware from
* `firmwareBuildNumber` can be specified to grab a specific firmware version, use `firmwareBuildNumber: ""` to grab the latest
* `fpgaRepo` determines the repo on Artifactory where to gather the fpga from, for f-host hardware this will grab from Fanuc FPGA
* `fpgaBuildNumber` can be specified to grab a specific fpga version, use `fpgaBuildNumber: ""` to grab the latest

#### Conformance

This key can be defined to perform protocol conformance testing (EIP only for now, Profinet, and safety to come). The tests are defined in a list and are executed in order. The conformance files are placed in the `configurations` repo on Bitbucket in the `configurations/conformance/<product>/<hardware>/` folder. Here is an example:

```
dev:
  version: v0.0.6
  product: eip
  eip:
      bakery:
        - cycle-power: {passive: False, tags: eip & conformance}
        - config: {passive: False, tags: eip & conformance}
        - eip: {passive: False, tags: f-host}
      conformance:
        - F_Host_Assembly.txt
        - F_Host_Connection_Manager.txt
        - F_Host_Encapsulation.txt
```

### Third Party Tests

The `third-party` key is defined to perform third party tests/operations within a docker environment for the specified product. The tests are defined in a list and are executed in order. The docker-compose files are generated depending on parameters defined in `thirdparty_container_conf.yml` within the jenkins sanity repository.

```
dev:
  version: v0.0.6
  product: osprey_mvp_1.0
  osprey_mvp_1.0:
    bakery:
      - osprey: {passive: True, tags: cycle-power}
      - osprey: {passive: True, tags: verify-config}
      - osprey: {passive: True, tags: verify-plc}
    third-party:
      - test: logicals_front_end
```

### Prod

The `prod` layer is used by the dummy products (ie. SSR-Demo) and it determines which Gauge tests are to be run when the dummy product calls automation. This will only happen from the `master` branch.

The standard sequence of events would be as follows:

1. Create branch on `gauge_framework_project` repo
1. Add/create test cases in `dev` layer and test them in the `Embedded_Automation_Sanity-Automated` pipeline
1. Once tests are finalized and completed, add them to the `prod` layer

For example purposes, lets say we made a branch and created some new Scenarios in the `nab.spec` Specification file. The user added the tests with tags `newTest` and then ran them in the `Embedded_Automation_Sanity-Automated` pipeline by pushing code changs to their branch. Once the tests are completed and are running to the users liking, they can add the test case to the `prod` section of the test-plan.yml and complete a final push before opening a pull request. Here is an example of the test-plan.yml with the `prod` section after completing it in `dev`:

```
dev:
  version: v0.0.6
  product: ssr
  ssr:
    bakery:
      - cycle-power: {passive: False, tags: ssr}
      - nab: {passive: False, tags: f-host}
      - nab: {passive: False, tags: newTest}
prod:
  ssr:
    bakery:
      - cycle-power: {passive: False, tags: ssr}
      - nab: {passive: False, tags: newTest}
```
<br/><br/>
### Test-Plan GUI

The GUI for creating a yaml file is located under the `Jenkins-Sanity` repository. To get to the GUI, cd into Jenkins Sanity and under terminal, type:
```
python automation_utility.py --gui
```
Once this step is done, a pop-up GUI appears. The GUI is divided into 3 sections.
  - The first is the product name. Current products can be found when pressing the `Link to see products` under the product entry box. Once a product has been decided, type it in the entry box and select confirm.
  - The second section contains an `add tag` button which spawns 3 boxes at once i.e, `Test Case`, `True or False` for passive, and `Tags` respectively. As you keep clicking the `add tag` button, more rows of these entry boxes will spawn.
  - The final section is to select an output file name which automaticaly converts to yaml file (No need to add .yaml)

After all the necessary boxes are filled, select `Execute` to generate a yaml file with your specification which will then be located in the same directory.
<br/><br/>
### Docker-Containers
The `use-docker` tag signals to the pipeline whether or not to run the tests using containers. 

The `docker-containers` layer is used to specify which Docker containers should be spawned during test runs. It is a YAML list with fields as follows:
```
- container:
      image: <image name>
      force-pull: <boolean whether or not to force a docker-pull for this container image>
      container-name: <name for container>
      workingDir: <where to execute the commands below>
      commands:
        - "<command to run on during container startup>"
        - "<another command to run on during container startup>"
```

The tag `force-gauge-pull` is a boolean which informs Jenkins to pull any updates for the Gauge docker image. Since this is already done nightly for each of the bakeries, this can be left to `False` if you haven't merged any changes to the master branch's Gauge Dockerfile.     
<br/><br/>

<a name="dynamic-variables"></a>

## Dynamic Variables

---

Jenkins can push variables from the build dynamically to Gauge to be used during the test cases. The variables can be accessed the the Step Implementation file using the Python method `os.getenv(<var-name>)` and it will return a string of the variable that was pushed from Jenkins. The following list is what is currently being pushed into environment variables by Jenkins:

* `firmware_version` is the firmware version from Artifactory
* `config_filepath` is the network configuration folder path
* `automation_index` is the bakery number of the current node that is running the test
* `ss1_usb` is the ttyUSB or COM port the FTDI cable on SS1 UART is connected to
* `ss2_usb` is the ttyUSB or COM port the FTDI cable on SS2 UART is connected to
* `ss3_usb` is the ttyUSB or COM port the FTDI cable on SS3 UART is connected to
* `ss1_firmware_filepath` is the firmware path that SS1 firmware was saved to
* `ss2_firmware_filepath` is the firmware path that SS2 firmware was saved to
* `ss3_firmware_filepath` is the firmware path that SS3 firmware was saved to
* `upgrade_firmware_filepath` is the firmware path for the user image for upgrading
* `ss1_jflash_usb` is the serial number for the SS1 JLink device
* `ss2_jflash_usb` is the serial number for the SS2 JLink device
* `ss3_jflash_usb` is the serial number for the SS3 JLink device
* `trace32_library_path` is the TRACE32 library path on the node
* `wireshark_interface` is the interface name for Wireshark to use
* `trace32_script_path` is the path of the TRACE32 scripts
* `nodename` is the name of the Jenkins node
* `vlan_id` is the VLAN ID of the current node for rounting resources
* `ss1_jlink_script_filepath` is the filepath for the JLink script for SS1
* `ss1_jflash_program_filepath` is the filepath for the JFlash program project for SS1
* `ss2_jflash_program_filepath` is the filepath for the JFlash program project for SS2
* `ss3_jflash_program_filepath` is the filepath for the JFlash program project for SS3
* `ss2_jflash_unlock_filepath` is the filepath for the JFlash unlock project for SS2
* `ss3_jflash_unlock_filepath` is the filepath for the JFlash unlock project for SS3
* `workspace_path` is the current workspace path
* `product_type` is the product type that is running
* `standard_protocol` is the standard protocol used by the product
* `safe_protocol` is the safe protocol used by the product

<br/><br/>

<a name="gauge-framework-api"></a>

## Gauge Framework API

---

The Gauge Framework API section will categorize each Step Implementation File and go over the available Steps that can be used. It will also go over the needed Automation Libraries for the Step Implementation file. Documentation of step implementation is available [here](https://confluence.atlassian.molexcloud.com/pages/viewpage.action?pageId=116885008)

There have been Concepts created to make some tasks simpler, see the [Concepts](#concepts) section for more details.

<br/><br/>

<a name="concepts"></a>

### Concepts

---

Concepts have been implemented to simpify the Specification files. Below are links to the implemented Concepts:

* [Connect Device](#concepts-connect-device)
* [Connect Safe Device](#concepts-connect-safe-device)
* [Download Configuration Lookup](#concepts-download-configuration-lookup)
* [Download Compressed Configuration](#concepts-download-compressed-configuration)
* [Download Configuration](#concepts-download-configuration)
* [Hard Reset](#concepts-hard-reset)
* [Hard Reset SSR](#concepts-hard-reset-ssr)
* [Interrupt UBOOT](#concepts-interrupt-uboot)
* [Remove Configuration](#concepts-remove-configuration)
* [Test IO](#concepts-test-io)
* [Test Safe IO](#concepts-test-safe-io)
* [Verify PC Connection](#concepts-verify-pc-connection)

<br/>

<sub><sup>[top](#gauge-framework-api)</sup></sub>

<br/>

<a name="concepts-connect-device"></a>

#### Connect Device

Connects to the card at the given index. Exists as `connect_device.cpt`.

```
# Connect to device <index>

* Init
* Enum drivers <index>
* Open interface <index>
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `index` | int | Index of card. | `True` |

Example usage:

```
* Connect to device "0"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-connect-safe-device"></a>

#### Connect Safe Device

Connects to the safe device at the given index. Exists as `connect_safe_device.cpt`.

```
# Connect to safe device <index>

* Safe init
* Open safe interface <index>
* Read safe config
* Enable safe connection
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `index` | int | Index of safe device. | `True` |

Example usage:

```
* Connect to safe device "0"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-download-configuration-lookup"></a>

#### Download Configuration Lookuup

Downloaded the network configuration based on the default hardware lookup. Exists as `download_configuration_lookup.cpt`.

```
# Download lookup configuration <hardware>

* Config lookup tool <hardware>
* Config register
* Config unregister
* Config lock
* Config unlock
* Write block network config
* Config mode
* Config validate
* Config apply
* Soft reset device
* Wait "10"
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `hardware` | string | Hardware for network configuration. | `True` |

Example usage:

```
* Download lookup configuration "f-host"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-download-compressed-configuration"></a>

#### Download Compressed Configuration

Downloaded the compressed network configuration based on given filename. Exists as `download_compressed_configuration.cpt`.

```
# Download compressed configuration <filename>

* Load config <filename>
* Get config crc <filename>
* Config register
* Config unregister
* Config lock
* Config unlock
* Write block network config compressed
* Config mode
* Config validate
* Config apply
* Soft reset device
* Wait "10"
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `filename` | string | Filename of compressed network configuration. | `True` |

Example usage:

```
* Download compressed configuration "f-host_port-25.bin"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-download-configuration"></a>

#### Download Configuration

Downloaded the network configuration based on given filename. Exists as `download_configuration.cpt`.

```
# Download configuration <filename>

* Load config <filename>
* Get config crc <filename>
* Config register
* Config unregister
* Config lock
* Config unlock
* Write block network config
* Config mode
* Config validate
* Config apply
* Soft reset device
* Wait "10"
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `filename` | string | Filename of network configuration. | `True` |

Example usage:

```
* Download configuration "f-host_port-25.bin"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-hard-reset"></a>

#### Hard Reset

Hard reset the DUT on the active bakery. Exists as `hard_reset.cpt`.

```
# Hard reset device

Cycle power using the web relay

* Set web relay power "0"
* Wait "5"
* Set web relay power "1"
* Verify web relay status "0"
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `none` |  |  |  |

Example usage:

```
* Hard reset device
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-hard-reset-ssr"></a>

#### Hard Reset SSR

Hard reset the DUT on the active bakery that has SSR-Demo firmware. Exists as `hard_reset_ssr.cpt`.

```
# Hard reset device ssr

Cycle power using the web relay

* Connect to serial ports
* Clear "SS1" serial port
* Hard reset device
* Clear "SS1" serial port
* Find "ssr_cfg_discovery" on "SS1" serial port "-1"
* Wait "30"
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `none` |  |  |  |

Example usage:

```
* Hard reset device ssr
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-interrupt-uboot"></a>

#### Interrupt UBOOT

Wait for the moment to hit any key and then send Enter key to serial port that is connected to SS1. Exists as `interrupt_uboot.cpt`.

```
# Interrupt uboot

Find "Hit any key to stop" and then send return key

* Find "Hit any key to stop autoboot" on "SS1" serial port "-1"
* Write "\r\n" on "SS1" serial port
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `none` |  |  |  |

Example usage:

```
* Interrupt uboot
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-remove-configuration"></a>

#### Remove Configuration

Remove network configuration on the DUT via CAPI. Exists as `remove_configuration.cpt`.

```
# Remove configuration

* Config register
* Config unregister
* Config lock
* Config unlock
* Config mode
* Config reset
* Soft reset device
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `none` |  |  |  |

Example usage:

```
* Remove configuration
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-test-io"></a>

#### Test IO

Performs a read/write on the connected IO and then verifys the write. Exists as `test_io.cpt`.

```
# Test IO <value>

* Read IO
* Write IO <value>
* Wait "0.5"
* Read IO
* Verify input <value>
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `value` | int | Value to write. | `True` |

Example usage:

```
* Test IO "1"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-test-safe-io"></a>

#### Test Safe IO

Performs a read/write on the connected safe IO and then verifys the write. Exists as `test_safe_io.cpt`.

```
# Test safe IO <value>

* Change NCS "4"
* Get NCS loop "2"
* Get NCS
* Verify NCS "0" or "16"
* Get state
* Read safe IO
* Write safe IO <value>
* Wait "0.5"
* Read safe IO
* Verify safe output <value>
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `value` | int | Value to write. | `True` |

Example usage:

```
* Test safe IO "1"
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>

<a name="concepts-verify-pc-connection"></a>

#### Verify PC Connection

Connects to serial ports and confirms string on SS1 to verify boot (for Fanuc only). Exists as `verify_pc_connection.cpt`.

```
# Verify device is connected to PC

Read from the serial port on SS1 to confirm 

* Connect to serial ports
* Verify device is ready from hard reset
* Wait "10"
```

| Attribute | Type | Description | Required |
| --- | --- | --- | --- |
| `value` | int | Value to write. | `True` |

Example usage:

```
* Verify device is connected to PC
```

<sub><sup>[back](#concepts)</sup></sub>

<br/>



