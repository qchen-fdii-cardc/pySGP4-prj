from ctypes import create_string_buffer
from typing import List, Tuple

from numpy.typing import ArrayLike

from ._wrapper.DllMainWrapper import LoadDllMainDll
from ._wrapper.EnvConstWrapper import LoadEnvConstDll
from ._wrapper.TimeFuncWrapper import LoadTimeFuncDll
from ._wrapper.AstroFuncWrapper import LoadAstroFuncDll, XA_KEP_SIZE, XA_CLS_SIZE, XA_EQNX_SIZE
from ._wrapper.AstroUtils import CreateCArray, c_double, c_int

DllMain = LoadDllMainDll()
EnvConst = LoadEnvConstDll()
TimeFunc = LoadTimeFuncDll()
AstroFunc = LoadAstroFuncDll()

# int 	AstroFuncInit(long apAddr)
# void 	AstroFuncGetInfo(byte[] infoStr)


def kep2eqnx(xa_kep: ArrayLike) -> List[float]:
    # void 	KepToEqnx(double[] xa_kep, double[] xa_eqnx)
    xa_eqnx = CreateCArray(c_double, [XA_EQNX_SIZE])
    AstroFunc.KepToEqnx((c_double * XA_KEP_SIZE)(*xa_kep), xa_eqnx)
    return xa_eqnx[:]


def kep2posvel(xa_kep: ArrayLike) -> Tuple[List[float], List[float]]:
    # void 	KepToPosVel(double[] xa_kep, double[] pos, double[] vel)
    pos = CreateCArray(c_double, [3])
    vel = CreateCArray(c_double, [3])
    AstroFunc.KepToPosVel((c_double * XA_KEP_SIZE)(*xa_kep), pos, vel)
    return pos[:], vel[:]


def kep2uvw(xa_kep: ArrayLike) -> Tuple[List[float], List[float], List[float]]:
    # void 	KepToUVW(double[] xa_kep, double[] uBar, double[] vBar, double[] wBar)
    uBar = CreateCArray(c_double, [3])
    vBar = CreateCArray(c_double, [3])
    wBar = CreateCArray(c_double, [3])
    AstroFunc.KepToUVW((c_double * XA_KEP_SIZE)(*xa_kep), uBar, vBar, wBar)
    return uBar[:], vBar[:], wBar[:]


def class2eqnx(xa_cls: ArrayLike) -> List[float]:
    # void 	ClassToEqnx(double[] xa_cls, double[] xa_eqnx)
    xa_eqnx = CreateCArray(c_double, [XA_EQNX_SIZE])
    AstroFunc.ClassToEqnx((c_double * XA_CLS_SIZE)(*xa_cls), xa_eqnx)
    return xa_eqnx[:]


def eqnx2class(xa_eqnx: ArrayLike) -> List[float]:
    # void 	EqnxToClass(double[] xa_eqnx, double[] xa_cls)
    xa_cls = CreateCArray(c_double, [XA_CLS_SIZE])
    AstroFunc.EqnxToClass((c_double * XA_EQNX_SIZE)(*xa_eqnx), xa_cls)
    return xa_cls[:]


def posvel2eqnx(pos: ArrayLike, vel: ArrayLike) -> List[float]:
    # void 	EqnxToKep(double[] xa_eqnx, double[] xa_kep)
    xa_eqnx = CreateCArray(c_double, [XA_EQNX_SIZE])
    AstroFunc.PosVelToEqnx((c_double * 3)(*pos), (c_double * 3)(*vel), xa_eqnx)
    return xa_eqnx[:]


def posvelmu2eqnx(pos: ArrayLike, vel: ArrayLike, mu: float) -> List[float]:
    # void 	EqnxToPosVel(double[] xa_eqnx, double[] pos, double[] vel)
    xa_eqnx = CreateCArray(c_double, [XA_EQNX_SIZE])
    AstroFunc.PosVelMuToEqnx((c_double * 3)(*pos),
                             (c_double * 3)(*vel), mu, xa_eqnx)
    return xa_eqnx[:]


def posvel2kep(pos: ArrayLike, vel: ArrayLike) -> List[float]:
    # void 	PosVelToKep(double[] pos, double[] vel, double[] xa_kep)
    xa_kep = CreateCArray(c_double, [XA_KEP_SIZE])
    AstroFunc.PosVelToKep((c_double * 3)(*pos), (c_double * 3)(*vel), xa_kep)
    return xa_kep[:]

    # void 	PosVelToEqnx(double[] pos, double[] vel, double[] xa_eqnx)

def posvelmu2eqnx(pos: ArrayLike, vel: ArrayLike, mu: float) -> List[float]:
    # void 	PosVelMuToEqnx(double[] pos, double[] vel, double mu, double[] xa_eqnx)
    xa_eqnx = CreateCArray(c_double, [XA_EQNX_SIZE])
    AstroFunc.PosVelMuToEqnx((c_double * 3)(*pos),
                             (c_double * 3)(*vel), mu, xa_eqnx)
    return xa_eqnx[:]


def posvelmu2kep(pos: ArrayLike, vel: ArrayLike, mu: float) -> List[float]:
    # void 	PosVelMuToKep(double[] pos, double[] vel, double mu, double[] xa_kep)
    xa_kep = CreateCArray(c_double, [XA_KEP_SIZE])
    AstroFunc.PosVelMuToKep((c_double * 3)(*pos),
                            (c_double * 3)(*vel), mu, xa_kep)
    return xa_kep[:]


def posvel2uuvw(pos: ArrayLike, vel: ArrayLike) -> Tuple[List[float], List[float], List[float]]:
    # void 	PosVelToUUVW(double[] pos, double[] vel, double[] uvec, double[] vVec, double[] wVec)
    uBar = CreateCArray(c_double, [3])
    vBar = CreateCArray(c_double, [3])
    wBar = CreateCArray(c_double, [3])
    AstroFunc.PosVelToUUVW((c_double * 3)(*pos),
                           (c_double * 3)(*vel), uBar, vBar, wBar)
    return uBar[:], vBar[:], wBar[:]

    # void 	PosVelToPTW(double[] pos, double[] vel, double[] uvec, double[] vVec, double[] wVec)
    # double 	SolveKepEqtn(double[] xa_kep)
    # double 	CompTrueAnomaly(double[] xa_kep)
    # double 	NToA(double n)
    # double 	AToN(double a)
    # double 	KozaiToBrouwer(double eccen, double incli, double nKozai)
    # double 	BrouwerToKozai(double eccen, double incli, double nBrouwer)
    # void 	KepOscToMean(double[] xa_OscKep, double[] xa_MeanKep)
    # void 	XYZToLLH(double thetaG, double[] metricPos, double[] metricLLH)
    # void 	XYZToLLHTime(double ds50UTC, double[] metricPos, double[] metricLLH)
    # void 	LLHToXYZ(double thetaG, double[] metricLLH, double[] metricXYZ)
    # void 	LLHToXYZTime(double ds50UTC, double[] metricLLH, double[] metricXYZ)
    # void 	EFGToECI(double thetaG, double[] posEFG, double[] velEFG, double[] posECI, double[] velECI)
    # void 	EFGToECITime(double ds50UTC, double[] posEFG, double[] velEFG, double[] posECI, double[] velECI)
    # void 	ECIToEFG(double thetaG, double[] posECI, double[] velECI, double[] posEFG, double[] velEFG)
    # void 	ECIToEFGTime(double ds50UTC, double[] posECI, double[] velECI, double[] posEFG, double[] velEFG)
    # void 	ECRToEFG(double polarX, double polarY, double[] posECR, double[] velECR, double[] posEFG, double[] velEFG)
    # void 	ECRToEFGTime(double ds50UTC, double[] posECR, double[] velECR, double[] posEFG, double[] velEFG)
    # void 	EFGToECR(double polarX, double polarY, double[] posEFG, double[] velEFG, double[] posECR, double[] velECR)
    # void 	EFGToECRTime(double ds50UTC, double[] posEFG, double[] velEFG, double[] posECR, double[] velECR)
    # void 	EFGPosToLLH(double[] posEFG, double[] metricLLH)
    # void 	LLHToEFGPos(double[] metricLLH, double[] posEFG)
    # void 	RotJ2KToDate(int spectr, int nutationTerms, double ds50TAI, double[] posJ2K, double[] velJ2K, double[] posDate, double[] velDate)
    # void 	RotDateToJ2K(int spectr, int nutationTerms, double ds50TAI, double[] posDate, double[] velDate, double[] posJ2K, double[] velJ2K)
    # void 	CompSunMoonPos(double ds50ET, double[] uvecSun, double[] sunVecMag, double[] uvecMoon, double[] moonVecMag)
    # void 	CompSunPos(double ds50ET, double[] uvecSun, double[] sunVecMag)
    # void 	CompMoonPos(double ds50ET, double[] uvecMoon, double[] moonVecMag)
    # void 	AstroConvFrTo(int xf_Conv, double[] frArr, double[] toArr)
    # void 	RADecToLAD(double ra, double dec, double[] l, double[] a_tilde, double[] d_tilde)
    # void 	AzElToLAD(double az, double el, double[] lh, double[] ah, double[] dh)
    # void 	ECIToTopoComps(double theta, double lat, double[] senPos, double[] satPos, double[] satVel, double[] xa_topo)
    # void 	RaDecToAzEl(double thetaG, double lat, double lon, double ra, double dec, double[] az, double[] el)
    # void 	RaDecToAzElTime(double ds50UTC, double lat, double lon, double ra, double dec, double[] az, double[] el)
    # void 	AzElToRaDec(double thetaG, double lat, double lon, double az, double el, double[] ra, double[] dec)
    # void 	AzElToRaDecTime(double ds50UTC, double lat, double lon, double az, double el, double[] ra, double[] dec)
    # void 	RAEToECI(double theta, double astroLat, double[] xa_rae, double[] senPos, double[] satPos, double[] satVel)
    # void 	GetInitialDrag(double semiMajorAxis, double eccen, double[] nDot, double[] bstar)
    # void 	CovMtxPTWToUVW(double[] pos, double[] vel, double[][] ptwCovMtx, double[][] uvwCovMtx)
    # void 	CovMtxUVWToPTW(double[] pos, double[] vel, double[][] uvwCovMtx, double[][] ptwCovMtx)
    # void 	EarthObstructionAngles(double earthLimb, double[] satECI, double[] senECI, double[] earthSenLimb, double[] earthSenSat, double[] satEarthSen)
    # int 	IsPointSunlit(double ds50ET, double[] ptEci)
    # void 	RotRADecl(int nutationTerms, int dir, double ds50UTCIn, double raIn, double declIn, double ds50UTCOut, double[] raOut, double[] declOut)
    # int 	RotRADec_DateToEqnx(int nutationTerms, int yrOfEqnx, double ds50UTCIn, double raIn, double declIn, double[] raOut, double[] declOut)
    # int 	RotRADec_EqnxToDate(int nutationTerms, int yrOfEqnx, double ds50UTCIn, double raIn, double declIn, double[] raOut, double[] declOut)
    # void 	CovMtxEqnxToUVW(double[] pos, double[] vel, double[][] covMtxEqnx, double[][] covMtxUVW)
    # void 	CovMtxUVWToEqnx(double[] pos, double[] vel, double[][] covMtxUVW, double[][] covMtxEqnx)
    # void 	CovMtxECIToUVW(double[] pos, double[] vel, double[][] covMtxECI, double[][] covMtxUVW)
    # void 	CovMtxUVWToECI(double[] pos, double[] vel, double[][] covMtxUVW, double[][] covMtxECI)
    # void 	CovMtxECIToEFG(double thetaG, double[][] covECI, double[][] covEFG)
    # void 	CovMtxEFGToECI(double thetaG, double[][] covEFG, double[][] covECI)
    # void 	Mtx6x6ToLTA21(double[][] symMtx6x6, double[] lta21)
    # void 	LTA21ToMtx6x6(double[] lta21, double[][] symMtx6x6)
    # void 	Mtx9x9ToLTA45(double[][] symMtx9x9, double[] lta45)
    # void 	LTA45ToMtx9x9(double[] lta45, double[][] symMtx9x9)
    # void 	PropCovFrState(double rms, double consider, double[] stateArray, double[][] cov, double[][] propCov)
    # void 	CovMtxECIToEqnx(double[] pos, double[] vel, double[][] covMtxECI, double[][] covMtxEqnx)
    # void 	CovMtxEqnxToECI9x9(double[] pos, double[] vel, double[][] covEqnx, double[][] covMtxECI)
    # void 	CovMtxEqnxToUVW9x9(double[] pos, double[] vel, double[][] covEqnx, double[][] covMtxUVW)
    # void 	CovMtxUpdate(double rmsIn, double consider, double[][] cov, double[] stateArray, double[][] propCov)
    # void 	AberrationAnnual(double ra, double decl, double dS50UTC, double[] raDelta, double[] decDelta)
    # void 	AberrationDiurnal(double ra, double decl, double dS50UTC, double[] senPos, double[] raDelta, double[] decDelta)
    # void 	JplSetParameters(byte[] jplFile, double ds50Start, double ds50Stop)
    # void 	JplGetParameters(byte[] jplFile, double[] ds50Start, double[] ds50Stop)
    # void 	JplReset()
    # void 	JplCompSunMoonVec(double ds50UTC, double[] uvecSun, double[] sunVecMag, double[] uvecMoon, double[] moonVecMag)
    # void 	JplCompSunMoonPos(double ds50UTC, double[] sunVec, double[] moonVec)
    # void 	RemoveJpl()
    # void 	TemeEpochToDate(int nutationTerms, double epochDs50TAI, double dateDs50TAI, double[] posEpoch, double[] velEpoch, double[] posDate, double[] velDate)
    # void 	ECRToECITime(double ds50UTC, double[] posECR, double[] velECR, double[] posECI, double[] velECI)
    # void 	ECIToECRTime(double ds50UTC, double[] posECI, double[] velECI, double[] posECR, double[] velECR)
    # void 	ECRToJ2KTime(int spectr, int nutationTerms, double ds50UTC, double[] posECR, double[] velECR, double[] posJ2K, double[] velJ2K)
    # void 	J2KToECRTime(int spectr, int nutationTerms, double ds50UTC, double[] posJ2K, double[] velJ2K, double[] posECR, double[] velECR)
