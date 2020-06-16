
import easygui
import pandas as pd
from numpy import shape
import os
from toolz import interleave
import numpy as np

                                                                                                            
file_WMloc = easygui.fileopenbox() 
seq = file_WMloc.split('/')[:-1] 
s='/'
path = s.join(seq) 
os.chdir(path)

df = pd.read_csv(file_WMloc, sep=" ") 


df =df[['first_second', 'radius', 'angle_t1', 'angle_t2', 'angle_p1', 'angle_p2', 'correct_direction', 'Response', 'C_I_M', 'start_trial', 
   'presentation_checkboard_time', 'presentation_target_time', 'start_delay',  'end_delay', 'presentation_probe_time', 'response_time' ]]



ref_time = df.iloc[0,0]
df = df.iloc[1:, :] 


#Start and end of the delay
df['start_delay_ref']= df['start_delay'] -ref_time
df['end_delay_ref'] = df['end_delay'] -ref_time
df['resp_time_ref'] = df['response_time'] -ref_time
df['checkboard_time_ref'] = df['presentation_checkboard_time'] -ref_time
df['target_pres_ref'] = df['presentation_target_time'] -ref_time
df['probe_pres_ref'] = df['presentation_probe_time'] -ref_time
df['stim_pres_duration'] = df['start_delay_ref'] - df['target_pres_ref']



## target presentation
df_target_pres = df.copy()
df_target_pres['time']=df['target_pres_ref']
#df_target_pres['condition']='target'

def get_q(df):
    quadrants=[]
    for i in range(len(df)):
        v = df.angle_t1.iloc[i]
        if v<90:
            q='target_q1'
        if v>90:
            if v<180:
                q='target_q2'
            elif v<270:
                q='target_q3'
            else:
                q='target_q4'
        ##
        quadrants.append(q)
    return quadrants


df_target_pres['condition']= get_q(df_target_pres)

#start delay
df_start_delay = df.copy()
df_start_delay['time']=df['start_delay_ref']
df_start_delay['condition']='delay'

#probe
df_probe = df.copy()
df_probe['time']=df['probe_pres_ref']
df_probe['condition']='probe'


#### baseline
responses = df[['presentation_probe_time', 'response_time']]
resp=[]
for i in range(len(responses)):
    if responses.response_time.iloc[i]==0:
        resp.append(responses.presentation_probe_time.iloc[i]+0.1)
    else:
        resp.append(responses.response_time.iloc[i])

#
baseline=pd.DataFrame(resp)
baseline.columns=['time']
baseline['time']= baseline['time'] - ref_time
b_ = np.roll(baseline.time.values, 1)
b_[0]=0
baseline['time']= b_
baseline['condition']= ['baseline', 'baselinech']*int(len(baseline)/2)


##Checkerboard
df_chek = pd.DataFrame(df.checkboard_time_ref.unique())
df_chek.columns=['time']
df_chek['condition']='checkerboard'


all_df = pd.concat([df_target_pres, df_start_delay, df_probe, baseline, df_chek])
all_df=all_df[['time', 'condition']]

all_df = all_df.sort_values('time')


times_1 = np.roll(all_df['time'].values, -1)
times_1[-1] = all_df['time'].iloc[-1] + 0.1
durations = times_1 - all_df['time'] 
all_df['duration'] =durations

all_df['intercept']=1
all_df['index_c'] = all_df.condition.values
all_df['index_c'] = all_df['index_c'].replace(['baseline', 'baselinech', 'checkerboard', 'target_q1', 'target_q2',
'target_q3', 'target_q4', 'delay', 'probe'], [1, 2, 3, 4, 5, 6, 7, 8, 9])


all_df = all_df.reset_index()

with open('wmmap4.par', 'w') as out:
    for i in range(0, shape(all_df)[0]):
        out.write(str( round(all_df.loc[i, 'time'], 2)  ) + '\t');
        out.write(str(all_df.loc[i, 'index_c'] ) + '\t');
        out.write(str( round(all_df.loc[i, 'duration'], 2)  ) + '\t');
        out.write(str( round(all_df.loc[i, 'intercept'], 2)  ) + '\t');
        out.write(str(all_df.loc[i, 'condition'])  + '\n');


