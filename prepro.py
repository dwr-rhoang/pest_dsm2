'''
prepro.py
parses mainconfig.txt and generates .inp files for DSM2 using pydsm read/write input
rHoang 20220107
'''
import shutil, os, glob
import numpy as np
import pandas as pd
from pydsm.input import read_input,write_input
from readconfig import dirs, obsgroups, configs, chan_dict, get_obs

dsm2_start_date = configs['dsm2_tw'].split('-')[0].strip()
dsm2_end_date = configs['dsm2_tw'].split('-')[1].strip()
dsm2_config_file = dirs['dsm2configfile']
chan_grp_df = pd.read_csv(dirs['changroupfile'])
calib_coef = configs['calib_var']

# function to parse config file and return a dictionary of channels and parameter values.
def getParamChs (ParamList): # Make a dictionary to store parameter channel - mannings N pairs, parsed from config file
    dict = {}
    for parameter in ParamList:
      coeftype = str(parameter.split(",")[0])
      r1 = int(parameter.split(",")[1])
      r2 = int(parameter.split(",")[2])
      val = float(parameter.split(",")[3])
      obsstn = str(parameter.split(",")[4])
      channelList = np.arange(r1,r2+1,1)

      for channel in range(len(channelList)):
        dict[channelList[channel]] = val

    return (dict)

def getParamVal (ParamList): # returns a list of observation stations
    val = []
    for parameter in ParamList:
      val.append(str(parameter.split(",")[3]))
    return (val)

def modDSM2Config(dsm2_config_file,param,paramval):
  #make a copy of the config file
  shutil.copyfile(dsm2_config_file, "temp.txt")
  rf = open("temp.txt",'r')
  lines = rf.readlines()
  wf = open(dsm2_config_file,'w')
  for line in lines:
    if line != '\n' and line.split()[0] == param:
      wf.write(param+'               '+paramval+'\n')
      continue
    wf.write(line)
  rf.close()
  os.remove("temp.txt")
  wf.close()
  return

tables=read_input(dirs["channeltabletemplate"])
chs = (tables['CHANNEL'])

# Modify the Channel table with the values from the dictionary
for channel in chan_dict.keys():
    chs.loc[chs.CHAN_NO == channel, calib_coef] = chan_dict[channel][calib_coef]

# Write new output
fname_out=dirs["channeltable"]
write_input(fname_out,tables, append = False)

modDSM2Config(dsm2_config_file,"START_DATE",dsm2_start_date)
modDSM2Config(dsm2_config_file,"END_DATE",dsm2_end_date)
print("Transferred parameters from mainconfig.txt to .inp file")

if __name__ == "__main__":
  # Delete DSM2 output files prior to run
  dsm2outputdir = dirs['dsm2outputdir']
  filelist = glob.glob(os.path.join(dsm2outputdir, "*"))
  for f in filelist:
      os.remove(f)
  print("Deleted DSM2 output from previous iteration")