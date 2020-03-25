# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:03:04 2017

@author: David Bestue
"""



## Libraries

from psychopy import visual, core, event, gui
import easygui
from math import cos, sin, radians, sqrt, degrees, asin, acos
from numpy import zeros, vstack, array, savetxt, mean, std, arange, shape, reshape, concatenate, loadtxt
import os
import sys
from pickle import dump
from random import choice
import random
import pyglet


ordenador='C:\\Users\\torkelslabb\\Desktop\\behaviour\\'


#name

if __name__ == "__main__":
    info = {'Subject':'Subject_1'}
    infoDlg = gui.DlgFromDict(dictionary=info, title='vs WM mapping fMRI')
    if infoDlg.OK:
        subject_name=info['Subject']
    if infoDlg.OK==False: core.quit() #user pressed cancel



name=subject_name



#Parameters 
#####################
#####################

#feature parameters
#radius=8 
radius = 16
r_small=13
r_big= 19  #10
size_stim= 2 
fix_squares_side=0.30 # 0.4 #0.2 #cm
fix_squares_sep=0.225 # 0.3 #0.2 #cm of the center --> separation between squares= 2* (fix_squares_sep-(fix_squares_side/2))
separation_between_squares=round(2*(fix_squares_sep-(fix_squares_side/2)), 2)
decimals=3

#colors
grey=[0,0,0]
black=[-1,-1,-1]
blue=[1,1,-1]
red=[1,-1,-1]
green=[-1,1,-1]

#time parameters
presentation_period= 0.5 
limit_time=2
delay=3 
Hz=6
fliker_time=float(1.0)/Hz
delay_checkerboard=13
delay_period=3
#inter_trial_period=2
ITImin = 2
ITImax = 3

#screen parametres
#screen= [1600, 900]
#diagonal= 17.32

screen= [1440, 900]
#diagonal= 17.32
diagonal = 29.1



#functions
#####################
#####################
width=screen[0]
length=screen[1]
pix_per_inch=sqrt(width**2+length**2)/diagonal
pix_per_cm= pix_per_inch /2.54 #2,54 are the inches per cm


def rad_checkboard(a1, a2):
    color_gr=[ round(choice(arange(-1,1, 0.1)), 2), round(choice(arange(-1,1, 0.1)), 2), round(choice(arange(-1,1, 0.1)), 2)] 
    #color_gr=random.choice([red, green, black, blue])
    #color_gr=black
    #color_gr=blue
    stim_vertical1=visual.RadialStim(win, units="pix", pos=(0.0, 0.0), ori=90, size=(cm2pix(r_big) * 2, cm2pix(r_big) * 2), radialCycles=12, angularCycles=11,   visibleWedge=(a1, a2), color=color_gr, colorSpace='rgb')
    stim_vertical2=visual.RadialStim(win, units="pix", pos=(0.0, 0.0), ori=90, size=(cm2pix(r_small) * 2, cm2pix(r_small) * 2), radialCycles=12, angularCycles=11,  visibleWedge=(a1, a2), color=grey, colorSpace='rgb')
    stim_vertical1.draw()
    stim_vertical2.draw()
    


def FIXATION():
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw()




def get_quadrant(angle): 
    #angle in degrees, return the quadrant which it belongs to
    if angle>=0 and angle<=90:
        Q=1
    elif angle>90 and angle<=180:
        Q=2
    elif angle>180 and angle<=270:
        Q=3
    elif angle>270 and angle<=360:
        Q=4
    
    return Q





def cm2pix(cm):
    return  pix_per_cm * cm  




################################################
#####            Get the stims from a file
################################################
stims_file = easygui.fileopenbox() #This line opens you a box from where you can select the file with stimuli
stim_input=open(stims_file,'r')
#stims_input=loadtxt(stims_file)

lines=stim_input.readlines()[1:]
stimList = []

for line in lines:
    line = line.split()
    # calculate number of R,Angle pair that we have - minus first 2 columns, Delay and Type
    T1=line[0] #In the future I will modify the code so it will accept stimuli without distractor    
    T2=line[1]
    P1=line[2]
    P2=line[3]
    up_down1=line[4]
    up_down2=line[5]
    stimList.append([float(T1), float(T2), float(P1), float(P2), float(up_down1), float(up_down2)])




##### window
win = visual.Window(size=screen, units="pix", fullscr=True, color=grey)
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




##### START OF THE TASK
#stimList=stimList[:2]


#OUTPUT=zeros(2*(len(stimList)+1, 16))
OUTPUT=[]

index_columns=array(['first_second', 'radius', 'angle_t1', 'angle_t2', 'angle_p1', 'angle_p2', 'correct_direction',
                     'Response', 'C_I_M', 'start_trial', 'presentation_checkboard_time', 'presentation_target_time',
                     'start_delay', 'end_delay',  'presentation_probe_time', 'response_time']) 
#####################
#####################
#####################



TIME = core.Clock()
TIME.reset()

print TIME.getTime()

while not event.getKeys('space'):
    win.flip()
else:
    event.getKeys()
    win.flip()


ref_time=TIME.getTime()
ref_time=round(ref_time, decimals)
print ref_time



ref_time_array=[ref_time for i in range(0,len(index_columns))]
OUTPUT.append(ref_time_array)
#OUTPUT[0, :]=ref_time_array



for i in range(0,len(stimList)):
    #take a new trial everytime and restore the features of fixation  
    trial=stimList[i]    
    #trial=stims_input[i]
    
    fixation=[f1_black,f2_black,f3_black,f4_black]
    
    #take the relevant info from the trial (Target=T, Non-Targuet=NT, Distractor=Dist)
    angle_T1=trial[0]
    angle_P1=trial[2]
    
    angle_T2=trial[1]
    angle_P2=trial[3]
    
    up_down=[trial[4], trial[5]]
    
    #Convert the (cm, degrees) to (x_cm. y_cm) and change it to pixels with the function cm2pix. We round everything up to three decimals
    X=[]
    Y=[]
    for COND in [angle_T1, angle_T2, angle_P1,  angle_P2]:
        X.append(round(cm2pix(radius*cos(radians(COND))), decimals))
        Y.append(round(cm2pix(radius*sin(radians(COND))), decimals) )
    
    
    ############# Start the display of the task
    #############################
    ############################# ITI Inter-trial-interval
    #############################
    FIXATION()
    win.flip()
    inter_trial_period=round(random.uniform( ITImin, ITImax),2)
    core.wait(inter_trial_period)
    
    # Start the display of elements
    #############################  
    ############################# PRESENTATION CHECKERBOARD
    #############################       
    a1, a2= [[269, 360], [179, 271], [89,181], [0, 91]][get_quadrant(angle_T1)-1]
    
    start_trial= TIME.getTime()
    start_trial=round(start_trial, decimals)
    presentation_checkerboard_time= TIME.getTime() #start of the trial unitil presentation
    presentation_checkerboard_time=round(presentation_checkerboard_time, decimals)
    duration_checkerboard=TIME.getTime()
    #Parameters
    Frames_sec_screen = 60
    Hz_stim=4
    
    myMouse = event.Mouse(visible=False,win=win)
    mouse_click = myMouse.getPressed()
    Response1=0
    Response2=0
    presentation_target1_time =0
    presentation_target2_time =0
    start_delay1=0
    start_delay2=0
    end_delay1=0
    end_delay2=0
    presentation_probe1_time=0
    presentation_probe2_time=0
    response1_time = 0
    response2_time = 0
    
    ST1=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X[0], Y[0]))
    ST2=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X[1], Y[1]))
    
    SP1=visual.PatchStim(win, mask='circle', color= green, tex=None, size=cm2pix(size_stim), pos=(X[2], Y[2]))
    SP2=visual.PatchStim(win, mask='circle', color= green, tex=None, size=cm2pix(size_stim), pos=(X[3], Y[3]))
    
    ### SHifts
    start_shift = inter_trial_period=round(random.uniform( 0.1, 0.5),2)
    r1_shift = inter_trial_period=round(random.uniform( 1, 3),2)
    r2_shift = inter_trial_period=round(random.uniform( 1, 2),2)
    
    
    while duration_checkerboard< presentation_checkerboard_time+ delay_checkerboard:
        for Hz in range(0, Hz_stim):
            for frM in range(Frames_sec_screen/(Hz_stim*2)):
                
                #   
                rad_checkboard(a1, a2)
                
                if duration_checkerboard>presentation_checkerboard_time + (start_shift) and duration_checkerboard<presentation_checkerboard_time + (0.5+start_shift) :
                    presentation_target1_time = round(TIME.getTime(),decimals) if presentation_target1_time == 0 else presentation_target1_time
                    #rad_checkboard(a1, a2)
                    ST1.draw()
                    start_delay1=round(TIME.getTime(),decimals)
                
                
                elif duration_checkerboard>presentation_checkerboard_time + (3.5+start_shift) and duration_checkerboard<presentation_checkerboard_time + (4+start_shift) :
                    end_delay1 = round(TIME.getTime(),decimals) if end_delay1 == 0 else end_delay1
                    presentation_probe1_time = round(TIME.getTime(),decimals) if presentation_probe1_time == 0 else presentation_probe1_time
                    mouse_click = myMouse.getPressed()
                    #rad_checkboard(a1, a2)
                    SP1.draw()
                    
                elif duration_checkerboard>presentation_checkerboard_time + (4+start_shift) and duration_checkerboard<presentation_checkerboard_time + (4+start_shift+r1_shift) :
                    if mouse_click[0]: #keyboard[key.A]:
                        response1_time = round(TIME.getTime(),decimals) if response1_time == 0 else response1_time
                        Response1=1
                        mouse_click = myMouse.getPressed()
                        
                    if mouse_click[2]: #keyboard[key.A]:
                        response1_time = round(TIME.getTime(),decimals) if response1_time == 0 else response1_time
                        Response1=-1
                        mouse_click = myMouse.getPressed()
                
                
                elif duration_checkerboard>presentation_checkerboard_time + (4+start_shift+r1_shift) and duration_checkerboard<presentation_checkerboard_time + (4.5+start_shift+r1_shift) :
                    presentation_target2_time = round(TIME.getTime(),decimals) if presentation_target2_time == 0 else presentation_target2_time
                    #rad_checkboard(a1, a2)
                    ST2.draw()
                    start_delay2=round(TIME.getTime(),decimals)
                
                
                elif duration_checkerboard>presentation_checkerboard_time + (7.5+start_shift+r1_shift) and duration_checkerboard<presentation_checkerboard_time + (8+start_shift+r1_shift) :
                    end_delay2 = round(TIME.getTime(),decimals) if end_delay2 == 0 else end_delay2
                    presentation_probe2_time = round(TIME.getTime(),decimals) if presentation_probe2_time == 0 else presentation_probe2_time
                    mouse_click = myMouse.getPressed()
                    #rad_checkboard(a1, a2)
                    SP2.draw()    
                
                
                elif duration_checkerboard>presentation_checkerboard_time + (8+start_shift+r1_shift) and duration_checkerboard<presentation_checkerboard_time + (8+start_shift+r1_shift+r2_shift) :
                    if mouse_click[0]: #keyboard[key.A]:
                        response2_time = round(TIME.getTime(),decimals) if response2_time == 0 else response2_time
                        Response2=1
                        mouse_click = myMouse.getPressed()
                        #print 1
                    if mouse_click[2]: #keyboard[key.A]:
                        response2_time = round(TIME.getTime(),decimals) if response2_time == 0 else response2_time
                        Response2=-1
                        mouse_click = myMouse.getPressed()
                        
                
                #
                
                FIXATION()
                win.flip()
                duration_checkerboard= round(TIME.getTime(),decimals) 
                          
            for frM in range(Frames_sec_screen/(Hz_stim*2)):
                if duration_checkerboard>presentation_checkerboard_time + (start_shift) and duration_checkerboard<presentation_checkerboard_time + (0.5+start_shift) :
                    ST1.draw()  
                
                if duration_checkerboard>presentation_checkerboard_time + (3.5+start_shift) and duration_checkerboard<presentation_checkerboard_time + (4+start_shift) :
                    SP1.draw()  
                
                if duration_checkerboard>presentation_checkerboard_time + (4+start_shift+r1_shift) and duration_checkerboard<presentation_checkerboard_time + (4.5+start_shift+r1_shift) :
                    ST2.draw()
                
                
                if duration_checkerboard>presentation_checkerboard_time + (7.5+start_shift+r1_shift) and duration_checkerboard<presentation_checkerboard_time + (8+start_shift+r1_shift) :
                    SP2.draw()
                
                #
                FIXATION()
                win.flip()  
                duration_checkerboard= round(TIME.getTime(),decimals)
    
    
    else:
        FIXATION()
        win.flip()
    
    
    
    
    ############################# 
    print Response1, Response2
    Responses=[Response1, Response2]
    C_I_Ms=[]
    correct_directions=up_down
    for tr_in in range(0,2):
        correct_direction=up_down[tr_in]
    #correct-incorrect
        if Responses[tr_in]==0:
            C_I_M=999 #Miss
        else:
            if correct_direction==Responses[tr_in]:
                C_I_M=0 #correct
            else:
                C_I_M=1 #incorrect
        
        C_I_Ms.append(C_I_M)
    
    
    #Features of the trial
    OUTPUT.append([1, radius, angle_T1, angle_T2, angle_P1, angle_P2, correct_directions[0], Response1, C_I_Ms[0],
                   start_trial, presentation_checkerboard_time, presentation_target1_time, start_delay1, end_delay1,
                   presentation_probe1_time, response1_time])
    
    
    OUTPUT.append([2, radius, angle_T1, angle_T2, angle_P1, angle_P2,  correct_directions[1], Response2, C_I_Ms[1],
                   start_trial, presentation_checkerboard_time, presentation_target2_time, start_delay2, end_delay2,
                   presentation_probe2_time, response2_time])
    
    
    BEHAVIOR=vstack((index_columns, OUTPUT))
    savetxt(ordenador + str(name) + '_beh_map_'+'.txt' ,  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
    
#
        
        



Final_text=visual.TextStim(win=win, text='Thank you!', pos=[-3,0], color=[1,1,1], units='pix', height=100)        
Final_text.draw()
win.flip()
core.wait(2)
win.flip()
win.close()



###Save the file



#ref_time list of

BEHAVIOR=vstack((index_columns, OUTPUT))
#
#
###Save a txt for the behavior and a pikle for movements inside a folder with the name
#current_directory=os.getcwd()
##os.chdir(str(current_directory)+'/behaviour')
#
#os.makedirs(name+ '_WM_mapping')
#current_directory=os.getcwd()
##
#new_directory= str(current_directory)+'/'+str(name) + '_WM_mapping'
#os.chdir(new_directory)
##
#savetxt(str(name)+'_beh_'+'.txt',  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
####



os.makedirs(ordenador + str(name)+ '_WM_mapping')
new_directory= ordenador + str(name) + '_WM_mapping\\' 
os.chdir(new_directory)
savetxt(new_directory + str(name) + '_beh_map_'+'.txt' ,  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))



