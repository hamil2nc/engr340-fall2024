import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, filtfilt, butter

"""
Step 1: Load pre-processed data that has already been filtered through the PT process
"""
#@TODO: fix import names
# list of available pre-processed datasets in the data/ekg folder
available_datasets = ["mitdb_201", "mitdb_213", "mitdb_219", "nstdb_118e00", "nstdb_118e06", "qtdb_118e06"]

# select a data set from the enumerated list above
dataset = available_datasets[3]

# load saved data from numpy array
filepath = '../../../data/ekg/processed_'+dataset+'.npy'

# once loaded, place in an array called filtered
signal = np.load(filepath)


# pass data through LOW PASS FILTER (OPTIONAL)
fs, fc, N = 250, 15, 6
b, a = butter(N, 2 * fc / fs, 'lowpass')
signal = filtfilt(b, a, signal)

# pass data through HIGH PASS FILTER (OPTIONAL) to create BAND PASS result
fs, fc, N = 250, 15, 6
b, a = butter(N, 2 * fc / fs, 'highpass')
signal = filtfilt(b, a, signal)

# pass data through differentiator
signal = np.diff(signal)

# pass data through square function
signal = np.square(signal)

# pass through moving average window
window_size = 10
window_array = np.ones(window_size, dtype=int)
signal = np.convolve(signal, window_array)


"""
Step 2: Determine how much data to use...
"""
# If you wish to only run on ~10s of data uncomment the line below
# if you wish to run on all data, comment out this line
## signal = signal[0:5300]


"""
Step 3: Use Find Peaks
"""

# you may want to explore various parameters for the function that will help you!
# Distance 67 is equal to 200 ms, from the Pan-Tompkins paper
# Height of 1.5 was determined by visually inspecting the plot
peaks, _ = find_peaks(signal, height=8, distance=160)
print("Within the sample we found ", len(peaks), " heart beats with find_peaks!")

"""
Step 4: Plot the results
"""

# plot all the find_peaks results on the same graph
plt.plot(signal)
plt.title('Filtered ECG Signal with Beat Annotations')

plt.plot(peaks, signal[peaks], 'X')
plt.show()
