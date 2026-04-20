from numpy import sqrt

from pysgp4.astrofunc import *
import pysgp4 as sgp4


def test_posvel2kep():
    # Example position and velocity vectors (in km and km/s)
    pos = [7000.0, 0.0, 0.0]  # Position vector in km
    vel = [0.0, 7.5, 1.0]      # Velocity vector in km/s

    kep_elements = posvel2kep(pos, vel)
    print("Keplerian Elements:", kep_elements)

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
