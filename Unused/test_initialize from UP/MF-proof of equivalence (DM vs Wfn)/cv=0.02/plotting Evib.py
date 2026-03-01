import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Evib_per_molecule.dat')
plt.plot(data[:,0], data[:,1])
plt.plot(data[:,0], data[:,2])
# plt.plot(data[:,0], data[:,3])

data = np.loadtxt('Evib_per_molecule-wfn.dat')
plt.plot(data[:,0], data[:,1], '--')
plt.plot(data[:,0], data[:,2], '--')
# plt.plot(data[:,0], data[:,3], '--')

plt.xlabel("Time (fs)")

plt.show()

data2 = np.loadtxt('Vib_pops_e.dat')

plt.plot(data2[:,0], data2[:,1], label='Pe, v=0 (DM)')
plt.plot(data2[:,0], data2[:,2], label='Pe, v=1 (DM)')

data2 = np.loadtxt('Vib_pops_e-wfn.dat')

plt.plot(data2[:,0], data2[:,1], '--', label='Pe, v=0 (Wfn)')
plt.plot(data2[:,0], data2[:,2], '--', label='Pe, v=1 (Wfn)')

plt.xlabel("Time (fs)")
plt.legend()

plt.show()

data2 = np.loadtxt('Vib_pops_g.dat')

plt.plot(data2[:,0], data2[:,1], label='Pg, v=0')
plt.plot(data2[:,0], data2[:,2], label='Pg, v=1')

plt.xlabel("Time (fs)")
plt.legend()

plt.show()

