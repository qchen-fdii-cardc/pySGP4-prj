# Understand and use the SGP4 Library from space-track.org

## SGP4Prop

SGP4Prop is a famous propagation (the name Prop) library for satellite orbit prediction, which is widely used in the aerospace industry. The SGP4Prop library is developed and maintained by the United States Air Force, and it is available for free on the space-track.org website.

SGP4 stand for Simplified General Perturbations Model 4, which is a quasi-analytical solution of the equations of motion for Earth-orbiting satellites. It is designed to provide accurate predictions of satellite positions and velocities over short time intervals, typically up to a few days. SGP4Prop is based on the SGP4 model, which takes into account various perturbations such as atmospheric drag, gravitational effects from the Earth and other celestial bodies, and solar radiation pressure.

[SGP4Prop_v9.8](https://www.space-track.org/documentation#/sgp4)

You need to login to space-track.org to download the SGP4 library. You can create a free account if you don't have one. And a [License](SGP4_Open_License.txt) is included in this repository, which is needed to use the SGP4 library. SGP4Prop will search for the Licese file in the current directory.

And you have to dowanload the [SGP4 library](https://www.space-track.org/documentation#stModal) , and get Lib folder from the downloaded file, and put it in pysgp4 folder. The structure of pysgp4 folder should be like this:

```txt
pysgp4/
├── __init__.py
├── Lib
│   ├── Windows
│   │   ├── AstroFunc.dll
│   │   └── DllMain.dll
│   └── Linux
│       └── x86
│           ├── libAstroFunc.so
│           └── libDllMain.so
└── MacOS
    └── x86
        ├── libAstroFunc.dylib
        └── libDllMain.dylib
```

Here with uv manage the python venv, the SGP4 library imported to  Python by importing pysgp4.

## Orbital mechanis basics

### How orbit is described

TLE (Two-Line Element set) is a data format used to describe the orbit of a satellite. It consists of two lines of text, each containing specific information about the satellite's orbit. The first line contains the satellite's name, its international designator, and the epoch time (the time at which the TLE was generated). The second line contains the satellite's orbital parameters, such as its inclination, right ascension of the ascending node, eccentricity, argument of perigee, mean anomaly, and mean motion.

![TLE](imgs/tles.png)

### Oribtal Mechanics 甲乙丙

whos knows the law that makes things fall on the ground is the same that makes the moon orbit around the earth, and the earth orbit around the sun?

![gravity](imgs/grav.png)

That's science and truth.

![EOM](imgs/eom.png)

#### Orbital Elements

To describe an orbit, first define the orientation of the orbital plane using:

- inclination (i): the angle between the orbital plane and the equatorial plane, in degrees
- right ascension of the ascending node (Ω): the ascending node is where the satellite crosses the equatorial plane from south to north; Ω is the angle from the vernal equinox direction to the ascending node, in degrees

The orbit shape is described by three parameters:

- a (semi-major axis): the semi-major axis of the orbit, in kilometers
- e (eccentricity): orbital eccentricity (dimensionless)
- ω (argument of perigee): the argument of perigee, in degrees

Finally, the object's position on the orbit is described by one parameter:

- M (mean anomaly): mean anomaly, in degrees, or true anomaly, in degrees

![orbital elements](imgs/orbit_elements.png)

In the figure, point P is the point on the ellipse closest to Earth (for a circular orbit, this point is conventionally chosen), called the perigee. The farthest point on the orbit is called the apogee.

In the figure, Ω and i describe how the orbital plane is oriented relative to the equatorial plane. Ω is the angle from the vernal equinox direction to the ascending node, and i is the angle between the orbital plane and the equatorial plane.

The argument of perigee ω is the angle from the ascending node to the perigee, while the mean anomaly M is the angle from the perigee to the satellite's position.

This description is useful, but when e=0 every point on the orbit is both perigee and apogee. In that case, ω is undefined, and M also becomes ambiguous.

To handle this more robustly, another representation was introduced: the equinoctial elements.

#### Equinoctial Elements

Keplerian elements (`a`, `e`, `i`, `Ω`, `ω`, `M`) are not well defined for circular orbits (e=0) and equatorial orbits (i=0), so the equinoctial elements are introduced to solve this problem. The equinoctial elements are defined as follows:

```python
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
```

#### Inertial frame and UVW frame

The UVW frame is a local orbital coordinate system. The u-axis points along the satellite's position vector (radial direction), the w-axis points along the orbital angular momentum vector (orbit normal), and the v-axis completes the right-handed frame. For a circular orbit, the v-axis aligns with the velocity direction; in general it is the in-track direction and is not exactly the same as the velocity vector when the orbit has a radial velocity component.

![uvw-orbit](imgs/frames.png)

The following give a definition of the UVW frame from Keplerian elements, the transformation start from Keplerian elements to ECI frame, and then from ECI frame to UVW frame:

![uvw](imgs/uvw.png)

where rotation matrices are defined as:

![rotation](imgs/rotation_matrix.png)

## API of SGP4Prop

### Architecture

The v9 SGP4 library is composed of several components. Only part of them are not export-controlled, SGP4Prop is source code export-controlled.

![arch](imgs/V9_architect.png)

### DllMain

#### Logging

The SGP4 library provides a logging mechanism that allows users to log messages at different levels (e.g., debug, info, warning, error). The logging can be configured to output to the console or to a file. The following code snippet shows how to configure logging in the SGP4 library:

```python
# filename = create_string_buffer(b"test_log.txt", 256)
fn = b"test_log.txt"
retValue = sgp4.OpenLogFile(fn)
assert retValue == 0  # successfully set log file

sgp4.LogMessage(b"Test log message from Python")
sgp4.LogMessage(b"Another log message")
# make sure do this
sgp4.CloseLogFile()

# test content of log file
with open(fn, "r") as f:
    log_content = f.read()
    assert "Test log message from Python" in log_content
    assert "Another log message" in log_content
```

#### MOIC user input data

Data file with the format of "AS_MOIC 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0" can be loaded by DllMainLoadFile function, and then the data can be retrieved by GetMOICData function. Maximum to 128 numerical data can be handled by the MOIC data file. The following code snippet shows how to load a MOIC data file and retrieve the data:

```python
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
```

### EnvConst

There are 8 geodetic models available in the SGP4 library, and each geodetic model has a set of constants. The following table shows the constants for each geodetic model:

| GeoModel | FF | J2 | J3 | J4 | KE | KMPER | RPTIM | CK2 | CK4 | KS2EK | THDOT | J5 | MU |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WGS-72 | 0.003352779454167505 | 0.001082616 | -2.53881e-06 | -1.65597e-06 | 0.07436691613317341 | 6378.135 | 0.0043752690880113 | 0.000541308 | 6.209887499999999e-07 | 0.1264962848571814 | 0.05883354205754931 | -2.184827e-07 | 398600.8 |
| WGS-84 | 0.0033528106647474805 | 0.00108263 | -2.5321531e-06 | -1.6109876e-06 | 0.07436685316871385 | 6378.137 | 0.0043752690880113 | 0.000541315 | 6.0412035e-07 | 0.12649635229263637 | 0.0588335918703627 | -2.3578565e-07 | 398600.5 |
| EGM-96 | 0.003352819752990295 | 0.00108262668355315 | -2.53265648533224e-06 | -1.619621591367e-06 | 0.07436685995417885 | 6378.1363 | 0.0043752690880113 | 0.00054131334177655 | 6.07358096762625e-07 | 0.12649635463367767 | 0.05883358650220168 | -2.27296082868698e-07 | 398600.4415 |
| EGM-08 | 0.003352819752990295 | 0.00108262617385222 | -2.53241051856772e-06 | -1.61989759991697e-06 | 0.07436685995417885 | 6378.1363 | 0.0043752690880113 | 0.00054131308692611 | 6.074615999688638e-07 | 0.12649635463367764 | 0.05883358650220168 | -2.27753590730836e-07 | 398600.4415 |
| JGM2   | 0.0033528106647474805 | 0.00108262692563881 | -2.53230781819177e-06 | -1.6204299e-06 | 0.07436685995417885 | 6378.1363 | 0.0043752690880113 | 0.000541313462819405 | 6.076612125e-07 | 0.12649635463367767 | 0.05883358650220168 | 0.0 | 398600.4415 |
| SEM68R | 0.003352891869237217 | 0.001082621 | -2.627e-06 | -1.583e-06 | 0.0743667785 | 6378.145 | 0.0043752690880113 | 0.0005413105 | 5.93625e-07 | 0.126496320640168 | 0.05883365094282389 | 0.0 | 398601.199437963 |
| GEM5   | 0.003352835660760088 | 0.001082629 | -2.5412e-06 | -1.6089e-06 | 0.0743666129867 | 6378.155 | 0.0043752690880113 | 0.0005413145 | 6.033375e-07 | 0.12649640384753477 | 0.05883378188534402 | 0.0 | 398601.299998451 |
| GEM9   | 0.003352835660760088 | 0.00108262708 | -2.5359e-06 | -1.62462e-06 | 0.0743668137601 | 6378.14 | 0.0043752690880113 | 0.00054131354 | 6.092325e-07 | 0.126496359827421 | 0.05883362304757988 | 0.0 | 398600.639998969 |

These 13 constants are defined as follows:

| Name | Index | Description |
| --- | --- | --- |
| XF_GEOCON_FF | 1 | Earth flattening (reciprocal, unitless) |
| XF_GEOCON_J2 | 2 | J2 (unitless) |
| XF_GEOCON_J3 | 3 | J3 (unitless) |
| XF_GEOCON_J4 | 4 | J4 (unitless) |
| XF_GEOCON_KE | 5 | Ke (er**1.5/min) |
| XF_GEOCON_KMPER | 6 | Earth radius (km/er) |
| XF_GEOCON_RPTIM | 7 | Earth rotation rate w.r.t. fixed equinox (rad/min) |
| XF_GEOCON_CK2 | 8 | J2/2 (unitless) |
| XF_GEOCON_CK4 | 9 | -3/8 J4 (unitless) |
| XF_GEOCON_KS2EK | 10 | Converts km/sec to er/kem |
| XF_GEOCON_THDOT | 11 | Earth rotation rate w.r.t. fixed equinox (rad/kemin) |
| XF_GEOCON_J5 | 12 | J5 (unitless) |
| XF_GEOCON_MU | 13 | Gravitational parameter km^3/(solar s)^2 |

And there are 3 other constants related to earth fundamental parameters:

| Name | Index | Description |
| --- | --- | --- |
| XF_FKCON_C1 | 1 | Earth rotation rate w.r.t. moving equinox (rad/day) |
| XF_FKCON_C1DOT | 2 | Earth rotation acceleration(rad/day**2) |
| XF_FKCON_THGR70 | 3 | Greenwich angle (1970 rad) |

| FKModel | C1 | C1DOT | THGR70 |
| --- | --- | --- | --- |
| FK4 | 0.017203 | 0.0 | 1.732131 |
| FK5 | 0.017203 | 0.0 | 1.732134 |

#### Example: Sun-synchronous orbit

Sun synchronous orbit is driven by the precession of the orbit plane, which is caused by the J2 perturbation. The following table shows the inclination of sun-synchronous orbit at different altitudes:

![sun_sync](imgs/sun_sync.png)

| Height in km | Inclination (deg) |
|--------------|-------------------|
|     100.0000 |           95.9958 |
|     200.0000 |           96.3273 |
|     300.0000 |           96.6719 |
|     400.0000 |           97.0300 |
|     500.0000 |           97.4017 |
|     600.0000 |           97.7876 |
|     700.0000 |           98.1879 |
|     800.0000 |           98.6030 |
|     900.0000 |           99.0333 |
|    1000.0000 |           99.4792 |

[Sun-synchronous orbit](scripts/sun_sync.py)

### TimeFunc

### AstroFunc

### ExtEphem/TLE/SpVec/VCM

### Sensor/Obs

### Sgp4Prop

### ElOps

### SatState
