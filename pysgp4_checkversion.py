from ctypes import *
import pysgp4


if __name__ == "__main__":

    verionInfo = create_string_buffer(128)

    # for each available module
    pysgp4.AstroFunc.AstroFuncGetInfo(verionInfo)
    print("AstroFunc DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.DllMain.DllMainGetInfo(verionInfo)
    print("DllMain DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.ElOps.ElOpsGetInfo(verionInfo)
    print("ElOps DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.EnvConst.EnvGetInfo(verionInfo)
    print("EnvConst DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.ExtEphem.ExtEphGetInfo(verionInfo)
    print("ExtEphem DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.Obs.ObsGetInfo(verionInfo)
    print("Obs DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.SatState.SatStateGetInfo(verionInfo)
    print("SatState DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.Sensor.SensorGetInfo(verionInfo)
    print("Sensor DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.Sgp4Prop.Sgp4GetInfo(verionInfo)
    print("Sgp4Prop DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.SpVec.SpVecGetInfo(verionInfo)
    print("SpVec DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.TimeFunc.TimeFuncGetInfo(verionInfo)
    print("TimeFunc DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.Tle.TleGetInfo(verionInfo)
    print("Tle DLL version: " + verionInfo.value.decode("UTF-8"))

    pysgp4.Vcm.VcmGetInfo(verionInfo)
    print("Vcm DLL version: " + verionInfo.value.decode("UTF-8"))

    assert (pysgp4.XA_KEP_A == 0)
