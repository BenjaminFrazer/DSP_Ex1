#!/usr/bin/env ipython
import os
import numpy as np
from scipy.io import wavfile


def voweldetector(targetwavefile):
    '''prints the detected vowel (a, o, e)'''

    doPrintDebug = True
    # define some constants

    vowelMaxF = 2000  # Hz maximum expected vowel freq

    # the range of frequencies where 'o' is dominant
    doorFbounds = [
        [176, 203],
        [267, 325],
        [355, 465],
        [1085, 1140],
        [1212, 1244],
        [1281, 1340],
        [1380, 1430],
    ]

    # the score achieved by the test data for this range
    doorMaxScore = 0.4789494436157115

    # the range of freqs where 'e' is dominant
    sheepFbounds = [
        [108, 125],
        [210, 245],
    ]

    # the score achieved by the test data for this range
    sheepMaxScore = 0.771509570998525

    # the range of freqs where 'a' is dominant
    farFbounds = [
        [500, 1011],
        ]

    # the score achieved by the test data for this range
    farMaxScore = 0.7346054181089477

    # stick all of the above into list that we can loop through
    vowels2Check = ['e',  # sheep
                    'o',  # door
                    'a']  # far

    bounds = [sheepFbounds,
              doorFbounds,
              farFbounds]

    maxScores = [sheepMaxScore,
                 doorMaxScore,
                 farMaxScore]

    # main section
    baseFileName = os.path.basename(targetwavefile)
    if doPrintDebug:
        print("Reading: ", baseFileName, "from:\n", targetwavefile, "\n")

    # read in data
    fs, data = wavfile.read(targetwavefile)
    if len(data.shape) > 1:  # make sure we only have one ch
        data = data[:, 1]

    data = np.int64(data)  # recast this incase we run out of bits
    # tSignalPower = np.sum(abs(data) ** 2)

    # define some constants
    N = len(data)  # Number of samples
    df = fs/N  # frequency resolution
    # ts = 1/fs  # sample period
    # fn = fs/2  # nyquist frequency

    # define frequency/time vectors
    freqs = np.arange(0, N) * df
    idxVowels = freqs < vowelMaxF
    # t = np.arange(0, N) * ts

    # take fft
    dataFft = np.fft.fft(data)
    # fSignalPower = 1/N * np.sum(abs(dataFft) ** 2)

    # here we look at the sig Pow in only the vowel range 0->200Hz
    vowelSignalPower = 2 * 1/N * np.sum(abs(dataFft[idxVowels]) ** 2)
    score = np.array([0, 0, 0], float)

    # loop through all of different vowels we are testing for
    for i in range(3):
        thisVowelFreqBounds = bounds[i]
        thisVowelIdStr = vowels2Check[i]

        # here we create a logical array which represents the idxs we have selected
        idxFreqsOfInterest = np.full(N, False, bool)  # create a blank logical arr 2 pop
        for ii in range(len(thisVowelFreqBounds)):
            theseBounds = thisVowelFreqBounds[ii]
            lowBound = min(theseBounds)
            uppBound = max(theseBounds)
            theseIdxs = (freqs > lowBound) & (freqs < uppBound)
            idxFreqsOfInterest = idxFreqsOfInterest | theseIdxs

        # calculate the signal power in the region we are interested
        maskedSignalPower = 2 * 1/N * np.sum(abs(dataFft[idxFreqsOfInterest]) ** 2)
        pRatio = (maskedSignalPower/vowelSignalPower)  # the faraction of sig P in the freq range
        score[i] = pRatio / maxScores[i]  # the ratio of pRatio to a perfect score in %
        # this will be 100% for training data

        # print out the scores for each of the tree vowels
        if doPrintDebug:
            print(round(score[i] * 100, 1), '%', thisVowelIdStr, "in ",
                  baseFileName, " ... ", " maskedPow/vowPow -> ",
                  round(pRatio, 3))

    # now we decide which vowel it was based on the score
    idxMax = score.argmax()
    print(vowels2Check[idxMax])
