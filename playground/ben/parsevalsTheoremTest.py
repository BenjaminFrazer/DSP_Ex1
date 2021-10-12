#!/usr/bin/env ipython
import numpy as np
import matplotlib.pyplot as plt


twopi = 2 * np.pi
Ts = 0.01
fs = 1/Ts
t = np.arange(0, 10, Ts)
N = len(t)
y = np.sin(twopi*t)+1/4*np.sin(4*twopi*t)
yfft = np.fft.fft(y)
yfftScaled = abs(yfft)*2/N
df = fs/N
freqs = np.linspace(0, df*N, N)

plt.plot(freqs, yfftScaled)
plt.show()

print("tPower=", sum(abs(y) ** 2))
print("fpower=", (1/N) * sum(abs(yfft) ** 2))
