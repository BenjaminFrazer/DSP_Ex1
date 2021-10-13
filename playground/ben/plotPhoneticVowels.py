#!/Usr/bin/env ipython
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import glob as glob
import re

max_values = 2 ** 16


"""Import an audio file in .wav format at 48KHz"""
currentFilePath = os.getcwd()
rootDir = os.path.dirname(os.path.dirname(currentFilePath))  # this goes up 2 directory levels
recordingDirRelPath = 'recordings/PhoneticLib/'
recordingDirAbsPath = os.path.join(rootDir, recordingDirRelPath)

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

sheepFbounds = [
    [108, 125],
    [210, 245],
    ]

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
                   'DSP_BF_door.wav',
                   #'DSP_BF_door_2.wav',
                   #'DSP_BF_sheep.wav',
                   #'DSP_BF_shoot.wav',

                   #'DSP_BF_shoot_x4',
                   #'DSP_BF_floor_x4',
                   'DSP_BF_door_x4',
                   #'DSP_BF_door_x4_2.wav',
                   'DSP_BF_far_x4',
                   #'DSP_BF_on_x4',
                   #'DSP_BF_sheep_x4',
                #'DSP_BF_work_x3',
                   #'DSP_BF_learn_x3',
                   #'DSP_BF_her_x4',
                   #
                   #'DSP_TP_sheep_x4',
                   #'DSP_TP_on_x4',
                   #'DSP_TP_door_x4',


                    ]

targetFilesFullPath = []
targetFiles2Plot_Regexp = ['.*{0}[.]wav'.format(targetFiles2Plot.split('.')[0]) for targetFiles2Plot in targetFiles2Plot]
allRecsOnPath = glob.glob(rootDir+'/**/*.wav', recursive=True)

for thisTargFileRegexp in targetFiles2Plot_Regexp:
    for thisPath2Cmp in allRecsOnPath:
        #print(thisTargFileRegexp)
        #print(thisPath2Cmp)
        thismatch = re.match(thisTargFileRegexp, thisPath2Cmp)
        if thismatch is not None:
            print(thismatch.string, '\n')
            targetFilesFullPath.append(thismatch.string)



legendList = []
#for i in range(0, len(targetFiles2Plot)):
    #targetFilesFullPath.append(os.path.join(recordingDirAbsPath, targetFiles2Plot[i]))

#targetFilesFullPath.append()

_absPath = targetFilesFullPath
# def plotAudioWaves(_absPath):
if type(_absPath) != list:
    _absPath = [_absPath]
"""takes a list of str paths 2 .wav files and plots in time + freq"""
plt.figure()  # create new figure
# loop through all of the audio files passed to the function
_ntraces = len(_absPath)
_colors = plt.cm.gist_rainbow(np.linspace(0, 1, _ntraces))
for i in range(0,_ntraces):
    #  Procces the raw timedomain data
    thisFilename = os.path.basename(_absPath[i])
    legendList.append(os.path.splitext(thisFilename)[0])
    print("Reading: " + thisFilename)
    _samplerate, _data = wavfile.read(_absPath[i])
    if len(_data.shape) > 1:  # make sure we only have one ch
        _data = _data[:, 1]
    _data = np.int64(_data)  # recast this so we can do the power calc

    #_data = _data/4 #  testing

    #  normalises sig power to 1 so 'volume' is normalised
    _signalPower = np.sum(abs(_data) ** 2)
    print("signal power original:", _signalPower)
    _sigPowerRescaling = 1  # 1/np.sqrt(_signalPower)
    _data_rs = _data * _sigPowerRescaling
    print("signal power rescaled:", sum(abs(_data_rs) ** 2))

    if len(_data_rs.shape) > 1:  # make sure we only have one ch
        _data_rs = _data_rs[:, 1]
    _t = np.linspace(0, len(_data_rs)/_samplerate, len(_data_rs))
    # rescale by the data length and multiply by 2 to correct
    # for the fact that spectral power is split between -+ freqs
    _dataFft = np.fft.fft(_data_rs)
    _dftResacaling = 2  # /len(_data_rs)  # compendates for dft scaling

    _freqStep = _samplerate/len(_dataFft)
    _freqs = np.arange(0, len(_dataFft)) * _freqStep

    _vowelIdx = _freqs < 2000
    _vowelPower = 2 * 1/len(_dataFft[_vowelIdx]) * np.sum(np.abs(_dataFft[_vowelIdx]) ** 2)
    _signalPowerRescaling = 1/np.sqrt(_vowelPower)
    _dataFft = _dataFft * _signalPowerRescaling
    # _dftResacaling = 2*20*np.log(_dataFft)

    # first plot time domain data
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(_t, _data_rs, color=_colors[i])
    plt.xlim(0, _t[len(_t)-1])

    # second plot is freqeuency domain data
    ax2 = plt.subplot(2, 1, 2)
    _idxPosFreqs = int(len(_dataFft)/2)
    _dataFft_rs = _dataFft * _dftResacaling
    plt.plot(_freqs[0:_idxPosFreqs], abs(_dataFft_rs[0:_idxPosFreqs]), color =_colors[i])
    plt.xlim(0, 2000)
    _maxAmp = max(abs(_dataFft_rs[0:_idxPosFreqs]))
    _maxf = _freqs[np.argmax(abs(_dataFft_rs[0:_idxPosFreqs]))]
    _pltText = "{:.1f}Hz".format(_maxf)
    ax2.annotate(_pltText, xy=(_maxf,_maxAmp))
    print("fsignal power", 1/len(_dataFft) * np.sum(np.abs(_dataFft) ** 2))
    print("vowelPower", 2/len(_dataFft[_vowelIdx]) * np.sum(np.abs(_dataFft[_vowelIdx]) ** 2))

plt.legend(legendList, loc='upper right')


for thisbound in doorFbounds:
    lb = min(thisbound)
    ub = max(thisbound)
    plt.axvspan(lb, ub)

plt.xlabel("freq (Hz)")
#plt.yscale('log')
plt.subplot(2, 1, 1)
plt.xlabel("time (s)")
plt.legend(legendList, loc='upper right')
plt.show()
