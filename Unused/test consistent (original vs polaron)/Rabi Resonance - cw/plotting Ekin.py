import matplotlib.pyplot as plt
import numpy as np

# data = np.loadtxt("Vg.dat")
data = np.loadtxt("./0.16/Ekin.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.16 eV")

data = np.loadtxt("./0.18/Ekin.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.18 eV")

data = np.loadtxt("./0.20/Ekin.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.20 eV")

data = np.loadtxt("./0.22/Ekin.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.22 eV")

data = np.loadtxt("./0.24/Ekin.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.24 eV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)

plt.legend()
plt.show()
