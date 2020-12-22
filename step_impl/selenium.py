##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   PyLogix Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``selenium_library`` is used for this Step Implementation file. All Steps are in the ``selenium.py`` file.

Below are a list of implemented Steps:
"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, before_suite, after_suite
import os
import sys
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
sys.path.append(r"../selenium_library")
try:
    from SeleniumLibrary import SeleniumController
except Exception as exc:
    print("import SeleniumLibrary:: {} occured: {}".format(type(exc).__name__, exc))

##########################################################################
# before suite
###
@before_suite
def beforeSuiteHook():
    """
    Initializes variables:
        * ``data_store.suite["seleniumConnected"]`` is set to ``False`` so that no Step can be run unless the Selenium Controller class is created.
    """
    data_store.suite["seleniumConnected"] = False

##########################################################################
# methods
###
# connect
###
@step("Selenium connect <type>")
def seleniumConnect(type):
    """
    Create the Selenium Contoller class using the ``data_store.suite["seleniumController"]`` variable.

    Args:
        type ([type]): [description]

    Step and function definition::

        @step("Selenium connect <type>")
        def seleniumConnect(type):

    Example usage:
        * Selenium Connect

    """
    if data_store.suite["seleniumConnected"]:
        Messages.write_message("Selenium object already connected")
    else:
        try:
            data_store.suite["seleniumDisplay"] = Display(visible=0, size=(1920, 1080))
            data_store.suite["seleniumDisplay"].start()
            if type == "firefox":
                # setup for firefox
                options = webdriver.FirefoxOptions()
                # options.add_argument('--no-sandbox')
                options.add_argument('--headless')
                data_store.suite["seleniumDriver"] = webdriver.Firefox(options=options, executable_path="{}/selenium_library/drivers/geckodriver".format(os.getenv("workspace_path")))
            elif type == "chrome":
                # setup for chrome
                options = Options()
                options.add_argument("--no-sandbox")
                options.add_argument('--headless')
                data_store.suite["seleniumDriver"] = webdriver.Chrome(chrome_options=options)
            else:
                assert False, "only chrome and firefox are supported currently"
            data_store.suite["seleniumDriver"].set_window_size(1920, 1080)
            # create class object
            data_store.suite["seleniumController"] = SeleniumController(data_store.suite["seleniumDriver"])
            Messages.write_message("Created Selenium object successful")
            data_store.suite["seleniumConnected"] = True
        except:
            Messages.write_message("Error creating Selenium object")
            assert False
###
# disconnect
###
@step("Selenium disconnect")
def seleniumDisconnect():
    """
    Disconnects the Selenium Controller object.

    Step and function definition::

        @step("Selenium disconnect")
        def seleniumDisconnect():

    Example Usage:
        * Selenium disconnect
    """
    if data_store.suite["seleniumConnected"]:
        del(data_store.suite["seleniumController"])
        data_store.suite["seleniumDriver"].close()
        data_store.suite["seleniumDriver"].quit()
        data_store.suite["seleniumDisplay"].stop()
    else:
        Messages.write_message("Selenium not connected")
    data_store.suite["seleniumConnected"] = False
###
# navigate
###
@step("Selenium navigate <url>")
def seleniumNavigate(url):
    """
    Navigates the controller object to the given url.

    Args:
        url (string): 	Url to navigate to.

    Step and function definition::

        @step("Selenium navigate <url>")
        def seleniumNavigate(url):

    Example usage:
        * Selenium navigate "http://192.168.1.10:8081/usr/config.html"
    """
    assert data_store.suite["seleniumConnected"] == True, "Selenium is not connected"
    results = data_store.suite["seleniumController"].navigate(url)
    Messages.write_message(results["description"])
    Messages.write_message(results)
    assert results["result"] == 0, "navigate failed"
###
# save screenshot
###
@step("Selenium save screenshot")
def seleniumSaveScreenshot():
    """
    Saves screenshot and can be viewed in the gauge report on Jenkins after.

    Step and function definition::

        @step("Selenium save screenshot")
        def seleniumSaveScreenshot():

    Example usage:
        * Selenium save screenshot
    """
    assert data_store.suite["seleniumConnected"] == True, "Selenium is not connected"
    results = data_store.suite["seleniumController"].saveScreenshot()
    Messages.write_message(results["description"])
    Messages.write_message(results)
    assert results["result"] == 0, "saveScreenshot failed"
###
# click
###
@step("Selenium click <byType> <identifier>")
def seleniumClick(byType, identifier):
    """
    Click the given element based on ID or Class and then string identifer.

    Args:
        byType (str): ID or By.ID and CLass for By.Class.
        identifier (string): Value for the identifier.

    Step and function definition::

        @step("Selenium click <byType> <identifier>")
        def seleniumClick(byType, identifier):

    Example usage:
        * Selenium click "Class" "btn-apply"
    """
    assert data_store.suite["seleniumConnected"] == True, "Selenium is not connected"
    if byType.lower() == "class":
        results = data_store.suite["seleniumController"].click((By.CLASS_NAME, identifier))
    elif byType.lower() == "id":
        results = data_store.suite["seleniumController"].click((By.ID, identifier))
    else:
        assert False, "byType needs to be Class or ID"
    Messages.write_message(results["description"])
    Messages.write_message(results)
    assert results["result"] == 0, "click failed"
###
# get selected text from dropdown
###
@step("Selenium get selected text from dropdown <byType> <identifier>")
def seleniumGetSelectedTextFromDropdown(byType, identifier):
    """
    Selenium Get Selected Text From Dropdown

    Args:
        byType (str): ID or By.ID and CLass for By.Class.
        identifier (string): Value for the identifier.

    Step and function definition::

        @step("Selenium get selected text from dropdown <byType> <identifier>")
        def seleniumGetSelectedTextFromDropdown(byType, identifier):

    Example usage:
        * Selenium get selected text from dropdown "ID" "item1_on_off_filter_time"
    """
    assert data_store.suite["seleniumConnected"] == True, "Selenium is not connected"
    if byType.lower() == "class":
        results = data_store.suite["seleniumController"].getSelectedTextFromDropDown((By.CLASS_NAME, identifier))
    elif byType.lower() == "id":
        results = data_store.suite["seleniumController"].getSelectedTextFromDropDown((By.ID, identifier))
    else:
        assert False, "byType needs to be Class or ID"
    Messages.write_message(results["description"])
    Messages.write_message(results)
    assert results["result"] == 0, "getSelectedTextFromDropdown failed"
###
# select by value
###
@step("Selenium select by value <byType> <identifier> <value>")
def seleniumSelectByValue(byType, identifier, value):
    """
    Select the given value for the given element.

    Args:
        byType (str): ID or By.ID and CLass for By.Class.
        identifier (string): Value for the identifier.
        value (string): Value to select.

    Step and function definition::

        @step("Selenium select by value <byType> <identifier> <value>")
        def seleniumSelectByValue(byType, identifier, value):

    Example usage:
        * Selenium select by value "ID" "item16_output_source" "0"

    """
    assert data_store.suite["seleniumConnected"] == True, "Selenium is not connected"
    if byType.lower() == "class":
        results = data_store.suite["seleniumController"].selectByValue((By.CLASS_NAME, identifier), value)
    elif byType.lower() == "id":
        results = data_store.suite["seleniumController"].selectByValue((By.ID, identifier), value)
    else:
        assert False, "byType needs to be Class or ID"
    Messages.write_message(results["description"])
    Messages.write_message(results)
    assert results["result"] == 0, "click failed"
###
# get text  
###
@step("Selenium get text <byType> <identifier> <verifyText>")
def seleniumGetText(byType, identifier, verifyText):
    """
    Get the selected text the given element based on ID or Class and then string identifer.

    Args:
        byType (str): ID or By.ID and CLass for By.Class.
        identifier (string): Value for the identifier.
        verifyText (string): Value of the text to compare, if blank will not compare.

    Step and function definition::

        @step("Selenium get text <byType> <identifier> <verifyText>")
        def seleniumGetText(byType, identifier, verifyText):

    Example usage:
        * Selenium get text "ID" "config_status_p" "Download successful. Please power-cycle the system for the changes to take effect."
        * Selenium get text "ID" "config_status_p" ""
    """    
    assert data_store.suite["seleniumConnected"] == True, "Selenium is not connected"
    if byType.lower() == "class":
        results = data_store.suite["seleniumController"].getText((By.CLASS_NAME, identifier))
    elif byType.lower() == "id":
        results = data_store.suite["seleniumController"].getText((By.ID, identifier))
    else:
        assert False, "byType needs to be Class or ID"
    Messages.write_message(results["description"])
    Messages.write_message(results)
    assert results["result"] == 0, "seleniumGetText failed"
    if verifyText != "":
        Messages.write_message("Text to verify: {}".format(verifyText))
        assert results["data"]["text"] == verifyText, "Text is not equal"