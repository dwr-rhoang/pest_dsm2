# PEST_DSM2
This script package facilitates the calibration of DSM2 Hydro and Qual using PEST (serial proccessing) or BeoPEST (parallel processing)  
using Parameter ESTimation (PEST) 17.3 software.  
As committed, this repository is ready to run (after following the steps outlined in Section 1)

# 1. Initial Set Up and First Run
This section describes how to run the example PEST DSM2, as committed in this repository. The example  
run is set up to calibrate a single channel group and only runs for one month; it is for demonstration  
purposes only to ensure that the set up runs on your computer.
## 1.1 Setting up the conda environment

```
conda env create -n pestdsm2 -f environment.yml
```

## 1.2 Clone the repository and data

1. Clone or download this repository onto your local machine.


2. The data files (dss format) required for running a PEST run are not committed to this repository due to their large sizes.  
Observations and DSM2 timeseries inputs need to be retrieved from our local server and placed into the correct directory.  
   ```
   \Share\DSM2\pestdsm2\data\observations
   \Share\DSM2\pestdsm2\data\timeseries
   ```
   The contents of the above folders should be copied over to their respective folders in the repository.  

   > **\observations** contains the historical timeseries data that PEST uses as a target  
   > **\timeseries** contains the standard timeseries that a DSM2 run needs.  

   These may be changed depending on the specific configuration of your run. 

## 1.3 Launching the run

```
start_pest.bat
```
# 2. Workflows for Modifying the PEST Parameters

## 2.1 Modifying channel groups
In its current form, this PEST DSM2 package is configured to calibrate channel groups, not individual channels. Channel groups are defined in the file *chngrp_8_3.csv*. Each channel group represents a grouping  of similar channels that share similar characteristics. Note: the channel groupings are not  resolute - they were established to facilitate the manual calibration process. Changing of the channel  groups (e.g. disaggregating them further) may be necessary, depending on calibration goals. If a single manning's n is not appropriate for all of the channels within a channel group, the group may be disaggregated to provide more flexibility.  

1. To change the channel group modify the *mainconfig.txt* file.  
   
   In the repo example, only channel group 24 is calibrated:

   ```
   START CHANNELGROUPS
   24    {0.0250,0.0250}
   END CHANNELGROUPS
   ```

   To add another channel group, add another entry between START_CHANNELGROUPS and END CHANNEL GROUPS as follows:

   ```
   START CHANNELGROUPS
   24    {0.0250,0.0250}
   25    {0.0250,0.0250}
   END CHANNELGROUPS
   ```
   > The syntax is as follows: CH_GRP_NUMBER      {PLACEHOLDER_VAL, INITIAL_VAL}  
   > where, PLACEHOLDER_VAL is an arbitrary number and INITIAL_VAL is the initial parameter value at which PEST starts the calibration (best available knowledge should be used as INITIAL_VAL)

   The code block above will tell PEST to calibrate both channel groups 24 and 25 (the file *chngrp_8_3.csv* shows which DSM2 channels are included in a given channel group)

2. Recompile the .pst file by running ``` python pestsetup.py```  
   > IMPORTANT: Any time that the *mainconfig.txt* file is changed, the .pst file needs to be recompiled by    running ``` python pestsetup.py```. pestsetupy.py is responsible for parsing the *mainconfig.txt* file and translating those configurations into the .pst file that PEST can recognize.


## 2.2 Modifying observations


# 3. Accessing results




# 4. File Structure
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

# 5. File Descriptions

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

