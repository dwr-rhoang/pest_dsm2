ptf @
# Main config file for the PEST-DSM2 run
# rhoang 20220111
# - readconfig.py parses this config file and reads the variables and values to dictionaries
# - PEST modifies this file only - it does not change any of the DSM2-read .inp files
#
START DIRECTORY
configfile                          {mainconfig.txt}                                        # this file
dsm2                                {DSM2Model}                                             # directory of the DSM2 model folder
channeltable                        {DSM2Model\channel_std_delta_grid.inp}                  # channel table to modify
obsfile                             {observations\ec_merged.dss}                      # historical observation file
obsfile_pp                          {observations\ec_merged_calib_postpro.dss}        # post-processed historical observation file
dsm2outputfile                      {DSM2Model\output\calib.dss}                   # dsm2 output file to compare against observation file
dsm2outputfile_pp                   {DSM2Model\output\calib_calib_postpro.dss}     # post-processed dsm2 output file to compare against observation file
dsm2outputdir                       {DSM2Model\output}                                      # dsm2 output file to compare against observation file
channeltabletemplate                {channel_std_delta_grid_TEMPLATE.inp}                   # template file for channel table. script makes copy of this
metricscsvfile                      {metrics.txt}                                           # raw output from pydsm.compare-dss
metricsdatfile                      {metrics.dat}                                           # formatted metrics from metrics.txt (simpler for PEST to read)
metricsinsfile                      {metrics.ins}                                           # instruction file for PEST to read metrics
metricstgtfile                      {metrics_target.obf}                                    # file to designate the target to set the metric (e.g. 1 for nse, and 0 for mse)
paramsinitfile                      {DSM2_820_init.par}                                     # initial conditions for parameters
templatefile                        {mainconfig.tpl}                                        # template of this file
dsm2configfile                      {DSM2Model\config.inp}                                  # dsm2 config file
pest_pstfile                        {dsm2_820.pst}                                          # pest control file
logfile                             {log.txt}                                               # log file to output parameters and metrics
changroupfile                       {chngrp_8_3.csv}                                        # channel group file
observationmaskfile                 {observationmask.csv}                                   # metricmaskfile
calibration_stations_flow           {location_info\calibration_flow_stations.csv}           # flow station locations for post pro
calibration_stations_stage          {location_info\calibration_stage_stations.csv}          # stage station locations for post pro
calibration_stations_ec             {location_info\calibration_ec_stations.csv}             # ec station locations for post pro
END DIRECTORY
#
#
#
START CONFIGS
pest_tw                             {01OCT2010 - 01NOV2011}                     # PEST time window 01OCT2009 - 30SEP2011 | 01SEP2013 0000 - 30SEP2013 0000
dsm2_tw                             {01SEP2010 - 01NOV2011}                     # DSM2 time window (changes DSM2 config file) 01SEP2009 - 30SEP2011 | 01SEP2011 - 30SEP2013
param_initval                       {0.0250}                                    # initial parameter value for the parameter
param_low_bound                     {0.0100}                                      # parameter lower bound
param_up_bound                      {0.0450}                                      # parameter upper bound
noptmax                             {100}                                       # max number of optimization runs
calib_var                           {MANNING}                                   # Calibration coefficient
END CONFIGS
#
#
#
START CHANNELGROUPS
24    {@    24    @,0.0250}
END CHANNELGROUPS
#
START OBSERVATIONS
{cll,flow,nrmse,1}
{anc,flow,nrmse,1}
{emm,flow,nrmse,1}
{jer,flow,nrmse,1}
{tsl,flow,nrmse,1}
{dsj,flow,nrmse,1}
END OBSERVATIONS
#
#
#
START OBSERVATIONMASK
END OBSERVATIONMASK
