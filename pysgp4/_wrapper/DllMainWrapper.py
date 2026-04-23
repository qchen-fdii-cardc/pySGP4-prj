# This wrapper file was generated automatically by the GenDllWrappers program.
import sys
import os
import platform
from ctypes import *
from .AstroUtils import *

# # get the right filename of the dll/so
if platform.uname()[0] == "Windows":
    DLL_NAME = 'DllMain.dll'

if platform.uname()[0] == "Linux":
    DLL_NAME = 'libdllmain.so'

if platform.uname()[0] == "Darwin":
    DLL_NAME = 'libdllmain.dylib'


def LoadDllMainDll():
    """ LoadDllMainDll() -- Loads DllMain.dll from the PATH or LD_LIBRARY_PATH
    depending on Operating System and returns the object type.
    for each of its functions.

    Return Value
    an object which can be used to access the dll."""

    # load the dll
    try:
        dllObj = CDLL(DLL_NAME)
    except:
        print("Unable to load " + DLL_NAME)
        sys.exit(1)
    # set parameter list and return type for each function

    # Notes: This function has been deprecated since v9.0.
    # Initializes DllMain program (host of Astro Standards libraries) for use in any Astro Standards applications
    dllObj.DllMainInit.restype = c_longlong
    dllObj.DllMainInit.argtypes = []

    # Returns information about the DllMain DLL.
    # The returned string provides information about the version number, build date, and the platform.
    # infoStr: A string to hold the information about DllMain.dll. (out-Character[128])
    dllObj.DllMainGetInfo.restype = None
    dllObj.DllMainGetInfo.argtypes = [c_char_p]

    # Loads DllMain-related parameters (AS_MOIC) from a text file
    # dllMainFile: The name of the input file. (in-Character[512])
    dllObj.DllMainLoadFile.restype = c_int
    dllObj.DllMainLoadFile.argtypes = [c_char_p]

    # Opens a log file and enables the writing of diagnostic information into it.
    # All of the DLLs in the library will write diagnostic information into the log file once this function has been called.
    # If the file specified by logFileName already exists, its contents are erased.
    #
    # Enabling logging can potentially result in large amounts of diagnostic information being generated, which can lead to large amounts of storage being consumed as well as performance decreases. For this reason, it is recommended that this function only be used for debugging purposes.
    # fileName: The name of the log file to use. (in-Character[512])
    dllObj.OpenLogFile.restype = c_int
    dllObj.OpenLogFile.argtypes = [c_char_p]

    # Closes the currently open log file and reset the last logged error message to null.
    # Remember to close the log file before exiting the program.
    dllObj.CloseLogFile.restype = None
    dllObj.CloseLogFile.argtypes = []

    # Writes a message into the log file.
    # Make sure the log file is open by calling OpenLogFile before using this function.
    #
    # The message is limited to 128 characters. If the message is longer than this, it will be truncated.
    # msgStr: A message to be written into the log file. (in-Character[128])
    dllObj.LogMessage.restype = None
    dllObj.LogMessage.argtypes = [c_char_p]

    # Returns a character string describing the last error that occurred.
    # As a common practice, this function is called to retrieve the error message when an error occurs.
    #
    # This function works with or without an opened log file.
    #
    # If you call this function before you have called DllMainInit(), the function will return an invalid string. This could result in undefined behavior.
    # lastErrMsg: A string that stores the last logged error message. The message will be placed in the string you pass to this function. (out-Character[128])
    dllObj.GetLastErrMsg.restype = None
    dllObj.GetLastErrMsg.argtypes = [c_char_p]

    # Returns a character string describing the last informational message that was recorded.
    # This function is usually called right after space objects (TLEs, VCMs, sensors, observations, etc.) in an input text file were loaded. It gives information about how many records were successfully loaded, how many were bad, and how many were duplicated.
    #
    # This function works with or without an opened log file.
    #
    # If you call this function before you have called DllMainInit(), the function will return an invalid string. This could result in undefined behavior.
    # This function provides a quick way to check whether all of the prerequisite DLLs have been loaded and initialized correctly. Improper initialization of the Standardized Astrodynamic Algorithms DLLs is one of the most common causes of program crashes.
    # lastInfoMsg: A string that stores the last logged informational message. The message will be placed in the string you pass to this function. (out-Character[128])
    dllObj.GetLastInfoMsg.restype = None
    dllObj.GetLastInfoMsg.argtypes = [c_char_p]

    # Notes: This function has been deprecated since v9.0.
    # Returns a list of names of the Standardized Astrodynamic Algorithms DLLs that were initialized successfully.
    # initDllNames: A string that stores names of the DLLs that were initialized successfully. (out-Character[512])
    dllObj.GetInitDllNames.restype = None
    dllObj.GetInitDllNames.argtypes = [c_char_p]

    # Tests different input/output data types that are supported by the Astrodynamic Standards library.
    # cIn: an input character (in-Character)
    # cOut: an output character - should return the same value as the input cIn (out-Character)
    # intIn: an input 32-bit integer (in-Integer)
    # intOut: an output 32-bit integer - should return the same value as the input intIn (out-Integer)
    # longIn: an input 64-bit integer (in-Long)
    # longOut: an output 64-bit integer - should return the same value as the input longIn (out-Long)
    # realIn: an input 64-bit real (in-Double)
    # realOut: an output 64-bit real - should return the same value as the input realIn (out-Double)
    # strIn: input string (in-Character[512])
    # strOut: output string - should return the same value as the input strIn (out-Character[512])
    # int1DIn: an input array of 32-bit integers (in-Integer[3])
    # int1DOut: an output array of 32-bit integers - should return the same values as the input int1DIn (out-Integer[3])
    # long1DIn: an input array of 64-bit integers (in-Long[3])
    # long1DOut: an output array of 64-bit integers - should return the same values as the input long1DIn (out-Long[3])
    # real1DIn: an input array of 64-bit reals (in-Double[3])
    # real1DOut: an output array of 64-bit reals - should return the same values as the input real1DIn (out-Double[3])
    # int2DIn: an input 2D-array of 32-bit integers (2 rows, 3 columns) - for column-major order language, reverse the order (in-Integer[2, 3])
    # int2DOut: an output 2D-array of 32-bit integers - should return the same values as the input int2DIn (out-Integer[2, 3])
    # long2DIn: an input 2D-array of 64-bit integers (2 rows, 3 columns) - for column-major order language, reverse the order (in-Long[2, 3])
    # long2DOut: an output 2D-array of 64-bit integers - should return the same values as the input long2DIn (out-Long[2, 3])
    # real2DIn: an input 2D-array of 64-bit reals (2 rows, 3 columns) - for column-major order language, reverse the order (in-Double[2, 3])
    # real2DOut: an output 2D-array of 64-bit reals - should return the same values as the input real2DIn (out-Double[2, 3])
    dllObj.TestInterface.restype = None
    dllObj.TestInterface.argtypes = [c_char, c_char_p, c_int, c_int_p, c_longlong, c_longlong_p, c_double, c_double_p, c_char_p, c_char_p,
                                     c_int * 3, c_int * 3, c_longlong * 3, c_longlong * 3, c_double * 3, c_double * 3, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]

    # Tests different input/output data types that are supported by the Astrodynamic Standards library.
    # cInOut: Output should return 'Z' (inout-Character)
    # intInOut: Output should return Input + 1 (inout-Integer)
    # longInOut: Output should return Input + 2 (inout-Long)
    # realInOut: Output should return Input + 42.123456 (inout-Double)
    # strInOut: Output should return "It doesn't matter what your string was." (inout-Character[512])
    # int1DInOut: Output should return Input + 1 (inout-Integer[3])
    # long1DInOut: Output should return Input + 1234567890123456789 (inout-Long[3])
    # real1DInOut: Output should return Input + 42.0 (inout-Double[3])
    # int2DInOut: Output should return Input + 1 (inout-Integer[2, 3])
    # long2DInOut: Output should return Input + 6 (inout-Long[2, 3])
    # real2DInOut: Output should return Input + 7.6 (inout-Double[2, 3])
    dllObj.TestInterface2.restype = None
    dllObj.TestInterface2.argtypes = [c_char_p, c_int_p, c_longlong_p, c_double_p,
                                      c_char_p, c_int * 3, c_longlong * 3, c_double * 3, c_void_p, c_void_p, c_void_p]

    # Tests input and output arrays with unknown length that are supported by the Astrodynamic Standards library.
    # unk1DIn: Unknown dimension should be length (3) (in-Integer[*])
    # unk1DOut: Unknown dimension should be length (3), unk1DOut should return same as unk1DIn * 4 (out-Integer[*])
    # unk2DIn: Unknown dimension should be length (2) (in-Integer[*, 3])
    # unk2DOut: Unknown dimension should be length (2), unk2DOut should return same as unk2DIn * 5 (out-Integer[*, 3])
    dllObj.TestInterface3.restype = None
    dllObj.TestInterface3.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]

    # Returns data parsed from user's AS_MOIC-typed input card - up to 128 fields are allowed.
    # arrSize: size of the xa_moc array - actual number of fields the user enters in an "AS_MOIC" input card (in-Integer)
    # xa_moic: The returning xa_moc array (out-Double[*])
    dllObj.GetMOICData.restype = None
    dllObj.GetMOICData.argtypes = [c_int, c_void_p]

    # Sets ELSET key mode
    # This mode can also be turned on if the user loads an input text file that includes this line - "AS_DMA_ON" -
    # and is currently calling any of these methods: DllMainLoadFile(), TleLoadFile(), SpVecLoadFile(), or VcmLoadFile()
    # elset_keyMode: Desired elset key mode (see ELSET_KEYMODE_?) (in-Integer)
    dllObj.SetElsetKeyMode.restype = c_int
    dllObj.SetElsetKeyMode.argtypes = [c_int]

    # Gets current ELSET key mode
    dllObj.GetElsetKeyMode.restype = c_int
    dllObj.GetElsetKeyMode.argtypes = []

    # Sets key mode for ALL (elsets/obs/sensors). This takes precedence over individual elset/obs/sensor key mode
    # This mode can also be turned on if the user loads an input text file that includes this line - "AS_DMA_ALL_ON"
    # all_keyMode: Desired elset key mode (see ALL_KEYMODE_?) (in-Integer)
    dllObj.SetAllKeyMode.restype = c_int
    dllObj.SetAllKeyMode.argtypes = [c_int]

    # Gets current ALL (elsets/obs/sensors) key mode
    dllObj.GetAllKeyMode.restype = c_int
    dllObj.GetAllKeyMode.argtypes = []

    # Resets ALL (elsets/obs/sensors) key mode to its default value which then allows individual elsets/obs/sensors to use their own key mode settings.
    # Also reset DUPLICATION key mode to its default value.
    dllObj.ResetAllKeyMode.restype = None
    dllObj.ResetAllKeyMode.argtypes = []

    # Sets DUPLICATION key mode - change the default behavior of returning a key which already exists in memory: zero versus actual value
    # dupKeyMode: Desired duplication key mode (see DUPKEY_?) (in-Integer)
    dllObj.SetDupKeyMode.restype = c_int
    dllObj.SetDupKeyMode.argtypes = [c_int]

    # Gets current DUPLICATION key mode
    dllObj.GetDupKeyMode.restype = c_int
    dllObj.GetDupKeyMode.argtypes = []

    # Retrieves error message associated with the input errCode.
    # As a common practice, this function is called to retrieve the error message when an error occurs.
    # errCode: Input error code (in-Integer)
    # errMsg: A string that stores the last logged error message. The message will be placed in the string you pass to this function. (out-Character[128])
    dllObj.GetErrMsg.restype = None
    dllObj.GetErrMsg.argtypes = [c_int, c_char_p]

    # Sets error message mode
    # mode = 0: Only last error message is stored and then retrieved via GetLastErrMsg(). Appropriate for single-thread applications
    # mode = 1: Each thread stores and retrieves its own error message via GetErrMsg(). Appropriate for multi-thread applications
    # mode: Error message mode: 0= use GetLastErrMsg(), 1= use GetErrMsg() to retrieve appropriate error message (in-Integer)
    dllObj.SetErrMsgMode.restype = c_int
    dllObj.SetErrMsgMode.argtypes = [c_int]

    # Gets error message mode
    # mode = 0: Only last error message is stored and then retrieved via GetLastErrMsg(). Appropriate for single-thread applications
    # mode = 1: Each thread stores and retrieves its own error message via GetErrMsg(). Appropriate for multi-thread applications
    dllObj.GetErrMsgMode.restype = c_int
    dllObj.GetErrMsgMode.argtypes = []

    # Comment out the below line to disable load message
    # print(DLL_NAME + ' loaded successfully.')
    return dllObj


# log message string length
LOGMSGLEN = 128

# DHN 06Feb12 - Increase file path length to 512 characters from 128 characters to handle longer file path
FILEPATHLEN = 512

# DHN 10Feb12 - Uniformally using 512 characters to passing/receiving string in all Get/Set Field functions
GETSETSTRLEN = 512

INFOSTRLEN = 128

# DHN 10Feb12 - All input card types' (elsets, ob, sensors, ...) can now have maximum of 512 characters
INPUTCARDLEN = 512

# Different orbital element types
# Element type - SGP Tle type 0
ELTTYPE_TLE_SGP = 1
# Element type - SGP4 Tle type 2
ELTTYPE_TLE_SGP4 = 2
# Element type - SP Tle type 6
ELTTYPE_TLE_SP = 3
# Element type - SP Vector
ELTTYPE_SPVEC_B1P = 4
# Element type - VCM
ELTTYPE_VCM = 5
# Element type - External ephemeris
ELTTYPE_EXTEPH = 6
# Element type - SGP Tle type 4 - XP
ELTTYPE_TLE_XP = 7
# Element type - PPT3 Tle type 3 - XP
ELTTYPE_TLE_PPT3 = 8

# *******************************************************************************

# Propagation types
# GP/SGP4/SGP4-XP propagator
PROPTYPE_GP = 1
# SP propagator
PROPTYPE_SP = 2
# External ephemeris
PROPTYPE_X = 3
# Unknown
PROPTYPE_UK = 4
# *******************************************************************************

# Add sat error
# Bad satellite key
BADSATKEY = -1
# Bad satellite number
BADSATNUM = -1
# Duplicate satellite key
DUPSATKEY = 0

# *******************************************************************************

# satellite/observation/sensor key possible errors
# Bad (satellite/observation/sensor) key
BADKEY = -1
# Duplicate (satellite/observation/sensor) key
DUPKEY = 0

# *******************************************************************************

# Options used in GetLoaded()
# ascending order
IDX_ORDER_ASC = 0
# descending order
IDX_ORDER_DES = 1
# order as read
IDX_ORDER_READ = 2
# tree traversal order
IDX_ORDER_QUICK = 9

# *******************************************************************************

# Different key mode options for all elset-satKey/obs-obsKey/sensor-senKey
# Default - duplicate elsets/observations/sensors can not be loaded in their binary trees
ALL_KEYMODE_NODUP = 0
# Allow duplicate elsets/obs/sensor to be loaded and have direct memory access (DMA - no duplication check and no binary tree)
ALL_KEYMODE_DMA = 1

# *******************************************************************************


# Different key mode options for elset satKey
# Default - duplicate elsets can not be loaded in binary tree
ELSET_KEYMODE_NODUP = 0
# Allow duplicate elsets to be loaded and have direct memory access (DMA - no duplication check and no binary tree)
ELSET_KEYMODE_DMA = 1

# *******************************************************************************

# Different duplication key mode options (apply to non DMA mode only)
# Returning (satellite/sensor/obs) key is zero to signify the existing data/key was already in memory
DUPKEY_ZERO = 0
# Return actual (satellite/sensor/obs) key regardless of the key/data duplication
DUPKEY_ACTUAL = 1

# *******************************************************************************


# Input time is in minutes since epoch
TIME_IS_MSE = 1
# Input time is in days since 1950 TAI
TIME_IS_TAI = 2
# Input time is in days since 1950 UTC
TIME_IS_UTC = 3

# *******************************************************************************

# ========================= End of auto generated code ==========================
