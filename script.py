import os
import numpy as np
import time
from rtlsdr import RtlSdr
import csv
import datetime

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

with open('frequency_usage.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Frequency (MHz)'])

    while True:
        # Read samples from the SDR device
        samples = sdr.read_samples(num_samples)
        # Convert the samples to a power spectrum
        spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))
        # Find the peak frequency in the spectrum
        peak_freq = np.argmax(spectrum)

        # Only print the peak frequency if it exceeds the squelch level and is not excluded
        # The frequencies are excluded using a filter size 34.2 KHz
        if spectrum[peak_freq] > squelch_level:
            excluded = False
            for excluded_start, excluded_end in [(393489966, 393490034), 
                                                 (393339966, 393340034),
                                                 (393239966, 393240034),
                                                 (393089966, 393090034),
                                                 (393064966, 393065034),
                                                 (393029966, 393030034),
                                                 (393389966, 393390034),
                                                 (391159966, 391160034),
                                                 (391089966, 391090034),
                                                 (390864966, 390865034),
                                                 (390794966, 390795034)]:
                if (peak_freq > excluded_start) and (peak_freq < excluded_end):
                    excluded = True
                    break

            if not excluded:
                print("Peak frequency: {:.6f} MHz".format(peak_freq / 1e6 + start_freq / 1e6))
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
                # Write the time and frequency to the file
                writer.writerow([current_time, peak_freq / 1e6 + start_freq / 1e6])
    
                # Sleep for 1 minute
                time.sleep(60)
