import matplotlib.pyplot as plt
import numpy as np

# import the CSV file using numpy
path = '../../../data/ekg/mitdb_201.csv'

# load data in matrix from CSV file; skip first two rows
### Your code here ###
data = np.loadtxt(path, delimiter=',', skiprows=2)

# save each vector as own variable
### Your code here ###
sample = 3000

time = data[:sample, 0]
voltage = data[:sample, 2]

# use matplot lib to generate a single
### Your code here ###
plt.plot(time, voltage, label='EKG Data')
plt.legend()
plt.show()
