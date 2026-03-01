import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, tick_params
import numpy as np
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"

fig, ax = plt.subplots()

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(10, 5), dpi = 128)

# ================= global ====================

# data = np.loadtxt("Vg.dat")
data = np.loadtxt("./0.16/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = "P_e_1 (0.16)")

data = np.loadtxt("./0.18/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = "P_e_1 (0.18)")

data = np.loadtxt("./0.20/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = "P_e_1 (0.20)")

data = np.loadtxt("./0.22/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = "P_e_1 (0.22)")

data = np.loadtxt("./0.24/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = "P_e_1 (0.24)")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 1e-5     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(2e-5)
y_minor_locator = MultipleLocator(1e-5)

# x-axis and LHS y-axis
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 8, labelsize = 10)
ax.tick_params(which = 'minor', length = 4)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

# RHS y-axis
ax2 = ax.twinx()
plt.ylim(y1, y2)

ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'Population', font = 'Times New Roman', size = 20)
ax.set_title('Average vibrational energy', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
# plt.legend()

# plt.show()

plt.savefig("P_e_1_population.pdf", bbox_inches='tight')
