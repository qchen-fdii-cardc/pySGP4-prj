import pysgp4 as sgp4
from ctypes import create_string_buffer
import pandas as pd
from pysgp4 import envconst


def test_coverage():
    funcs = [func for func in dir(sgp4.EnvConst) if not func.startswith("_")]
    for func in funcs:
        assert hasattr(
            sgp4, func), f"Function {func} is not accessible in pysgp4 module"

    py_funcs = [func for func in dir(
        sgp4.envconst) if not func.startswith("_")]
    for func in py_funcs:
        assert hasattr(
            envconst, func), f"Function {func} in envconst.py is not accessible in pysgp4 module"

    # nothing more, nothing less
    assert len(funcs) == len(
        py_funcs), f"Number of functions in EnvConst ({len(funcs)}) does not match number of functions in envconst.py ({len(py_funcs)})"

    # py funcs cover all funcs in EnvConst
    pyfuncnames = [func.lower().replace("_", "") for func in py_funcs]
    funcnames = [func.lower().removeprefix("env").removeprefix("get")
                 for func in funcs]
    for pyf in pyfuncnames:
        assert pyf in funcnames, f"Function {pyf} in envconst.py does not have a corresponding function in EnvConst"


def test_env_save_file():
    # filename = create_string_buffer(b"test_env_const.txt", 256)
    # retValue = sgp4.EnvSaveFile(b"test_env_const.txt", 0, 0)
    retValue = envconst.save_file("test_env_const.txt", 0, 0)
    assert retValue == 0  # successfully saved


def test_env_earth_shape():
    shape = sgp4.EnvGetEarthShape()
    assert shape == 1   # default oblate earth
    sgp4.EnvSetEarthShape(0)  # set to spherical earth
    shape = sgp4.EnvGetEarthShape()
    assert shape == 0  # now it should be spherical earth
    sgp4.EnvSetEarthShape(1)


"""For GEO model, the valid names are 
    GEOCONST, BCONST and 
    the valid values are 
    WGS-72, WGS72, 72, [default],
    WGS-84, WGS84, 84, 
    EGM-96, EGM96, 96, 
    EGM-08, EGM08, 08, 
    JGM-2, JGM2, 2, 
    SEM68R, 68, 
    GEM5, 5, 
    GEM9, and 9.
"""

"""For FK model, the valid name is FKCONST 
    and the valid values are: FK4, 4, FK5, 5.
"""


def test_env_get_fk_const():
    """
    XF_FKCON_C1	1	Earth rotation rate w.r.t. moving equinox (rad/day)
    XF_FKCON_C1DOT	2	Earth rotation acceleration(rad/day**2)
    XF_FKCON_THGR70	3	Greenwich angle (1970 rad)
    """
    c1 = sgp4.EnvGetFkConst(sgp4.XF_FKCON_C1)
    C1Dot = sgp4.EnvGetFkConst(sgp4.XF_FKCON_C1DOT)
    Thgr70 = sgp4.EnvGetFkConst(sgp4.XF_FKCON_THGR70)
    assert c1 == 0.017202791694070362
    assert C1Dot == 5.075514194322695e-15
    assert Thgr70 == 1.7321343856509375

    const_names = ["C1", "C1DOT", "THGR70"]
    consts = [
        sgp4.__getattr__(f"XF_FKCON_{const}") for const in const_names
    ]
    table = pd.DataFrame(columns=["FKModel"] + const_names)
    for fk_model in [4, 5]:
        sgp4.EnvSetFkIdx(fk_model)
        model_name = f"FK{fk_model}"
        values = [sgp4.EnvGetFkConst(const) for const in consts]

        table = pd.concat([table, pd.DataFrame(
            [[model_name] + values], columns=["FKModel"] + const_names)], ignore_index=True)

    print()
    print(table)
    table.to_csv("fk_const_table.csv", index=False)


def test_env_get_geo_const():
    """
    XF_GEOCON_FF	1	Earth flattening (reciprocal, unitless)
    XF_GEOCON_J2	2	J2 (unitless)
    XF_GEOCON_J3	3	J3 (unitless)
    XF_GEOCON_J4	4	J4 (unitless)
    XF_GEOCON_KE	5	Ke (er**1.5/min)
    XF_GEOCON_KMPER	6	Earth radius (km/er)
    XF_GEOCON_RPTIM	7	Earth rotation rate w.r.t. fixed equinox (rad/min)
    XF_GEOCON_CK2	8	J2/2 (unitless)
    XF_GEOCON_CK4	9	-3/8 J4 (unitless)
    XF_GEOCON_KS2EK	10	Converts km/sec to er/kem
    XF_GEOCON_THDOT	11	Earth rotation rate w.r.t. fixed equinox (rad/kemin)
    XF_GEOCON_J5	12	J5 (unitless)
    XF_GEOCON_MU	13	Gravitational parameter km^3/(solar s)^2
    """
    ff = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_FF)
    J2 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J2)
    J3 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J3)
    J4 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J4)
    Ke = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KE)
    Kmp = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KMPER)
    Rptim = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_RPTIM)
    Ck2 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_CK2)
    Ck4 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_CK4)
    Ks2ek = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KS2EK)
    Thdot = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_THDOT)
    J5 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J5)
    Mu = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_MU)

    assert ff == 0.003352779454167505
    assert J2 == 0.001082616
    assert J3 == -2.53881e-06
    assert J4 == -1.65597e-06
    assert Ke == 0.07436691613317341
    assert Kmp == 6378.135
    assert Rptim == 0.0043752690880113
    assert Ck2 == 0.000541308
    assert Ck4 == 6.209887499999999e-07
    assert Ks2ek == 0.1264962848571814
    assert Thdot == 0.05883354205754931
    assert J5 == -2.184827e-07
    assert Mu == 398600.8

    sgp4.EnvSetGeoStr(b"WGS-84")
    ff = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_FF)
    J2 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J2)
    J3 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J3)
    J4 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J4)
    Ke = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KE)
    Kmp = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KMPER)
    Rptim = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_RPTIM)
    Ck2 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_CK2)
    Ck4 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_CK4)
    Ks2ek = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_KS2EK)
    Thdot = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_THDOT)
    J5 = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_J5)
    Mu = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_MU)

    assert ff == 0.0033528106647474805
    assert J2 == 0.00108263
    assert J3 == -2.5321531e-06
    assert J4 == -1.6109876e-06
    assert Ke == 0.07436685316871385
    assert Kmp == 6378.137
    assert Rptim == 0.0043752690880113
    assert Ck2 == 0.000541315
    assert Ck4 == 6.0412035e-07
    assert Ks2ek == 0.12649635229263637
    assert Thdot == 0.0588335918703627
    assert J5 == -2.3578565e-07
    assert Mu == 398600.5

    geo_models = [72, 84, 96, 8, 2, 68, 5, 9]

    const_names = ["FF", "J2", "J3", "J4", "KE", "KMPER",
                   "RPTIM", "CK2", "CK4", "KS2EK", "THDOT", "J5", "MU"]
    consts = [
        sgp4.__getattr__(f"XF_GEOCON_{const}") for const in const_names
    ]
    table = pd.DataFrame(columns=["GeoModel"] + const_names)
    for geo_model in geo_models:
        sgp4.EnvSetGeoIdx(geo_model)
        model_name = create_string_buffer(6)
        sgp4.EnvGetGeoStr(model_name)
        name = model_name.value.decode('utf-8')
        values = [sgp4.EnvGetGeoConst(const) for const in consts]

        table = pd.concat([table, pd.DataFrame(
            [[name] + values], columns=["GeoModel"] + const_names)], ignore_index=True)

    print()
    print(table)
    table.to_csv("geo_const_table.csv", index=False)

    # format a markdown table of the table
    md = '| ' + ' | '.join(table.columns) + ' |\n'
    md += '| ' + ' | '.join(['---'] * len(table.columns)) + ' |\n'
    for _, row in table.iterrows():
        md += '| ' + ' | '.join(str(x) for x in row.values) + ' |\n'
    print("\nMarkdown Table:\n")
    print(md)


def test_set_get_geo():
    geo_strs = [b"WGS-72", b"WGS72", b"72", b"WGS-84", b"WGS84", b"84", b"EGM-96", b"EGM96", b"96",
                b"EGM-08", b"EGM08", b"JGM-2", b"JGM2", b"2", b"SEM68R", b"68", b"GEM5", b"5", b"GEM9", b"9"
                ]
    print(f"\n{'Input Geostr':14}{'GeoStr':14}{'GeoIdx':3}")
    geoStrs = dict()
    for geo_str in geo_strs:
        sgp4.EnvSetGeoStr(geo_str)
        current_geo = create_string_buffer(6)
        sgp4.EnvGetGeoStr(current_geo)
        retIdx = sgp4.EnvGetGeoIdx()
        print(
            f"{geo_str.decode('utf-8'):14}{current_geo.value.decode('utf-8'):14}{retIdx:3}")
        geoStrs[geo_str] = (current_geo.value, retIdx)

    for geo_str, (current_geo, retIdx) in geoStrs.items():
        sgp4.EnvSetGeoIdx(retIdx)
        _current_geo = create_string_buffer(6)
        sgp4.EnvGetGeoStr(_current_geo)
        assert current_geo == _current_geo.value

        sgp4.EnvSetGeoStr(geo_str)
        sgp4.EnvGetGeoStr(_current_geo)
        assert current_geo == _current_geo.value
        assert retIdx == sgp4.EnvGetGeoIdx()
