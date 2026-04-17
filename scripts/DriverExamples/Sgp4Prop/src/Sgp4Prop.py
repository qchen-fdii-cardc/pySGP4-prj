#!/usr/bin/python
"""
This program shows how a Python program can call the Astrodynamics Standard libraries to propagate satellites to the requested time using the Air Force Simplified General Perturbations, Version 4 (SGP4) propagator.

This program reads in a set of TLEs, and generates a series of output files containing various information about each satellite. (See below.)

Usage
Sgp4Prop.py <inFile> <outDir> -I<libpath>
<inFile>: The name of an input file containing TLE's, as well as a 6P-Card which controls start/stop times and step size.
<outDir>: Directory for output files.

Input
The program reads in a single input file. This file should contain a 6P-Card to control start/stop time and step size, and a set of TLE satellites to be propagated.

output
The program generates 5 output files, as well as a log file. The log file is called sgp4Prop.log, and is generated for diagnostic purposes. The 5 output files contain the following information for each satellite in the input file:

-- Ephemeris of position and velocity (<output directory>/OscState.txt)
-- Osculating Keplerian elements (<output directory>/OscElem.txt)
-- Mean Keplerian elements (<output directory>/MeanElem.txt)
-- Latitude/longitude/height/pos (<output directory>/LatLonHeight.txt)
-- Nodal period/apogee/perigee/pos (<output directory>/NodalApPer.txt)
 
"""

import os
import sys
import time
from ctypes import *
from scripts.DriverExamples.Sgp4Prop.src.AstroUtils import *
from wrappers.DllMainWrapper import *
from wrappers.EnvConstWrapper import *
from wrappers.AstroFuncWrapper import *
from wrappers.TimeFuncWrapper import *
from wrappers.TleWrapper import *
from wrappers.Sgp4PropWrapper import *

class Sgp4Prop(object):
   # Constants used when we need to pass an integer control value to a function
   DEFAULT_STRING_LENGTH = 513 # 512 + 1 for NULL
   ELSET_LOAD_ORDER = 2
   PROPOUT_NODAL_AP_PER = 2
   PROPOUT_MEAN_ELEM = 3
   PROPOUT_OSC_ELEM = 4
   
   # Global constants specifying the output file names
   OSC_STATE_FILE = 'OscState.txt'
   OSC_ELEM_FILE = 'OscElem.txt'
   MEAN_ELEM_FILE = 'MeanElem.txt'
   LLH_ELEM_FILE = 'LatLonHeight.txt'
   NODAL_AP_PER_FILE = 'NodalApPer.txt'
   
   # the name of the log file to open
   LOG_FILE_NAME = 'sgp4prop.log'

   # time tolerance
   EPSI = 0.00500
   
   # Global variables used to store the dll objects
   # We place them here so that all of our functions will have access to them, although they're initially set to None
   DllMain = None
   EnvConst = None
   AstroFunc = None
   TimeFunc = None
   Tle = None
   Sgp4Prop = None
   
   # These make it easier for routines that write to the output files
   # Since there are 5 of them, we chose to define these globally instead of passing 5 parameters to all of the routines that need them.
   # We define 5 file objects, as well as  a list that will contain them to make it easier for routines to write the same data to all 5 files since this is a common operation.
   oscStateFile = None
   oscElemFile = None
   meanElemFile = None
   llhElemFile = None
   nodalApPerFile = None
   outfiles = {}
   
   def run(self):
      # Print startup message and process command line
      print( 'Program starts.' )

      # time.clock() was deprected in 3.3
      if sys.version_info[0] > 3 or (sys.version_info[0] == 3 and sys.version_info[1] >= 3):
         start = time.process_time()
      else:
         start = time.clock()

      # Did we at least specify enough arguments?
      if len(sys.argv) < 3:
         ShowMsgAndTerminate('Invalid number of arguments.')
      inputFileName = sys.argv[1]
      outputDir = sys.argv[2]

      # Print the parameters
      print( 'Input File=%s\n' % inputFileName )
      print( 'Output Directory=%s\n' % outputDir )

      # Load and initialize dll's
      self.DllMain = LoadDllMainDll()
      self.EnvConst = LoadEnvConstDll()
      self.TimeFunc = LoadTimeFuncDll()
      self.AstroFunc = LoadAstroFuncDll()
      self.Tle = LoadTleDll()
      self.Sgp4Prop = LoadSgp4PropDll()

      # Open the log file
      if self.DllMain.OpenLogFile(self.LOG_FILE_NAME.encode("UTF-8")):
         ShowMsgAndTerminate(self.DllMain)

      # Load TLE's and the 6P-Card from the input file
      if self.Tle.TleLoadFile(inputFileName.encode("UTF-8")):
         ShowMsgAndTerminate(self.DllMain)
      if self.TimeFunc.TConLoadFile(inputFileName.encode("UTF-8")):
         ShowMsgAndTerminate(self.DllMain)

      # Load the satellite keys we loaded into a ctypes array for later processing
      numSats = c_int()
      numSats = self.Tle.TleGetCount()
      satKeys = CreateCArray(c_longlong, [numSats])
      self.Tle.TleGetLoaded(self.ELSET_LOAD_ORDER, satKeys)

      # Retrieve information about Sgp4Prop.dll
      # We'll print it here, and also use it in file headers
      cInfo = create_string_buffer(self.DEFAULT_STRING_LENGTH)
      self.Sgp4Prop.Sgp4GetInfo(cInfo)
      info = cInfo.value.rstrip()
      print( info )

      # Open output files and print header
      self.oscStateFile = self.OpenOutputFile(os.path.join(outputDir, self.OSC_STATE_FILE))
      self.oscElemFile = self.OpenOutputFile(os.path.join(outputDir, self.OSC_ELEM_FILE))
      self.meanElemFile = self.OpenOutputFile(os.path.join(outputDir, self.MEAN_ELEM_FILE))
      self.llhElemFile = self.OpenOutputFile(os.path.join(outputDir, self.LLH_ELEM_FILE))
      self.nodalApPerFile = self.OpenOutputFile(os.path.join(outputDir, self.NODAL_AP_PER_FILE))
      
      self.outFiles = [self.oscStateFile, self.oscElemFile, self.meanElemFile, self.llhElemFile, self.nodalApPerFile]
      self.PrintHeaders(info, inputFileName)

      # Process each TLE
      for key in satKeys:
         self.PropagateSatellite(key)

      # Clean up and print exit message
      self.Sgp4Prop.Sgp4RemoveAllSats()
      for outFile in self.outFiles:
         outFile.close()
      self.DllMain.CloseLogFile()
      print( 'Program completed successfully.' )

      # time.clock() was deprected in 3.3
      if sys.version_info[0] > 3 or (sys.version_info[0] == 3 and sys.version_info[1] >= 3):
         finish = time.process_time()
      else:
         finish = time.clock()

      print( 'Total run time = %10.2f seconds\n\n\n' % (finish - start) )

   def OpenOutputFile(self, fileName):
      """Opens the specified file for writing.

      If the file can not be opened, the function terminates the program with a status of 1. If the file already exists, it will be over written.

      Parameters
      fileName -- The name of the file to open. if the file already exists, it will be over written.

      """
      try:
         fileObj = open(fileName, 'w')
      except IOError:
         ShowMsgAndTerminate('Unable to open output file ' + fileName)
      return fileObj

   def PrintHeaders(self, info, inputFileName):
      """Prints the header at the top of each output file.

      This function handles both the standard and file-specific headers.

      Parameters
      info -- A string containing the info about Sgp4Prop.dll.
      inputFileName -- A string containing the name of the input file.

      """
      # Load the individual elements of the 6P card
      pStartFrEpoch = c_int()
      pStopFrEpoch = c_int()
      pStartTime = c_double()
      pStopTime = c_double()
      pStepSize = c_double()
      self.TimeFunc.Get6P(byref(pStartFrEpoch), byref(pStopFrEpoch), byref(pStartTime), byref(pStopTime), byref(pStepSize))
      # Write the common portion of the header to the output files
      for outFile in self.outFiles:
         PrintWarning('SGP4', outFile)
         outFile.write( '%s\n\n\n' % info )
         outFile.write( 'EPHEMERIS GENERATED BY SGP4 USING THE WGS-72 EARTH MODEL\n' )
         outFile.write( 'COORDINATE FRAME=TRUE EQUATOR AND MEAN EQUINOX OF EPOCH\n' )
         outFile.write( 'USING THE FK5 MEAN OF J2000 TIME AND REFERENCE FRAME\n\n\n' )
         outFile.write( 'INPUT FILE = %s\n' % inputFileName )
         if pStartFrEpoch:
            outFile.write( 'Start time = %14.4f min from epoch\n' % pStartTime.value )
         else:
            pStartDTG20Str = create_string_buffer(self.DEFAULT_STRING_LENGTH)
            self.TimeFunc.UTCToDTG20(pStartTime, pStartDTG20Str)
            outFile.write( 'Start time = %s\n' % pStartDTG20Str.value.rstrip() )
         if (pStopFrEpoch):
            outFile.write( 'Stop time = %14.4f min from epoch\n' % pStopTime.value )
         else:
            pStopDTG20Str = create_string_buffer(self.DEFAULT_STRING_LENGTH)
            self.TimeFunc.UTCToDTG20(pStopTime, pStopDTG20Str)
            outFile.write( 'Stop time = %s\n' % pStopDTG20Str.value.rstrip() )
         outFile.write( 'Step size = %14.4f min\n\n' % pStepSize.value )

      # Write the file-specific portion of the header to each output file
      self.oscStateFile.write( '     TSINCE (MIN)           X (KM)           Y (KM)           Z (KM)      XDOT (KM/S)       YDOT(KM/S)    ZDOT (KM/SEC)\n' )
      self.oscElemFile.write( '     TSINCE (MIN)           A (KM)          ECC (-)        INC (DEG)       NODE (DEG)      OMEGA (DEG)   TRUE ANOM(DEG)\n' )
      self.meanElemFile.write( '     TSINCE (MIN)     N (REVS/DAY)          ECC (-)        INC (DEG)       NODE (DEG)      OMEGA (DEG)         MA (DEG)\n' )
      self.llhElemFile.write( '     TSINCE (MIN)         LAT(DEG)        LON (DEG)          HT (KM)           X (KM)           Y (KM)           Z (KM)\n' )
      self.nodalApPerFile.write( '     TSINCE (MIN)   NODAL PER(MIN)1/NODAL(REVS/DAY)       N(REVS/DY)    ANOM PER(MIN)      APOGEE (KM)      PERIGEE(KM)\n\n' )

   def PropagateSatellite(self, key):
      """Propagates a satellite to the times specified in the TLE.

      The results will be written to the 5 output files.

      Parameters
      key -- The satellite key. this must exist in the currently loaded set of TLE's. It will be wrapped in a c_longlong before it is looked up because of the fact it was converted to a standard Python integer by the TLE iteration loop in run().

      """
      # Print the TLE to all output files
      line1 = create_string_buffer(self.DEFAULT_STRING_LENGTH)
      line2 = create_string_buffer(self.DEFAULT_STRING_LENGTH)
      self.Tle.TleGetLines(c_longlong(key), line1, line2)
      for outFile in self.outFiles:
         outFile.write( '\n\n %s\n %s\n' % (line1.value.rstrip(), line2.value.rstrip()) )

      # Initialize
      if self.Sgp4Prop.Sgp4InitSat(key):
         ShowMsgAndTerminate(self.DllMain)

      # Calculate start/stop time and step size based on this TLE and the 6P card
      pStartFrEpoch = c_int()
      pStopFrEpoch = c_int()
      pStartTime = c_double()
      pStopTime = c_double()
      pStepSize = c_double()
      self.TimeFunc.Get6P(byref(pStartFrEpoch), byref(pStopFrEpoch), byref(pStartTime), byref(pStopTime), byref(pStepSize))
      epochDs50UTCStr = create_string_buffer(self.DEFAULT_STRING_LENGTH)
      self.Tle.TleGetField(key, 4, epochDs50UTCStr)
      epochDs50UTC = self.TimeFunc.DTGToUTC(epochDs50UTCStr)
      if  pStartFrEpoch.value:
         startTime = epochDs50UTC + (pStartTime.value / 1440)
      else:
         startTime = pStartTime.value
      if  pStopFrEpoch.value:
         stopTime = epochDs50UTC + (pStopTime.value / 1440)
      else:
         stopTime = pStopTime.value
      if startTime > stopTime:
         stepSize = -abs(pStepSize.value)
      else:
         stepSize = abs(pStepSize.value)

      # Set up ctypes variables we'll need for the propagation
      ds50UTC = c_double()
      mse = c_double()
      pos = CreateCArray(c_double, [3])
      vel = CreateCArray(c_double, [3])
      llh = CreateCArray(c_double, [3])
      oscElem = CreateCArray(c_double, [6])
      meanElem = CreateCArray(c_double, [6])
      nodalApPer = CreateCArray(c_double, [3])

      # Propagate the satellite over the requested steps
      step = 0
      ds50UTC.value = startTime
      while (stepSize >= 0 and ds50UTC.value < stopTime) or (stepSize < 0 and ds50UTC.value > stopTime):
         # Compute time to which to propagate, adjusting for tolerance
         ds50UTC.value = startTime + (step * stepSize / 1440.0)
         if (stepSize >= 0 and ds50UTC.value + (self.EPSI / 86400) > stopTime) or (stepSize < 0 and ds50UTC.value - (self.EPSI / 86400) < stopTime):
            ds50UTC.value = stopTime

         # Propagate the satellite
         if self.Sgp4Prop.Sgp4PropDs50UTC(c_longlong(key), ds50UTC, byref(mse), pos, vel, llh):
            # Decay condition, print error and move to next satellite
            propErrMsg = create_string_buffer(self.DEFAULT_STRING_LENGTH)
            self.DllMain.GetLastErrMsg(propErrMsg)
            print( propErrMsg.value.rstrip() )
            for outFile in self.outFiles:
               outFile.write( str(propErrMsg.value.rstrip()) + "\n" )
            break # Stop propagating

         # Compute/retrieve other propagator output data
         self.Sgp4Prop.Sgp4GetPropOut(key, self.PROPOUT_OSC_ELEM, oscElem)
         self.Sgp4Prop.Sgp4GetPropOut(key, self.PROPOUT_MEAN_ELEM, meanElem)
         self.Sgp4Prop.Sgp4GetPropOut(key, self.PROPOUT_NODAL_AP_PER, nodalApPer)
         trueAnomaly = self.AstroFunc.CompTrueAnomaly(oscElem)
         meanMotion = self.AstroFunc.AToN(c_double(meanElem[0]))

         # Print information to output files
         self.oscStateFile.write( " %17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f\n" % (mse.value, pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]) )
         self.oscElemFile.write( " %17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f\n" % (mse.value, oscElem[0], oscElem[1], oscElem[2], oscElem[4], oscElem[5], self.AstroFunc.CompTrueAnomaly(oscElem)) )
         self.meanElemFile.write( " %17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f\n" % (mse.value, meanMotion, meanElem[1], meanElem[2], meanElem[4], meanElem[5], meanElem[3]) )
         self.llhElemFile.write( " %17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f\n" % (mse.value, llh[0], llh[1], llh[2], pos[0], pos[1], pos[2]) )
         self.nodalApPerFile.write( " %17.7f%17.7f%17.7f%17.7f%17.7f%17.7f%17.7f\n" % (mse.value, nodalApPer[0], (1440.0 / nodalApPer[0]), meanMotion, (
         1440.0 / meanMotion), nodalApPer[1], nodalApPer[2]) )

         # Check if height is below 100 km, stop propogation if so
         if llh[2] < 100.0:
            # Print an error
            if llh[2] < 0.0:
               for outFile in self.outFiles:
                  outFile.write( "Warning: Decay condition. Distance from the Geoid (Km) = %10.3f\n" % llh[2] )
            else:
               for outFile in self.outFiles:
                  outFile.write( "Warning: Height is low. HT (Km) = %10.3f\n" % llh[2] )
            break # Stop propagating
         step = step + 1

      # Remove the satellite from the propagator since we're finished with it
      if self.Sgp4Prop.Sgp4RemoveSat(key):
         ShowMsgAndTerminate(self.DllMain)

# Standard object oriented start
app = Sgp4Prop()
app.run()
