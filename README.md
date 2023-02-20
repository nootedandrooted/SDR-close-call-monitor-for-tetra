# SDR Close Call Monitor for TETRA

License: MIT

Description:

This project is a simple script that reads samples from one or two SDR devices, calculates the power spectrum of the samples, and detects the peak frequency in the spectrum. If the peak frequency exceeds a certain squelch level and is not on a blacklist, the script will print a warning and play a sound. This can be used as a "close call" monitor for TETRA frequencies.

The script runs an automated scan to blacklist frequencies, which is necessary for peak detection on TETRA frequencies, as TETRA downlinks can create false positives. This method should also eliminate any noise peaks that may be present.

This project is for a small school project and will later be modified to upload statistics of TETRA usage in Finland to an IoT dashboard using a Raspberry Pi 4. I will also try to make this script work as a legal "radar" detector since radar detectors are illegal to use here in Finland. FYI There is also a commercial product that works in a similar way.

To-do list (not in any particular order):

-    Improve user-friendliness
-    Add exception handling
-    Test and determine the correct levels of squelch, etc.
-    Make this script work with a Raspberry Pi 4
-    Create an LED and/or sound warning system (to be used in a car)
-    Figure out how to explain to law enforcement that this is NOT a radar detector of any kind
-    Create statistics of TETRA (VIRVE) usage in Finland

Installation:

To install the necessary dependencies for this script, run the following command:

bash

pip install -r requirements.txt

You will also need to have one or two SDR devices connected to your computer and configured correctly for the script to work.

Usage:

To use this script, simply run the following command:

bash

python3 script.py

This will start the script, which will continuously read samples from the SDR device(s) and detect peak frequencies.

You can customize the behavior of the script by modifying the following variables at the top of the main.py file:

    start_freq: The starting frequency of the samples to read (in Hz).
    end_freq: The ending frequency of the samples to read (in Hz).
    num_samples: The number of samples to read at a time.
    squelch_level: The minimum power level required for a frequency to be detected as a peak.
    blacklist: A list of frequencies (in MHz) that should be ignored.

Contributing:

If you would like to contribute to this project, feel free to submit a pull request or open an issue.

License:

This project is licensed under the terms of the MIT license. See the LICENSE file for more information.
