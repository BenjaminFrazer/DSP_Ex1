#!/usr/bin/env ipython
#!/Usr/bin/env ipython
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import glob as glob
import re

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
                   #'DSP_BF_far.wav',
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
                   #'DSP_BF_far_x4',
                   #'DSP_BF_on_x4',
                   #'DSP_BF_sheep_x4',
                   'DSP_BF_work_x3',
                   'DSP_BF_learn_x3',
                   'DSP_BF_her_x4',
                    ]

doorFbounds = [
    [176, 203],
    #[206, 211],
    [267, 325],
    [355, 465],
    #[731, 736],
    #[930, 952],
    #[1010, 1045],
    [1085, 1140],
    [1212, 1244],
    [1281, 1340],
    [1380, 1430],
]

doorMaxScore = 0.4789494436157115#0.3374416993872681  # 0.25786093367150753 #  0.0869910581253902

sheepFbounds = [
    [108, 125],
    [210, 245],

]
onFbounds = [
    [480, 490],
    [560, 622],
    [664, 672],
    [757, 782],
    [802, 825],
    ]

targetFilesFullPath = []
targetFiles2Plot_Regexp = ['.*{0}[.]wav'.format(targetFiles2Plot.split('.')[0]) for targetFiles2Plot in targetFiles2Plot]
allRecsOnPath = glob.glob(rootDir+'/**/*.wav', recursive=True)

for thisTargFileRegexp in targetFiles2Plot_Regexp:
    for thisPath2Cmp in allRecsOnPath:
        thismatch = re.match(thisTargFileRegexp, thisPath2Cmp)
        if thismatch is not None:
            print(thismatch.string, '\n')
            targetFilesFullPath.append(thismatch.string)

# main section

filename = targetFilesFullPath[0]
print("Reading: " + filename)

# read in data
fs, data = wavfile.read(filename)
if len(data.shape) > 1:  # make sure we only have one ch
    data = data[:, 1]

data = np.int64(data)
tSignalPower = np.sum(abs(data) ** 2)

# define some constants
N = len(data)  # Number of samples
df = fs/N  # frequency resolution
ts = 1/fs  # sample period
fn = fs/2  # nyquist frequency

# define frequency/time vectors
freqs = np.arange(0, N) * df
idxVowels = freqs < vowelMaxF
t = np.arange(0, N) * ts

#take fft
dataFft = np.fft.fft(data)
fSignalPower = 1/N * np.sum(abs(dataFft) ** 2)

vowelSignalPower = 2 * 1/N * np.sum(abs(dataFft[idxVowels]) ** 2)

# here we create a logical array which represents the idxs we have selected
idxFreqsOfInterest = np.full(N, False, bool)
for ii in range(len(doorFbounds)):
    theseBounds = doorFbounds[ii]
    lowBound = min(theseBounds)
    uppBound = max(theseBounds)
    theseIdxs = (freqs > lowBound) & (freqs < uppBound)
    idxFreqsOfInterest = idxFreqsOfInterest | theseIdxs

# calculate the signal power in the region we are interested
maskedSignalPower = 2 * 1/N * np.sum(abs(dataFft[idxFreqsOfInterest]) ** 2)

print(os.path.basename(filename), "door:", (maskedSignalPower/vowelSignalPower)/doorMaxScore * 100, '%')
