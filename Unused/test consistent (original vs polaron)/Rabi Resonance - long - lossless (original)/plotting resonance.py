import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("./P_g_1.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,2], 'o-', markersize = 8, color = 'navy')

plt.show()
