import ctypes as _ctypes

from ._wrapper.DllMainWrapper import LoadDllMainDll as _LoadDllMainDll

_DllMain = _LoadDllMainDll()

# static native long 	DllMainInit ()

# static native void 	DllMainGetInfo(byte[] infoStr)

# static native int 	DllMainLoadFile(byte[] dllMainFile)

# static native int 	OpenLogFile(byte[] fileName)

# static native void 	CloseLogFile()

# static native void 	LogMessage(byte[] msgStr)

# static native void 	GetLastErrMsg(byte[] lastErrMsg)

# static native void 	GetLastInfoMsg(byte[] lastInfoMsg)

# static native void 	GetInitDllNames(byte[] initDllNames)

# static native void 	TestInterface(char cIn, byte[] cOut, int intIn, int[] intOut, long longIn, long[] longOut, double realIn, double[] realOut, byte[] strIn, byte[] strOut, int[] int1DIn, int[] int1DOut, long[] long1DIn, long[] long1DOut, double[] real1DIn, double[] real1DOut, int[][] int2DIn, int[][] int2DOut, long[][] long2DIn, long[][] long2DOut, double[][] real2DIn, double[][] real2DOut)

# static native void 	TestInterface2(byte[] cInOut, int[] intInOut, long[] longInOut, double[] realInOut, byte[] strInOut, int[] int1DInOut, long[] long1DInOut, double[] real1DInOut, int[][] int2DInOut, long[][] long2DInOut, double[][] real2DInOut)

# static native void 	TestInterface3(int[] unk1DIn, int[] unk1DOut, int[][] unk2DIn, int[][] unk2DOut)

# static native void 	GetMOICData(int arrSize, double[] xa_moic)

# static native int 	SetElsetKeyMode(int elset_keyMode)

# static native int 	GetElsetKeyMode()

# static native int 	SetAllKeyMode(int all_keyMode)

# static native int 	GetAllKeyMode()

# static native void 	ResetAllKeyMode()

# static native int 	SetDupKeyMode(int dupKeyMode)

# static native int 	GetDupKeyMode()

# static native void 	GetErrMsg(int errCode, byte[] errMsg)

# static native int 	SetErrMsgMode(int mode)

# static native int 	GetErrMsgMode()
