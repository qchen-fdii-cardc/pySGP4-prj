import ctypes as _ctypes

from ._wrapper.DllMainWrapper import LoadDllMainDll as _LoadDllMainDll
from ._wrapper.EnvConstWrapper import LoadEnvConstDll as _LoadEnvConstDll

# _DllMain = _LoadDllMainDll()
_EnvConst = _LoadEnvConstDll()


def init(apAddr: int) -> int:
    """
    Notes: This function has been deprecated since v9.0. Initializes the EnvInit DLL for use in the program. If this function returns an error, it is recommended that you stop the program immediately.

    An error will occur if you forget to load and initialize all the prerequisite DLLs, as listed in the DLL Prerequisites section of the accompanying documentation, before using this DLL.

    When the function is called, the GEO model is set to WGS-72 and the FK model is set to FK5. If the user plans to use the SGP4 propagator, do NOT change this default setting. Otherwise, SGP4 won't work

    Parameters
    apAddr	The handle that was returned from DllMainInit, see the documentation for DllMain.dll for details. (in-Long)
    Returns
    Returns zero indicating the EnvConst DLL has been initialized successfully. Other values indicate an error.
    """
    return int(_EnvConst.EnvInit(_ctypes.c_long(apAddr)))


def info() -> str:
    """
    Returns information about the EnvConst DLL. The returned string provides information about the version number, build date, and the platform of the EnvConst DLL.

    Parameters
        infoStr	A string to hold the information about EnvConst.dll. (out-Character[128])
    """
    info_buffer = _ctypes.create_string_buffer(128)
    _EnvConst.EnvGetInfo(info_buffer)
    return info_buffer.value.decode('utf-8')


def load_file(filename: str) -> int:
    """
    Loads the environment constants from a file. The file should be in the format of "name=value" pairs, one per line. The function returns zero if the file is loaded successfully, and a non-zero value if there is an error.

    Parameters
        filename	The name of the file to load the environment constants from. (in-Character[256])
    Returns
        Returns zero if the file is loaded successfully, and a non-zero value if there is an error.
    """
    return int(_EnvConst.EnvLoadFile(filename.encode('utf-8')))


def save_file(filename: str, mode: bool = False, format: int = 0) -> int:
    """
    Saves the current Earth constants (GEO) model and fundamental catalogue (FK) model settings to a file. Returns zero indicating the GEO and FK settings have been successfully saved to the file. Other values indicate an error.

    Parameters
        envConstFile	The name of the file in which to save the settings. (in-Character[512])
        saveMode	Specifies whether to create a new file or append to an existing one. (0 = create, 1= append) (in-Integer)
        saveForm	Specifies the mode in which to save the file. (0 = text format, 1 = xml (not yet implemented, reserved for future)) (in-Integer)
    Returns
        Returns zero indicating the GEO and FK settings have been successfully saved to the file. Other values indicate an error.   
    """
    saveMode = 1 if mode else 0
    return int(_EnvConst.EnvSaveFile(filename.encode('utf-8'), saveMode, format))


def fk_idx() -> int:
    """
    Returns the current fundamental catalogue (FK) setting. The FK model is shared among all the Standardized Astrodynamic Algorithms DLLs in the program.

    Returns
        Return the current FK setting as an integer. Valid values are: (4 = FK4, 5 = FK5)
    """
    return int(_EnvConst.EnvGetFkIdx())


def set_fk_idx(idx: int) -> None:
    """
    Changes the fundamental catalogue (FK) setting to the specified value. If the users enter an invalid value for the fkIdx, the program will continue to use the current setting.

    The FK model is globally shared among the Standardized Astrodynamic Algorithms DLLs. If its setting is changed, the new setting takes effect immediately. The FK model must be set to FK5 to use the SGP4 propagator.

    Parameters
        xf_FkMod	Specifies the FK model to use. The following values are accepted: xf_FkMod= 4: FK4, xf_FkMod= 5: FK5 (in-Integer)
    """
    if idx not in (4, 5):
        raise ValueError(
            f"Invalid FK index: {idx}. Valid values are 4 (FK4) and 5 (FK5). Keeping the current setting.")
    _EnvConst.EnvSetFkIdx(_ctypes.c_int(idx))


def geo_idx() -> int:
    """
    Returns the current Earth constants (GEO) model setting. The GEO model is shared among all the Standardized Astrodynamic Algorithms DLLs in the program.

    The following table lists possible values of the return value GEO setting:

        table
    Value	Value interpretation
    84	    WGS-84
    96	    EGM-96
    08	    EGM-08
    72	    WGS-72 (default)
    2	    JGM2
    68	    STEM68R, SEM68R
    5	    GEM5
    9	    GEM9   

    Returns
        Return the current GEO setting as an integer. Valid values are: (72 = WGS-72, 84 = WGS-84, 96 = EGM-96, 08 = EGM-08, 2 = JGM-2, 68 = SEM68R, 5 = GEM5, 9 = GEM9)
    """
    return int(_EnvConst.EnvGetGeoIdx())


def set_geo_idx(idx: int) -> None:
    """
    Changes the Earth constants (GEO) setting to the specified value.
    If you specify an invalid value for xf_GeoMod, the program will continue to use the current setting.
    The GEO model is globally shared among the Standardized Astrodynamic Algorithms DLLs. If its setting is changed, the new setting takes effect immediately
    The following table lists possible values of the parameter value GEO setting:

    table
    Value	Value interpretation
    84	    WGS-84
    96	    EGM-96
    08	    EGM-08
    72	    WGS-72 (default)
    2	    JGM2
    68	    STEM68R, SEM68R
    5	    GEM5
    9	    GEM9

    The GEO model must be set to WGS-72 to use the SGP4 propagator.

    Parameters
        xf_GeoMod	Specifies the GEO model to use. (in-Integer)
    """
    if idx not in (72, 84, 96, 8, 2, 68, 5, 9):
        raise ValueError(
            f"Invalid GEO index: {idx}. Valid values are 72 (WGS-72), 84 (WGS-84), 96 (EGM-96), 8 (EGM-08), 2 (JGM-2), 68 (SEM68R), 5 (GEM5), and 9 (GEM9). Keeping the current setting.")
    _EnvConst.EnvSetGeoIdx(_ctypes.c_int(idx))


def geo_str() -> str:
    """
    Returns the name of the current Earth constants (GEO) model.
    The geoStr parameter may contain one of the following values:

    table
    WGS-84
    EGM-96
    EGM-08
    WGS-72
    JGM2
    SEM68R
    GEM5
    GEM9
    Parameters
        geoStr	A string to store the name of the current GEO model. (out-Character[6])
    """
    str_buffer = _ctypes.create_string_buffer(6)
    _EnvConst.EnvGetGeoStr(str_buffer)
    return str_buffer.value.decode('utf-8')


def set_geo_str(geo_str: str) -> None:
    """
    Changes the Earth constants (GEO) setting to the model specified by a string literal.
    If you specify an invalid value for geoStr, the program will continue to use the current setting.
    The GEO model is globally shared among the Standardized Astrodynamic Algorithms DLLs. If its setting is changed, the new setting takes effect immediately.
    The following table lists possible values of the parameter value GEO setting:

    table
    geoStr (any string in the row)	Interpretation
    'WGS-84', 'WGS84', '84'	        WGS-84
    'EGM-96', 'EGM96', '96'	        EGM-96
    'EGM-08', 'EGM08', '8'	        EGM-08
    'WGS-72', 'WGS72', '72'	        WGS-72 (default)
    'JGM-2, 'JGM2', '2'	            JGM-2
    'SEM68R', '68'	                STEM68R, SEM68R
    'GEM5', '5'	                    GEM5
    'GEM9', '9'	                    GEM9


    The GEO model must be set to WGS-72 to use the SGP4 propagator.

    Parameters
        geoStr	The GEO model to use, expressed as a string. (in-Character[6])
    """
    geo_str = geo_str.strip().upper()
    valid_geo_strs = ['WGS-84', 'WGS84', '84', 'EGM-96', 'EGM96', '96', 'EGM-08',
                      'EGM08', '8', 'WGS-72', 'WGS72', '72', 'JGM-2', 'JGM2', '2',
                      'SEM68R', '68', 'GEM5', '5', 'GEM9', '9']
    if geo_str not in valid_geo_strs:
        raise ValueError(
            f"Invalid GEO string: '{geo_str}'. Valid values are: {', '.join(valid_geo_strs)}. Keeping the current setting.")
    _EnvConst.EnvSetGeoStr(geo_str.encode('utf-8'))


def geo_const(idx: int) -> float:
    """
    Retrieves the value of one of the constants from the current Earth constants (GEO) model.

    Note: This table may show index values that are not used. Those are reserved for future use.

    Named Constants
    Name	        Index	Description
    XF_GEOCON_FF	1	    Earth flattening (reciprocal, unitless)
    XF_GEOCON_J2	2	    J2 (unitless)
    XF_GEOCON_J3	3	    J3 (unitless)
    XF_GEOCON_J4	4	    J4 (unitless)
    XF_GEOCON_KE	5	    Ke (er**1.5/min)
    XF_GEOCON_KMPER	6	    Earth radius (km/er)
    XF_GEOCON_RPTIM	7	    Earth rotation rate w.r.t. fixed equinox (rad/min)
    XF_GEOCON_CK2	8	    J2/2 (unitless)
    XF_GEOCON_CK4	9	    -3/8 J4 (unitless)
    XF_GEOCON_KS2EK	10	    Converts km/sec to er/kem
    XF_GEOCON_THDOT	11	    Earth rotation rate w.r.t. fixed equinox (rad/kemin)
    XF_GEOCON_J5	12	    J5 (unitless)
    XF_GEOCON_MU	13	    Gravitational parameter km^3/(solar s)^2
    Parameters
        xf_GeoCon	An index specifying the constant you wish to retrieve (see XF_GEOCON_?) (in-Integer)
    Returns
        Value of the requested GEO constant   

    """
    if idx < 1 or idx > 13:
        raise ValueError(
            f"Invalid GEO constant index: {idx}. Valid values are integers from 1 to 13.")
    return float(_EnvConst.EnvGetGeoConst(_ctypes.c_int(idx)))


def fk_const(xf_fkcon: int) -> float:
    """
    Retrieves the value of one of the constants from the current fundamental catalogue (FK) model.

    Note: This table may show index values that are not used. Those are reserved for future use.

    Named Constants
    Name	        Index	Description
    XF_FKCON_C1	    1	    Earth rotation rate w.r.t. moving equinox (rad/day)
    XF_FKCON_C1DOT	2	    Earth rotation acceleration(rad/day**2)
    XF_FKCON_THGR70	3	    Greenwich angle (1970 rad)
    Parameters
        xf_FkCon	An index specifying the constant you wish to retrieve, (see XF_FKCON_?) (in-Integer)
    Returns
        Value of the requested FK constant
    """
    if xf_fkcon < 1 or xf_fkcon > 3:
        raise ValueError(
            f"Invalid FK constant index: {xf_fkcon}. Valid values are integers from 1 to 3.")
    return float(_EnvConst.EnvGetFkConst(_ctypes.c_int(xf_fkcon)))


def fk_ptr() -> int:
    """
    Returns a handle that can be used to access the fundamental catalogue (FK) data structure.
    This function is needed when calling the ThetaGrnwch function from TimeFunc.dll.
    The handle returned by this function is sometimes called a pointer for historical reasons. The name EnvGetFkPtr comes from the fact that the handle used to be called a pointer.

    Returns
        A handle which can be used to access the FK data structure.
    """
    return int(_EnvConst.EnvGetFkPtr())


def set_earth_shape(earth_shape: int) -> None:
    """
    Specifies the shape of the earth that will be used by the Astro Standards software, either spherical earth or oblate earth

    Parameters
        earthShape	The value indicates the shape of the earth: 0=spherical earth, 1= oblate earth (default) (in-Integer)
    """
    if earth_shape not in (0, 1):
        raise ValueError(
            f"Invalid Earth shape index: {earth_shape}. Valid values are 0 (spherical Earth) and 1 (oblate spheroid Earth). Keeping the current setting.")
    _EnvConst.EnvSetEarthShape(_ctypes.c_int(earth_shape))


def earth_shape() -> int:
    """
    Returns the value representing the shape of the earth being used by the Astro Standards software, either spherical earth or oblate earth

    Returns
        The value indicates the shape of the earth that is being used in the Astro Standards software: 0=spherical earth, 1= oblate earth
    """
    return int(_EnvConst.EnvGetEarthShape())
