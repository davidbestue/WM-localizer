# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:01:37 2018

@author: David
"""



import easygui
import pandas as pd
from numpy import shape
import os
from toolz import interleave

                                                                                                            
file_WMloc = easygui.fileopenbox() 
seq = file_WMloc.split('\\')[:-1] 
s='\\'
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

## Duration delay
df['duration_delay'] = df['end_delay_ref'] - df['start_delay_ref']

df['zeros'] = 0
df['ones'] = 1

df_delays = df[[ 'start_delay_ref',  'duration_delay', 'ones']]

#### Add columns for the time in between (2)
a=[]
a.append( 0)
starts_inter_delay = a + list(df['end_delay_ref'].iloc[0:-1] .values)  

durations_inter_delays=[]

for i in range(1, len(df)+1):
    if i ==1:
        dur = df.loc[1, 'start_delay_ref'] 
    else:
        dur = df.loc[i, 'start_delay_ref'] - df.loc[i-1, 'end_delay_ref'] 
    
    durations_inter_delays.append(dur)


#
durations_inter_delays

df['durations_inter'] = durations_inter_delays
df['starts_inter_delay'] = starts_inter_delay


#### Two dataframes
df_delays = df[[ 'start_delay_ref', 'ones', 'duration_delay']]
df_delays.columns=['start', 'index' , 'duration']
df_delays['condition']='delay'

df_inter_delays = df[[ 'starts_inter_delay', 'zeros', 'durations_inter']]
df_inter_delays.columns=['start', 'index' , 'duration']
df_inter_delays['condition']='baseline'

##### Interleave
#concat_df = pd.concat([df_inter_delays, df_delays ]).sort_index().reset_index(drop=True)
#concat_df['intercept'] = 1

#
concat_df = pd.DataFrame(interleave([df_inter_delays.values, df_delays.values]))
concat_df.columns=['start', 'index_c' , 'duration', 'condition']
concat_df['intercept'] = 1


#Matrix = pd.DataFrame(concat_df.values) 
#Matrix= Matrix.round(2)
#Matrix.to_csv('dm_fs.par', header=False, index=False, sep='\t', mode='a')
#
#
#
#
#
#concat_df.values.to_csv('dm_fs.par', header=False, index=False, sep='\t', mode='a')
#
#
#np.savetxt('xgboost.txt', concat_df.values, fmt='%d', delimiter="\t", header="X\tY\tZ\tValue")  


with open('wmmap.par', 'w') as out:
    for i in range(0, shape(concat_df)[0]):
        out.write(str( round(concat_df.loc[i, 'start'], 2)  ) + '\t')
        out.write(str(concat_df.loc[i, 'index_c'] ) + '\t')
        out.write(str( round(concat_df.loc[i, 'duration'], 2)  ) + '\t')
        out.write(str( round(concat_df.loc[i, 'intercept'], 2)  ) + '\t')
        out.write(concat_df.loc[i, 'condition']  + '\n')




#with open('durations.par', 'w') as out:
#    for i in range(1, shape(df_delays)[0]):
#        out.write(str( round(df_delays.loc[i, 'duration'], 2)  ) + '\n')
#        
#        
        








