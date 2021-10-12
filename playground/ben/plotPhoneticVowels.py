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

targetFilesFullPath.append()

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
    _sigPowerRescaling = 1/np.sqrt(_signalPower)
    _data_rs = _data * _sigPowerRescaling
    print("signal power rescaled:", sum(abs(_data_rs) ** 2))

    if len(_data_rs.shape) > 1:  # make sure we only have one ch
        _data_rs = _data_rs[:, 1]
    _t = np.linspace(0, len(_data_rs)/_samplerate, len(_data_rs))
    # rescale by the data length and multiply by 2 to correct
    # for the fact that spectral power is split between -+ freqs
    _dataFft = np.fft.fft(_data_rs)
    _dftResacaling = 2/len(_data_rs)  # compendates for dft scaling

    _freqStep = _samplerate/len(_dataFft)
    _freqs = np.arange(0, len(_dataFft)) * _freqStep

    # first plot time domain data
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(_t, _data_rs, color=_colors[i])
    plt.xlim(0, _t[len(_t)-1])

    # second plot is freqeuency domain data
    ax2 = plt.subplot(2, 1, 2)
    _idxPosFreqs = int(len(_dataFft)/2)
    _dataFft_rs = _dataFft * _dftResacaling
    plt.plot(_freqs[0:_idxPosFreqs], abs(_dataFft_rs[0:_idxPosFreqs]), color=_colors[i])
    plt.xlim(0, _freqs[_idxPosFreqs])
    _maxAmp = max(abs(_dataFft_rs[0:_idxPosFreqs]))
    _maxf = _freqs[np.argmax(abs(_dataFft_rs[0:_idxPosFreqs]))]
    _pltText = "{:.1f}Hz".format(_maxf)
    ax2.annotate(_pltText, xy=(_maxf,_maxAmp))
    print("fsignal power", 1/len(_dataFft) * np.sum(np.abs(_dataFft) ** 2))


plt.legend(legendList, loc='upper right')


plt.xlabel("freq (Hz)")
plt.subplot(2, 1, 1)
plt.xlabel("time (s)")
plt.legend(legendList, loc='upper right')
plt.show()
