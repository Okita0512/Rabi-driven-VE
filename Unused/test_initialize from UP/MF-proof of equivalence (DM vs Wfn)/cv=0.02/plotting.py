import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('photon_number.dat')
plt.plot(data[:,0], data[:,1], label = 'photon (DM)')
data = np.loadtxt('photon_number-wfn.dat')
plt.plot(data[:,0], data[:,1], '--', label = 'photon (Wfn)')

data2 = np.loadtxt('Excited_population.dat')
plt.plot(data2[:,0], 10000 * data2[:,1], label = 'exciton (DM)')
data2 = np.loadtxt('Excited_population-wfn.dat')
plt.plot(data2[:,0], 10000 * data2[:,1], '--', label = 'exciton (Wfn)')

plt.xlabel("Time (fs)")

plt.legend()
plt.show()



