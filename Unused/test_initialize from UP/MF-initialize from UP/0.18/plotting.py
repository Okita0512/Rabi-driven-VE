import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('photon_number.dat')
plt.plot(data[:,0], data[:,1])

data2 = np.loadtxt('Excited_population.dat')

plt.plot(data2[:,0], 10000 * data2[:,1])

plt.xlabel("Time (fs)")

plt.show()



