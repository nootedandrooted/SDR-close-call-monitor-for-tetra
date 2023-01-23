import os
import numpy as np
from rtlsdr import RtlSdr

# Set the SDR device parameters
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 385e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

# Set the frequency range to scan
start_freq = 380e6  # Hz
end_freq = 390e6  # Hz

# Set the number of samples to read at a time
num_samples = 2**16

while True:
    # Read samples from the SDR device
    samples = sdr.read_samples(num_samples)
    # Convert the samples to a power spectrum
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))
    # Find the peak frequency in the spectrum
    peak_freq = np.argmax(spectrum)
    # Print the peak frequency to the command line
    print("Peak frequency: {:.6f} MHz".format(peak_freq / 1e6 + start_freq / 1e6))
