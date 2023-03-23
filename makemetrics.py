'''
makemetrics.py
makes metrics file by comparing observed and modeled outputs
rHoang 20220107
'''
import shutil, os, glob
from datetime import datetime
import pyhecdss
import pandas as pd
import numpy as np
from pydsm.functions import tsmath
from pydsm import lockutil
from pydsm import postpro
from readconfig import dirs, configs, obsgroups, changroups, get_obs, get_kind
from prepro import getParamVal, getParamChs
from pydelmod import calibplot

dssfile = dirs['dsm2outputfile']
vartypes = ('FLOW','STAGE','EC')
vartypes = (['EC'])
locationfile_dict = {'FLOW':dirs['calibration_stations_flow'],
                     'STAGE':dirs['calibration_stations_stage'],
                     'EC':dirs['calibration_stations_ec'],}
units_dict = {'FLOW':'cfs','STAGE':'feet','EC':'US/CM'}
study_name = 'output'


timewindow = configs['pest_tw']
obs_study=postpro.Study('Observed',dirs['obsfile'])
model_studies=postpro.Study('Modeled',dirs['dsm2outputfile'])
studies = [obs_study,model_studies]


def postprocess(dssfile, locationfile_dict, vartypes, units_dict, study_name):
  for vartype in vartypes:
    processors = postpro.build_processors(dssfile, locationfile_dict[vartype], vartype, units_dict[vartype], study_name)
    for p in processors:
      postpro.run_processor(p)

def buildmetricsdf(studies,vartypes,units_dict,locationfile_dict,timewindow):
    metrics_df = pd.DataFrame()
    for vartype in vartypes:
        vt = postpro.VarType(vartype,units_dict[vartype])
        dfloc = postpro.load_location_file(locationfile_dict[vartype])
        locations=[postpro.Location(r['Name'],r['BPart'],r['Description'],
                                    r['time_window_exclusion_list'],r['threshold_value'])\
                                    for i,r in dfloc.iterrows()]
        #print(locations)
        for location in locations:
            print(location.name)
            all_data_found, pp = calibplot.load_data_for_plotting(studies, location, vt, timewindow)
            dfdisplayed_metrics, metrics_table = calibplot.build_metrics_table(studies, pp, location, vt, tidal_template=True)
            dfdisplayed_metrics['variable'] = str(location.name.upper() + '/' + vt.name)
            metrics_df = metrics_df.append(dfdisplayed_metrics)
            print(metrics_df)
    metrics_df = metrics_df.rename({'R Squared':'rsquared',
                                    'N Mean Error':'nmean_err',
                                    'Amp Avg %Err':'amp_err',
                                    'NMSE':'nmse',
                                    'NRMSE':'nrmse',
                                    'NSE':'nse',
                                    'PBIAS':'pbias',     
                                    'RSR':'rsr',                                                                        
                                    'Avg Phase Err':'phase_err'}, axis=1)
    metrics_df.to_csv('metrics.csv')

# Check to see if an output dss file exists
# If does not exist due to run failure, then pass -1 to metrics to tell PEST to recourse (?)
runcomplete = False
filelist = glob.glob(os.path.join(dirs['dsm2outputdir'], "*"))
for f in filelist:
      if f == dirs['dsm2outputfile']:
          runcomplete = True
          break
      else: runcomplete = False

dfloc = postpro.load_location_file(locationfile_dict['FLOW'])
print(dfloc)
#locations=[postpro.Location(r['Name'],r['BPart'],r['Description']) for i,r in dfloc.iterrows()]
#print(locations)
if runcomplete == True:
    print("***********Post-Process DSS File***********")
    lockutil.do_with_lock(postprocess,lockfile='my.func.lock', timeout=10, check_interval=5)\
        (dssfile, locationfile_dict, vartypes, units_dict, study_name)
    print("***********Build Metrics Dataframe***********")
    lockutil.do_with_lock(buildmetricsdf,lockfile='my.func.lock', timeout=10, check_interval=5)\
        (studies,vartypes,units_dict,locationfile_dict,timewindow)
    buildmetricsdf(studies,vartypes,units_dict,locationfile_dict,timewindow)
    print("***********Write metrics .csv file***********")
    metrics_df = pd.read_csv('metrics.csv')
#print(metrics_df)
obs_list = get_obs(list(obsgroups.values()))
kind_list = get_kind(list(obsgroups.values()))
param_vals = getParamVal(list(obsgroups.values()))

# Write metrics
print("***********Write metrics .dat file***********")
wf = open(dirs['metricsdatfile'], 'w')
wf.write(
    "variable name" +
    "        metric_value                         metric_type \n")
for i, obs in enumerate(obs_list):
    metric_name = ("%s/%s") % (obs.split('-')[0].upper(), kind_list[i].upper())
    print('Writing ' + obs)
    colname = obs.split('-')[1]
    if runcomplete == True:
        metric_val = float(metrics_df.loc[metrics_df.variable == metric_name, colname])
    if runcomplete == False:
        metric_val = -100
    if pd.isna(metric_val):
        metric_val = 0
    else:
        metric_val = metric_val
    wf.write(
        metric_name +
        "        " +
        format(metric_val,'.12f') +
        "                        " +
        colname +
        "\n")
wf.close()

shutil.copy(dirs['metricsdatfile'],"metrics_copy.dat")

print("***********Write log file***********")
if runcomplete == True:
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H:%M:%S")
    metrics_df['date_time'] = dt_string
    appendfrom = open(dirs['metricsdatfile'], 'r')
    appendto = open(dirs["logfile"], 'a+')
    appendto.write('\n')
    appendto.write(str(changroups))
    appendto.write('\n')
    appendto.write(metrics_df.to_string(header=True, index=False))
if runcomplete == False:
    now = datetime.now()
    appendto = open(dirs["logfile"], 'a+')
    appendto.write('\n')
    appendto.write(str(changroups))
    appendto.write('\n')
    appendto.write("DSM2 model failed at %s" %now)

print('all done')