# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 12:56:14 2016

@author: David
"""

#take off the circles and checkerboard

#To run this code you have to run in a Terminal  "python WM task.py 'name and session' " Open a terminal and move with cd to the
#path where WM task.py is placed.

#Before that you must have created a file with stimuli by using the file: generator_stim.py 

#Libraries that are needed! Psychopy, easygui, math, numpy, pygaze, pickle, os and pyglet are going to be needed.
from psychopy import visual, core, event, gui
import easygui
from math import cos, sin, radians, sqrt, degrees, asin, acos
from numpy import zeros, vstack, array, savetxt, mean, std, arange, shape, load
import os
import sys
from pickle import dump
from random import choice
import random
import pyglet


#Place where you want to save the results (set your path) depending on the computer
orde='C:\\Users\\torkelslabb\\Desktop\\David\\fMRI_tasks\\'
orde='/home/david/Desktop'

os.chdir(orde)

pos_channels=list(load('position_channels.npy'))

#ordenador=os.getcwd()
ordenador='C:\\Users\\torkelslabb\\Desktop\\behaviour\\'



if __name__ == "__main__":
    info = {'Subject':'name'}
    infoDlg = gui.DlgFromDict(dictionary=info, title='Encoding mapping fMRI')
    if infoDlg.OK:
        subject_name=info['Subject']
    if infoDlg.OK==False: core.quit() #user pressed cancel



name=subject_name
#### PRELIMINARY STUFF

#Parameters
Frames_sec_screen = 60
Hz_stim=4

radius= [14, 16, 18]
delay=3 

presentation_period= 0.5 
inter_trial_period= 4 
ITImin = 3
ITImax = 5

size_stim= 1
size_delay_stim=2.7
fliker_time=0.25

decimals=3

limit_time=4
limit_time=2

#colors in rgb code
grey=[0,0,0]
black=[-1,-1,-1]
blue=[1,1,-1]

fix_squares_side=0.30 # 0.4 #0.2 #cm
fix_squares_sep=0.225 # 0.3 #0.2 #cm of the center --> separation between squares= 2* (fix_squares_sep-(fix_squares_side/2))
separation_between_squares=round(2*(fix_squares_sep-(fix_squares_side/2)), 2)

mouse_fix_min=-2.5 #cm #This refers to the distance when the cursor disappears.
mouse_fix_max=2.5 #cm


#Screen parameters. This parameters must be ajusted according to your screen features.
 #screen refers to the resolution (check on All settings --> Displays or internet: http://www.whatismyscreenresolution.com/)
#screen parametres
screen= [1440, 900]
#diagonal= 17.32
diagonal = 29.1

width=screen[0]
length=screen[1]

#inches of the screen diagonal (check on All settings --> Displays or internet: http://howbigismyscreen.co/ )
#Has de vigilar segun si es full screen o no... siempre será la diagonal de la screen que aparezca!!!
### screen psycho 22.05 (47.4cm x 29,8 --> 56 cm de diagonal--> 22.05 inches)
pix_per_inch=sqrt(width**2+length**2)/diagonal
pix_per_cm= pix_per_inch /2.54 #2,54 are the inches per cm


#Functions that will be used
def inch2cm(inches):
    return inches*2.54


def cm2inch(cm):
    return cm/2.54  


def cm2pix(cm):
    return  pix_per_cm * cm  


def pix2cm(pixels):
    return pixels*(1/pix_per_cm)



def deg_rad2x_y(deg, radius):
    x=round(radius*cos(radians(deg)),decimals)
    y=round(radius*sin(radians(deg)),decimals)
    return (x,y)



def circ_dist(a1,a2):
    ## Returns the minimal distance in angles between to angles 
    op1=abs(a2-a1)
    angs=[a1,a2]
    op2=min(angs)+(360-max(angs))
    options=[op1,op2]
    return min(options)



def module_fixation(x, y):
    #units given in degrees and cm
    m = sqrt(x**2 + y**2)
    return m


def mod(target,report,radius_t, radius_r):
    #units given in degrees and cm
    y_t=radius_t*sin(radians(target))
    x_t=radius_t*cos(radians(target))
    y_r=radius_r*sin(radians(report))
    x_r=radius_r*cos(radians(report))
    m = sqrt((x_t - x_r)**2 + (y_t - y_r)**2)
    return m



def isEven(number):
    return number % 2 == 0



def choicePop(list):
    c=choice(list)
    i=0
    for n in list:
      if n == c: 
        new_list = list[0:i]+list[i+1:]
      i+=1
    return (c,new_list)




#convert cm distane in pixels
mouse_fix_min=cm2pix(float(mouse_fix_min))
mouse_fix_max=cm2pix(float(mouse_fix_max))

#Round and create an int (as it is going to be in a range function where float are not admitted)
mouse_fix_min=int(round(mouse_fix_min))
mouse_fix_max=int(round(mouse_fix_max))


####################################################################
####################################################################
##################   Stims
####################################################################
####################################################################
#Create the stims
#stimList=[]
#
#list_of_deg=arange(0,360,10)
#for r in [4,6,8]:
#    for deg in list_of_deg:
#        stimList.append([r,deg])
#
#
#   
#random.shuffle(stimList)
#
##half of them with a o (same) and half with 1 (different)
#[stimList[:len(stimList)/2][i].append(0) for i in range(0, len(stimList)/2)]
#[stimList[len(stimList)/2 :][i].append(1) for i in range(0, len(stimList)/2)]
#
#
#random.shuffle(stimList)
#stimList=stimList[:10]


################################################
#####            Get the stims from a file
################################################
stims_file = easygui.fileopenbox() #This line opens you a box from where you can select the file with stimuli
stim_input=open(stims_file,'r')
lines=stim_input.readlines()[1:]
stimList = []


for line in lines:
    line = line.split()
    # calculate number of R,Angle pair that we have - minus first 2 columns, Delay and Type
    RAD=line[0] #In the future I will modify the code so it will accept stimuli without distractor    
    degree=line[1]
    same_diff=line[2]
    stimList.append([float(RAD), float(degree), float(same_diff)])




#stimList=stimList[:10]
    
    
#list to append the results
OUTPUT=zeros((len(stimList)+1 , 14)) #target angle, target rad, probe angle, same/diff, Respond
index_columns=array(['angle_target', 'angle_probe', 'radius', 'delay', 'angle_FCHB_delay', 'same_diff', 'Response', 'C_I_M', 'time_start_trial',
                      'display_time', 'presentation_target_time', 'present_CHB', 'presentation_probe_time', 'response_time']) 


####################################################################
####################################################################
############   Task
####################################################################
####################################################################
##### START OF THE TASK

#Open a psychopy window
#win = visual.Window(size=screen, units="pix", fullscr=False, color=grey)
win = visual.Window(size=screen, units="pix", fullscr=True, color=grey)
key=pyglet.window.key
keyboard = key.KeyStateHandler()
win.winHandle.push_handlers(keyboard)

MOUSE=event.Mouse(win=win, visible=False)

###########################
#############################

    


#Fixation squares (four squares together)
fix_squares_sep=cm2pix(fix_squares_sep)
pos_cue=[(fix_squares_sep,fix_squares_sep),(-fix_squares_sep,fix_squares_sep),(-fix_squares_sep, -fix_squares_sep), (fix_squares_sep, -fix_squares_sep)]

fix_squares_side=cm2pix(fix_squares_side)

f1_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(fix_squares_sep,fix_squares_sep), fillColor=black, lineColor=black)
f2_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(-fix_squares_sep,fix_squares_sep), fillColor=black, lineColor=black)
f3_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(-fix_squares_sep,-fix_squares_sep), fillColor=black, lineColor=black)
f4_black = visual.Rect(win=win, units="pix", width=fix_squares_side, height=fix_squares_side, pos=(fix_squares_sep,-fix_squares_sep), fillColor=black, lineColor=black)


def FIXATION():
    f1_black.draw()
    f2_black.draw()
    f3_black.draw()
    f4_black.draw()


    
#circle

circ_1 = visual.Circle(win=win, units="pix", radius=cm2pix(radius[0]), edges=180, pos=(0,0), fillColor=grey, lineColor=black)
circ_2 = visual.Circle(win=win, units="pix", radius=cm2pix(radius[1]), edges=180, pos=(0,0), fillColor=grey, lineColor=black)
circ_3 = visual.Circle(win=win, units="pix", radius=cm2pix(radius[2]), edges=180, pos=(0,0), fillColor=grey, lineColor=black)



tex = array([[1,-1, 1 ,-1, 1, -1 ],[-1,1, -1, 1, -1, 1], [1,-1, 1 ,-1, 1, -1 ],[-1,1, -1, 1, -1, 1], [1,-1, 1 ,-1, 1, -1 ],[-1,1, -1, 1, -1, 1]])




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

ref_time_array=[ref_time for i in range(0,14)]
OUTPUT[-1,:]=ref_time_array




for i in range(0,len(stimList)):
    #take a new trial everytime and restore the features of fixation  
    trial=stimList[i]    
    fixation=[f1_black,f2_black,f3_black,f4_black]
    
    #take the relevant info from the trial (Target=T, Non-Targuet=NT, Distractor=Dist)
    radius=trial[0]  
    angle_checkerboard = trial[1]
    angle_target = angle_checkerboard + random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    angle_probe=trial[2]
    
    #Convert the (cm, degrees) to (x_cm. y_cm) and change it to pixels with the function cm2pix. We round everything up to three decimals
    X_T=round(cm2pix(radius*cos(radians(angle_target))), decimals)
    Y_T=round(cm2pix(radius*sin(radians(angle_target))), decimals)
    
    #Convert the (cm, degrees) to (x_cm. y_cm) and change it to pixels with the function cm2pix. We round everything up to three decimals
    #move_probe = random.choice(range(-5,5)) 
    #angle_FCHB_delay = angle_target + move_probe
    angle_checkerboard = trial[1]
    angle_FCHB_delay = angle_checkerboard
    X_Td=round(cm2pix(radius*cos(radians(  angle_checkerboard    ))), decimals)
    Y_Td=round(cm2pix(radius*sin(radians(  angle_checkerboard    ))), decimals)
    
    if angle_probe==0:
        angle_pr=angle_target
        X_probe=round(cm2pix(radius*cos(radians(angle_target))), decimals)
        Y_probe=round(cm2pix(radius*sin(radians(angle_target))), decimals)
        
    elif angle_probe==1:
        angle_pr=angle_target + random.choice([-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10])
        if angle_pr<0:
            angle_pr = 360+ angle_pr
        
        if angle_pr>360:
            angle_pr = angle_pr-360
        
        
        X_probe=round(cm2pix(radius*cos(radians(angle_pr))), decimals)
        Y_probe=round(cm2pix(radius*sin(radians(angle_pr))), decimals)
    
    
    ############# Start the display of the task
    #############################
    ############################# ITI Inter-trial-interval
    #############################
    #win.flip()
    FIXATION()
    win.flip() 
    inter_trial_period=round(random.uniform( ITImin, ITImax),2)
    core.wait(float(inter_trial_period))
    # Start the display of elements
    time_start_trial=TIME.getTime() #time you need to fixate
    time_start_trial=round(time_start_trial, decimals)
    #time (start the time)       
    #Start the trial whe the mouse is fixated 
    #MOUSE=event.Mouse(win=win, visible=True)
    #pos_mouse=MOUSE.getPos()
    #x_mouse=pos_mouse[0]
    #y_mouse=pos_mouse[1]
    #while not x_mouse in range(mouse_fix_min, mouse_fix_max) or y_mouse not in range(mouse_fix_min, mouse_fix_max): 
    #    pos_mouse=MOUSE.getPos()
    #    x_mouse=pos_mouse[0]
    #    y_mouse=pos_mouse[1]
    #    FIXATION()
    #    win.flip()
    #else:
    #    MOUSE=event.Mouse(win=win, visible=False)
    #    FIXATION()
    #    win.flip()
               
    
    #Start the display time when the subject is fixated
    #time_to_fixate=TIME.getTime() #time you need to fixate
    #time_to_fixate=round(time_to_fixate - time_start_trial, decimals)
    
    display_time = core.Clock()
    display_time.reset()
    
    #Draw the components of the fixation square and the circle
    #core.wait(float(pre_stim_period))
    ######
    #############################
    ############################# PRESENTATION PERIOD (presnetation of the Targuet and the NT)
    #############################       
    presentation_target_time= TIME.getTime() #start of the trial unitil presentation
    presentation_target_time=round(presentation_target_time, decimals)
    
    target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_T, Y_T))  
    target.draw()
    
    FIXATION()
    win.flip() 
    core.wait(float(presentation_period))
    
    #############################
    ############################# DELAY 
    #############################
    start_delay=TIME.getTime()
    present_CHB=round(start_delay, decimals)
    duration_delay=TIME.getTime()
    target=visual.GratingStim(win, tex=tex, mask='circle', pos=(X_Td, Y_Td), size=cm2pix(size_delay_stim), units='pix', interpolate=False)
    #############################
    while duration_delay< start_delay + delay:
        for Hz in range(0, Hz_stim):
            for frM in range(Frames_sec_screen/(Hz_stim*2)):
                FIXATION()
                target.draw()
                win.flip()
                duration_delay= TIME.getTime()
            for frM in range(Frames_sec_screen/(Hz_stim*2)):
                FIXATION()
                win.flip()  
                duration_delay= TIME.getTime()
    else:
        FIXATION()
    
    
     
    #############################
    ############################# PRESENTATION PERIOD (presnetation of the Targuet and the NT)
    #############################       
    presentation_probe_time= TIME.getTime() #start of the trial unitil presentation
    presentation_probe_time=round(presentation_probe_time, decimals)
    target=visual.PatchStim(win, mask='circle', color= black, tex=None, size=cm2pix(size_stim), pos=(X_probe, Y_probe))  
    target.draw()
    
    FIXATION()
    win.flip() 
    core.wait(float(presentation_period))
    FIXATION()
    win.flip()
    
    display_time=display_time.getTime()
    display_time=round(display_time, decimals)
    
    #############################
    ############################# RESPONSE
    ############################# 
    #event.getKeys()
    Reaction_time = core.Clock()
    Reaction_time.reset()    
    
    start_response=TIME.getTime()
    response_time=TIME.getTime()
    
    myMouse = event.Mouse(visible=False,win=win)
    mouse_click = myMouse.getPressed()
    
    
    #
    Resp_time= start_response + limit_time        
    while response_time< start_response + limit_time:
        
        ####
        if keyboard[key.E]:
            win.close()
        
        ####
        
        
        if mouse_click[0]:#keyboard[key.A]:
            resp_text=visual.TextStim(win=win, text='same', pos=[-3,0], color=[1,1,1], units='pix', height=100)        
            Response=0
            #RT=Reaction_time.getTime()
            trial_time=TIME.getTime()
            response_time=TIME.getTime()
            Resp_time=TIME.getTime()
            FIXATION()
            win.flip()
            break
        
        elif mouse_click[2]:
            resp_text=visual.TextStim(win=win, text='diff', pos=[-3,0], color=[1,1,1], units='pix', height=100)        
            Response=1
            #RT=Reaction_time.getTime()
            trial_time=TIME.getTime()
            response_time=TIME.getTime()
            Resp_time=TIME.getTime()
            FIXATION()
            win.flip()
            break
        
        else:
            resp_text=visual.TextStim(win=win, text='Miss', pos=[-3,0], color=[1,1,1], units='pix', height=100)
            Response=999
            #RT=limit_time
            trial_time=TIME.getTime()
            FIXATION()
            win.flip()
            response_time=TIME.getTime()
    
    
    
    #compensate if break
    dif=(start_response + limit_time) - response_time
    #print dif
    core.wait(  dif )    
    #response_time=TIME.getTime()
    #resp_text.draw()
    response_time=round(Resp_time, decimals)
    FIXATION()
    win.flip()
    
    ################################################################################
    #################################################################################
    #################################################################################      
    #correct-incorrect
    if Response==999:
        C_I_M=999 #Miss
    else:
        if angle_probe==Response:
            C_I_M=0 #correct
        else:
            C_I_M=1 #incorrect
    
    
    #Features of the trial
    OUTPUT[i,:]= [angle_target, angle_pr, radius, delay, angle_FCHB_delay, angle_probe, Response, C_I_M, time_start_trial, 
                  display_time, presentation_target_time, present_CHB, presentation_probe_time, response_time]
    
    BEHAVIOR=vstack((index_columns, OUTPUT))
    savetxt(ordenador + str(name) + '_beh_enc_'+'.txt' ,  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
    #savetxt(str(name)+'_beh_'+'.txt',  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))


    
    



Final_text=visual.TextStim(win=win, text='Thank you!', pos=[-3,0], color=[1,1,1], units='pix', height=100)        
Final_text.draw()
win.flip()
core.wait(2)
win.flip()
win.close()
    

###Save the file

BEHAVIOR=vstack((index_columns, OUTPUT))
#
#
##Save a txt for the behavior and a pikle for movements inside a folder with the name

#current_directory=os.getcwd()
#os.makedirs(name+ '_encoding_mapping')
#
##
#new_directory= str(current_directory)+'/'+str(name) + '_encoding_mapping'
#os.chdir(new_directory)
##
#savetxt(str(name)+'_beh_'+'.txt',  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
####


os.makedirs(ordenador + str(name)+ '_encoding_mapping')
new_directory= ordenador + str(name) + '_encoding_mapping\\' 
os.chdir(new_directory)
savetxt(new_directory + str(name) + '_beh_enc_'+'.txt' ,  BEHAVIOR, fmt='{0: ^{1}}'.format("%s", 5))
