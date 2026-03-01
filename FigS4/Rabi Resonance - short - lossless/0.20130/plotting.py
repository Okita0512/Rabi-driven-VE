import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Vib_pops_g.dat')
plt.plot(data[:, 0], data[:, 2], label='Pg_1')

plt.show()