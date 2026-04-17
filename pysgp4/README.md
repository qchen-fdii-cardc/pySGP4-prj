# General
- This package contains examples of using the **Astrodynamics Standards (AS)** libraries in Python

## Preparing to Run:
- Suggest adding the directory to your Python interpreter in your PATH environment variable, so
  you can run from anywhere.
 
## Notes:
- Drivers and Wrappers support versions 2.x and 3.x of the Python interepreter, even though they
  are not compatible with each other.  So you should be able to run the driver examples regardless
  of what version of Python you are using.
- Look at the source code for the driver examples and notice the order of all the LoadXXX(libpath)
  commands.  You will need to follow this example to load all the dependent libraries.
- If using Conda, you may need to ensure the Astro Standards libraries are ahead of the Conda
  PATH changes.  To do so, you may need to use a script (e.g.. edit runExample.bat) to ensure the
  PATH is set after the conda.bat scrpt is run.
