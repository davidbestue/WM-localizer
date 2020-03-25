# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 15:14:54 2018

@author: David Bestue
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:41:18 2017

@author: David Bestue
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 12:56:14 2016

@author: David
"""

## holaaaaa
#To run this code you have to run in a Terminal  "python WM task.py 'name and session' " Open a terminal and move with cd to the
#path where WM task.py is placed.

#Before that you must have created a file with stimuli by using the file: generator_stim.py 
#Libraries that are needed! Psychopy, easygui, math, numpy, pygaze, pickle, os and pyglet are going to be needed.
from psychopy import visual, core, event, gui
import easygui
from math import cos, sin, radians, sqrt, degrees, asin, acos
from numpy import zeros, vstack, array, savetxt, mean, std, arange
import os
import sys
from pickle import dump
from random import choice
import pyglet
#import pygaze
#from pygaze import libscreen, libtime,  liblog,  libinput, eyetracker, libgazecon, settings                                                   # eyetracker

#Place where you want to save the results (set your path) depending on the computer
#ordenador=os.getcwd()
ordenador='C:\\Users\\torkelslabb\\Desktop\\behaviour\\'

## Name subject and session

if __name__ == "__main__":
    info = {'Subject':'Subject_1'}
    infoDlg = gui.DlgFromDict(dictionary=info, title='WM experiment')
    if infoDlg.OK:
        subject_name=info['Subject']
    if infoDlg.OK==False: core.quit() #user pressed cancel



name=subject_name
#### PRELIMINARY STUFF

#Parameters
presentation_period= 0.35 
presentation_period_cue=  0.50
inter_trial_period= 0.1 
pre_cue_period= 0.5 
pre_stim_period= 0.5 
limit_time=5 
decimals=3 #decimals to round

#size things to change
radius= 8 
size_stim= 1
fix_squares_side=0.30 
fix_squares_sep=0.225 

#separation_between_squares=round(2*(fix_squares_sep-(fix_squares_side/2)), 2)

#colors in rgb code
grey=[0,0,0]
black=[-1,-1,-1]
yellow=[1, 1, 0]


#Screen parameters. This parameters must be ajusted according to your screen features.
screen= [1440, 900]
diagonal= 17.32


width=screen[0]
length=screen[1]

#inches of the screen diagonal (check on All settings --> Displays or internet: http://howbigismyscreen.co/ )
#Has de vigilar segun si es full screen o no... siempre será la diagonal de la screen que aparezca!!!
### screen psycho 22.05 (47.4cm x 29,8 --> 56 cm de diagonal--> 22.05 inches)
pix_per_inch=sqrt(width**2+length**2)/diagonal
pix_per_cm= pix_per_inch /2.54 #2,54 are the inches per cm


#Functions that will be used
def cm2pix(cm):
    return  pix_per_cm * cm  



def circ_dist(a1,a2):
    ## Returns the minimal distance in angles between to angles 
    op1=abs(a2-a1)
    angs=[a1,a2]
    op2=min(angs)+(360-max(angs))
    options=[op1,op2]
    return min(options)


def choicePop(list):
    c=choice(list)
    i=0
    for n in list:
      if n == c: 
        new_list = list[0:i]+list[i+1:]
      i+=1
    return (c,new_list)


#Select the file with the trials (python gen_input_dist.py 'Subject Name') the file 
# is going to be in a folder with the name of the subject.

stims_file = easygui.fileopenbox() #This line opens you a box from where you can select the file with stimuli
stim_input=open(stims_file,'r')
lines=stim_input.readlines()[1:]
stimList = []

#Take the info of the file to create a dictionary with all the trials and its values labeled

for line in lines:
    line = line.split()
    # calculate number of R,Angle pair that we have - minus first 2 columns, Delay and Type
    ttype=line[0] #In the future I will modify the code so it will accept stimuli without distractor    
    delay1=line[1]; delay2=line[2]; orientation=line[3]; order=line[4]; axis_response=line[5]; A_DC=line[6];
    A_DC_dist=line[7]; Q_DC=line[8]; A_DF=line[9]; A_DF_dist=line[10]; Q_DF=line[11]; A_DVF=line[12]; Q_DVF=line[13];
    A_DVF_dist=line[14]; Q_DVF_dist=line[15]; Target=[float(radius), float(line[16])]; quadrant_target=line[17];
    NT1=[float(radius), float(line[18])]; NT2=[float(radius), float(line[19])]; Distractor=[float(radius), float(line[20])];
    quadrant_dist=line[21]; Distractor_NT1=[float(radius), float(line[22])]; Distractor_NT2=[float(radius), float(line[23])];    
    distance_T_dist=float(line[24])
    
    
    stimList.append({'type':float(ttype), 'delay1':float(delay1), 'delay2': float(delay2), 'orientation':float(orientation), 'order':float(order),
                     'axis_response':float(axis_response), 'A_DC': float(A_DC), 'A_DC_dist': float(A_DC_dist), 'Q_DC': float(Q_DC), 
                     'A_DF': float(A_DF), 'A_DF_dist': float(A_DF_dist), 'Q_DF': float(Q_DF), 'A_DVF': float(A_DVF), 'Q_DVF': float(Q_DVF), 
                     'A_DVF_dist': float(A_DVF_dist), 'Q_DVF_dist': float(Q_DVF_dist),  'Target': (Target),  
                     'quadrant_target':float(quadrant_target), 'NT1': (NT1), 'NT2': (NT2), 'Distractor': (Distractor),  
                     'quadrant_dist':float(quadrant_dist),  'Distractor_NT1': (Distractor_NT1), 'Distractor_NT2': (Distractor_NT2), 'distance_T_dist':float(distance_T_dist) }) 

stim_input.close() # Close the stim file
    



#list to append the results
OUTPUT=zeros((len(stimList) + 1 , 35))
RESPONSE_MOVEMENT=[]


##### START OF THE TASK
#Open a psychopy window
win = visual.Window(size=screen, units="pix", fullscr=True, color=grey)
#allow the continuous pressing
key=pyglet.window.key
keyboard = key.KeyStateHandler()
win.winHandle.push_handlers(keyboard)


MOUSE=event.Mouse(win=win, visible=False)
#Fixation squares (four squares together)
fix_squares_sep=cm2pix(fix_squares_sep)
pos_cue=[(fix_squares_sep,fix_squares_sep),(-fix_squares_sep,fix_squares_sep),(-fix_squares_sep, -fix_squares_sep), (fix_squares_sep, -fix_squares_sep)]
fix_squares_side=cm2pix(fix_squares_side)
f1_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(fix_squares_sep,fix_squares_sep), fillColor=black, lineColor=black)
f2_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(-fix_squares_sep,fix_squares_sep), fillColor=black, lineColor=black)
f3_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(-fix_squares_sep,-fix_squares_sep), fillColor=black, lineColor=black)
f4_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(fix_squares_sep,-fix_squares_sep), fillColor=black, lineColor=black)

#circle
circ = visual.Circle(win=win, units="pix", radius=cm2pix(radius), edges=180, pos=(0,0), fillColor=grey, lineColor=black)


def FIX():
    circ.draw()
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw()



TIME = core.Clock()
TIME.reset()

while not event.getKeys('space'):
    win.flip()
else:
    event.getKeys()
    win.flip()


ref_time=TIME.getTime()
ref_time=round(ref_time, decimals)
OUTPUT[-1, :]=ref_time


for i in range(0,len(stimList)):
    #### loop scape
    #take a new trial everytime and restore the features of fixation  
    movement=[]
    trial=stimList[i]    
    fixation=[f1_black,f2_black,f3_black,f4_black]
    #take the relevant info from the trial (Target=T, Non-Targuet=NT, Distractor=Dist)
    angle_target=trial['Target'][1]
    angle_NT1=trial['NT1'][1]
    angle_NT2=trial['NT2'][1]
    angle_Dist=trial['Distractor'][1]
    angle_NT1_Dist=trial['Distractor_NT1'][1]
    angle_NT2_Dist=trial['Distractor_NT2'][1]
    
    delay1=trial['delay1']
    delay2=trial['delay2']
    
    distance_T_dist=trial['distance_T_dist']
    ttype=trial['type']
    
    #Convert the (cm, degrees) to (x_cm. y_cm) and change it to pixels with the function cm2pix. We round everything up to three decimals
    X_T=round(cm2pix(radius*cos(radians(angle_target))), decimals)
    Y_T=round(cm2pix(radius*sin(radians(angle_target))), decimals)
    X_NT1=round(cm2pix(radius*cos(radians(angle_NT1))), decimals)
    Y_NT1=round(cm2pix(radius*sin(radians(angle_NT1))), decimals)
    X_NT2=round(cm2pix(radius*cos(radians(angle_NT2))), decimals)
    Y_NT2=round(cm2pix(radius*sin(radians(angle_NT2))), decimals)
    X_Dist=round(cm2pix(radius*cos(radians(angle_Dist))), decimals)
    Y_Dist=round(cm2pix(radius*sin(radians(angle_Dist))), decimals)
    X_NT1_Dist=round(cm2pix(radius*cos(radians(angle_NT1_Dist))), decimals)
    Y_NT1_Dist=round(cm2pix(radius*sin(radians(angle_NT1_Dist))), decimals)
    X_NT2_Dist=round(cm2pix(radius*cos(radians(angle_NT2_Dist))), decimals)
    Y_NT2_Dist=round(cm2pix(radius*sin(radians(angle_NT2_Dist))), decimals)
    
    #order (1 or 2) and quadrant
    order=trial['order']
    quadrant=trial['quadrant_target']
    axis_response=trial['axis_response']
    horiz_vertical=trial['axis_response']
    
    ############# Start the display of the task
    #############################
    ############################# ITI Inter-trial-interval
    #############################
    win.flip()
    core.wait(inter_trial_period)
    display_time = core.Clock()
    display_time.reset()
    
    #Draw the components of the fixation square and the circle
    FIX()
    win.flip() 
    
    #############################
    ############################# Pre cue period (between fixation and presentation of the cue)
    #############################    
    core.wait(float(pre_cue_period))
    
    ############################# #CUE PERIOD (commend this for the WM gratting scroll)
    #############################    
    if order!=2: #==1 or ==0 (controls)
        presentation_dist_time=0 
        presentation_att_cue_time= TIME.getTime()
        presentation_att_cue_time=round(presentation_att_cue_time, decimals)
        CUE=visual.TextStim(win=win, text='1', pos=[0,0], color=[1,1,1], units='pix', height=50)        
        CUE.draw()
        #FIX()
        win.flip() 
        core.wait(float(presentation_period_cue))
    elif order==2:
        presentation_att_cue_time= TIME.getTime()
        presentation_att_cue_time=round(presentation_att_cue_time, decimals)
        CUE=visual.TextStim(win=win, text='2', pos=[0,0], color=[1,1,1], units='pix', height=50)        
        CUE.draw()
        #FIX()
        win.flip() 
        core.wait(float(presentation_period_cue)) 
    
    #############################
    ############################# Pre stim period (between fixation and presentation of the target)
    #############################
    FIX() 
    win.flip()     
    core.wait(float(pre_stim_period))
    
    
    #############################
    ############################# PRESENTATION PERIOD (presnetation of the Targuet and the NT)
    #############################       
    if order!=2: #==1 or ==0 (controls)
        FIX()        
        
        target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))  
        #NT1=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1, Y_NT1)) 
        #NT2=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2, Y_NT2)) 
        
        target.draw()
        #NT1.draw()
        #NT2.draw()
        
        win.flip() 
        presentation_target_time= TIME.getTime() #start of the trial unitil presentation
        presentation_target_time=round(presentation_target_time, decimals)
        core.wait(float(presentation_period))
    elif order==2:
        FIX()
        
        Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))  
        #NT1_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1_Dist, Y_NT1_Dist))  
        #NT2_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2_Dist, Y_NT2_Dist))  
        
        Distractor.draw() 
        #NT1_Distractor.draw()
        #NT2_Distractor.draw()
        
        win.flip()
        presentation_dist_time= TIME.getTime()
        presentation_dist_time=round(presentation_dist_time, decimals)
        core.wait(float(presentation_period))  
    
    #############################
    ############################# DELAY 1
    ############################# 
    FIX()
    win.flip()
    core.wait(float(delay1))
    
    #DISTRACTOR PERIOD (presentation of Distractor or not)
    if order==2:
        FIX()
        
        target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))  
        #NT1=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1, Y_NT1)) 
        #NT2=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2, Y_NT2)) 
        
        target.draw()
        #NT1.draw()
        #NT2.draw()
        
        win.flip() 
        presentation_target_time= TIME.getTime() #start of the trial unitil presentation
        presentation_target_time=round(presentation_target_time, decimals)
        core.wait(float(presentation_period))
        
    elif order==1:
        FIX()
        
        Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_Dist, Y_Dist))  
        #NT1_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT1_Dist, Y_NT1_Dist))  
        #NT2_Distractor= visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_NT2_Dist, Y_NT2_Dist))  
        
        Distractor.draw() 
        #NT1_Distractor.draw()
        #NT2_Distractor.draw()
        
        win.flip()
        presentation_dist_time= TIME.getTime()
        presentation_dist_time=round(presentation_dist_time, decimals)
        core.wait(float(presentation_period))
    
    
    #############################
    ############################# DELAY 2
    ############################# 
    FIX()
    win.flip()
    core.wait(float(delay2))
    
    #############################
    ############################# RESPONSE
    ############################# 
    disp_time=display_time.getTime() #from fixation until presentation of the probe (it is gonna be constant)
    disp_time=round(disp_time, decimals)
    
    #############################################################################
    #decide where appears the yellow bar    
    target=angle_target
    if quadrant==1:
        if axis_response==0:
            initial_angle=90
        else:
            initial_angle=0
    if quadrant==2:
        if axis_response==0:
            initial_angle=90
        else:
            initial_angle=180
    if quadrant==3:
        if axis_response==0:
            initial_angle=270
        else:
            initial_angle=180
    if quadrant==4:
        if axis_response==0:
            initial_angle=270
        else:
            initial_angle=0  
    
    
    #initial_angle=choicePop(list(arange(0,359,1)))[0]             
    x_initial=round(cm2pix(radius*cos(radians(initial_angle))), decimals)
    y_initial=round(cm2pix(radius*sin(radians(initial_angle))), decimals)
    
    CURSOR=visual.Line(win, start=(0, 0), end=(x_initial, y_initial), lineColor=yellow)
    circ.draw()
    fixation[int(quadrant)-1] = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=pos_cue[int(quadrant)-1], fillColor=yellow, lineColor=black)
    fixation[0].draw()
    fixation[1].draw()
    fixation[2].draw()
    fixation[3].draw()
    CURSOR.draw()
    win.flip()
    
    presentation_probe_time= TIME.getTime() #start of the trial unitil presentation of the probe (starts when you can move)
    presentation_probe_time=round(presentation_probe_time, decimals)
    
    Reaction_time = core.Clock()
    Reaction_time.reset()   
    ###########################################################################
    ###########################################################################
    
    angle=initial_angle
    movement.append(angle)
    time_of_response=Reaction_time.getTime()
    #######
    #######
    ####### When using the mouse
    #######
    myMouse = event.Mouse(visible=False,win=win)
    mouse_click = myMouse.getPressed()        
    ####### 
    while time_of_response<limit_time:
        
        
        #scape loop
        if keyboard[key.E]:
            win.close()
        
        
        #######
        
        if mouse_click[0]: #keyboard[key.A]:
            mov_ang=1
        elif mouse_click[2]: #keyboard[key.L]:
            mov_ang=-1
        else:
            mov_ang=0
        
        angle=angle+mov_ang #2
        if angle<0:
            angle=360+angle
        if angle>360:
            angle=angle-360
        #print angle
        movement.append(angle)
        x_mouse=round(cm2pix(radius*cos(radians(angle))), decimals)
        y_mouse=round(cm2pix(radius*sin(radians(angle))), decimals)
        CURSOR=visual.Line(win, start=(0, 0), end=(x_mouse, y_mouse), lineColor=yellow)
        circ.draw()
        fixation[0].draw()
        fixation[1].draw()
        fixation[2].draw()
        fixation[3].draw()
        CURSOR.draw()
        time_of_response=Reaction_time.getTime()
        win.flip()
    else:
        response_time= display_time.getTime() #response_time: after fixation until time when you respond
        response_time=round(response_time, decimals)
        R_T=Reaction_time.getTime()
        R_T=round(R_T, decimals)
        trial_time= TIME.getTime()
        trial_time=round(trial_time, decimals)
        A_response=angle
        
        FIX()
        win.flip()
    
    
    ################################################################################
    #################################################################################
    #################################################################################      
    
    #Features of the trial
    distance_T_dist=trial['distance_T_dist']
    cue=trial['quadrant_target'] 
    orient=trial['orientation'] #-1 is ccw, 1 is cw
    order=trial['order']
    
    
    #Errors (Target - Response) 
    Abs_angle_error=round(circ_dist(A_response, trial['Target'][1]), decimals)
    A_err=round(trial['Target'][1]-A_response, decimals)
    
    if A_err < -180:
	A_err=round(trial['Target'][1] + 360 -A_response, decimals)
    if A_err > 180:
	A_err=round(trial['Target'][1] - (A_response + 360), decimals)
    
    #Error_interference; positive for attractionand negative for repulsion
    if circ_dist(A_response, trial['Distractor'][1])<=circ_dist(trial['Target'][1], trial['Distractor'][1]):
        Error_interference=Abs_angle_error 
    else:
        Error_interference=-Abs_angle_error 
    
    
    #Append each trial 
    RESPONSE_MOVEMENT.append(movement)
    OUTPUT[i,:]=[trial['type'], trial['delay1'], trial['delay2'], trial['Target'][1], 0, 0, trial['Distractor'][1], 0, 0,
           distance_T_dist, cue, order, orient, horiz_vertical, A_response, A_err, Abs_angle_error, Error_interference, trial['A_DC'], trial['A_DC_dist'], trial['Q_DC'], trial['A_DF'], 
           trial['A_DF_dist'], trial['Q_DF'], trial['A_DVF'], trial['Q_DVF'], trial['A_DVF_dist'],  trial['Q_DVF_dist'], presentation_att_cue_time,
           presentation_target_time, presentation_dist_time, presentation_probe_time, R_T, trial_time,  disp_time] 
    
    
    index_columns=array(['type', 'delay1', 'delay2', 'T', 'NT1', 'NT2', 'Dist', 'Dist_NT1', 'Dist_NT2', 'distance_T_dist', 'cue', 'order',
                     'orient', 'horiz_vertical', 'A_R', 'A_err', 'Abs_angle_error', 'Error_interference', 'A_DC', 'A_DC_dist', 'Q_DC', 'A_DF',
                     'A_DF_dist', 'Q_DF', 'A_DVF', 'Q_DVF', 'A_DVF_dist', 'Q_DVF_dist', 'presentation_att_cue_time', 
                     'presentation_target_time', 'presentation_dist_time', 'presentation_probe_time', 'R_T', 'trial_time',  'disp_time']) 
    
    BEHAVIOR=vstack((index_columns, OUTPUT))
	#savetxt(ordenador + str(name) + '_beh_'+'.txt' ,  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
    #savetxt(str(name)+'_beh_'+'.txt',  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
         
    






Final_text=visual.TextStim(win=win, text='Thank you!', pos=[-3,0], color=[1,1,1], units='pix', height=100)        
Final_text.draw()
win.flip()
core.wait(2)
win.flip()
win.close()



#cw means that is the closest to the next 12 o'clock. when distracting the target, if it is a cw trial, the traget is going to be nearer the next 12 o'clock
#and the same with the NT, when distracting a NT, the NT is going to be nearer the next 12 0'clock. Between target and NT, in a cw trial the target is going to 
#be nearer the next 12 o'clock




##Save the file
index_columns=array(['type', 'delay1', 'delay2', 'T', 'NT1', 'NT2', 'Dist', 'Dist_NT1', 'Dist_NT2', 'distance_T_dist', 'cue', 'order',
                 'orient', 'horiz_vertical', 'A_R', 'A_err', 'Abs_angle_error', 'Error_interference', 'A_DC', 'A_DC_dist', 'Q_DC', 'A_DF',
                 'A_DF_dist', 'Q_DF', 'A_DVF', 'Q_DVF', 'A_DVF_dist', 'Q_DVF_dist', 'presentation_att_cue_time', 
                 'presentation_target_time', 'presentation_dist_time', 'presentation_probe_time', 'R_T', 'trial_time',  'disp_time']) 


BEHAVIOR=vstack((index_columns, OUTPUT))


#Save a txt for the behavior and a pikle for movements inside a folder with the name

os.makedirs(ordenador + str(name)+ '_WM_L1_task')
new_directory= ordenador + str(name) + '_WM_L1_task\\' 
os.chdir(new_directory)
savetxt(new_directory + str(name) + '_beh_'+'.txt' ,  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
dump( RESPONSE_MOVEMENT, open( str(name)+'_movements_'+'.p', 'wb' ) )


#current_directory=os.getcwd()
#os.makedirs(name+ '_WM_task')

#
#new_directory= str(current_directory)+'/'+str(name) + '_WM_task'
#os.chdir(new_directory)

#savetxt(str(name)+'_beh_'+'.txt',  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
#dump( RESPONSE_MOVEMENT, open( str(name)+'_movements_'+'.p', 'wb' ) )




#pickle.load( open( "namefile.p", "rb" ) )




