import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt

"""
Step 0: Select which database you wish to use.
"""

# database name
database_name = 'mitdb_201'

# path to ekg folder
path_to_folder = "../../../data/ekg/"

# select a signal file to run
signal_filepath = path_to_folder + database_name + ".csv"

#sample size so entire thing is not graphed making it easier to look at
sample_size = 3500

"""
Step #1: load data in matrix from CSV file; skip first two rows. Call the data signal.
"""

signal = np.loadtxt(signal_filepath, delimiter=',', skiprows=2)
time = signal[:sample_size, 0]
voltage = signal[:sample_size, 2]

plt.title('Raw Signal for ' + database_name)
plt.plot(time, voltage)
plt.show()

"""
Step 2: (OPTIONAL) pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6). These may not be correctly in radians
"""

## YOUR CODE HERE ##
# https://dsp.stackexchange.com/questions/49460/apply-low-pass-butterworth-filter-in-python
# user jojeck's reply was helpful
fs, fc, N = 250, 15, 6
b, a = butter(N, fc / (fs / 2), 'lowpass')
filtered_voltage = filtfilt(b, a, voltage)

plt.title('Filtered Signal for ' + database_name)
plt.plot(time, filtered_voltage)
plt.show()

"""
Step 3: Pass data through weighted differentiator
"""

## YOUR CODE HERE ##
diff_voltage = np.diff(filtered_voltage)
plt.title('Differentiated Signal for ' + database_name)
plt.plot(time[:-1], diff_voltage)
plt.show()

"""
Step 4: Square the results of the previous step
"""

 ## YOUR CODE HERE ##
squared_voltage = np.square(diff_voltage)
plt.title('Squared Signal for ' + database_name)
plt.plot(time[:-1], squared_voltage)
plt.show()

"""
Step 5: Pass a moving filter over your data
"""

## YOUR CODE HERE
window_size = 10
window_array = np.ones(window_size, dtype=int)
convolved_voltage = np.convolve(squared_voltage, window_array)

# make a plot of the results. Can change the plot() parameter below to show different intermediate signals
plt.title('Process Signal for ' + database_name)
plt.plot(time, convolved_voltage[window_size - 2:])
plt.show()
