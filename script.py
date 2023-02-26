# This is the same thing as script2.py but for a RTL-SDR device with a different serial number
# Due to the hardware limitations of RTL-SDR the device can only handle a bandwidth of 2.56Mhz stable. Therefore two RTL-SDR devices are needed to cover the whole TETRA frequencies.
# This script is set up for VIRVE frequencies.

import time
import numpy as np
from rtlsdr import RtlSdr
from playsound import playsound

# Set the SDR device parameters
sdr = RtlSdr(serial_number='00000001')
sdr.sample_rate = 2e6  # Hz

sdr.freq_correction = 18   # PPM
sdr.gain = 30              # dB

# Set the frequency range to scan (392MHz-394MHz)
start_freq = 392e6  # Hz
end_freq = 394e6  # Hz
sdr.center_freq = (start_freq + end_freq) / 2 


# Set the number of samples to read at a time
num_samples = 2**16

# Set the threshold for the squelch level
squelch_level = -30

# Create the blacklist
blacklist = []

# Run for 60 seconds
print("Scanning for frequencies to be blacklisted. This will take a minute.")
t_end = time.time() + 60
while time.time() < t_end:

    # Read samples from the SDR device
    samples3 = sdr.read_samples(num_samples)

    # Calculate the frequency range of the samples
    freq_range3 = np.linspace(start_freq, end_freq, num_samples, endpoint=False)
    
    # Convert the samples to a power spectrum
    spectrum3 = np.abs(np.fft.fftshift(np.fft.fft(samples3)))
    
    # Find the peak frequency in the spectrum
    peak_index3 = np.argmax(spectrum3)
    peak_freq3 = freq_range3[peak_index3]

    # Convert peak frequency to MHz
    peak_freq_mhz3 = f"{peak_freq3 / 1e6:.3f}"

    for i in blacklist:
        if i == peak_freq_mhz3:
            break
    else:
        blacklist.append(peak_freq_mhz3)
        print("Added frequency to blacklist")

print(f"The following frequencie(s) are blacklisted: {blacklist}")
print("Blacklist created successfully!")
print("CTRL + c to stop")

# The main loop with exception handling
try:
    while True:
        # Read samples from the SDR device
        samples = sdr.read_samples(num_samples)

        # Calculate the frequency range of the samples
        freq_range = np.linspace(start_freq, end_freq, num_samples, endpoint=False)

        # Convert the samples to a power spectrum
        spectrum = np.abs(np.fft.fftshift(np.fft.fft(samples)))

        # Find the peak frequency in the spectrum
        peak_index = np.argmax(spectrum)
        peak_freq = freq_range[peak_index]

        # Convert peak frequency to MHz
        peak_freq_mhz = f"{peak_freq / 1e6:.3f}"

        # Only print the peak frequency if it exceeds the squelch level and is not excluded
        if spectrum[peak_index] > squelch_level and peak_freq_mhz in blacklist:
            pass
        else:
            print(f"Peak frequency detected: {peak_freq_mhz}Mhz")
            playsound('/home/pop/Downloads/warning.wav')
            time.sleep(1)
except KeyboardInterrupt:
    print("Bye!")
finally:
    # Close the SDR
    sdr.close()
