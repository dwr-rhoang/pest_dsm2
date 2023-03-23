''' 
pestsetup.py
PEST preparation script
Generates the PEST control file based on parameters in the mainconfig.txt file
rHoang 20220107
'''
import sys,os
import re
import pandas
import pyhecdss
from pyemu import Pst
from pydsm.input import read_input,write_input
from readconfig import dirs, configs, obsgroups, changroups
from readconfig import get_obs, get_weight

this_dir = os.path.dirname(__file__)                                        # Dir of this file

# Define vars
configfile = dirs['configfile']
templatefile = dirs['templatefile']
PEST_pstfile = dirs['pest_pstfile']
PESTStudy = PEST_pstfile.split('.')[0]
metricsinsfile = dirs['metricsinsfile']
tpl_files = 'mainconfig.tpl' #dirs['templatefile']
in_files = 'mainconfig.txt'    #dirs['configfile']
ins_files = 'metrics.ins'    #dirs['metricsinsfile']
out_files = 'metrics.dat'    #dirs['metricsdatfile']
param_list = list(changroups.keys())
obs_list = get_obs(list(obsgroups.values()))
obs_weights = get_weight(list(obsgroups.values()))
ws = "    "

# Define Functions    
def escape_regex(path):
    return path.replace("+","\+")
    
def extract_from_dss(dssfile,loc,type,tw): 
    ts = list(pyhecdss.get_ts(dssfile,'//%s/%s/%s///'%(loc,type,tw)))[0]
    return ts 

def create_instruction_file(configfile,instructionfile):
    print ("Write instruction file")
    wf = open(instructionfile,'w')
    wf.write("pif @\n")
    wf.write("l1\n")
    for stn in obs_list:
      wf.write('l1 [%s]16:36\n' %(stn))
    return

def create_template_file(configfile,templatefile,changroups):
    print ("Write template file from config file")
    lines = open(configfile).readlines()
    wf = open(templatefile,'w')
    wf.write("ptf @\n")
    input_type = None
    for line in lines:
        if line.split()[0] == "END":
          input_type = None
        if input_type == "CHANNELGROUPS":
          chan_group = line.split()[0]
          val_list = (re.search('{(.*)}',line.split()[1]).group(1)).split(',')
          manning = str(val_list[0])
          init_val = changroups[int(chan_group)].split(',')[1]
          wf.write(chan_group + ws + '{@' + ws + chan_group + ws +'@,'+init_val+'}'+'\n')
        if input_type != "CHANNELGROUPS":
          wf.write(line)
        if line.split()[0] == "START":
          input_type = line.split()[1]
    wf.close()
    return

def write_pst(pst_f):
    ''' write model section to pst
    '''
    print ("Add model in contrl pst")
    tmplt = 'pst_template'
    if os.path.exists(tmplt):os.remove(tmplt)
    os.rename(pst_f,tmplt)
    fr=open(tmplt,"r")
    fw=open(pst_f,"w")
    for line in fr:
      if line=='* model command line\n':
        fw.write(line)
        fr.readline()
        fw.write('runDSM2.bat\n')
      else:
        fw.write(line)

    fr.close()
    fw.close()
    os.remove(tmplt)


create_template_file(configfile,templatefile,changroups)
create_instruction_file(configfile,metricsinsfile)

pst = Pst.from_io_files(tpl_files,in_files,ins_files,out_files)
# Modify control data
pst.control_data.pestmode = "estimation"
pst.control_data.noptmax = configs["noptmax"]
pst.control_data.relparstp = 0.0001
#pst.control_data.lamforgive = "lamforgive"

# Modify parameter group settings
# PARGPNME INCTYP DERINC DERINCLB FORCEN DERINCMUL DERMTHD [SPLITTHRESH SPLITRELDIFF SPLITACTION]
pst.parameter_groups.loc[:,"forcen"] = "always_3"

# Modify parameter data 
# PARNME PARTRANS PARCHGLIM PARVAL1 PARLBND PARUBND PARGP SCALE OFFSET DERCOM
for i, param in enumerate(param_list):
  pst.parameter_data.loc[str(param),"partrans"] = "none"
  pst.parameter_data.loc[str(param),"parchglim"] = "relative"
  pst.parameter_data.loc[str(param),"parval1"] = changroups[param].split(',')[1] #configs["param_initval"]
  pst.parameter_data.loc[str(param),"parlbnd"] = float(configs['param_low_bound'])
  pst.parameter_data.loc[str(param),"parubnd"] = float(configs['param_up_bound'])
  
# Modify observation data
# OBSNME OBSVAL WEIGHT OBGNME
for i, obs in enumerate(obs_list):
    if obs.split('-')[1] == "nse" or obs.split('-')[1] == "rsquared":
        metrictgt = 1
    else:
        metrictgt = 0
    if obs.split('-')[2] == "flow":
      obsgrp_name = "flowobsgrp"
    elif obs.split('-')[2] == "stage":
      obsgrp_name = "stageobsgrp"
    elif obs.split('-')[2] == "ec":
      obsgrp_name = "ecobsgrp"


    pst.observation_data.loc[obs,"obsval"] = metrictgt
    pst.observation_data.loc[obs,"weight"] = float(obs_weights[i])
    pst.observation_data.loc[obs,"obgnme"] = obsgrp_name

# Write PEST control file
pst.write(PESTStudy+".pst")

# Modify command line
write_pst(os.path.join(this_dir,PESTStudy+".pst")) # Modify control file to replace generic template input/output file name (e.g. "model")