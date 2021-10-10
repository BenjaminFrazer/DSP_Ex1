import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile


def identifier(list, vowel, data):
    j = 0
    indexList = []
    while j <= len(list)-1:
        if list[j] in vowel:
            indexList.append(j)
        j += 1

    for k in indexList:
        if data[k] > data[k-1] and data[k] > data[k+1] and data[k] > data[k-2] and data[k] > data[k+2] \
                and data[k] > data[k-3] and data[k] > data[k+3] and data[k] > data[k-4] and data[k] > data[k+4]:
            return 1
        else:
            return 0


def voweldetector(name):

    v = 0
    foundVowels = []

    sheep = 280.0, 2620.0, 3380.0
    ship = 360.0, 2220.0, 2960.0
    bed = 600.0, 2060.0, 2840.0
    cat = 800.0, 1760.0, 2500.0
    up = 760.0, 1320.0, 2500.0
    far = 740.0, 1180.0, 2640.0
    on = 560.0, 920.0, 2560.0
    door = 480.0, 760.0, 2620.0
    good = 380.0, 940.0, 2300.0
    shoot = 320.0, 920.0, 2200.0
    bird = 0, 0, 0
    teacher = 0, 0, 0

    vowels = [sheep,ship,bed,cat,up,far,on,door,good,shoot,bird,teacher]
    vowels_name = ['sheep','ship','bed','cat','up','far','on','door','good','shoot','bird','teacher']

    """Import an audio file in .wav format at 48KHz"""
    path = os.getcwd()
    file_name = name

    location = os.path.join(path, file_name)
    samplerate, data = wavfile.read(location)

    """Create the FFT of the data(np array of numbers) obtained from the audio file"""
    data_fft = np.fft.fft(data)

    """Define the frequency and time domains"""
    f = np.linspace(0, samplerate/2, len(data_fft))

    """Plot the Frequency domain spectrum"""
    plt.plot(f, np.abs(data_fft))
    plt.title('Frequency Domain')
    plt.xlabel('Frequency(rad/s)')
    plt.ylabel('Amplitude(dB)')

    # plt.show()
    frequencyList = np.round(f, 1)

    while v <= len(vowels)-1:
        p = (identifier(frequencyList, vowels[v], np.abs(data_fft)))
        if p == 1:
            foundVowels.append(vowels_name[v])
        v += 1

    return foundVowels


vowel_1 = voweldetector('Test_recording.wav')
vowel_2 = voweldetector('Fox.wav')

for vowel in vowel_1:
    print('Wave file 1: ',vowel)

for vowel in vowel_2:
    print('Wave file 2: ',vowel)
