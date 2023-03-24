# PEST_DSM2
This script package facilitates the calibration of DSM2 Hydro and Qual using PEST (serial proccessing) or BeoPEST (parallel processing)  
using Parameter ESTimation (PEST) 17.3 software.

# 1. Initial Set Up and First Run
## 1.1 Setting up the conda environment

```
conda env create -n pestdsm2 -f environment.yml
```

## 1.2 Clone the repository and data

1. Clone or download this repository onto your local machine.


2. The large data files required for running a PEST run are not committed to this repository due to their large sizes.  
observations and DSM2 timeseries inputs need to be retrieved from our local server and placed into the correct directory.  
   ```
   \Share\DSM2\pestdsm2\data\observations
   \Share\DSM2\pestdsm2\data\timeseries
   ```
   The contents of the above folders should be copied over to their respective folders in the repository.  
   **\observations** contains the historical timeseries data that PEST uses as a target  
   **\timeseries** contains the standard timeseries that a DSM2 run needs.  
   These may be changed depending on the specific configuration of your run. 
# File Structure
```
1├─runPESTsetup.bat
    ├────pestsetup.py


2├─runpest.bat (main batch file to launch PEST)

    ├────pest.exe  <───────────────┐
       iterates:                   │
       ├────rundsm2.bat            │
         ├────prepro.py        [Metrics]
         ├────**dsm2 hydro**       │
         ├────makemetrics.py       │
         ├────formatmetrics.py─────┘
    

|mainconfig.txt| stores the updated parameters
|metrics.dat| stores the metrics to minimize(e.g. rmse, nse)
```

# File Descriptions

**mainconfig.txt**
contains the user-defined directories, configurations and parameters. PEST modifies the parameter values in this file.

**readconfig.py**
parses mainconfig.txt. reads directories, configurations and parameters into python dictionaries for use in python scripts

**pestsetup.py**
generates the PEST control file based on parameters in the mainconfig.txt file. Calls pestgen.exe.

**prepro.py**
parses mainconfig.txt and generates .inp files for DSM2 using pydsm read_input and write_input

**makemetrics.py**
makes metrics csv file using pydsm compare_dss. I/O: (observed dss file, dsm2 output file)/(metrics.csv)

**formatmetrics.py**
makes PEST-readable metrics file for PEST from metrics.csv. I/O: (metrics.csv, parameter type)/(metrics.dat file)

