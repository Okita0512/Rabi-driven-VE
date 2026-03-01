import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, tick_params
import numpy as np
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"

fig, ax = plt.subplots()

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(10, 5), dpi = 128)
plt.subplots_adjust(wspace=0.3)

# ================= global ====================

plt.subplot(1, 2, 1)

# data = np.loadtxt("Vg.dat")
data = np.loadtxt("./0.16/Vib_pops_g.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.16 eV")

data = np.loadtxt("./0.18/Vib_pops_g.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.18 eV")

data = np.loadtxt("./0.20/Vib_pops_g.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.20 eV")

data = np.loadtxt("./0.22/Vib_pops_g.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.22 eV")

data = np.loadtxt("./0.24/Vib_pops_g.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.24 eV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 5e-14     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(1e-14)
y_minor_locator = MultipleLocator(2e-15)

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
ax.set_title('P_g_1', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
# plt.legend()

# plt.show()

plt.subplot(1, 2, 2)

# data = np.loadtxt("Vg.dat")
data = np.loadtxt("./0.16/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.16 eV")

data = np.loadtxt("./0.18/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.18 eV")

data = np.loadtxt("./0.20/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.20 eV")

data = np.loadtxt("./0.22/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.22 eV")

data = np.loadtxt("./0.24/Vib_pops_e.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.24 eV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 1.2e-7     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(5e-8)
y_minor_locator = MultipleLocator(1e-8)

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
ax.set_title('P_e_1', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)




plt.savefig("P_ge_1.pdf", bbox_inches='tight')
