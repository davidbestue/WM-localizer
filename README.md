## WM localizer

<br/>

Now you need to set the enviroment to link all the analysis you do in freesurfer to your structural
**You need to run this everytime you use freesurfer**

```
export SUBJECTS_DIR=/mnt/c/Users/David/Desktop/KI_Desktop/freesurfer/David/structurals/struct_1
cd $SUBJECTS_DIR
cd /mnt/c/Users/David/Desktop/KI_Desktop/freesurfer/David/WM_mapping
```

<br/>
<br/>

Different directories in the WM_mapping folder (one for each session)
WMmap_1/ WMmap_2 /WMmap_3 /WMmap_4/sessidlist
WMmap_1/bold, subjectname
bold/001, 002...

Move the files from akalla
```
Example:
scp -r davsan@akalla.cns.ki.se:~/Desktop/Distractor_project/imaging/David/WM_mapping/run1/fmri4_WM_map.nii /home/david/Desktop/freesurfer/David/WMmap/WMmap_1/bold/001/f.nii

```

The name of run folders has to be 3-digit with padding 0s. Something like “01″ or “1″ won’t work. Under run folders, put the functional imaging data “f.nii” and paradigm file (rtopy.par) 

The functional data has to be in .nii format. If the data that you get is in .dcm you can convert it to a 4D .nii format by using the matlab tool [dcm2nii](https://www.mathworks.com/matlabcentral/fileexchange/42997-xiangruili-dicm2nii)
After transformig the functional .dcm to .nii I moved it to the local

<br/>
<br/>



# Run the preprocessing of the data
<br/>

From the WM_mapping directory run the preprocessing

[More details about preprocessing in freesurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FsFastTutorialV5.1/FsFastPreProc)

```
preproc-sess -s WMmap_1 -s WMmap_2 -s WMmap_3 -s WMmap_4 -fsd bold -surface self lhrh -fwhm 5 -per-run
```
<br/>


#Preprocessing check the registration
```
tkregister-sess -s WMmap_1 -s WMmap_2 -s WMmap_3 -s WMmap_4 -fsd bold -per-run -bbr-sum
```

#dm_fas.par files

To see how they should look like visit [this](https://surfer.nmr.mgh.harvard.edu/fswiki/WorkmemPar)

Three columns
start  //   condition   //  duration // intercept // name_condition


Use the code to extracte the dm_fas.par file from raw behaviour (The example of the behaviour is: example_beh.txt)

Example:
```
python WM_mapping_beh_dmfas
```

(select the example_beh.txt in the dialogue box)

The dm_fas.par file  will be in the folder where the behaviour was. 



#Analysis
------------------------------------

More information about first level analyisis [here](https://surfer.nmr.mgh.harvard.edu/fswiki/FsFastTutorialV5.1/FsFastFirstLevel)

```
mkanalysis-sess -analysis wm_mapping.lh -paradigm wmmap.par -fsd bold -surface self lh -fwhm 5 -event-related  -nconditions 2 -spmhrf 0 -TR 2.335 -refeventdur 3 -nskip 4 -polyfit 2  -per-run -force

mkcontrast-sess -analysis wm_mapping.lh -contrast memory-v-base -a 1
```
There can be some problems with the Matlab path when running the mkcontrast (matlab required)
ou have to set the Matlab path in your .bashrc In my case, what worked was:  

***PATH=”/usr/local/MATLAB/R2018a/bin”:”$PATH”***  

(In the .bashrc, edited with nano, using the path of the matlab installed in the local (it did not wok with the runtime)

```
selxavg3-sess -s WMmap_1 -s WMmap_2 -s WMmap_3 -analysis wm_mapping.lh
tksurfer-sess -s WMmap_1 -s WMmap_2 -s WMmap_3 -analysis wm_mapping.lh -c memory-v-base 
```


Codes for merging masks: 
```
mri_mergelabels -i /home/david/Desktop/l001_parietal1_rh.label -i /home/david/Desktop/l001_parietal2_rh.label  -o /home/david/Desktop/l001_parietal_rh.label
```
