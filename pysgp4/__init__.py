from .AstroUtils import *
import platform
import os

# Constants defined in wrappers
from .DllMainWrapper import *
from .EnvConstWrapper import *
from .TimeFuncWrapper import *
from .AstroFuncWrapper import *
from .ExtEphemWrapper import *
from .TleWrapper import *
from .SpVecWrapper import *
from .VcmWrapper import *
from .SensorWrapper import *
from .Sgp4PropWrapper import *
from .ElOpsWrapper import *
from .SatStateWrapper import *
from .ObsWrapper import *

# Dealing with DLL files


def _add_dll_dir():
    """Adds the appropriate DLL directory to the system path based on the current platform."""
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

# Load DLLs and assign to module-level variables for easier access
DllMain = LoadDllMainDll()
EnvConst = LoadEnvConstDll()
TimeFunc = LoadTimeFuncDll()
AstroFunc = LoadAstroFuncDll()
ExtEphem = LoadExtEphemDll()
Tle = LoadTleDll()
SpVec = LoadSpVecDll()
Vcm = LoadVcmDll()
Sensor = LoadSensorDll()
Sgp4Prop = LoadSgp4PropDll()
ElOps = LoadElOpsDll()
SatState = LoadSatStateDll()
Obs = LoadObsDll()

# Define __getattr__ to allow direct access to functions in the DLLs without needing to specify the module


def __getattr__(name):
    """Allows direct access to functions in the DLLs without needing to specify the module."""
    if name in globals():
        return globals()[name]
    modules = [DllMain, EnvConst, TimeFunc, AstroFunc, ExtEphem,
               Tle, SpVec, Vcm, Sensor, Sgp4Prop, ElOps, SatState, Obs]
    for module in modules:
        if hasattr(module, name):
            return getattr(module, name)
    raise AttributeError(f"module 'pysgp4' has no attribute '{name}'")
