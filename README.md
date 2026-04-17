# Understand and use the SGP4 Library from space-track.org

## SGP4Prop

SGP4Prop is a famous propagation (the name Prop) library for satellite orbit prediction, which is widely used in the aerospace industry. The SGP4Prop library is developed and maintained by the United States Air Force, and it is available for free on the space-track.org website.

SGP4 stand for Simplified General Perturbations Model 4, which is a quasi-analytical solution of the equations of motion for Earth-orbiting satellites. It is designed to provide accurate predictions of satellite positions and velocities over short time intervals, typically up to a few days. SGP4Prop is based on the SGP4 model, which takes into account various perturbations such as atmospheric drag, gravitational effects from the Earth and other celestial bodies, and solar radiation pressure.

[SGP4Prop_v9.8](https://www.space-track.org/documentation#/sgp4)

You need to login to space-track.org to download the SGP4 library. You can create a free account if you don't have one. And a [License](SGP4_Open_License.txt) is included in this repository, which is needed to use the SGP4 library. SGP4Prop will search for the Licese file in the current directory.

And you have to dowanload the [SGP4 library](https://www.space-track.org/documentation#stModal) , and get Lib folder from the downloaded file, and put it in pysgp4 folder. The structure of pysgp4 folder should be like this:

```
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

Then you can use the SGP4 library in Python by importing pysgp4.

## How orbit is described

TLE (Two-Line Element set) is a data format used to describe the orbit of a satellite. It consists of two lines of text, each containing specific information about the satellite's orbit. The first line contains the satellite's name, its international designator, and the epoch time (the time at which the TLE was generated). The second line contains the satellite's orbital parameters, such as its inclination, right ascension of the ascending node, eccentricity, argument of perigee, mean anomaly, and mean motion.

![TLE](imgs/tles.png)
