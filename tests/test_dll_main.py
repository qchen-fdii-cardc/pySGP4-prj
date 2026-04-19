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


