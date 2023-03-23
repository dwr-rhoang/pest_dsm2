# PEST_DSM2
DSM2 calibration package using Parameter ESTimation (PEST) 17.3. 
environment: pydelmod

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

