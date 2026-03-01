import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Evib_per_molecule.dat')
plt.plot(data[:,0], data[:,1])

plt.xlabel("Time (fs)")

plt.show()

data2 = np.loadtxt('Q.dat')

plt.plot(data2[:,0], data2[:,1], label='Qt')

plt.show()


