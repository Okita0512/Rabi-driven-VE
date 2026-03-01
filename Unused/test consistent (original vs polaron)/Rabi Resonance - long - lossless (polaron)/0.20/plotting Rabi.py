import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("Photon_number.dat")

plt.plot(data[:,0], data[:,1] / 1e4, '-', label = "N_ph")

data = np.loadtxt("Excited_population.dat")
#data = np.loadtxt("Total_excited_population.dat")

plt.plot(data[:,0], data[:,1], '-', label = "N_ex")

plt.legend()
plt.show()
