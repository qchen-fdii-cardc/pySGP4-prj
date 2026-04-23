from numpy import cos, pi, radians, sin, tan, sqrt

import pysgp4
from ctypes import *
from pysgp4 import *
from pysgp4._wrapper.AstroUtils import *

from typing import *

# static native int 	AstroFuncInit(long apAddr)


def test_astrofunc_init():
    # depricated in current version
    assert True
    pass

# static native void 	AstroFuncGetInfo(byte[] infoStr)


def test_astrofunc_get_info():
    ptr = create_string_buffer(128)
    pysgp4.AstroFunc.AstroFuncGetInfo(ptr)
    assert ptr.value.decode().strip(
    ) == "HQ SpOC AstroFunc - Version: v9.8 - Build: Mar 04 2026 - Platform: Windows 64-bit - Compiler: OneAPI ifort"

# static native void 	KepToEqnx(double[] xa_kep, double[] xa_eqnx)


def test_kep_to_eqnx():
    # Example 1: Convert Keplerian elements to equinoctial elements
    (a, e, incli, m0, raan, omega) = [7000, 0.001, 98.7, 40, 250, 0]
    kep = CreateCArray(c_double, [pysgp4.XA_KEP_SIZE])
    # semi-major axis (km)
    kep[pysgp4.XA_KEP_A] = a
    # eccentricity (unitless)
    kep[pysgp4.XA_KEP_E] = e
    # inclination (degrees)
    kep[pysgp4.XA_KEP_INCLI] = incli
    # mean anomaly (degrees)
    kep[pysgp4.XA_KEP_MA] = m0
    # right ascension of ascending node (degrees)
    kep[pysgp4.XA_KEP_NODE] = raan
    # argument of perigee (degrees)
    kep[pysgp4.XA_KEP_OMEGA] = omega

    # output array for equinoctial elements
    eqnx = CreateCArray(c_double, [pysgp4.XA_EQNX_SIZE])
    pysgp4.AstroFunc.KepToEqnx(kep, eqnx)
    (Af, Ag, chi, psi, L, N) = eqnx[:pysgp4.XA_EQNX_SIZE]

    # Calculate expected equinoctial elements based on the input Keplerian elements
    _Ag = e * sin(radians(omega + raan))
    _Af = e * cos(radians(omega + raan))
    _chi = tan(radians(incli) / 2) * sin(radians(raan))
    _psi = tan(radians(incli) / 2) * cos(radians(raan))
    _L = (omega + raan + m0) % 360
    MU_EARTH: float = pysgp4.EnvConst.EnvGetGeoConst(pysgp4.XF_GEOCON_MU)
    assert MU_EARTH == 398600.8
    # Gravitational parameter km ^ 3/(solar s) ^ 2
    _N = sqrt(MU_EARTH / (a ** 3)) * 24 * 60 * 60 / (2 * pi)  # revs per day

    # Af (unitless)
    assert eqnx[pysgp4.XA_EQNX_AF] == -0.00034202014332566856
    assert eqnx[pysgp4.XA_EQNX_AF] == _Af
    # Ag (unitless)
    assert eqnx[pysgp4.XA_EQNX_AG] == -0.0009396926207859085
    assert eqnx[pysgp4.XA_EQNX_AG] == _Ag
    # chi (unitless)
    assert eqnx[pysgp4.XA_EQNX_CHI] == -1.0944238622242743
    assert eqnx[pysgp4.XA_EQNX_CHI] == _chi
    # psi (unitless)
    assert eqnx[pysgp4.XA_EQNX_PSI] == -0.39833770952029085
    assert eqnx[pysgp4.XA_EQNX_PSI] == _psi
    # L (degrees)
    assert eqnx[pysgp4.XA_EQNX_L] == 290.0
    assert eqnx[pysgp4.XA_EQNX_L] == _L
    # N (revs/days)
    assert eqnx[pysgp4.XA_EQNX_N] == 14.823675420737096
    assert eqnx[pysgp4.XA_EQNX_N] == _N

    # Platform-G （IMP-G）lunar/solar perturbations are important
    (a, e, i, M, RAAN, omega) = [
        94820.03, 0.8940664, 0, 103.62458, 83.864809, -157.19876]
    kep = CreateCArray(c_double, [pysgp4.XA_KEP_SIZE])
    kep[:] = [a, e, i, M, RAAN, omega]
    eqnx = CreateCArray(c_double, [pysgp4.XA_EQNX_SIZE])
    pysgp4.AstroFunc.KepToEqnx(kep, eqnx)

    _Af = e * cos(radians(omega + RAAN))
    _Ag = e * sin(radians(omega + RAAN))
    _chi = tan(radians(i) / 2) * sin(radians(RAAN))
    _psi = tan(radians(i) / 2) * cos(radians(RAAN))
    _L = (omega + RAAN + M) % 360
    MU_EARTH = pysgp4.EnvConst.EnvGetGeoConst(pysgp4.XF_GEOCON_MU)
    _N = sqrt(MU_EARTH / (a ** 3)) * 24 * 60 * 60 / (2 * pi)  # revs per day

    assert eqnx[pysgp4.XA_EQNX_AF] == _Af
    assert eqnx[pysgp4.XA_EQNX_AG] == _Ag
    assert eqnx[pysgp4.XA_EQNX_CHI] == _chi
    assert eqnx[pysgp4.XA_EQNX_PSI] == _psi
    # _L = 30.290628999999996
    assert eqnx[pysgp4.XA_EQNX_L] == 30.290628999999992
    # _N = 0.2973396490807063
    assert eqnx[pysgp4.XA_EQNX_N] == 0.29733964908070626


# static native void 	KepToPosVel(double[] xa_kep, double[] pos, double[] vel)
def test_kep_to_pos_vec():
    for i in [40]:
        xa = CreateCArray(c_double, [6])
        pos = CreateCArray(c_double, [3])
        vel = CreateCArray(c_double, [3])
        xa[:] = [7000, 0.001, 98.7, i, 250, 0]

        pysgp4.AstroFunc.KepToPosVel(xa, pos, vel)

        assert pos[:] == [-2470.6786434529795, -4796.668166845987, 4451.147991660561]
        assert vel[:] == [0.839682234624599, 4.864101668605924, 5.715389883948284]

# static native void 	KepToUVW(double[] xa_kep, double[] uBar, double[] vBar, double[] wBar)
def test_kep_to_uvw():
    xa = CreateCArray(c_double, [6])
    uBar = CreateCArray(c_double, [3])
    vBar = CreateCArray(c_double, [3])
    wBar = CreateCArray(c_double, [3])
    xa[:] = [7000, 0.001, 98.7, 40, 250, 0]

    pysgp4.AstroFunc.KepToUVW(xa, uBar, vBar, wBar)

    assert uBar[:] == [-0.35322453149968863, -0.6857633510871137, 0.636365505548971]
    assert vBar[:] == [0.11141639095317687, 0.6445364847868799, 0.756411995942384]
    assert wBar[:] == [-0.928880411126101, 0.33808482084285313, -0.15126082024721924]
    # print("uBar:", uBar[:])
    # print("vBar:", vBar[:])
    # print("wBar:", wBar[:])

# static native void 	ClassToEqnx(double[] xa_cls, double[] xa_eqnx)

# static native void 	EqnxToClass(double[] xa_eqnx, double[] xa_cls)

# static native void 	EqnxToKep(double[] xa_eqnx, double[] xa_kep)

# static native void 	EqnxToPosVel(double[] xa_eqnx, double[] pos, double[] vel)

# static native void 	PosVelToEqnx(double[] pos, double[] vel, double[] xa_eqnx)

# static native void 	PosVelMuToEqnx(double[] pos, double[] vel, double mu, double[] xa_eqnx)

# static native void 	PosVelToKep(double[] pos, double[] vel, double[] xa_kep)

# static native void 	PosVelMuToKep(double[] pos, double[] vel, double mu, double[] xa_kep)

# static native void 	PosVelToUUVW(double[] pos, double[] vel, double[] uvec, double[] vVec, double[] wVec)

# static native void 	PosVelToPTW(double[] pos, double[] vel, double[] uvec, double[] vVec, double[] wVec)

# static native double 	SolveKepEqtn(double[] xa_kep)

# static native double 	CompTrueAnomaly(double[] xa_kep)

# static native double 	NToA(double n)

# static native double 	AToN(double a)

# static native double 	KozaiToBrouwer(double eccen, double incli, double nKozai)

# static native double 	BrouwerToKozai(double eccen, double incli, double nBrouwer)

# static native void 	KepOscToMean(double[] xa_OscKep, double[] xa_MeanKep)

# static native void 	XYZToLLH(double thetaG, double[] metricPos, double[] metricLLH)

# static native void 	XYZToLLHTime(double ds50UTC, double[] metricPos, double[] metricLLH)

# static native void 	LLHToXYZ(double thetaG, double[] metricLLH, double[] metricXYZ)

# static native void 	LLHToXYZTime(double ds50UTC, double[] metricLLH, double[] metricXYZ)

# static native void 	EFGToECI(double thetaG, double[] posEFG, double[] velEFG, double[] posECI, double[] velECI)

# static native void 	EFGToECITime(double ds50UTC, double[] posEFG, double[] velEFG, double[] posECI, double[] velECI)

# static native void 	ECIToEFG(double thetaG, double[] posECI, double[] velECI, double[] posEFG, double[] velEFG)

# static native void 	ECIToEFGTime(double ds50UTC, double[] posECI, double[] velECI, double[] posEFG, double[] velEFG)

# static native void 	ECRToEFG(double polarX, double polarY, double[] posECR, double[] velECR, double[] posEFG, double[] velEFG)

# static native void 	ECRToEFGTime(double ds50UTC, double[] posECR, double[] velECR, double[] posEFG, double[] velEFG)

# static native void 	EFGToECR(double polarX, double polarY, double[] posEFG, double[] velEFG, double[] posECR, double[] velECR)

# static native void 	EFGToECRTime(double ds50UTC, double[] posEFG, double[] velEFG, double[] posECR, double[] velECR)

# static native void 	EFGPosToLLH(double[] posEFG, double[] metricLLH)

# static native void 	LLHToEFGPos(double[] metricLLH, double[] posEFG)

# static native void 	RotJ2KToDate(int spectr, int nutationTerms, double ds50TAI, double[] posJ2K, double[] velJ2K, double[] posDate, double[] velDate)

# static native void 	RotDateToJ2K(int spectr, int nutationTerms, double ds50TAI, double[] posDate, double[] velDate, double[] posJ2K, double[] velJ2K)

# static native void 	CompSunMoonPos(double ds50ET, double[] uvecSun, double[] sunVecMag, double[] uvecMoon, double[] moonVecMag)

# static native void 	CompSunPos(double ds50ET, double[] uvecSun, double[] sunVecMag)

# static native void 	CompMoonPos(double ds50ET, double[] uvecMoon, double[] moonVecMag)

# static native void 	AstroConvFrTo(int xf_Conv, double[] frArr, double[] toArr)

# static native void 	RADecToLAD(double ra, double dec, double[] l, double[] a_tilde, double[] d_tilde)

# static native void 	AzElToLAD(double az, double el, double[] lh, double[] ah, double[] dh)

# static native void 	ECIToTopoComps(double theta, double lat, double[] senPos, double[] satPos, double[] satVel, double[] xa_topo)

# static native void 	RaDecToAzEl(double thetaG, double lat, double lon, double ra, double dec, double[] az, double[] el)

# static native void 	RaDecToAzElTime(double ds50UTC, double lat, double lon, double ra, double dec, double[] az, double[] el)

# static native void 	AzElToRaDec(double thetaG, double lat, double lon, double az, double el, double[] ra, double[] dec)

# static native void 	AzElToRaDecTime(double ds50UTC, double lat, double lon, double az, double el, double[] ra, double[] dec)

# static native void 	RAEToECI(double theta, double astroLat, double[] xa_rae, double[] senPos, double[] satPos, double[] satVel)

# static native void 	GetInitialDrag(double semiMajorAxis, double eccen, double[] nDot, double[] bstar)

# static native void 	CovMtxPTWToUVW(double[] pos, double[] vel, double[][] ptwCovMtx, double[][] uvwCovMtx)

# static native void 	CovMtxUVWToPTW(double[] pos, double[] vel, double[][] uvwCovMtx, double[][] ptwCovMtx)

# static native void 	EarthObstructionAngles(double earthLimb, double[] satECI, double[] senECI, double[] earthSenLimb, double[] earthSenSat, double[] satEarthSen)

# static native int 	IsPointSunlit(double ds50ET, double[] ptEci)

# static native void 	RotRADecl(int nutationTerms, int dir, double ds50UTCIn, double raIn, double declIn, double ds50UTCOut, double[] raOut, double[] declOut)

# static native int 	RotRADec_DateToEqnx(int nutationTerms, int yrOfEqnx, double ds50UTCIn, double raIn, double declIn, double[] raOut, double[] declOut)

# static native int 	RotRADec_EqnxToDate(int nutationTerms, int yrOfEqnx, double ds50UTCIn, double raIn, double declIn, double[] raOut, double[] declOut)

# static native void 	CovMtxEqnxToUVW(double[] pos, double[] vel, double[][] covMtxEqnx, double[][] covMtxUVW)

# static native void 	CovMtxUVWToEqnx(double[] pos, double[] vel, double[][] covMtxUVW, double[][] covMtxEqnx)

# static native void 	CovMtxECIToUVW(double[] pos, double[] vel, double[][] covMtxECI, double[][] covMtxUVW)

# static native void 	CovMtxUVWToECI(double[] pos, double[] vel, double[][] covMtxUVW, double[][] covMtxECI)

# static native void 	CovMtxECIToEFG(double thetaG, double[][] covECI, double[][] covEFG)

# static native void 	CovMtxEFGToECI(double thetaG, double[][] covEFG, double[][] covECI)

# static native void 	Mtx6x6ToLTA21(double[][] symMtx6x6, double[] lta21)

# static native void 	LTA21ToMtx6x6(double[] lta21, double[][] symMtx6x6)

# static native void 	Mtx9x9ToLTA45(double[][] symMtx9x9, double[] lta45)

# static native void 	LTA45ToMtx9x9(double[] lta45, double[][] symMtx9x9)

# static native void 	PropCovFrState(double rms, double consider, double[] stateArray, double[][] cov, double[][] propCov)

# static native void 	CovMtxECIToEqnx(double[] pos, double[] vel, double[][] covMtxECI, double[][] covMtxEqnx)

# static native void 	CovMtxEqnxToECI9x9(double[] pos, double[] vel, double[][] covEqnx, double[][] covMtxECI)

# static native void 	CovMtxEqnxToUVW9x9(double[] pos, double[] vel, double[][] covEqnx, double[][] covMtxUVW)

# static native void 	CovMtxUpdate(double rmsIn, double consider, double[][] cov, double[] stateArray, double[][] propCov)

# static native void 	AberrationAnnual(double ra, double decl, double dS50UTC, double[] raDelta, double[] decDelta)

# static native void 	AberrationDiurnal(double ra, double decl, double dS50UTC, double[] senPos, double[] raDelta, double[] decDelta)

# static native void 	JplSetParameters(byte[] jplFile, double ds50Start, double ds50Stop)

# static native void 	JplGetParameters(byte[] jplFile, double[] ds50Start, double[] ds50Stop)

# static native void 	JplReset()

# static native void 	JplCompSunMoonVec(double ds50UTC, double[] uvecSun, double[] sunVecMag, double[] uvecMoon, double[] moonVecMag)

# static native void 	JplCompSunMoonPos(double ds50UTC, double[] sunVec, double[] moonVec)

# static native void 	RemoveJpl()

# static native void 	TemeEpochToDate(int nutationTerms, double epochDs50TAI, double dateDs50TAI, double[] posEpoch, double[] velEpoch, double[] posDate, double[] velDate)

# static native void 	ECRToECITime(double ds50UTC, double[] posECR, double[] velECR, double[] posECI, double[] velECI)

# static native void 	ECIToECRTime(double ds50UTC, double[] posECI, double[] velECI, double[] posECR, double[] velECR)

# static native void 	ECRToJ2KTime(int spectr, int nutationTerms, double ds50UTC, double[] posECR, double[] velECR, double[] posJ2K, double[] velJ2K)

# static native void 	J2KToECRTime(int spectr, int nutationTerms, double ds50UTC, double[] posJ2K, double[] velJ2K, double[] posECR, double[] velECR)
