#!/usr/bin/env ipython
#!/Usr/bin/env ipython
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
import os
import glob as glob
import re
from voweldetector import voweldetector

max_values = 2 ** 16
vowelMaxF = 2000  # Hz maximum expected vowel freq

"""Import an audio file in .wav format at 48KHz"""
currentFilePath = os.getcwd()
rootDir = os.path.dirname(os.path.dirname(currentFilePath))  # this goes up 2 directory levels
recordingDirRelPath = 'recordings/PhoneticLib/'
recordingDirAbsPath = os.path.join(rootDir, recordingDirRelPath)

# build out path
targetFiles2Plot = [
                   #'DSP_BF_a_far.wav',
                   #'DSP_BF_a_on.wav',
                   #'DSP_BF_ae_cat.wav',
                   #'DSP_BF_c_door.wav',
                   #'DSP_BF_e_bed.wav',
                   #'DSP_BF_i_sheep.wav',
                   #'DSP_BF_u_shoot.wav',

                   #'DSP_BF_cat.wav',
                   'DSP_BF_far.wav',
                   #'DSP_BF_on.wav',
                   #'DSP_BF_door.wav',
                   # 'DSP_BF_door_2.wav'
                   #'DSP_BF_sheep.wav',
                   #'DSP_BF_shoot.wav',
                   #doesnt exist! 'DSP_BF_floor.wav',

                   #'DSP_BF_shoot_x4',
                   #'DSP_BF_floor_x4',
                   #'DSP_BF_door_x4',
                   #'DSP_BF_door_x4_2.wav'
                   'DSP_BF_far_x4',
                   #'DSP_BF_on_x4',
                   #'DSP_BF_sheep_x4',
                   #'DSP_BF_work_x3',
                   #'DSP_BF_learn_x3',
                   #'DSP_BF_her_x4',
                    ]

# figure out the abolute file path
targetFilesFullPath = []
targetFiles2Plot_Regexp = ['.*{0}[.]wav'.format(targetFiles2Plot.split('.')[0]) for targetFiles2Plot in targetFiles2Plot]
allRecsOnPath = glob.glob(rootDir+'/**/*.wav', recursive=True)

for thisTargFileRegexp in targetFiles2Plot_Regexp:
    for thisPath2Cmp in allRecsOnPath:
        thismatch = re.match(thisTargFileRegexp, thisPath2Cmp)
        if thismatch is not None:
            print(thismatch.string, '\n')
            targetFilesFullPath.append(thismatch.string)

# call vowel detector function
voweldetector(targetFilesFullPath[0])
