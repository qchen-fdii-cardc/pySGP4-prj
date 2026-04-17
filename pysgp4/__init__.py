from . import AstroUtils
import platform
import sys
import os


# from .AofWrapper import *
from .AstroFuncWrapper import *
# from .BamWrapper import *
# from .BatchDCWrapper import *
# from .ComboWrapper import *
from .DllMainWrapper import *
# from .ElCompWrapper import *
from .ElOpsWrapper import *
from .EnvConstWrapper import *
from .ExtEphemWrapper import *
# from .FovWrapper import *
# from .LamodWrapper import *
# from .ObsOpsWrapper import *
from .ObsWrapper import *
# from .RotasWrapper import *
# from .SaasWrapper import *
from .SatStateWrapper import *
from .SensorWrapper import *
from .Sgp4PropWrapper import *
# from .SpPropWrapper import *
from .SpVecWrapper import *
from .TimeFuncWrapper import *
from .TleWrapper import *
from .VcmWrapper import *


# pysgp4: Expose wrappers as submodules/aliases for lazy DLL loading and clean usage
def _add_dll_dir():
    if platform.system() == "Windows":
        dll_dir = os.path.join(os.path.dirname(__file__), "Lib", "Windows")
        os.add_dll_directory(dll_dir)
    if platform.system() == "Linux":
        dll_dir = os.path.join(os.path.dirname(
            __file__), "Lib", "Linux", "x86", "IFORT")
        os.environ["LD_LIBRARY_PATH"] = dll_dir + \
            os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")
    if platform.system() == "Darwin":
        dll_dir = os.path.join(os.path.dirname(
            __file__), "Lib", "MacOS", "x86", "IFORT")
        os.environ["DYLD_LIBRARY_PATH"] = dll_dir + \
            os.pathsep + os.environ.get("DYLD_LIBRARY_PATH", "")


_add_dll_dir()

# Aliases for user-friendly access (e.g., pysgp4.Aof, pysgp4.AstroUtils, ...)


# change the behavior of pysgp4.aof to return AofWrapper.LoadAofDll() instead of the module itself, so that the DLL will be loaded when the user accesses pysgp4.aof for the first time

# Python 3.7+ module-level __getattr__ for lazy DLL loading
def __getattr__(name):
    if name in globals():
        return globals()[name]
    if name == "AstroFunc":
        sys.modules[__name__].AstroFunc = LoadAstroFuncDll()
        return sys.modules[__name__].AstroFunc
    if name == "DllMain":
        sys.modules[__name__].DllMain = LoadDllMainDll()
        return sys.modules[__name__].DllMain
    if name == "ElOps":
        sys.modules[__name__].ElOps = LoadElOpsDll()
        return sys.modules[__name__].ElOps
    if name == "EnvConst":
        sys.modules[__name__].EnvConst = LoadEnvConstDll()
        return sys.modules[__name__].EnvConst
    if name == "ExtEphem":
        sys.modules[__name__].ExtEphem = LoadExtEphemDll()
        return sys.modules[__name__].ExtEphem
    if name == "Obs":
        sys.modules[__name__].Obs = LoadObsDll()
        return sys.modules[__name__].Obs
    if name == "SatState":
        sys.modules[__name__].SatState = LoadSatStateDll()
        return sys.modules[__name__].SatState
    if name == "Sensor":
        sys.modules[__name__].Sensor = LoadSensorDll()
        return sys.modules[__name__].Sensor
    if name == "Sgp4Prop":
        sys.modules[__name__].Sgp4Prop = LoadSgp4PropDll()
        return sys.modules[__name__].Sgp4Prop
    if name == "SpVec":
        sys.modules[__name__].SpVec = LoadSpVecDll()
        return sys.modules[__name__].SpVec
    if name == "TimeFunc":
        sys.modules[__name__].TimeFunc = LoadTimeFuncDll()
        return sys.modules[__name__].TimeFunc
    if name == "Tle":
        sys.modules[__name__].Tle = LoadTleDll()
        return sys.modules[__name__].Tle
    if name == "Vcm":
        sys.modules[__name__].Vcm = LoadVcmDll()
        return sys.modules[__name__].Vcm
    raise AttributeError(f"module 'pysgp4' has no attribute '{name}'")
