#!/Usr/bin/env ipython
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os


max_values = 2 ** 16


"""Import an audio file in .wav format at 48KHz"""
currentFilePath = os.getcwd()
rootDir = os.path.dirname(os.path.dirname(currentFilePath))  # this goes up 2 directory levels
recordingDirRelPath = 'recordings/PhoneticLib/'
recordingDirAbsPath = os.path.join(rootDir, recordingDirRelPath)

# file_name = 'FFT Test.wav'
# file_name = 'FFT_2.wav'
targetFiles2Read = ['DSP_BF_a_far.wav',
                    'DSP_BF_a_on.wav',
                    'DSP_BF_ae_cat.wav',
                    'DSP_BF_c_door.wav',
                    'DSP_BF_e_bed.wav',
                    'DSP_BF_i_sheep.wav',
                    'DSP_BF_u_shoot.wav',
                    ]

targetFilesFullPath = []
legendList = []
for i in range(0, len(targetFiles2Read)):
    targetFilesFullPath.append(os.path.join(recordingDirAbsPath, targetFiles2Read[i]))



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
    thisFilename = os.path.basename(_absPath[i])
    legendList.append(os.path.splitext(thisFilename)[0])
    print("Reading: " + thisFilename)
    _samplerate, _data = wavfile.read(_absPath[i])
    _data = np.int64(_data)  # recast this so we can do the power calc

    #_data = _data/4

    #  normalises sig power to 1 so 'volume' is normalised
    _signalPower = np.sum(abs(_data) ** 2)/len(_data)
    print("signal power", _signalPower)
    _sigPowerRescaling = np.sqrt(1/_signalPower)
    print("signalowerRescaling", _sigPowerRescaling)
    _data = _data * _sigPowerRescaling
    if len(_data.shape) > 1:  # make sure we only have one ch
        _data = _data[:, 1]
    _t = np.linspace(0, len(_data)/_samplerate, len(_data))
    # rescale by the data length and multiply by 2 to correct
    # for the fact that spectral power is split between -+ freqs
    _dataFft = np.fft.fft(_data)
    _dftResacaling = 2/len(_data)  # compendates for dft scaling

    _freqStep = _samplerate/len(_dataFft)
    _freqs = np.arange(0, len(_dataFft)) * _freqStep

    # first plot time domain data
    plt.subplot(2, 1, 1)
    plt.plot(_t, _data, color=_colors[i])
    plt.xlim(0, _t[len(_t)-1])

    # second plot is freqeuency domain data
    plt.subplot(2, 1, 2)
    _idxPosFreqs = int(len(_dataFft)/2)
    _dataFft_rs = _dataFft * _dftResacaling
    plt.plot(_freqs[0:_idxPosFreqs], abs(_dataFft_rs[0:_idxPosFreqs]), color=_colors[i])
    plt.xlim(0, _freqs[_idxPosFreqs])
    print("fsignal power", np.sum(np.abs(_dataFft_rs) ** 2))


plt.legend(legendList)
plt.xlabel("time (s)")
plt.subplot(2, 1, 1)
plt.xlabel("freq (Hz)")
plt.legend(legendList)
plt.show()
