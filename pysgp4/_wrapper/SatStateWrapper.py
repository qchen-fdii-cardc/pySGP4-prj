# This wrapper file was generated automatically by the GenDllWrappers program.
import sys
import os
import platform
from ctypes import *
from .AstroUtils import *

# get the right filename of the dll/so
if platform.uname()[0] == "Windows":
    DLL_NAME = 'SatState.dll'

if platform.uname()[0] == "Linux":
    DLL_NAME = 'libsatstate.so'

if platform.uname()[0] == "Darwin":
    DLL_NAME = 'libsatstate.dylib'


def LoadSatStateDll():
    """ LoadSatStateDll() -- Loads SatState.dll from the PATH or LD_LIBRARY_PATH
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
    # Initializes SatState DLL for use in the program
    # If this function returns an error, it is recommended that the users stop the program immediately.
    # The error occurs if the users forget to load and initialize all the prerequisite DLLs,
    # as listed in the DLL Prerequisite section, before using this DLL.
    # apAddr: The handle that was returned from DllMainInit() (in-Long)
    dllObj.SatStateInit.restype = c_int
    dllObj.SatStateInit.argtypes = [c_longlong]

    # Returns information about the current version of SatState DLL.
    # The information is placed in the string parameter passed in.
    # The returned string provides information about the version number, build date, and the platform of the SatState DLL.
    # infoStr: A string to hold the information about SatState.dll (out-Character[128])
    dllObj.SatStateGetInfo.restype = None
    dllObj.SatStateGetInfo.argtypes = [c_char_p]

    # Loads any orbital element types (TLE's/SPVEC's/VCM's), EXTEPHEM's, and/or propagator controls from an input text file
    # Internally, if taskMode = 1, this function calls SpProp.SpLoadFile();
    # and if taskMode = 2, this function calls Tle.TleLoadFile(), SpVec.SpVecLoadFile(), Vcm.VcmLoadFile(), ExtEphem.ExtEphLoadFile();
    # if taskMode = 3, both tasks (1 and 2) are executed.
    # inputFile: The name of the input file to load (in-Character[512])
    # xf_Task: Specified task mode: 1=load SP control parameters, 2=load elsets only, 3=both 1 + 2 (in-Integer)
    dllObj.SatStateLoadFile.restype = c_int
    dllObj.SatStateLoadFile.argtypes = [c_char_p, c_int]

    # Saves currently loaded orbital element types (TLE's/SPVEC's/VCM's), EXTEPHEM's, and/or propagator controls to a file
    # The purpose of this function is to save the current SatState-related settings, usually used in GUI applications, for future use.
    #
    # Internally, if taskMode = 1, this function calls SpProp.SpSaveFile();
    # and if taskMode = 2, this function calls Tle.TleSaveFile(), SpVec.SpVecSavedFile(), Vcm.VcmSaveFile(), ExtEphem.ExtEphSaveFile();
    # if taskMode = 3, both tasks (1 and 2) are executed.
    # outFile: The name of the file in which to save the settings (in-Character[512])
    # saveMode: Specifies whether to create a new file or append to an existing one (0 = create, 1= append) (in-Integer)
    # saveForm: Specifies the mode in which to save the file (0 = text format, 1 = not yet implemented, reserved for future) (in-Integer)
    # xf_Task: Specified task mode: 1=Only save propagator control parameters, 2=Only save orbital elements/external ephemeris data,	3=Save both 1 + 2 (in-Integer)
    dllObj.SatStateSaveFile.restype = c_int
    dllObj.SatStateSaveFile.argtypes = [c_char_p, c_int, c_int, c_int]

    # Removes a satellite from the appropriate elset DLL's set of loaded satellites.
    # The function will automatically choose the proper set of elsets from which to remove the satellite.
    # The choices are: Tle.dll, SpVec.dll, Vcm.dll, or ExtEphem.dll
    # If the users enter an invalid satKey (a satKey that does not exist in memory), the function will return a non-zero value indicating an error.
    # satKey: The unique key of the satellite to be removed (in-Long)
    dllObj.SatStateRemoveSat.restype = c_int
    dllObj.SatStateRemoveSat.argtypes = [c_longlong]

    # Removes a satellite from the appropriate sets of loaded satellites (elset dll and propagator dll).
    # The function will remove the satellite from the elset DLL's sets as in SatStateRemoveSat() and
    # from the appropriate propagator's set of initialized satellites if it exists there.
    # satKey: The unique key of the satellite to be removed (in-Long)
    dllObj.SatStateRemoveSatAll.restype = c_int
    dllObj.SatStateRemoveSatAll.argtypes = [c_longlong]

    # Removes all satellites from all of the loaded data sets.
    # It will remove all satellites from the following sets: Tle, SpVec, Vcm, ExtEphem, Sgp4Prop, and SpProp
    dllObj.SatStateRemoveAllSats.restype = c_int
    dllObj.SatStateRemoveAllSats.argtypes = []

    # Resets propagator settings back to their default values
    dllObj.SatStateReset.restype = None
    dllObj.SatStateReset.argtypes = []

    # Returns the total number of satellites (TLE's, SPVEC's, VCM's, and EXTEPHEM's) currently loaded in memory
    # See SatStateGetLoaded for example.
    # This function is useful for dynamically allocating memory for the array that is passed to the function SatStateGetLoaded.
    dllObj.SatStateGetCount.restype = c_int
    dllObj.SatStateGetCount.argtypes = []

    # Retrieves all of the currently loaded satKeys.
    # These satKeys can be used to access the internal data for the satellites.
    # It is recommended that SatStateGetCount() is used to count how many satellites are currently loaded in memory.
    # The user can then use this number to dynamically allocate the satKeys array and pass it to this function.
    #
    # If the user prefers to pass a static array to the function, make sure it is big enough to store all the satKeys in memory.
    # order: Specifies the order in which the satKeys should be returned:	0=ascending order, 1=descending order, 2=order in which the satKeys were loaded in memory (in-Integer)
    # satKeys: The array in which to store the satKeys (out-Long[*])
    dllObj.SatStateGetLoaded.restype = None
    dllObj.SatStateGetLoaded.argtypes = [c_int, c_void_p]

    # Returns the first satKey that contains the specified satellite number in all sets of loaded satellites.
    # These sets will be searched: Tle, SpVec, Vcm, and ExtEphem.
    # This function is useful when a satellite is used in applications that require only one record for one
    # satellite and the applications refer to that satellite by its satellite number.
    # However, the Astrodynamic Standard Shared library is only working with satKeys, this function helps to return the associated satKey of that satellite.
    # satNum: The satellite number to search for (in-Integer)
    dllObj.SatStateNumToKey.restype = c_longlong
    dllObj.SatStateNumToKey.argtypes = [c_int]

    # Retrieves the data which is common to all satellite types.
    # All common fields are retrieved with a single function call.
    # The apogee height and perigee height are defined as the distance above an ellipsoid
    # created using the earth flattening factor from the selected geopotential model.
    # Note:  When using SP elsets (TLE type 6, SPVEC, or VCM), calling SatStateGetSatDataAll
    # will implicitly call SpInit in order to extract the mu value from the GEO file the elset is tied to.
    # The elset must have a valid GEO directory available or an error will be returned.
    # satKey: The satellite's unique key (in-Long)
    # satNum: Satellite number (out-Integer)
    # satName: Satellite international designator (out-Character[8])
    # eltType: Element type (see ELTTYPE_?) (out-Integer)
    # revNum: Revolution number at epoch (out-Integer)
    # epochDs50UTC: Epoch time time in days since 1950 UTC (out-Double)
    # bField: Ballistic coefficient (m^2/kg) (out-Double)
    # elsetNum: Element set number (out-Integer)
    # incli: Inclination (deg) (out-Double)
    # node: Right ascension of ascending node (deg) (out-Double)
    # eccen: Eccentricity (out-Double)
    # omega: Argument of perigee (deg) (out-Double)
    # mnAnomaly: Mean anomaly (deg) (out-Double)
    # mnMotion: Mean motion (rev/day) (out-Double)
    # period: Satellite period (min) (out-Double)
    # perigeeHt: Satellite perigee height (km) above the ellipsoid (out-Double)
    # apogeeHt: Satellite apogee height (km) above the ellipsoid (out-Double)
    # perigee: Satellite perigee height from the center of the earth (km) (out-Double)
    # apogee: Satellite apogee height from the center of the earth (km) (out-Double)
    # a: Semi-major axis (km) (out-Double)
    dllObj.SatStateGetSatDataAll.restype = c_int
    dllObj.SatStateGetSatDataAll.argtypes = [c_longlong, c_int_p, c_char_p, c_int_p, c_int_p, c_double_p, c_double_p, c_int_p, c_double_p,
                                             c_double_p, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p]

    # Retrieves an individual field of a satellite.
    # satKey: The satellite's unique key (in-Long)
    # xf_Sat: Predefined number specifying which field to retrieve (see XF_SAT_?) (in-Integer)
    # retVal: A string to contain the value of the requested field (out-Character[512])
    dllObj.SatStateGetSatDataField.restype = c_int
    dllObj.SatStateGetSatDataField.argtypes = [c_longlong, c_int, c_char_p]

    # Initializes a TLE, SPVEC, or VCM in preparation for propagation, or an EXTEPHEM in preparation for interpolation
    # satKey: The satellite's unique key (in-Long)
    dllObj.SatStateInitSat.restype = c_int
    dllObj.SatStateInitSat.argtypes = [c_longlong]

    # Propagates a TLE/SPVEC/VCM, or interpolates an EXTEPHEM.
    # The satellite is propagated/interpolated to the specified time calculated in minutes since the satellite's epoch time
    # satKey: The satellite's unique key (in-Long)
    # mse: The time to propagate to, specified in minutes since the satellite's epoch time (in-Double)
    # ds50UTC: Resulting time in days since 1950, UTC (out-Double)
    # revNum: Revolution number (out-Integer)
    # pos: Resulting ECI position vector (km) in True Equator and Mean Equinox of Epoch (out-Double[3])
    # vel: Resulting ECI velocity vector (km/s) in True Equator and Mean Equinox of Epoch (out-Double[3])
    # llh: Resulting geodetic latitude (deg), longitude(deg), and height (km) (out-Double[3])
    dllObj.SatStateMse.restype = c_int
    dllObj.SatStateMse.argtypes = [
        c_longlong, c_double, c_double_p, c_int_p, c_double * 3, c_double * 3, c_double * 3]

    # Propagates a TLE/SPVEC/VCM, or interpolates an EXTEPHEM.
    # The satellite is propagated/interpolated to the specified time calculated in days since 1950, UTC.
    # satKey: The satellite's unique key (in-Long)
    # ds50UTC: The time to propagate to, specified in days since 1950, UTC (in-Double)
    # mse: Resulting time in minutes since the satellite's epoch time (out-Double)
    # revNum: Revolution number (out-Integer)
    # pos: Resulting ECI position vector (km) in True Equator and Mean Equinox of Epoch (out-Double[3])
    # vel: Resulting ECI velocity vector (km/s) in True Equator and Mean Equinox of Epoch (out-Double[3])
    # llh: Resulting geodetic latitude (deg), longitude(deg), and height (km) (out-Double[3])
    dllObj.SatStateDs50UTC.restype = c_int
    dllObj.SatStateDs50UTC.argtypes = [
        c_longlong, c_double, c_double_p, c_int_p, c_double * 3, c_double * 3, c_double * 3]

    # Returns additional propagated/interpolated results (reserved for future implementation)
    # Reserved for future implementation
    # Use this function immediately after the call to SatStateMse or SatStateDs50UTC.
    # satKey: the satellite's unique key (in-Long)
    # index: type of returned data (in-Integer)
    # destArr: the resulting array (out-Double[128])
    dllObj.SatStateGetPropOut.restype = c_int
    dllObj.SatStateGetPropOut.argtypes = [c_longlong, c_int, c_double * 128]

    # Returns various ephemeris comparison results between two satellite states.
    #
    # The "in-track" is NOT the velocity direction, but is defined as completing the right handed coordinate system
    # defined by the position vector (radial) and the angular momentum vector (cross-track).
    # primSatKey: The primary satellite's unique key (in-Long)
    # secSatKey: The secondary satellite's unique key (in-Long)
    # ds50UTC: Requested time in days since 1950 UTC (in-Double)
    # uvwFlag: UVW coordinate system flag: 0=use rotating UVW, 1=use inertial UVW (in-Integer)
    # xa_Delta: The resulting ephemeris comparison deltas (see XA_DELTA_?) (out-Double[100])
    dllObj.SatStateEphCom.restype = c_int
    dllObj.SatStateEphCom.argtypes = [
        c_longlong, c_longlong, c_double, c_int, c_double * 100]

    # Returns various ephemeris comparison results between two satellite states (_OS one step) .
    #
    # The "in-track" is NOT the velocity direction, but is defined as completing the right handed coordinate system
    # defined by the position vector (radial) and the angular momentum vector (cross-track).
    # priPosVel: The primary satellite's state (TEME of Date) in an array (position(1st-3rd, km), velocity(4th-6th, km/s)) (in-Double[6])
    # secPosVel: The secondary satellite's state (TEME of Date) in an array (position(1st-3rd, km), velocity(4th-6th, km/s)) (in-Double[6])
    # ds50UTC: Requested time in days since 1950 UTC (in-Double)
    # uvwFlag: UVW coordinate system flag: 0=use rotating UVW, 1=use inertial UVW (in-Integer)
    # xa_Delta: The resulting ephemeris comparison deltas (see XA_DELTA_?) (out-Double[100])
    dllObj.SatStateEphCom_OS.restype = None
    dllObj.SatStateEphCom_OS.argtypes = [
        c_double * 6, c_double * 6, c_double, c_int, c_double * 100]

    # Determines if a satellite contains covariance matrix.
    # 0=no, 1=yes
    # satKey: the satellite's unique key (in-Long)
    dllObj.SatStateHasCovMtx.restype = c_int
    dllObj.SatStateHasCovMtx.argtypes = [c_longlong]

    # Propagates/Interpolates UVW covariance matrix from VCM/External ephemeris to the time in days since 1950
    # satKey: The satellite's unique key (in-Long)
    # ds50UTC: The input time in days since 1950 UTC (in-Double)
    # covUVW: 6x6 UVW covariance matrix (out-Double[6, 6])
    dllObj.SatStateGetCovUVW.restype = c_int
    dllObj.SatStateGetCovUVW.argtypes = [c_longlong, c_double, c_void_p]

    # Generate external ephemeris file for the specified satellite (via its unique satKey)
    # Note: No need to initialize the satellite before this call. If it was intialized, it will be removed after this call
    # satKey: The satellite's unique key (in-Long)
    # startDs50UTC: Start time in days since 1950 UTC (in-Double)
    # stopDs50UTC: Stop time in days since 1950 UTC (in-Double)
    # stepSizeSecs: Step size in seconds. Set to zero if natural integration step size (auto adjust) is desired for SP propagator, and use original data points for external ephemeris file (in-Double)
    # ephFileName: The generated external ephemeris file name (in-Character[512])
    # ephFileType: External ephemeris file type (see EPHFILETYPE_?) (in-Integer)
    dllObj.SatStateGenEphFile.restype = c_int
    dllObj.SatStateGenEphFile.argtypes = [
        c_longlong, c_double, c_double, c_double, c_char_p, c_int]

    # Finds the time of ascending nodal crossing of the specified satellite prior to an input time in days since 1950 TAI
    # satKey: The satellite's unique key (in-Long)
    # ds50TAI: Input time in ds50TAI (in-Double)
    dllObj.GetNodalCrossingPriorToTime.restype = c_double
    dllObj.GetNodalCrossingPriorToTime.argtypes = [c_longlong, c_double]

    # Get the Gobs parameters for a TLE (SGP4/XP only)
    # satKey: The satellite's unique key (in-Long)
    # ds50UTC: Propagation in days since 1950 UTC (in-Double)
    # xa_gobs: (See XA_GOBS_?) (out-Double[32])
    # errCode: Error code (out-Integer)
    dllObj.GetGobsParams.restype = None
    dllObj.GetGobsParams.argtypes = [
        c_longlong, c_double, c_double * 32, c_int_p]

    # Does an XP GOBS comparison
    # primSatKey: The primary satellite's unique key (in-Long)
    # secSatKey: The secondary satellite's unique key (in-Long)
    # ds50UTC: Common epoch to compare in days since 1950 UTC (in-Double)
    # xa_gobs_lim: The gobs comparison limits (see XA_GOBS_LIM?) (in-Double[16])
    # xa_gobs_delta: The resulting gobs comparison deltas (see XA_GOBS_DELTA_?) (out-Double[16])
    dllObj.GobsCom.restype = c_int
    dllObj.GobsCom.argtypes = [c_longlong, c_longlong,
                               c_double, c_double * 16, c_double * 16]

    # Does an XP GOBS comparison using gobs arrays
    # xa_gobs_prim: Primary sat GOBS parameters (see XA_GOBS_?) (in-Double[32])
    # xa_gobs_sec: Secondary sat GOBS parameters (see XA_GOBS_?) (in-Double[32])
    # xa_gobs_lim: The gobs comparison limits (see XA_GOBS_LIM_?) (in-Double[16])
    # xa_gobs_delta: The resulting gobs comparison deltas (see XA_GOBS_DELTA_?) (out-Double[16])
    dllObj.GobsComArr.restype = None
    dllObj.GobsComArr.argtypes = [c_double * 32,
                                  c_double * 32, c_double * 16, c_double * 16]

    # Comment out the below line to disable load message
    # print(DLL_NAME + ' loaded successfully.')
    return dllObj


# Indexes of available satellite data fields
# Satellite epoch time in days since 1950 UTC
XF_SATFIELD_EPOCHUTC = 1
# Mean anomaly (deg)
XF_SATFIELD_MNANOM = 2
# Right ascension of asending node (deg)
XF_SATFIELD_NODE = 3
# Argument of perigee (deg)
XF_SATFIELD_OMEGA = 4
# Satellite's period (min)
XF_SATFIELD_PERIOD = 5
# Eccentricity
XF_SATFIELD_ECCEN = 6
# Orbit inclination (deg)
XF_SATFIELD_INCLI = 7
# Mean motion (rev/day)
XF_SATFIELD_MNMOTION = 8
# GP B* drag term (1/er)  or SP Radiation Pressure Coefficient
XF_SATFIELD_BFIELD = 9
# Perigee height above the geoid (km)
XF_SATFIELD_PERIGEEHT = 10
# Apogee height above the geoid (km)
XF_SATFIELD_APOGEEHT = 11
# Perigee height above the center of the earth (km)
XF_SATFIELD_PERIGEE = 12
# Apogee height above the center of the earth (km)
XF_SATFIELD_APOGEE = 13
# Semimajor axis (km)
XF_SATFIELD_A = 14
# Mean motion derivative (rev/day**2 /2)
XF_SATFIELD_NDOT = 15
# Satellite category (Synchronous, Deep space, Decaying, Routine)
XF_SATFIELD_SATCAT = 16
# Astat 3 Height multiplier
XF_SATFIELD_HTM3 = 17
# Center of mass offset (m)
XF_SATFIELD_CMOFFSET = 18
# Unused
XF_SATFIELD_N2DOT = 19
# GP node dot (deg/s)
XF_SATFIELD_NODEDOT = 20
# GP only - the last time when propagation has error
XF_SATFIELD_ERRORTIME = 21
# value of mu
XF_SATFIELD_MU = 22


# *******************************************************************************

# Indexes of available deltas
# delta position (km)
XA_DELTA_POS = 0
# delta time (sec)
XA_DELTA_TIME = 1
# delta position in radial direction (km)
XA_DELTA_PRADIAL = 2
# delta position in in-track direction (km)
XA_DELTA_PINTRCK = 3
# delta position in cross-track direction (km)
XA_DELTA_PCRSSTRCK = 4
# delta velocity (km/sec)
XA_DELTA_VEL = 5
# delta velocity in radial direction (km/sec)
XA_DELTA_VRADIAL = 6
# delta velocity in in-track direction (km/sec)
XA_DELTA_VINTRCK = 7
# delta velocity in cross-track direction (km/sec)
XA_DELTA_VCRSSTRCK = 8
# delta Beta (deg)
XA_DELTA_BETA = 9
# delta height (km)
XA_DELTA_HEIGHT = 10
# delta angular momentum (deg)
XA_DELTA_ANGMOM = 11
# 3D position Mahalanobis distance in UVW Space (Bubble Covariance, only if covariance propagation is available or turned on)
XA_DELTA_MHLNBS_UVW = 12
# 3D position Mahalanobis distance in Height-Time_Beta Space (Banana Covariance, only if covariance propagation is available or turned on)
XA_DELTA_MHLNBS_HTB = 13

XA_DELTA_SIZE = 100

# Indexes of Satellite data fields
# Satellite number I5
XF_SAT_NUM = 1
# Satellite international designator A8
XF_SAT_NAME = 2
# Element type I1 (old name XF_SAT_EPHTYPE)
XF_SAT_ELTTYPE = 3
# Obsolete - should use new name XF_SAT_ELTTYPE instead
XF_SAT_EPHTYPE = 3
# Epoch revolution number I6
XF_SAT_REVNUM = 4
# Epoch time in days since 1950
XF_SAT_EPOCH = 5
# BStar drag component (GP) or Ballistic coefficient-BTerm (SP) (m^2/kg)
XF_SAT_BFIELD = 6
# Element set number
XF_SAT_ELSETNUM = 7
# Inclination (deg)
XF_SAT_INCLI = 8
# Right ascension of ascending node (deg)
XF_SAT_NODE = 9
# Eccentricity
XF_SAT_ECCEN = 10
# Argument of perigee (deg)
XF_SAT_OMEGA = 11
# Mean anomaly (deg)
XF_SAT_MNANOM = 12
# Mean motion (revs/day)
XF_SAT_MNMOTN = 13
# Satellite period (min)
XF_SAT_PERIOD = 14
# Perigee Height(km)
XF_SAT_PERIGEEHT = 15
# Apogee Height (km)
XF_SAT_APOGEEHT = 16
# Perigee(km)
XF_SAT_PERIGEE = 17
# Apogee (km)
XF_SAT_APOGEE = 18
# Semi-major axis (km)
XF_SAT_A = 19


# Indexes of SatState's load/save file task mode
# Only load/save propagator control parameters
XF_TASK_CTRLONLY = 1
# Only load/save orbital elements/external ephemeris data
XF_TASK_SATONLY = 2
# Load/Save both 1 and 2
XF_TASK_BOTH = 3


# Different external ephemeris file types
# ITC file format
EPHFILETYPE_ITC = 1
# ITC compact (without covariance matrix) file format
EPHFILETYPE_ITC_WOCOV = 2


# Gobs records
# Satellite number
XA_GOBS_SATNUM = 0
# East Longitude
XA_GOBS_LONE = 1
# Longitude Drift Rate
XA_GOBS_DRIFT = 2
# satellite's relative energy (deg^2/sec^2) - only for GOBS
XA_GOBS_RELENERGY = 3
# sin(incl)*sin(r.a. node)
XA_GOBS_WX = 4
# -sin(incl)*cos(r.a. node)
XA_GOBS_WY = 5
# cos(incl)
XA_GOBS_WZ = 6
# abar x
XA_GOBS_ABARX = 7
# abar y
XA_GOBS_ABARY = 8
# abar z
XA_GOBS_ABARZ = 9
# AGOM
XA_GOBS_AGOM = 10
# Trough/Drift Flag, 0 - 75 deg trough, 1 - 255 deg trough, 2 - both troughs, 3 - unstable point, 4 - East drift, 5 - West drift
XA_GOBS_TROUGH = 11
# Total Energy of sat (-mu/(2*a))
XA_GOBS_TOTENERGY = 12
# Inclination of sat
XA_GOBS_INCL = 13

XA_GOBS_SIZE = 32


# Indexes of GOBS limits
# 0 - ignore trough logic, 1 - implement trough logic
XA_GOBS_LIM_TROUGH = 0
# Primary satellite is plane changer
XA_GOBS_LIM_PCP = 1
# Secondary satellite is plane changer
XA_GOBS_LIM_PCS = 2
# Primary satellite is plane changer
XA_GOBS_LIM_ACTIVEP = 3
# Secondary satellite is plane changer
XA_GOBS_LIM_ACTIVES = 4
# Min Longitude of sat
XA_GOBS_LIM_LONGMIN = 5
# Max Longitude of sat
XA_GOBS_LIM_LONGMAX = 6
# Min Agom of sat
XA_GOBS_LIM_AGOMMIN = 7
# Max Agom of sat
XA_GOBS_LIM_AGOMMAX = 8
# Max Inclination of sat
XA_GOBS_LIM_INCLMAX = 9

XA_GOBS_LIM_SIZE = 16


# Indexes of available deltas
# Primary satellite number
XA_GOBS_DELTA_PRIMESAT = 0
# Secondary satellite number
XA_GOBS_DELTA_SECONDARYSAT = 1
# GOBS correlation score
XA_GOBS_DELTA_ASTAT = 2
# delta orbital plane
XA_GOBS_DELTA_DOP = 3
# delta shape
XA_GOBS_DELTA_DABAR = 4
# delta Relative Energy (deg^2/day^2)
XA_GOBS_DELTA_DRELENERGY = 5
# Longitude of Primary
XA_GOBS_DELTA_LONGP = 6
# Minimum Longitude of Secondary
XA_GOBS_DELTA_LONGMIN = 7
# Maximum Longitude of Secondary
XA_GOBS_DELTA_LONGMAX = 8
# 0 - opposite throughs or drift rates, 1 - trough or drift rates match
XA_GOBS_DELTA_TROUGH = 9
# 0|1    Plane Match Flag
XA_GOBS_DELTA_PLANE = 10
# 0|1    Shape Match Flag
XA_GOBS_DELTA_SHAPE = 11
# 0|1    Relative Energy Match Flag
XA_GOBS_DELTA_ENERGY = 12
# 0|1|2  Longitude Match Flag (2 is fuzzy match)
XA_GOBS_DELTA_LONG = 13
# 0|1    Agom Match Flag
XA_GOBS_DELTA_AGOM = 14
# 0|1    Incl Match Flag
XA_GOBS_DELTA_INCL = 15

XA_GOBS_DELTA_SIZE = 16


# *******************************************************************************

# ========================= End of auto generated code ==========================
