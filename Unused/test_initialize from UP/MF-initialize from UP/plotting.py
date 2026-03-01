import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("Evib_per_molecule_avg.csv", delimiter=",", skiprows=1)

plt.plot(data[:, 0], data[:, 3], marker='o', linestyle='-')

plt.xlabel(r"$\nu$ (eV)")
plt.ylabel(r"$\langle E_{vib} \rangle$ (eV)")

plt.show()