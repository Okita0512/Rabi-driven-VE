import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("energy_summary.csv", delimiter=",", skiprows=1)

plt.plot(data[:, 0], data[:, 2], marker='o', linestyle='-')

plt.xlabel(r"$\nu$ (eV)")
plt.ylabel(r"$\langle E_{vib} \rangle$ (eV)")

plt.show()