#!/usr/bin/python
"""
   Purpose:
      This program shows how a Python program can call the Astrodynamic Standard using every data type.

      The program is simplified to show only the core functionalities of the involved DLLs. 
      File I/O and other output statements are intentionally not included for this purpose.

"""
import sys
#import time
from ctypes import *
from scripts.DriverExamples.TestInterfaces.src.AstroUtils import *
from wrappers.DllMainWrapper import *

class TestInterfaces(object):
   # Global variables used to store the dll objects
   # We place them here so that all of our functions will have access to them, although they're initially set to None
   DllMain = None
   
   def run(self):
      """The main function of the program.

      All of the main operations of the program are done from here; the program sets up global data, then calls this function. We do it this way to make reading the code easier, and in order to facilitate unit testing.

      """

      # Load and initialize dll's
      self.DllMain = LoadDllMainDll()

      print("")
      print("TestInterface")
      cIn  = b"Z"
      intIn = c_int(42)
      longIn = c_longlong(42)
      realIn = c_double(3.14)
      strIn = b"Hello World!"
      int1DIn = (c_int * 3)(1, 2, 3)
      long1DIn = (c_longlong * 3)(1, 2, 3)
      real1DIn = (c_double * 3)(1.0, 2.0, 3.0)
      int2DIn = (c_int * 3 * 2)((1, 2, 3),(4, 5, 6))
      long2DIn = (c_longlong * 3 * 2)((1, 2, 3),(4, 5, 6))
      real2DIn = (c_double * 3 * 2)((1, 2, 3),(4, 5, 6))
      
      cOut = create_string_buffer(1)
      intOut = c_int()
      longOut =  c_longlong()
      realOut =  c_double()
      strOut = create_string_buffer(512)
      int1DOut = CreateCArray(c_int, [3])
      long1DOut = CreateCArray(c_longlong, [3])
      real1DOut = CreateCArray(c_double, [3])
      int2DOut = CreateCArray(c_int, [2,3])
      long2DOut = CreateCArray(c_longlong, [2,3])
      real2DOut = CreateCArray(c_double, [2,3])
      self.DllMain.TestInterface(cIn, cOut, intIn, byref(intOut), longIn, byref(longOut), realIn, byref(realOut) , strIn, strOut, int1DIn, int1DOut, long1DIn, long1DOut, real1DIn, real1DOut, int2DIn, int2DOut, long2DIn, long2DOut, real2DIn, real2DOut)

      print(cOut.value.rstrip())
      print(intOut.value)
      print(longOut.value)
      print(realOut.value)
      print(strOut.value.rstrip())
      print(int1DOut[0], int1DOut[1], int1DOut[2])
      print(long1DOut[0], long1DOut[1], long1DOut[2])
      print(real1DOut[0], real1DOut[1], real1DOut[2])
      print(int2DOut[0][0], int2DOut[0][1], int2DOut[0][2])
      print(int2DOut[1][0], int2DOut[1][1], int2DOut[1][2])
      print(long2DOut[0][0], long2DOut[0][1], long2DOut[0][2])
      print(long2DOut[1][0], long2DOut[1][1], long2DOut[1][2])
      print(real2DOut[0][0], real2DOut[0][1], real2DOut[0][2])
      print(real2DOut[1][0], real2DOut[1][1], real2DOut[1][2])
      

      print("")
      print("TestInterface2")
      cInOut = create_string_buffer(512)
      cInOut[0]  = b"Z"
      intInOut = c_int(42)
      longInOut = c_longlong(42)
      realInOut = c_double(3.14)
      strInOut = create_string_buffer(512)
      strInOut[:12] = b"Hello World!"
      int1DInOut = (c_int * 3)(1, 2, 3)
      long1DInOut = (c_longlong * 3)(1, 2, 3)
      real1DInOut = (c_double * 3)(1.0, 2.0, 3.0)
      int2DInOut = (c_int * 3 * 2)((1, 2, 3),(4, 5, 6))
      long2DInOut = (c_longlong * 3 * 2)((1, 2, 3),(4, 5, 6))
      real2DInOut = (c_double * 3 * 2)((1, 2, 3),(4, 5, 6))
      
      self.DllMain.TestInterface2(cInOut, byref(intInOut), byref(longInOut), byref(realInOut) , strInOut, int1DInOut, long1DInOut, real1DInOut, int2DInOut, long2DInOut, real2DInOut)

      print(cInOut.value.rstrip())
      print(intInOut.value)
      print(longInOut.value)
      print(realInOut.value)
      print(strInOut.value.rstrip())
      print(int1DInOut[0], int1DInOut[1], int1DInOut[2])
      print(long1DInOut[0], long1DInOut[1], long1DInOut[2])
      print(real1DInOut[0], real1DInOut[1], real1DInOut[2])
      print(int2DInOut[0][0], int2DInOut[0][1], int2DInOut[0][2])
      print(int2DInOut[1][0], int2DInOut[1][1], int2DInOut[1][2])
      print(long2DInOut[0][0], long2DInOut[0][1], long2DInOut[0][2])
      print(long2DInOut[1][0], long2DInOut[1][1], long2DInOut[1][2])
      print(real2DInOut[0][0], real2DInOut[0][1], real2DInOut[0][2])
      print(real2DInOut[1][0], real2DInOut[1][1], real2DInOut[1][2])


      print("")
      print("TestInterface3")
      length1D = 3
      length2D = 2
      unk1DIn = (c_int * length1D)(1, 2, 3)
      unk2DIn = (c_int * 3 * length2D)((1, 2, 3),(4, 5, 6))

      unk1DOut = CreateCArray(c_int, [length1D])
      unk2DOut = CreateCArray(c_int, [length2D, 3])
      
      self.DllMain.TestInterface3(unk1DIn, unk1DOut, unk2DIn, unk2DOut)

      print(unk1DOut[0], unk1DOut[1], unk1DOut[2])
      print(unk2DOut[0][0], unk2DOut[0][1], unk2DOut[0][2])
      print(unk2DOut[1][0], unk2DOut[1][1], unk2DOut[1][2])
      
      # Test Global Variables
      print("")
      print("Show Named Constant")
      print(BADSATKEY)
# Standard object oriented start
app = TestInterfaces()
app.run()
