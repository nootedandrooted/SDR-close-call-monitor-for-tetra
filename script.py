import os
import numpy as np
import time
from rtlsdr import RtlSdr
from pylab import *
from rtlsdr import *

# Set the SDR device parameters
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 385e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 22              # dB

# Set the frequency range to scan (390MHz-395MHz)
start_freq = 390e6  # Hz
end_freq = 395e6  # Hz

# Set the number of samples to read at a time
num_samples = 2**16

# Set the threshold for the squelch level
squelch_level = 100


# Read samples from the SDR device
samples = sdr.read_samples(num_samples)
# Convert the samples to a power spectrum
spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))
# Find the peak frequency in the spectrum
peak_freq = np.argmax(spectrum)


# Only print the peak frequency if it exceeds the squelch level and is not excluded
# The frequencies are excluded using a filter size 34.2 KHz
if spectrum[peak_freq] > squelch_level:
    if (peak_freq > 393489966) and (peak_freq < 393490034):
        pass
    elif (peak_freq > 393339966) and (peak_freq < 393340034):
        pass
    elif (peak_freq > 393239966) and (peak_freq < 393240034):
        pass
    elif (peak_freq > 393089966) and (peak_freq < 393090034):
        pass
    elif (peak_freq > 393064966) and (peak_freq < 393065034):
        pass
    elif (peak_freq > 393029966) and (peak_freq < 393030034):
        pass
    elif (peak_freq > 393389966) and (peak_freq < 393390034):
        pass
    elif (peak_freq > 391159966) and (peak_freq < 391160034):
        pass
    elif (peak_freq > 391089966) and (peak_freq < 391090034):
        pass
    elif (peak_freq > 390864966) and (peak_freq < 390865034):
        pass
    elif (peak_freq > 390794966) and (peak_freq < 390795034):
        pass
    else:
        print("Peak frequency: {:.6f} MHz".format(peak_freq / 1e6 + start_freq / 1e6))
        psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
        xlabel('Frequency (MHz)')
        ylabel('Relative power (dB)')
        show()

sdr.close()
