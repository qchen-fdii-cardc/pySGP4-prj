from ctypes import create_string_buffer

from ._wrapper.DllMainWrapper import LoadDllMainDll
from ._wrapper.EnvConstWrapper import LoadEnvConstDll
from ._wrapper.TimeFuncWrapper import LoadTimeFuncDll
from ._wrapper.AstroUtils import CreateCArray, c_double, c_int

DllMain = LoadDllMainDll()
EnvConst = LoadEnvConstDll()
TimeFunc = LoadTimeFuncDll()


#############################################################################
# Timing Constants Functions
#############################################################################

def is_tcon_file_loaded():
    """
    Checks if the timing constants file is loaded.
    Returns:
        bool: True if the timing constants file is loaded, False otherwise.
    """
    return TimeFunc.IsTConFileLoaded() == 1


def time_func_load_file(file_path):
    """
    Loads timing constants data and prediction control (6P-card) from an input file. 
    Time constants can be included directly in the main input file or they can be
      read from a separate file identified with "TIMFIL=[pathname\filename]".

    The input file is read in two passes. The function first looks for "TIMFIL=" lines, 
    then it looks for timing constant data which was included directly. 
    The result of this is that data entered using both methods will be processed, 
    but the "TIMFIL=" data will be processed first.

    The time constants are also read in from each VCM. However, 
    only the most recent time constants among VCMs are stored 
    in the memory, see VCM.dll documentation.

    Parameters
        tconFile	The name of the file from which to read timing constants data and/or prediction control data. (in-Character[512])
    Returns
        0 if the input file is loaded successfully, non-0 if there is an error.    
    """

    if TimeFunc.TimeFuncLoadFile(file_path.encode('utf-8')) != 0:
        raise RuntimeError(
            f"Failed to load timing constants file: {file_path}")


def tcon_load_file(file_path):
    """
    Loads the timing constants file from the specified path.
    Args:
        file_path (str): The path to the timing constants file.
    Raises:
        RuntimeError: If the file cannot be loaded.
    """
    result = TimeFunc.TConLoadFile(file_path.encode('utf-8'))
    if result != 0:
        raise RuntimeError(
            f"Failed to load timing constants file: {file_path}")


def tcon_reomove_all():
    """
    Removes all timing constants records from memory.

    Raises:
        RuntimeError: If the records cannot be removed.
    """
    if TimeFunc.TConRemoveAll() != 0:
        raise RuntimeError(
            "Failed to remove timing constants records from memory.")


def tcon_save_file(file_path: str, save_mode: int = 0, save_form: int = 0):
    """
    Saves currently loaded timing constants data to a file. The data will be saved in the format specified by the form parameter, regardless of the format or method originally used to load it.

    Parameters
        tconFile	The name of the file in which to save the timing constants data. (in-Character[512])
        saveMode	Specifies whether to create a new file or append to an existing one. (0 = Create new file, 1= Append to existing file) (in-Integer)
        saveForm	Specifies the format in which to save the file. (0 = SPECTER Print Record format, 1 = XML format (future implementation)) (in-Integer)
    Returns
        0 if the data is successfully saved to the file, non-0 if there is an error.
    """
    result = TimeFunc.TConSaveFile(
        file_path.encode('utf-8'), save_mode, save_form)
    if result != 0:
        raise RuntimeError(
            f"Failed to save timing constants data to file: {file_path}")


def tcon_add_a_record(ds50utc, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY):
    """
    Adds a timing constant record to memory. 
    Note that this function is solely for backward compatible with legacy software. 
    Notes: only the latest timing record is stored in memory using this method. 
    Input timing record will be skipped/ignored if it's earlier than the existing one 
    The users should use TConLoadFile or TimeFuncLoadFile to load timing constants file instead.

    Parameters
        refDs50UTC	Reference time (days since 1950, UTC) (in-Double)
        leapDs50UTC	Leap Second time (days since 1950, UTC) (in-Double)
        taiMinusUTC	TAI minus UTC offset at the reference time (seconds) (in-Double)
        ut1MinusUTC	UT1 minus UTC offset at the reference time (seconds) (in-Double)
        ut1Rate	UT1 rate of change versus UTC at the reference time (msec/day) (in-Double)
        polarX	Polar wander (X direction) at the reference time (arc-seconds) (in-Double)
        polarY	Polar wander (Y direction) at the reference time (arc-seconds) (in-Double)
    Returns
        0 if the timing constants record is successfully added to memory, non-0 if there is an error.
    """
    result = TimeFunc.TConAddARec(
        ds50utc, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)
    if result != 0:
        raise RuntimeError(
            f"Failed to add timing constant record to memory for ds50UTC: {ds50utc}")


def tcon_add_one(refDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY):
    """
    Adds one timing constant record to memory. 
    This API can be used to avoid TConLoadFile's file I/O

    Parameters
        refDs50UTC	Reference time (days since 1950, UTC) (in-Double)
        leapDs50UTC	Leap Second time (days since 1950, UTC) (in-Double)
        taiMinusUTC	TAI minus UTC offset at the reference time (seconds) (in-Double)
        ut1MinusUTC	UT1 minus UTC offset at the reference time (seconds) (in-Double)
        ut1Rate	UT1 rate of change versus UTC at the reference time (msec/day) (in-Double)
        polarX	Polar wander (X direction) at the reference time (arc-seconds) (in-Double)
        polarY	Polar wander (Y direction) at the reference time (arc-seconds) (in-Double)
    Returns
        0 if the timing constants record is successfully added to memory, non-0 if there is an error.
    """
    result = TimeFunc.TConAddOne(
        refDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)
    if result != 0:
        raise RuntimeError(
            f"Failed to add timing constant record to memory for ds50UTC: {refDs50UTC}")


def tcon_time_span():
    """
    Returns the time span of the loaded timing constants - the earliest and latest of loaded timing constant records

    Parameters
        numOfRecs	Number of timing constants records loaded in memory (zero if timing constants aren't loaded) (out-Integer)
        frTimeDs50UTC	The time, in days since 1950 UTC, of the earliest timing constant record loaded in memory (zero if timing constants aren't loaded) (out-Double)
        toTimeDs50UTC	The time, in days since 1950 UTC, of the latest timing constant record loaded in memory (zero if timing constants aren't loaded) (out-Double)
    """
    numOfRecs = CreateCArray(c_int, [1])
    frTimeDs50UTC = CreateCArray(c_double, [1])
    toTimeDs50UTC = CreateCArray(c_double, [1])

    TimeFunc.TConTimeSpan(numOfRecs, frTimeDs50UTC, toTimeDs50UTC)

    return (numOfRecs[0], frTimeDs50UTC[0], toTimeDs50UTC[0])


def utc2correction(ds50utc):
    """
    Retrieves the timing constants record, if exists, at the requested input time in ds50UTC. 
    If the requested record is not found, 0's will be returned for all of the constants. 
    You can use this fact to determine whether the record was found or not. 
    Simply check the taiMinusUTC value after calling this function. 
    Since that value can never be 0 for a valid record, if it is 0 the record was not found.
    """
    if not is_tcon_file_loaded():
        pass
    taiMinusUTC = CreateCArray(c_double, [1])
    ut1MinusUTC = CreateCArray(c_double, [1])
    ut1Rate = CreateCArray(c_double, [1])
    polarX = CreateCArray(c_double, [1])
    polarY = CreateCArray(c_double, [1])

    TimeFunc.UTCToTConRec(
        ds50utc,
        taiMinusUTC,
        ut1MinusUTC,
        ut1Rate,
        polarX,
        polarY
    )

    if taiMinusUTC[0] == 0:
        print(
            f"No timing constants record found for the given ds50UTC: {ds50utc}."
        )

    return (taiMinusUTC[0], ut1MinusUTC[0], ut1Rate[0], polarX[0], polarY[0])


#############################################################################
# Time conversion functions: to str
#############################################################################
def utc2dtg20(ds50utc: float) -> str:
    """
    Converts an internal time in ds50UTC to a string in DTG20 format. 
    The resulting string takes the form "YYYY/DDD HHMM SS.SSS".
      The input ds50UTC must be greater than 2192.0, 
      which corresponds to a time later than 1st Jan 1956. 
      Any input value less than or equal to 2192.0 will yield "1956/001 0000 00.000".

    Parameters
        ds50UTC	Days since 1950, UTC to be converted. (in-Double)
        dtg20	A string to hold the result of the conversion. (out-Character[20])
    """
    # assert ds50utc >= 2192.0, "Input ds50UTC must be greater than 2192.0 to convert to valid DTG20 format."
    dtg20_buffer = create_string_buffer(
        20)  # DTG20 format is 20 characters + null terminator
    TimeFunc.UTCToDTG20(ds50utc, dtg20_buffer)
    return dtg20_buffer.value.decode('utf-8')


def utc2dtg(ds50utc: float, fmtIdx: int) -> str:
    """
    Converts an internal time in ds50UTC to the specified DTG format 
    - dtgFmt The input ds50UTC must be greater than 2192.0, 
    which corresponds to a time later than 1st Jan 1956. 
    Any input value less than or equal to 2192.0 will yield "1956/001 0000 00.000".

    Note: This table may show index values that are not used. 
    Those are reserved for future use.

    Name	Index	Description
    DTGFMT_DTG15	1	YYDDDHHMMSS.SSS (DTG15)
    DTGFMT_DTG17	2	YYYY/DDD.DDDDDDDD (DTG17)
    DTGFMT_DTG19	3	YYYYMonDDHHMMSS.SSS (DTG19)
    DTGFMT_DTG20	4	YYYY/DDD HHMM SS.SSS (DTG20)
    DTGFMT_DTG21	5	YYYY ddd HH MM SS.SSS (DTG21)
    DTGFMT_DTG22	6	YYYY-DDDTHH:MM:SS.SSSZ (DTG22)
    DTGFMT_DTG24	7	DD Mon YYYY HH:MM:SS.SSS (DTG24)
    DTGFMT_DTG25A	8	YYYY/mm/DD HH:MM:SS.SSSSSS (DTG25A)
    DTGFMT_DTG25B	9	YYYY-mm-DD HH:MM:SS.SSSSSS (DTG25B)
    DTGFMT_DTG30	10	YYYY ddd (DD Mon) HH:MM:SS.SSS (DTG30)
    """
    # assert ds50utc >= 2192.0, "Input ds50UTC must be greater than 2192.0 to convert to valid DTG format."
    # max length of the supported DTG formats is less than 64 characters
    dtg_buffer = create_string_buffer(31)
    TimeFunc.UTCToDTG(ds50utc, fmtIdx, dtg_buffer)
    return dtg_buffer.value.decode('utf-8').strip()
