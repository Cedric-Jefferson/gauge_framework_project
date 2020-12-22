##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Raman Brar
#   raman.brar@molex.com
#
#   FTP Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``gpio_library`` is used for this Step Implementation file. All Steps are in the ``GPIOLibrary.py`` file.

Go to the Concepts to see any concepts that simplify the steps.
"""
from getgauge.python import step, Messages, after_step, data_store, after_scenario, before_scenario
import sys
import json

sys.path.append(r"../gpio_library")

try:
    from  GPIOLibrary import GPIOController
except Exception as exc:
    print("import GPIOLibrary:: {} occured: {}".format(type(exc).__name__, exc))

##########################################################################
# before scenario setup
###
@before_scenario
def beforeScenarioHook():
    """
    Initializes variables:
        * ``data_store.scenario["GPIOController"]`` is set to None so that GPIOController class object can be stored in it.
        * ``data_store.scenario["gpioConnected"]`` is set to ``False`` so that no Step can be run unless the object of GPIO class is created.
    """
    data_store.scenario["GPIOController"] = None
    data_store.scenario["gpioConnected"] = False
    Messages.write_message("GPIO before scenario completed")

##########################################################################
# methods
###
# GPIO connect
###
@step("GPIO connect")
def gpioConnect():
    """
    Creates the object of GPIOController() class.

    Step and function definition::

        @step("GPIO connect")
        def gpioConnect():

    Example usage:
        * GPIO connect
    """
    try:
        data_store.scenario["gpioController"] = GPIOController()
        Messages.write_message("create gpio object successful")
    except:
        Messages.write_message("error creating gpio object")
        assert False, "Creating GPIO object failed."
    data_store.scenario["gpioConnected"] = True

###
# Init GPIO
###
@step("Init GPIO <pinNumber> <dir>")
def initGpio(pinNumber, dir):
    """
    Initialize the GPIO object and set direction for GPIO.

    Args:
        pinNumber (int): Number of the pin.
        dir (string): direction of pin. it can take "in" or "out" value.

    Step and function definition::

        @step("Init GPIO <pinNumber> <dir>")
        def initGpio(pinNumber, dir):

    Example usage:
        * Init GPIO "329" "out"
    """
    assert data_store.scenario["gpioConnected"] == True, "Call GPIO connect first. As GPIO class is not instentiated"
    Messages.write_message("Initialize the GPIO object and set direction for GPIO.")
    pinNumber = int(pinNumber)
    __dir_list = ["in", "out"]
    if dir in __dir_list == False:
        assert False, "dir can only take only 'in' and 'out' values."
    results = data_store.scenario["gpioController"].initGpio(pinNumber, dir)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Init GPIO failed"

###
# Read pin level
###
@step("Read pin level <pinNumber>")
def readPinLevel(pinNumber):
    """
    Read the state of the GPIO.

    Args:
        pinNumber (int): Number of the pin.

    Step and function definition::

        @step("Read pin level <pinNumber>")
        def readPinLevel(self, pinNumber):

    Example usage:
        * Read pin level "329"
    """
    assert data_store.scenario["gpioConnected"] == True, "Call GPIO connect first. As GPIO class is not instentiated"
    pinNumber = int(pinNumber)
    results = data_store.scenario["gpioController"].readPinLevel(pinNumber)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Read pin level failed"

###
# Set pin level
###
@step("Set pin level <pinNumber> <value>")
def setPinLevel(pinNumber, value):
    """
    Set logic level of pin.

    Args:
        pinNumber (int): Number of the pin.
        value (bool): Logic level to set on the pin.

    Step and function definition::

        @step("Set pin level <pinNumber> <value>")
        def setPinLevel(self, pinNumber, value):

    Example usage:
        * Set pin level "329" "False"
    """
    assert data_store.scenario["gpioConnected"] == True, "Call GPIO connect first. As GPIO class is not instentiated"
    pinNumber = int(pinNumber)
    value = json.loads(value.lower())
    if isinstance(value, bool) == False:
        assert False, "Value can take only boolen input. Provide either True or False input."
    results = data_store.scenario["gpioController"].setPinLevel(pinNumber, value)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Set pin level failed"

###
# Close sysfs GPIO
###
@step("Close sysfs GPIO <pinNumber>")
def closeSysfsGpio(pinNumber):
    """
    Close the sysfs GPIO.

    Args:
        pinNumber (int): Number of the pin.

    Step and function definition::

        @step("Close sysfs GPIO <pinNumber>")
        def closeSysfsGpio(pinNumber):

    Example usage:
        * Close sysfs GPIO "329"
    """
    assert data_store.scenario["gpioConnected"] == True, "Call GPIO connect first. As GPIO class is not instentiated"
    pinNumber = int(pinNumber)
    results = data_store.scenario["gpioController"].closeSysfsGpio(pinNumber)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "Close sysfs GPIO failed"