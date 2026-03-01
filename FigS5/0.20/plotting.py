import matplotlib.pyplot as plt
import numpy as np

# ================= global ====================

# data = np.loadtxt("Vg.dat")

# plt.plot(data[:,0], data[:,1], '-', label = "Vg")

# data = np.loadtxt("Vib_pops_g.dat")

# plt.plot(data[:,0], data[:,2], '-', label = "P_g_1")

data = np.loadtxt("Evib_per_molecule.dat")

plt.plot(data[:,0], data[:,1], '-', label = "Evib total")
plt.plot(data[:,0], data[:,2], '-', label = "Evib g")
plt.plot(data[:,0], data[:,3], '-', label = "Evib e")


#data = np.loadtxt("Ekin.dat")

#plt.plot(data[:,0], data[:,1], '-', label = "Ekin total")
#plt.plot(data[:,0], data[:,2], '-', label = "Ekin g")
#plt.plot(data[:,0], data[:,3], '-', label = "Ekin e")

plt.show()

