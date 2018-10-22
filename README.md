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
Three columns
start  //   condition   //  final


Use the code to extracte the dm_fas.par file from raw

Example:
```
python -i WM_mapping_beh_dmfas

```

Put the dm_fas.par file in the bold/00X



#Analysis
------------------------------------

```
mkanalysis-sess -fsd bold -stc up -surface self lh -fwhm 5 -event-related -paradigm dm_fs.par -nconditions 2 -spmhrf 0 -TR 2.335 -refeventdur 20 -nskip 4 -polyfit 2 -analysis analysis_WMmapp.sm05.lh -per-run -force

mkcontrast-sess -analysis analysis_WMmapp.sm05.lh -contrast delay -a 2
mkcontrast-sess -analysis analysis_WMmapp.sm05.lh -contrast delay_base -a 2 -c 1


selxavg3-sess -s WMmap_1 -s WMmap_2 -s WMmap_3 -analysis analysis_WMmapp.sm05.lh
tksurfer-sess -s WMmap_1 -s WMmap_2 -s WMmap_3 -analysis analysis_WMmapp.sm05.lh -c delay -c delay_base 
```

