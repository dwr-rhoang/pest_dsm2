# PEST_DSM2
This script package facilitates the calibration of DSM2 Hydro and Qual using PEST (serial proccessing) or BeoPEST (parallel processing)  
using Parameter ESTimation (PEST) 17.3 software.  
As committed, this repository is ready to run (after following the steps outlined in Section 1)

# 1. Initial Set Up and First Run
This section describes how to run the example PEST DSM2, as committed in this repository. The example  
run is set up to calibrate a single channel group and only runs for one month; it is for demonstration  
purposes only to ensure that the set up runs on your computer. This runs PEST using a single core.
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
   > where,  
   > * PLACEHOLDER_VAL can be an arbitrary number. This is the number that PEST will modify for each iteration. At the end of the run, the final results will be stored here.
   > * INITIAL_VAL is the initial parameter value at which PEST starts the calibration (best available knowledge should be used as INITIAL_VAL)

   The code block above will tell PEST to calibrate both channel groups 24 and 25 (the file *chngrp_8_3.csv* shows which DSM2 channels are included in a given channel group)

2. Recompile the .pst file by running ``` python pestsetup.py```  
   > ⚠ IMPORTANT: Any time that the *mainconfig.txt* file is changed, the .pst file needs to be recompiled by    running ``` python pestsetup.py```. pestsetupy.py is responsible for parsing the *mainconfig.txt* file and translating those configurations into the .pst file that PEST can recognize.

3. The run with the added channel group can now be launched.
   ```
   start_pest.bat
   ```

## 2.2 Modifying observations
PEST compares the outcomes of each DSM2 iterations with observed historical data from the **\observations** directory. PEST optimizes the manning's n of the channel group (section 2.1) to minimize the difference between the observed data and DSM2 timeseries of the same name.

1. To add an observation point, modify the *mainconfig.txt* file.  

   In the repo example, the following observation points are compared with their respective DSM2 outputs:

   ```
   START OBSERVATIONS
   {cll,flow,nrmse,1}
   {anc,flow,nrmse,1}
   {emm,flow,nrmse,1}
   END OBSERVATIONS
   ```
   To instruct PEST to optimize manning's n by also minimizing error at Jersey Point (jer), modify the file as follows: 
   ```
   START OBSERVATIONS
   {cll,flow,nrmse,1}
   {anc,flow,nrmse,1}
   {emm,flow,nrmse,1}
   {jer,flow,nrmse,1}
   END OBSERVATIONS
   ```
   > The syntax is as follows: {STN_NAME, VAR_KIND, METRIC_KIND, WEIGHT}  
   > where,  
   > * STN_NAME is the variable name (choose from the available stations from the .dss files in **\observations**). A timeseries output from DSM2 with the same name must also exist (check \DSM2Model\output_calib.inp)  
   > * VAR_KIND is the kind of variable to compare. Choose from: ``` flow, ec ```.
   > * METRIC_KIND is the metric to minimize (or maximize, if r <sup>2</sup>, or nse). Choose from: ``` rsquared, nmean_err, amp_err, nmse, nrms, nse, pbias, rsr, phase_err```
   > * WEIGHT is the relative weight to put on each observation. The absolute value of the number is not important, weights are relative. Lower the weights of the stations that are known to not perform well in DSM2, or have low data reliability. Increase the weights of key compliance locations.  

2. Recompile the .pst file by running ``` python pestsetup.py```  
   > ⚠ IMPORTANT: Any time that the *mainconfig.txt* file is changed, the .pst file needs to be recompiled by    running ``` python pestsetup.py```. pestsetupy.py is responsible for parsing the *mainconfig.txt* file and translating those configurations into the .pst file that PEST can recognize.

3. The run with the added observation can now be launched.
   ```
   start_pest.bat
   ```
# 3. Changing the simulation period
To change the simulation period, modify the *mainconfig.txt* file.  
Change ``` pest_tw ``` and ``` dsm2_tw ```.  
``` dsm2_tw ``` configures the DSM2 simulation period (i.e. it modifies the DSM2 configuration file) and should start a month earlier than ``` pest_tw ```, to allow for warm up.
```
START CONFIGS
pest_tw                             {01OCT2010 - 01NOV2011}
dsm2_tw                             {01SEP2010 - 01NOV2011}
.
.
.
END CONFIGS
```
# 4. Changing the upper and lower bounds for parameter adjustment
In the *mainconfig.txt* file, ``` param_low_bound ``` and ``` param_up_bound ``` dictate the allowable range of the  upper and lower bounds of the parameters. These bounds are applied to all the channel groups being adjusted; currently, the bounds of the individual channel groups cannot be adjusted.

```
START CONFIGS
.
.
.
param_low_bound                     {0.0100}
param_up_bound                      {0.0450}
.
.
.
END CONFIGS
```
> IMPORTANT: Make sure to change the upper and lower bound of the parameters when switching between HYDRO and QUAL calibrations.

# 4. Accessing results
The results from a completed PEST run are stored in *mainconfig.txt*. The PLACEHOLDER_VAL will be replaced with PEST-calculated manning's n resulting from the PEST calibration.

# 5. Key File Descriptions

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


