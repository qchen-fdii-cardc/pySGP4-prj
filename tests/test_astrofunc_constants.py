import pysgp4

def test_AstroFunc_constants_Keplerian_elements():
    # Index of Keplerian elements
    # semi-major axis (km)
    assert pysgp4.XA_KEP_A == 0
    # eccentricity (unitless)
    assert pysgp4.XA_KEP_E == 1
    # inclination (deg)
    assert pysgp4.XA_KEP_INCLI == 2
    # mean anomaly (deg)
    assert pysgp4.XA_KEP_MA == 3
    # right ascension of the asending node (deg)
    assert pysgp4.XA_KEP_NODE == 4
    # argument of perigee (deg)
    assert pysgp4.XA_KEP_OMEGA == 5
    assert pysgp4.XA_KEP_SIZE == 6

def test_AstroFunc_constants_classical_elements():
    # Index of classical elements
    # N mean motion (revs/day)
    assert pysgp4.XA_CLS_N == 0
    # eccentricity (unitless)
    assert pysgp4.XA_CLS_E == 1
    # inclination (deg)
    assert pysgp4.XA_CLS_INCLI == 2
    # mean anomaly (deg)
    assert pysgp4.XA_CLS_MA == 3
    # right ascension of the asending node (deg)
    assert pysgp4.XA_CLS_NODE == 4
    # argument of perigee (deg)
    assert pysgp4.XA_CLS_OMEGA == 5
    assert pysgp4.XA_CLS_SIZE == 6

def test_AstroFunc_constants_equinoctial_elements():
    # Index of equinoctial elements
    # Af (unitless)
    assert pysgp4.XA_EQNX_AF == 0
    # Ag (unitless)
    assert pysgp4.XA_EQNX_AG == 1
    # chi (unitless)
    assert pysgp4.XA_EQNX_CHI == 2
    # psi (unitless)
    assert pysgp4.XA_EQNX_PSI == 3
    # L mean longitude (deg)
    assert pysgp4.XA_EQNX_L == 4
    # N mean motion (revs/day)
    assert pysgp4.XA_EQNX_N == 5
    assert pysgp4.XA_EQNX_SIZE == 6

def test_AstroFunc_constants_conversion():
    # Indexes of AstroConvFrTo
    # SGP4 (A, E, Incli, BStar) to SGP (nDot, n2Dot)
    assert pysgp4.XF_CONV_SGP42SGP == 101

def test_AstroFunc_constants_topocentric():
    # Indexes for topocentric components
    # Right ascension (deg)
    assert pysgp4.XA_TOPO_RA == 0
    # Declination (deg)
    assert pysgp4.XA_TOPO_DEC == 1
    # Azimuth (deg)
    assert pysgp4.XA_TOPO_AZ == 2
    # Elevation (deg)
    assert pysgp4.XA_TOPO_EL == 3
    # Range (km)
    assert pysgp4.XA_TOPO_RANGE == 4
    # Right ascension dot (deg/s)
    assert pysgp4.XA_TOPO_RADOT == 5
    # Declincation dot (deg/s)
    assert pysgp4.XA_TOPO_DECDOT == 6
    # Azimuth dot (deg/s)
    assert pysgp4.XA_TOPO_AZDOT == 7
    # Elevation dot (deg/s)
    assert pysgp4.XA_TOPO_ELDOT == 8
    # Range dot (km/s)
    assert pysgp4.XA_TOPO_RANGEDOT == 9
    assert pysgp4.XA_TOPO_SIZE == 10

def test_AstroFunc_constants_RAE():
    # Indexes for RAE components
    # Range (km)
    assert pysgp4.XA_RAE_RANGE == 0
    # Azimuth (deg)
    assert pysgp4.XA_RAE_AZ == 1
    # Elevation (deg)
    assert pysgp4.XA_RAE_EL == 2
    # Range dot (km/s)
    assert pysgp4.XA_RAE_RANGEDOT == 3
    # Azimuth dot (deg/s)
    assert pysgp4.XA_RAE_AZDOT == 4
    # Elevation dot (deg/s)
    assert pysgp4.XA_RAE_ELDOT == 5
    assert pysgp4.XA_RAE_SIZE == 6

def test_AstroFunc_constants_YROFEQNX():
    # Year of Equinox indicator
    # Date of observation
    assert pysgp4.YROFEQNX_OBTIME == 0
    # 0 Jan of Date
    assert pysgp4.YROFEQNX_CURR == 1
    # J2000
    assert pysgp4.YROFEQNX_2000 == 2
    # B1950
    assert pysgp4.YROFEQNX_1950 == 3

# ========================= End of auto generated code ==========================
