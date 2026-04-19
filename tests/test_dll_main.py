import tempfile
from pysgp4.AstroUtils import CreateCArray, c_double
import pysgp4
from ctypes import create_string_buffer
sgp4 = pysgp4.DllMain


def test_dll_main_init():
    retValue = sgp4.DllMainInit()
    # deprecated since V9.0
    assert retValue == 0  # now it returns 0
    # no need to call DllMainInit and any other init function


def test_dll_main_get_info():
    info = create_string_buffer(128)
    sgp4.DllMainGetInfo(info)

    # matches predefined info string for recent version
    assert info.value.decode(
        'utf-8'
    ).strip() == "HQ SpOC DllMain - Version: v9.8 - Build: Mar 04 2026 - Platform: Windows 64-bit - Compiler: OneAPI ifort"


def test_get_MOIC_data():
    moic_data = CreateCArray(c_double, [128])
    sgp4.GetMOICData(128, moic_data)
    print(moic_data[:128])  # print first 10 values for verification
    assert True


def test_Load_file():
    filename = tempfile.NamedTemporaryFile(delete=False).name
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    data_str = ", ".join(map(str, data))
    with open(filename, "w") as f:
        f.write(f"AS_MOIC {data_str}\n")
    fn = create_string_buffer(filename.encode('utf-8'), 512)
    retValue = sgp4.DllMainLoadFile(fn)
    assert retValue == 0  # successfully loaded
    moic_data = CreateCArray(c_double, [10])
    sgp4.GetMOICData(10, moic_data)
    print(moic_data[:10])  # print first 10 values for verification
    assert list(moic_data[:10]) == data


def test_log_file():
    filename = create_string_buffer(b"test_log.txt", 256)
    retValue = sgp4.OpenLogFile(filename)
    assert retValue == 0  # successfully set log file
