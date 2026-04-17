import pysgp4


def test_import_wrappers():
    # 测试 DLL 是否能被正常加载，只有如下的dll可用
    pysgp4.AstroFunc
    pysgp4.DllMain
    pysgp4.ElOps
    pysgp4.EnvConst
    pysgp4.ExtEphem
    pysgp4.Obs
    pysgp4.SatState
    pysgp4.Sensor
    pysgp4.Sgp4Prop
    pysgp4.SpVec
    pysgp4.TimeFunc
    pysgp4.Tle
    pysgp4.Vcm
    assert True  # 如果没有异常，说明 DLL 加载正常
