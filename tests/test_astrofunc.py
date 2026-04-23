from numpy import sqrt

from pysgp4.astrofunc import *
import pysgp4 as sgp4

def test_coverage():
    funcs = [func for func in dir(sgp4.AstroFunc) if not func.startswith("_")]
    print("Testing coverage of AstroFunc functions:")
    for func in funcs:
        print(f"Testing {func}...")
        getattr(sgp4, func)  # Just call the function to ensure it's accessible
    py_funcs = [func for func in dir(sgp4.astrofunc) if not func.startswith("_")]

    print(f"\n{len(funcs)} functions in AstroFunc, {len(py_funcs)} functions in astrofunc.py")

def test_kep2eqnx():
    # Example Keplerian elements (a, e, i, raan, argp, M)
    kep_elements = [7000.0, 0.001, 98.0, 40.0, 30.0, 10.0]

    eqnx_elements = kep2eqnx(kep_elements)
    print("\nEquinoctial Elements:", eqnx_elements)

    # Check that the returned equinoctial elements are reasonable
    assert len(eqnx_elements) == XA_EQNX_SIZE
    assert eqnx_elements[0] > 0  # Semi-major axis should be positive

def test_kep2posvel():
    # Example Keplerian elements (a, e, i, raan, argp, M)
    kep_elements = [7000.0, 0.001, 98.0, 40.0, 30.0, 10.0]

    pos, vel = kep2posvel(kep_elements)
    print("\nPosition and Velocity:", pos, vel)

    # Check that the returned position and velocity are reasonable
    assert len(pos) == 3
    assert len(vel) == 3
    assert sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2) > 0  # Position should not be zero
    assert sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2) > 0  # Velocity should not be zero

def test_kep2uvw():
    # Example Keplerian elements (a, e, i, raan, argp, M)
    kep_elements = [7000.0, 0.001, 98.0, 40.0, 30.0, 10.0]

    u, v, w = kep2uvw(kep_elements)
    print("\nUVW Components:", u, v, w)

    # Check that the returned UVW components are reasonable
    assert len(u) == 3
    assert len(v) == 3
    assert len(w) == 3
    assert sqrt(u[0]**2 + u[1]**2 + u[2]**2)  == 1.0  # U component should not be zero
    assert sqrt(v[0]**2 + v[1]**2 + v[2]**2) == 1.0  # V component should not be zero
    assert sqrt(w[0]**2 + w[1]**2 + w[2]**2) == 1.0  # W component should not be zero

def test_class2eqnx():
    # Example classical orbital elements (a, e, i, raan, argp, M)
    cls_elements = [7000.0, 0.001, 98.0, 40.0, 30.0, 10.0]

    eqnx_elements = class2eqnx(cls_elements)
    print("\nEquinoctial Elements from Classical Elements:", eqnx_elements)

    # Check that the returned equinoctial elements are reasonable
    assert len(eqnx_elements) == XA_EQNX_SIZE
    assert eqnx_elements[0] > 0  # Semi-major axis should be positive

def test_eqnx2class():
    # Example equinoctial elements (a, h, k, p, q, M)
    eqnx_elements = [0.000766044443118978, 0.0006427876096865392,
                     0.5751842036105046, 0.9962482643644363, 80.0, 7000.0]

    cls_elements = eqnx2class(eqnx_elements)
    print("\nClassical Elements from Equinoctial Elements:", cls_elements)

    # Check that the returned classical elements are reasonable
    assert len(cls_elements) == XA_CLS_SIZE
    assert cls_elements[0] > 0  # Semi-major axis should be positive

def test_posvel2kep():
    # Example position and velocity vectors (in km and km/s)
    pos = [7000.0, 0.0, 0.0]  # Position vector in km
    vel = [0.0, 7.5, 1.0]      # Velocity vector in km/s

    kep_elements = posvel2kep(pos, vel)
    print("\nKeplerian Elements:", kep_elements)

    # calculate the expected Keplerian elements explicitly for the given pos and vel

    r_bar = sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)  # Semi-major axis
    v_bar = sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2)  # Velocity magnitude
    mu = sgp4.EnvGetGeoConst(sgp4.XF_GEOCON_MU)  # Gravitational parameter
    _a = 1 / (2 / r_bar - v_bar**2 / mu)  # Semi-major axis
    print(f"Expected Semi-major axis (a): {_a:.4f} km")
    assert abs(kep_elements[0] - _a) < 1e-4

    # Check that the returned Keplerian elements are reasonable
    assert len(kep_elements) == XA_KEP_SIZE
    assert kep_elements[0] > 0  # Semi-major axis should be positive
