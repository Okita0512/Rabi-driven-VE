import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Photon_number.dat')
plt.plot(data[:, 0], data[:, 1], label='Photon number')

data = np.loadtxt('Excited_population.dat')
plt.plot(data[:, 0], 10000 * data[:, 1], label='Excited population')

plt.show()