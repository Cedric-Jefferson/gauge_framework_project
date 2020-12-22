##########################################################################
#
#   MOLEX Ltd. Test Library
#   developed by Brennan Koopman
#   Brennan.Koopman@molex.com
#
#   NAB/NAT Automation Tests in Gauge Framework
#
##########################################################################
"""
The ``nab_agent_library`` is used for this Step Implementation file. All Steps are in the ``nab.py`` file.

Go to the Concepts to see any concepts that simplify the steps.

"""
##########################################################################
# import libraries
###
from getgauge.python import step, Messages, data_store, before_suite, after_suite, before_spec
import os
import sys
import filecmp
sys.path.append(r"../nab_agent_library")
from NABAgentLibrary import NABAgentController

##########################################################################
# before suite
###
@before_suite
def beforeSuiteHook():
    """
    Initializes variables.


    ``data_store.suite["nabAgentConnected"]`` is set to ``False`` so that no Step can be run unless the NAB Agent Controller class is created.
    """
    data_store.suite["nabAgentConnected"] = False
    data_store.suite["transferFileCrc"] = 0

##########################################################################
# before spec
###
@before_spec
def beforeSpecHook():
    """
    Initializes variables.

    ``data_store.spec["nabAgentSubTransactions"]`` is set to ``[]`` to keep track of the data subscriptions to be unsubscribed if all is requested in the unsubscribe Step.
    """
    data_store.spec["nabAgentSubTransactions"] = []

##########################################################################
# methods
###
# connect
###
@step("NAB connect")
def nabConnect():
    """
    Create the NAB Agent Contoller class using the ``data_store.suite["nabAgentController"]`` variable.

    Step and function definition::

        @step("NAB connect")
        def nabConnect():

    Example usage:
        * NAB connect
    """    
    if data_store.suite["nabAgentConnected"]:
        Messages.write_message("NAB Agent object already connected")
    else:
        try:
            data_store.suite["nabAgentController"] = NABAgentController()
            Messages.write_message("create NAB Agent object successful")
            data_store.suite["nabAgentConnected"] = True
        except:
            Messages.write_message("error creating NAB Agent object")
            assert False
###
# disconnect
###
@step("NAB disconnect")
def nabDisconnect():
    """
    Deconstruct the NAB Agent Contoller class variable ```data_store.suite["nabAgentController"]``.

    Step and function definition::

        @step("NAB disconnect")
        def nabDisconnect():

    Example usage:
        * NAB disconnect
    """    
    if data_store.suite["nabAgentConnected"]:
        del(data_store.suite["nabAgentController"])
    else:
        Messages.write_message("NAB Agent not connected")
    data_store.suite["nabAgentConnected"] = False
###
# echo data
###
@step("NAB echo data <echoData> <verifyResponseResult>")
def nabEchoData(echoData, verifyResponseResult):
    """
    Call the Echo Data method using given data array and then clarify if the response from the NAB needs to be non-zero.

    Args:
        echoData (string): Data to send (leaving empty will use default data).
        verifyResponseResult (bool): True to verify NAB returncode is non-zero.

    Step and function definition::

        @step("NAB echo data <echoData> <verifyResponseResult>")
        def nabEchoData(echoData, verifyResponseResult):

    Example usage:
        * NAB echo data "" "True"
        * NAB echo data "1, 1, 3, 51" "True"
        * NAB echo data "1, 2, 3, 4, 5, 6" "True"
    """
    assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
    if echoData != "":
        data = [int(x) for x in echoData.split(",")]
        Messages.write_message("data to echo: {}".format("".join("0x{:02X} ".format(x) for x in data)))
    else:
        data = list()
        Messages.write_message("data to echo: empty")

    #TODO - need a way to store nab/ssr specific values like the command type
    results = data_store.suite["nabAgentController"].exchange(0x5002005c, 0x0000, 0x0001, len(data), data)
    # This is the success response for the socket exchange
    Messages.write_message(results["description"])
    assert results["result"] == 0, "nab connection error"
    
    Messages.write_message("Response Header: 0x{:08X} 0x{:04X} 0x{:04X} 0x{:04X} 0x{:04X}".format(*results["data"]["header"]))
    Messages.write_message("Response Result: {}".format(results["data"]["result"]))
    Messages.write_message("Response Data: {}".format("".join("0x{:02X} ".format(x) for x in results["data"]["data"])))

    # Confirm the formatting of the response header, except the msg_id
    assert int(results["data"]["header"][0]) == int(0x5002805c), "replied command is incorrect"
    assert int(results["data"]["header"][2]) == int(0x0000), "replied instance is incorrect" 
    assert int(results["data"]["header"][3]) == int(len(data)), "replied data size is incorrect"
    assert int(results["data"]["header"][4]) == int(0x0001), "replied version is incorrect"
 

    if verifyResponseResult.lower() == "zero":
        assert results["data"]["result"] == 0, "return from nat was non-zero when expected zero"
        # Now check to make sure the message was properly echo'd
        for index, x in enumerate(results["data"]["data"]):
            assert int(data[index]) == int(x), "data was not echoed properly"
    elif verifyResponseResult.lower() == "non-zero":
        assert results["data"]["result"] != 0, "return from nat was zero when expected non-zero"

###
# inverse data
###
@step("NAB inverse data <inverseData> <verifyResponseResult>")
def nabInverseData(inverseData, verifyResponseResult):
    """
    Call the Inverse Data method using given data array and then clarify if the response from the NAB needs to be non-zero.

    Args:
        inverseData (string): Data to send (leaving empty will use default data).
        verifyResponseResult (bool): True to verify NAB returncode is non-zero.

    Step and function definition::

        @step("NAB inverse data <inverseData> <verifyResponseResult>")
        def nabInverseData(inverseData, verifyResponseResult):

    Example usage:
        * NAB inverse data "" "True"
        * NAB inverse data "1, 1, 3, 51" "True"
        * NAB inverse data "1, 2, 3, 4, 5, 6" "True"
    """
    assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
    if inverseData != "":
        data = [int(x) for x in inverseData.split(",")]
        Messages.write_message("data to inverse: {}".format("".join("0x{:02X} ".format(x) for x in data)))
    else:
        data = list()
        Messages.write_message("data to inverse in empty, sending empty inverse request")
       
    results = data_store.suite["nabAgentController"].exchange(0x500200ba, 0x0000, 0x0001, len(data), data)
    Messages.write_message(results["description"])
    assert results["result"] == 0, "nab connection error"

    Messages.write_message("Response Header: 0x{:08X} 0x{:04X} 0x{:04X} 0x{:04X} 0x{:04X}".format(*results["data"]["header"]))
    Messages.write_message("Response Result: {}".format(results["data"]["result"]))
    Messages.write_message("Response Data: {}".format("".join("0x{:02X} ".format(x) for x in results["data"]["data"])))

    # Confirm the formatting of the response header, except the msg_id
    assert int(results["data"]["header"][0]) == int(0x500280ba), "replied command is incorrect"
    assert int(results["data"]["header"][2]) == int(0x0000), "replied instance is incorrect" 
    assert int(results["data"]["header"][3]) == int(len(data)), "replied data size is incorrect"
    assert int(results["data"]["header"][4]) == int(0x0001), "replied version is incorrect" 

    if verifyResponseResult.lower() == "zero":
        assert results["data"]["result"] == 0, "return from nab was non-zero when expected zero"
        for i in zip(data, results["data"]["data"]):
            assert "{:08b}".format(i[0]).replace("0", "x").replace("1", "y") == "{:08b}".format(i[1]).replace("1", "x").replace("0", "y"), "data was not reversed correctly"
    elif verifyResponseResult.lower() == "non-zero":
        assert results["data"]["result"] != 0, "return from nab was zero when expected non-zero"

#######################IGNORE BELOW FOR NOW, KEEP IT TO MAINTAIN EXAMPLES #################################

# ###
# # read internal diag
# ###
# @step("NAB read internal diag <verifyResponseResult>")
# def nabReadInternalDiag(verifyResponseResult):
#     """
#     Call the Read Internal Diag method then clarify if the response from the NAB needs to be non-zero.

#     Args:
#         verifyResponseResult (bool): True to verify NAB returncode is non-zero.

#     Step and function definition::

#         @step("NAB read internal diag <verifyResponseResult>")
#         def nabReadInternalDiag(verifyResponseResult):

#     Example usage:
#         * NAB read internal diag "True"
#     """
#     assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
#     results = data_store.suite["nabAgentController"].readInternalDiag()
#     Messages.write_message(results["description"])
#     Messages.write_message(results)
#     assert results["result"] == 0, "read internal diag failed"
#     try:
#         Messages.write_message("Response Header: 0x{:08X} 0x{:04X} 0x{:04X} 0x{:04X} 0x{:04X}".format(*results["data"][0]["header"]))
#         Messages.write_message("Response Result: {}".format(results["data"][0]["result"]))
#         Messages.write_message("Response Data: {}".format("".join("0x{:02X} ".format(x) for x in results["data"][0]["data"])))
#         Messages.write_message("Response Header: 0x{:08X} 0x{:04X} 0x{:04X} 0x{:04X} 0x{:04X}".format(*results["data"][1]["header"]))
#         Messages.write_message("Response Result: {}".format(results["data"][1]["result"]))
#         Messages.write_message("Response Data: {}".format("".join("0x{:02X} ".format(x) for x in results["data"][1]["data"])))
#     except:
#         Messages.write_message("Issue printing data")
#         Messages.write_message(results)
#     if verifyResponseResult.lower() == "true":
#         assert results["data"][0]["result"] == 0, "return 0 from nab was non-zero"
#         assert results["data"][1]["result"] == 0, "return 1 from nab was non-zero"
# ###
# # write config
# ###
# @step("NAB write config <filePath> <verifyResult>")
# def nabWriteConfig(filePath, verifyResult):
#     """
#     Call the Write Config method using the given filepath then clarify if the response from the NAB needs to be non-zero.

#     Args:
#         filePath (string): Name of file (relative to Jenkins workspace).
#         verifyResult (bool): True to verify NAB returncode is non-zero.

#     Step and function definition::

#         @step("NAB write config <filePath> <verifyResult>")
#         def nabWriteConfig(filePath, verifyResult):

#     Example usage:
#         * NAB read config "/nab_agent_library/test/to1.bin" "True"
#     """
#     filePath = os.getenv("workspace_path") + filePath
#     assert os.path.exists(filePath), "file does not exist, {}".format(filePath)
#     assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
#     results = data_store.suite["nabAgentController"].writeConfigFile(filePath)
#     Messages.write_message(results["description"])
#     Messages.write_message(results)
#     if verifyResult.lower() == "true":
#         assert results["result"] == 0, "write config failed"
#     elif verifyResult.lower() == "non-zero":
#         assert results["result"] != 0, "write config was successful"
# ###
# # read config
# ###
# @step("NAB read config <filePath> <verifyResult>")
# def nabReadConfig(filePath, verifyResult):
#     """
#     Call the Subscribe Data method using the given thread delay rate in seconds (use "" for default and "-1" for no delay).

#     Args:
#         filePath (string): Name of file (relative to Jenkins workspace).
#         verifyResult (bool): True to verify NAB returncode is non-zero.

#     Step and function definition::

#         @step("NAB read config <filePath> <verifyResult>")
#         def nabReadConfig(filePath, verifyResult):

#     Example usage:
#         * NAB read config "/nab_agent_library/test/to1.bin" "True"
#     """
#     filePath = os.getenv("workspace_path") + filePath
#     assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
#     results = data_store.suite["nabAgentController"].readConfigFile(filePath)
#     Messages.write_message(results["description"])
#     Messages.write_message(results)
#     if verifyResult.lower() == "true":
#         assert results["result"] == 0, "read config failed"
#     elif verifyResult.lower() == "non-zero":
#         assert results["result"] != 0, "read config was successful"
# ###
# # subscribe data update
# ###
# @step("NAB subscribe data update <threadRate>")
# def nabSubscribeData(threadRate):
#     """
#     Call the Subscribe Data method using the given thread delay rate in seconds (use "" for default and "-1" for no delay).

#     Args:
#         threadRate (float): Thread loop rate in seconds.

#     Step and function definition::

#         @step("NAB subscribe data update <threadRate>")
#         def nabSubscribeData(threadRate):

#     Example usage:
#         * NAB subscribe data update "-1"
#     """
#     assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
#     if threadRate == "":
#         results = data_store.suite["nabAgentController"].subscribeDataUpdate()
#     else:
#         threadRate = float(threadRate)
#         results = data_store.suite["nabAgentController"].subscribeDataUpdate(threadRate)
#     Messages.write_message(results["description"])
#     Messages.write_message(results)
#     assert results["result"] == 0, "subscribe update failed"
#     data_store.spec["nabAgentSubTransactions"].append(results["data"]["transaction"])
# ###
# # unsubscribe data update
# ###
# @step("NAB unsubscribe data update <transaction> <timeout> <verifyResult>")
# def nabUnsubscribeData(transaction, timeout, verifyResult):
#     """
#     Call the Unsubscribe Data method using the given transaction id (specify "All" to loop through all subscribed transactions), timeout (leave as "" for default), and if the NAB needs to verify a non-zero return code.

#     Args:
#         transaction (int): Transaction ID.
#         timeout (float): Timeout for request in seconds.
#         verifyResult (bool): True to verify NAB returncode is non-zero.

#     Step and function definition::

#         @step("NAB unsubscribe data update <transaction> <timeout> <verifyResult>")
#         def nabUnsubscribeData(transaction, timeout, verifyResult):

#     Example usage:
#         * NAB unsubscribe data update "All" "" "True"
#         * NAB unsubscribe data update "0" "10" "True"
#     """
#     assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
#     assert data_store.spec["nabAgentSubTransactions"], "NAB Agent isn't subscribed to anything"
#     if transaction.lower() == "all":
#         for transactionId in data_store.spec["nabAgentSubTransactions"]:
#             if timeout == "":
#                 results = data_store.suite["nabAgentController"].unsubscribeDataUpdate(transactionId)
#             else:
#                 results = data_store.suite["nabAgentController"].unsubscribeDataUpdate(transactionId, int(timeout))
#             Messages.write_message(results["description"])
#             Messages.write_message(results)
#             if verifyResult.lower() == "true":
#                 assert results["result"] == 0, "unsubscribe update failed"
#             elif verifyResult.lower() == "non-zero":
#                 assert results["result"] != 0, "unsubscribe update was successful"
#         data_store.spec["nabAgentSubTransactions"] = []
#     else:
#         transaction = int(transaction)
#         assert transaction in data_store.spec["nabAgentSubTransactions"], "Transaction doesn't exist in list"
#         results = data_store.suite["nabAgentController"].unsubscribeDataUpdate(transaction)
#         if timeout == "":
#             results = data_store.suite["nabAgentController"].unsubscribeDataUpdate(transaction)
#         else:
#             results = data_store.suite["nabAgentController"].unsubscribeDataUpdate(transaction, int(timeout))
#         Messages.write_message(results["description"])
#         Messages.write_message(results)
#         if verifyResult.lower() == "true":
#             assert results["result"] == 0, "unsubscribe update failed"
#         elif verifyResult.lower() == "non-zero":
#             assert results["result"] != 0, "unsubscribe update was successful"
#         data_store.spec["nabAgentSubTransactions"].remove(transaction)

# ##########################################################################
# # verify steps
# ###
# # verify config file
# ###
# @step("NAB verify config <filePathRead> <filePathWrite> <assertValue>")
# def nabVerifyConfig(filePathRead, filePathWrite, assertValue):
#     """
#     This method is used to check if two files are equal or not equal in size.

#     Args:
#         filePathRead (string): Name of file (relative to Jenkins workspace).
#         filePathWrite (string): Name of file (relative to Jenkins workspace).
#         assertValue (bool): True to verify files are the same size, False to verify they are different.

#     Step and function definition::

#         @step("NAB verify config <filePathRead> <filePathWrite> <assertValue>")
#         def nabVerifyConfig(filePathRead, filePathWrite, assertValue):

#     Example usage:
#         * NAB verify config "/nab_agent_library/test/to_1998.bin" "/nab_agent_library/test/from_1998.bin" "True"
#         * NAB verify config "/nab_agent_library/test/to_1001.bin" "/nab_agent_library/test/from_999.bin" "False"
#     """
#     filePathRead = os.getenv("workspace_path") + filePathRead
#     assert os.path.exists(filePathRead), "file does not exist, {}".format(filePathRead)
#     filePathWrite = os.getenv("workspace_path") + filePathWrite
#     assert os.path.exists(filePathWrite), "file does not exist, {}".format(filePathWrite)
#     assert data_store.suite["nabAgentConnected"] == True, "NAB Agent is not connected"
#     if assertValue.lower() == "false":
#         assert filecmp.cmp(filePathRead, filePathWrite) == False, "Files are equal"
#     elif assertValue.lower() == "true":
#         assert filecmp.cmp(filePathRead, filePathWrite) == True, "Files are not equal"
#     else:
#         assert False, "Could not determine assertValue"
