import pysgp4
from ctypes import create_string_buffer


def test_env_save_file():
    # filename = create_string_buffer(b"test_env_const.txt", 256)
    retValue = pysgp4.EnvConst.EnvSaveFile(b"test_env_const.txt", 0, 0)
    assert retValue == 0  # successfully saved


def test_env_earth_shape():
    shape = pysgp4.EnvConst.EnvGetEarthShape()
    assert shape == 1   # default oblate earth
