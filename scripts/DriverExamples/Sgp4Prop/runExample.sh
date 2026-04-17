#!/bin/bash

# This script runs the Sgp4Prop example.
# Note: the bit size of the python executable must match the bit size 
# of the Astro Standards libraries.
# Arguments to this script:
# $1 - Path to the python executable

PY_EXE=$1

# Check if PY_EXE was set.  No need to check for "python"
# because the executable could be named differently.
if [[ "$PY_EXE" == "" ]]; then
    echo Please pass the path to the python executable
    echo "For example: runExample <python exe> <DLL directory>"
    exit 1
else
    if [[ ! -f "$PY_EXE" ]]; then
        echo "Python executable does not exist: $PY_EXE".
        echo "For example: runExample <python exe> <DLL directory>"
        exit 1
    fi
fi

$PY_EXE -c "import struct,sys;print(sys.argv[1] + ' is ' + str(8 * struct.calcsize('P')) + ' bit ')"

$PY_EXE -c "import struct,sys;sys.exit(0 if struct.calcsize('P')==8 else 1)"
if [[ $? -ne 0 ]]; then
	echo "ERROR: 32-bit Python detected.  Please use 64 bit"
	exit 1
fi

# Check if LD_LIBRARY_PATH environment variable was set.
if [[ "$LD_LIBRARY_PATH" == "" ]]; then
    echo Please ensure LD_LIBRARY_PATH environment variable is set to your Astrodynamics Standards libraries 
	echo For example export LD_LIBRARY_PATH=../../Linux64/
    exit 1
fi

# copy wrapper code to the src directory for this example.
echo Copying over the wrapper code.
mkdir -p src/wrappers
cp -r ../../wrappers/* src/wrappers

touch src/wrappers/__init__.py

if [[ ! -d "output" ]]; then
    mkdir output
fi

echo Running example
"$PY_EXE" src/Sgp4Prop.py input/rel14.inp output
