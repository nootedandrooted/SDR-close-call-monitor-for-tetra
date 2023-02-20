import time
import numpy as np
from rtlsdr import RtlSdr
from playsound import playsound

# Set the SDR device parameters
sdr = RtlSdr(serial_number='00000001')
sdr.sample_rate = 2.4e6  # Hz

sdr.freq_correction = 60   # PPM
sdr.gain = 30              # dB

# Set the frequency range to scan (390MHz-392.5MHz)
start_freq = 392e6  # Hz
end_freq = 394e6  # Hz
sdr.center_freq = (start_freq + end_freq) / 2


# Set the number of samples to read at a time
num_samples = 2**16

# Set the threshold for the squelch level
squelch_level = -40

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
    peak_freq_mhz3 = f"{peak_freq3 / 1e6:.9f}"

    for i in blacklist:
        if i == peak_freq_mhz3:
            break
    else:
        blacklist.append(peak_freq_mhz3)
        print("Added frequency to blacklist")

print(f"The following frequencie(s) are blacklisted: {blacklist}")
print("Blacklist created successfully!")



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
    peak_freq_mhz = f"{peak_freq / 1e6:.9f}"

    # Read another sample to compare with the first sample
    samples2 = sdr.read_samples(num_samples)

    # Calculate the frequency range of the samples
    freq_range2 = np.linspace(start_freq, end_freq, num_samples, endpoint=False)

    # Convert the samples to a power spectrum
    spectrum2 = np.abs(np.fft.fftshift(np.fft.fft(samples2)))

    # Find the peak frequency in the spectrum
    peak_index2 = np.argmax(spectrum2)
    peak_freq2 = freq_range2[peak_index2]

    # Convert peak frequency to MHz
    peak_freq2_mhz2 = f"{peak_freq2 / 1e6:.9f}"

    # Only print the peak frequency if it exceeds the squelch level and is not excluded
    if spectrum[peak_index] > squelch_level and peak_freq_mhz in blacklist:
        pass
    else:
        print(f"Peak frequency detected but no enough difference between samples...: {peak_freq_mhz} MHz")
        if abs(peak_freq2 - peak_freq) > 10000:
            print(f"Peak frequency detected: {peak_freq_mhz}Mhz")
            playsound('/home/pop/Downloads/warning.wav')
