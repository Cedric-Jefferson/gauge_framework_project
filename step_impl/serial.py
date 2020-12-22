##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   Serial Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The serial_comms_library is used for this Step Implementation file. All Steps are in the serial.py file.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, before_suite, after_suite
import sys
sys.path.append(r"../serial_comms_library") # append lib path
from SerialLibrary import SerialController
import os
import time

##########################################################################
# before suite setup
###
@before_suite
def beforeSuiteHook():
    """
    Initializes variables:
        * data_store.suite["ss1Controller"] using the Dynamic Variable os.getenv("ss1_usb")
        * data_store.suite["ss2Controller"] using the Dynamic Variable os.getenv("ss2_usb")
        * data_store.suite["ss3Controller"] using the Dynamic Variable os.getenv("ss3_usb")
        * data_store.suite["hardReset"] is set to False which is used in later Step
    """
    try:
        data_store.suite["ss1Controller"] = SerialController("/dev/{}".format(os.getenv("ss1_usb")), loggerName="SS1")
    except:
        Messages.write_message("unable to connect to {}".format(os.getenv("ss1_usb")))
    try:
        data_store.suite["ss2Controller"] = SerialController("/dev/{}".format(os.getenv("ss2_usb")), loggerName="SS2")
    except:
        Messages.write_message("unable to connect to {}".format(os.getenv("ss2_usb")))
    try:
        data_store.suite["ss3Controller"] = SerialController("/dev/{}".format(os.getenv("ss3_usb")), loggerName="SS3")
    except:
        Messages.write_message("unable to connect to {}".format(os.getenv("ss3_usb")))
    data_store.suite["hardReset"] = False
    Messages.write_message("serial before suite complete")

##########################################################################
# methods
###
# connect to serial port
###
@step("Connect to serial ports")
def connectToSerialPorts():
    """
    Verify that the ``data_store.suite`` SS1/SS2/SS3 controller classes were created.

    Step and function definition::

        @step("Connect to serial ports")
        def connectToSerialPorts():

    Example usage:
        * Connect to serial ports
    """
    assert data_store.suite["ss1Controller"] != None, "{} is null".format(os.getenv("ss1_usb"))
    assert data_store.suite["ss2Controller"] != None, "{} is null".format(os.getenv("ss2_usb"))
    assert data_store.suite["ss3Controller"] != None, "{} is null".format(os.getenv("ss3_usb"))
###
# find string
###
@step("Find <findText> on <controller> serial port <timeout>")
def findOnSerialPort(findText, controller, timeout=30):
    """
    Find given text on the given serial port with given timeout ("" for default value).

    Args:
        findText (string): Text to find.
        controller (string): Subsystem to read from.
        timeout (int, optional): Timeout in seconds (-1 to ignore if value was found). Defaults to 30.

    Step and function definition::

        @step("Find <findText> on <controller> serial port <timeout>")
        def findOnSerialPort(findText, controller, timeout=30):

    Example usage:
        * Find "Hit any key to stop autoboot" on "SS1" serial port "-1"
        * Find "SSR Agent is Ready ..." on "SS1" serial port "120"
    """
    timeout = float(timeout)
    ignoreAssert = False
    if timeout == -1:
        ignoreAssert = True
        timeout = 30
    Messages.write_message("Text to find: {}".format(findText))
    Messages.write_message("Connection: {}".format(controller))
    if controller == "SS1":
        results = data_store.suite["ss1Controller"].find(timeout, findText)
    elif controller == "SS2":
        results = data_store.suite["ss2Controller"].find(timeout, findText)
    elif controller == "SS3":
        results = data_store.suite["ss3Controller"].find(timeout, findText)
    else:
        assert False, "Serial connection device {}, not found".format(controller)
    Messages.write_message(results["description"])
    if not ignoreAssert:
        assert results["result"] == 0, "Was not able to find {} on controller {}".format(findText, controller)
###
# write string
###
@step("Write <writeText> on <controller> serial port")
def writeOnSerialPort(writeText, controller):
    """
    Write given text on the given serial port.

    Args:
        writeText (string): Text to write.
        controller (string): Subsystem to read from.

    Step and function definition::

        @step("Write <writeText> on <controller> serial port")
        def writeOnSerialPort(writeText, controller):

    Example usage:
        * Write "setenv fullimg ss1_firmware.bin%\n" on "SS1" serial port
    """
    Messages.write_message("Text to write: {}".format(writeText))
    Messages.write_message("Connection: {}".format(controller))
    if controller == "SS1":
        results = data_store.suite["ss1Controller"].write(writeText)
    elif controller == "SS2":
        results = data_store.suite["ss2Controller"].write(writeText)
    elif controller == "SS3":
        results = data_store.suite["ss3Controller"].write(writeText)
    else:
        assert False, "Serial connection device {}, not found".format(controller)
    Messages.write_message(results["description"])
###
# read string
###
@step("Read on <controller> serial port")
def readOnSerialPort(controller):
    """
    Read single line from the given serial port.

    Args:
        controller (string): Subsystem to read from.

    Step and function definition::

        @step("Read on <controller> serial port")
        def readOnSerialPort(controller):

    Example usage:
        * Read on "SS1" serial port
    """
    Messages.write_message("Connection: {}".format(controller))
    if controller == "SS1":
        results = data_store.suite["ss1Controller"].read()
    elif controller == "SS2":
        results = data_store.suite["ss2Controller"].read()
    elif controller == "SS3":
        results = data_store.suite["ss3Controller"].read()
    else:
        assert False, "Serial connection device {}, not found".format(controller)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
###
# read all string
###
@step("Read all on <controller> serial port")
def readAllOnSerialPort(controller):
    """
    Read all lines from the given serial port.

    Args:
        controller (string): Subsystem to read from

    Step and function definition::

        @step("Read all on <controller> serial port")
        def readAllOnSerialPort(controller):

    Example usage::
        * Read on all "SS1" serial port
    """
    Messages.write_message("Connection: {}".format(controller))
    if controller == "SS1":
        results = data_store.suite["ss1Controller"].readAll()
    elif controller == "SS2":
        results = data_store.suite["ss2Controller"].readAll()
    elif controller == "SS3":
        results = data_store.suite["ss3Controller"].readAll()
    else:
        assert False, "Serial connection device {}, not found".format(controller)
    Messages.write_message(results["description"])
    Messages.write_message(results["data"])
###
# clear serial port
###
@step("Clear <controller> serial port")
def clearSerialPort(controller):
    """
    Clear all lines in the buffer from the given serial port (will clear the buffer for find and read).

    Args:
        controller (string): Subsystem to read from.

    Step and function definition::

        @step("Clear <controller> serial port")
        def clearSerialPort(controller):

    Example usage::
        * Clear "SS1" serial port
    """
    Messages.write_message("Connection: {}".format(controller))
    if controller == "SS1":
        results = data_store.suite["ss1Controller"].clearQueue()
    elif controller == "SS2":
        results = data_store.suite["ss2Controller"].clearQueue()
    elif controller == "SS3":
        results = data_store.suite["ss3Controller"].clearQueue()
    else:
        assert False, "Serial connection device {}, not found".format(controller)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Was not able to clear on controller {}".format(controller)
###
# before flash step; try to interupt uboot but if it fails hard reset
### 
@step("Before flash find <findText> on <controller> serial port")
def beforeFlashFind(findText, controller, timeout=30):
    """
    Used to find text on serial port to verify if the DUT was able to get into UBOOT. The variable ``data_store.scenario["factoryFlashRestart"]`` is set with the result.

    Args:
        findText (string): Text to find.
        controller (string): Subsystem to read from.
        timeout (int, optional):  Timeout in seconds. Defaults to 30.

    Step and function definition::

        @step("Before flash find <findText> on <controller> serial port")
        def beforeFlashFind(findText, controller, timeout=30):

    Example usage:
        * Before flash find "Hit any key to stop autoboot" on "SS1" serial port
    """
    Messages.write_message("Text to find: {}".format(findText))
    Messages.write_message("Connection: {}".format(controller))
    if controller == "SS1":
        results = data_store.suite["ss1Controller"].find(timeout, findText)
    elif controller == "SS2":
        results = data_store.suite["ss2Controller"].find(timeout, findText)
    elif controller == "SS3":
        results = data_store.suite["ss3Controller"].find(timeout, findText)
    else:
        assert False, "Serial connection device {}, not found".format(controller)
    Messages.write_message(results["description"])
    if results["result"] == 0:
        # try to interrupt uboot
        writeOnSerialPort("\r\n", "SS1")
        data_store.scenario["factoryFlashRestart"] = False
    else:
        # could not interupt so restart device
        data_store.scenario["factoryFlashRestart"] = True
        
##########################################################################
# verify methods
###
# verify device is connected by reading SS1 output
###
@step("Verify device is ready from hard reset")
def verifyDeviceIsReadyFromHardReset():
    """
    Find specific text () on SS1 to verify if the firmware was flashed correctly.

    Step and function definition::

        @step("Verify device is ready from hard reset")
        def verifyDeviceIsReadyFromHardReset():

    Example usage:
        * Verify device is ready from hard reset

    """
    results = data_store.suite["ss1Controller"].find(120, "SSR agent is ready...")
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Was not able to verify reboot"
    data_store.suite["hardReset"] = True

##########################################################################
# after suite tasks
###
@after_suite
def afterSuiteHook():
    """
    Stops the Serial Controller class threads.
    """    
    try:
        data_store.suite["ss1Controller"].stop()
    except:
        pass
    try:
        data_store.suite["ss2Controller"].stop()
    except:
        pass
    try:
        data_store.suite["ss3Controller"].stop()
    except:
        pass
    Messages.write_message("serial after suite complete")