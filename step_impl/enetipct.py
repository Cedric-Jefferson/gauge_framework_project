
##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Steve Korber
#   Steve.Korber@molex.com
#
#   General Test Functions for Test Automation in Gauge Framework
#
##########################################################################
"""
The ``enetipct_library`` is used for this Step Implementation file. All Steps are in the ``enetipct.py`` file.

Go to the Concepts to see any concepts that simplify the steps.

Below are a list of implemented Steps:

"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, after_step
import time
import sys
import os
import subprocess
sys.path.append(r"..\enetipct_library")
try:
    from ENetIPCTLibrary import ENetIPCTController
except ModuleNotFoundError:
    pass

##########################################################################
# methods
###
# wait step
###
@step("Run conformance tests")
def runConformanceTests():
    """
    Runs the conformances tests specified in the ``test-plan.yml``.

    Step and function definition::

        @step("Run conformance tests")
        def runConformanceTests():

    Example usage:
        * Run conformance tests
    """
    conformanceTool = ENetIPCTController()
    files = os.getenv("conformance_files")
    conformanceConfigFilePath = os.getenv("conformance_config_file_path")
    Messages.write_message("Conformance Config File Path: {}".format(conformanceConfigFilePath))
    files = files.split(",")
    Messages.write_message("Files: {}".format(files))
    print("\n\n")
    for newFile in files:
        print("Running Test: {}".format(newFile))
        filePath = "{}{}".format(conformanceConfigFilePath.strip(), newFile.strip())
        Messages.write_message("Running File Path: {}".format(filePath))
        result = conformanceTool.runTest(filePath)
        Messages.write_message("Results: {}".format(result))
        conformanceTool.renameLog(newFile.strip())
    print("\n\n")
    assert True
