'''
readconfig.py 
parses mainconfig.txt. reads directories, configurations and parameters into python dictionaries for use in python scripts
rHoang 20220107
'''
import os, sys, re
import csv
import pandas as pd
from pydsm.input import read_input,write_input

this_dir = os.path.dirname(__file__)

#calib_coef = 'DISPERSION'
calib_coef = 'MANNING'

# returns a list of station-metric-kind. each station-metric-kind pair represents one PEST observation
def get_obs (paramlist):    
    obsstn = []
    for parameter in paramlist:
      obsstn.append(str(parameter.split(",")[0]+'-'+parameter.split(",")[2]+'-'+parameter.split(",")[1]))
    return (obsstn)

# returns a list of observation weights
def get_weight (paramlist):    
    weight = []
    for parameter in paramlist:
      weight.append(parameter.split(",")[3])
    return (weight)

# returns a list of observation kind (flow, stage)
def get_kind (paramlist): 
    kind = []
    for parameter in paramlist:
      kind.append(parameter.split(",")[1])
    return (kind)

# Read Config and make dictionary
configs = {}
dirs = {}
obsgroups = {}
changroups = {}
metricmask = {}
lines = filter(None, open(os.path.join(this_dir,"mainconfig.txt"), "r").read().splitlines())
read = False
input_type = None
for line in lines:
    li=line.strip()
    if not li.startswith('#'):
        if line.split()[0] == "END":
            read = False
        if read and input_type == "CONFIGS":
            configs[line.split()[0]] = re.search('{(.*)}',line).group(1)
        if read and input_type == "OBSERVATIONS":
            obsgroups[line.split()[0]] = re.search('{(.*)}',line).group(1)
        if read and input_type == "CHANNELGROUPS":
            changroups[int(line.split()[0])] = re.search('{(.*)}',line).group(1)
        if read and input_type == "OBSERVATIONMASK":
            metricmask[line.split()[0]] = re.search('{(.*)}',line).group(1)
        if read and input_type == "DIRECTORY":
            dirs[line.split()[0]] = os.path.join(this_dir,re.search('{(.*)}',line).group(1))
        if line.split()[0] == "START":
            input_type = line.split()[1]
            read = True
chan_dict = {}
group_dict={}
chan_grp_df = pd.read_csv(dirs['changroupfile'])

# Read in a TEMPLATE .inp file to a dataframe
fname_template=dirs["channeltabletemplate"]
tables=read_input(fname_template)

# Channel table dataframe
chs = (tables['CHANNEL'])

# Dictionary with {group_id:{channel, mannings}}
for group_id in chan_grp_df['group_id']:
    if group_id in changroups:
        coef = changroups[group_id]
        group_dict[group_id] = {'channel_id': chan_grp_df.loc[chan_grp_df['group_id']==group_id,'channel_id'].to_list(),
                                calib_coef:coef}
    else:
        continue

# Dictionary with {chan_no:{manning, group_id}}
for channel_id in chan_grp_df['channel_id']:
    group_id = int(chan_grp_df.loc[chan_grp_df['channel_id'] == channel_id,'group_id'])
    if group_id in group_dict:    # if channel ID is associated with a PEST-modified group ID, then use it
        coef = group_dict[group_id][calib_coef].split(',')[0]
    else:    # otherwise, use the value in the template file
        coef = float(chs.loc[chs['CHAN_NO']==channel_id,calib_coef])
    
    chan_dict[channel_id] = {calib_coef:coef,
                             'group_id':int(chan_grp_df.loc[chan_grp_df['channel_id'] == channel_id,'group_id'])}

print ("Parse mainconfig.txt complete")