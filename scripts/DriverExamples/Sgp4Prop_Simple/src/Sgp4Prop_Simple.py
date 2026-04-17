#!/usr/bin/python
"""
   Purpose:
      This program shows how a Python program can call the Astrodynamic Standard libraries to propagate
      satellites to the requested time using SGP4 propagator.

      The program is simplified to show only the core functionalities of the involved DLLs. 
      File I/O and other output statements are intentionally not included for this purpose.

      Steps to implement the SGP4 propagator:
      1. Load and initialize all the required DLLs  (LoadAstroStdDlls and InitAstroStdDlls)  
      2. Load TLE(s) (TleAddSatFrLines, TleLoadFile, TleAddSatFrFieldsGP)
      3. Initialize the loaded TLE(s) (Sgp4InitSat)
      4. Propagate the initialized TLE(s) to the requested time 
         (either minutes since epoch: Sgp4PropMse, or specific date: Sgp4PropDs50UTC, Sgp4PropDs50UtcPos, Sgp4PropDs50UtcLLH)
      5. Deallocate loaded DLLs (FreeAstroStdDlls)

"""
import sys
import time
from ctypes import *
from scripts.DriverExamples.Sgp4Prop_Simple.src.AstroUtils import *
from wrappers.DllMainWrapper import *
from wrappers.EnvConstWrapper import *
from wrappers.AstroFuncWrapper import *
from wrappers.TimeFuncWrapper  import *
from wrappers.TleWrapper import *
from wrappers.Sgp4PropWrapper import *

class Sgp4Prop_Simple(object):
   # Global variables used to store the dll objects
   # We place them here so that all of our functions will have access to them, although they're initially set to None
   DllMain = None
   EnvConst = None
   AstroFunc = None
   TimeFunc = None
   Tle = None
   Sgp4Prop = None
   
   def run(self):
      """The main function of the program.

      All of the main operations of the program are done from here; the program sets up global data, then calls this function. We do it this way to make reading the code easier, and in order to facilitate unit testing.

      """

      # Load and initialize dll's
      self.DllMain = LoadDllMainDll()
      self.EnvConst = LoadEnvConstDll()
      self.TimeFunc = LoadTimeFuncDll()
      self.AstroFunc = LoadAstroFuncDll()
      self.Tle = LoadTleDll()
      self.Sgp4Prop = LoadSgp4PropDll()

      # load a TLE using strings (see TLE dll document)
      satKey = self.Tle.TleAddSatFrLines("1 90021U RELEAS14 00051.47568104 +.00000184 +00000+0 +00000-4 0 0814".encode("UTF-8"), "2 90021   0.0222 182.4923 0000720  45.6036 131.8822  1.00271328 1199".encode("UTF-8"))

      # other ways to load TLEs into memory to work with
      #self.Tle.TleLoadFile(fileName)  # load TLEs from a text file
      #self.Tle.TleAddSatFrFieldsGP()  # load a TLE by passing its data fields

      # initialize the loaded TLE before it can be propagated (see Sgp4Prop dll document)
      # This is important!!!
      if self.Sgp4Prop.Sgp4InitSat(satKey):
         ShowMsgAndTerminate(self.DllMain)
         

      # propagate using specific date, days since 1950 UTC (for example using "2000 051.051.47568104" as a start time)
      startTime = self.TimeFunc.DTGToUTC("00051.47568104".encode("UTF-8")) # convert date time group string "YYDDD.DDDDDDDD" to days since 1950, UTC (see TimeFunc dll document)
      stopTime = startTime + 10               # from start time propagate for 10 days 

      ds50UTC = c_double()
      mse = c_double()
      pos = CreateCArray(c_double, [3])
      vel = CreateCArray(c_double, [3])
      llh = CreateCArray(c_double, [3])
      
      step = 0
      ds50UTC.value = startTime
      
      # propagate for 10 days from start time with 0.5 day step size
      while (ds50UTC.value < stopTime):
         ds50UTC.value = startTime + (step * 0.5)
         self.Sgp4Prop.Sgp4PropDs50UTC(c_longlong(satKey), ds50UTC, byref(mse), pos, vel, llh)
         step = step + 1
         # other available propagation methods
         #self.Sgp4Prop.Sgp4PropDs50UtcLLH(c_longlong(key), ds50UTC, llh)
         #self.Sgp4Prop.Sgp4PropDs50UtcPos(c_longlong(key), ds50UTC, pos)
         print( "%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f" % (ds50UTC.value, pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]) )
      

      # propagate using minutes since satellite's epoch
      # propagate for 30 days since satellite's epoch with 1 day (1440 minutes) step size
      for mse in range(0, (30*1440), 1440):
         # propagate the initialized TLE to the specified time in minutes since epoch
         self.Sgp4Prop.Sgp4PropMse(c_longlong(satKey), mse, byref(ds50UTC), pos, vel, llh) # see Sgp4Prop dll document
         print( "%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f" % (mse, pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]) )
         
      
      # Remove loaded satellites if no longer needed
      self.Tle.TleRemoveSat(satKey)   # remove loaded TLE from memory
      self.Sgp4Prop.Sgp4RemoveSat(satKey)  # remove initialized TLE from memory
      #self.Tle.TleRemoveAllSats()   # remove all loaded TLEs from memory
      #self.Sgp4Prop.Sgp4RemoveAllSats()  # remove all initialized TLEs from memory

      
# Standard object oriented start
app = Sgp4Prop_Simple()
app.run()

