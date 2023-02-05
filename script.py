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
sdr.gain = 40

# Set the frequency range to scan (380MHz-400MHz)
start_freq = 380e6  # Hz
end_freq = 400e6  # Hz

# Set the number of samples to read at a time
num_samples = 2**16

# Set the threshold for the squelch level
squelch_level = 100

while True:
    # Read samples from the SDR device
    samples = sdr.read_samples(num_samples)
    # Convert the samples to a power spectrum
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))
    # Find the peak frequency in the spectrum
    peak_freq = np.argmax(spectrum)
    # Only print the peak frequency if it exceeds the squelch level and is not excluded
    if spectrum[peak_freq] > squelch_level:
        print("Peak frequency: {:.6f} MHz".format(peak_freq / 1e6 + start_freq / 1e6))

        #Plot the PSD with matplotlib
        psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
        xlabel('Frequency (MHz)')
        ylabel('Relative power (dB)')
        show()
        
sdr.close()
