import numpy as np
from rtlsdr import RtlSdr
from playsound import playsound

# Set the SDR device parameters
sdr = RtlSdr(serial_number='00000001')
sdr.sample_rate = 2.4e6  # Hz

sdr.freq_correction = 60   # PPM
sdr.gain = 30              # dB

# Set the frequency range to scan (390MHz-392.5MHz)
start_freq = 433e6  # Hz
end_freq = 435e6  # Hz
sdr.set_center_freq((start_freq + end_freq) / 2)

# Set the number of samples to read at a time
num_samples = 2**16

# Set the threshold for the squelch level
squelch_level = -40

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
    peak_freq2_mhz = f"{peak_freq2 / 1e6:.9f}"

    # Only print the peak frequency if it exceeds the squelch level and is not excluded
    # The frequencies are excluded using a filter size 34.2 KHz
    if spectrum[peak_index] > squelch_level:
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
            print(f"Peak frequency: {peak_freq_mhz} MHz")
            if abs(peak_freq2 - peak_freq) > 2000:
                print(peak_freq_mhz)
                playsound('/home/pop/Downloads/warning.wav')
