import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, tick_params
import numpy as np
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"

# ================= global ====================

Unitlen = 5
fig, ax = plt.subplots(2, 4, figsize=(4.5 * Unitlen, 1.5 * Unitlen), dpi = 512, sharex = 'all')
fig.subplots_adjust(hspace = 0, wspace = 0.25)
font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}

# ==============================================================================================
#                                      Fig 1a    
# ==============================================================================================

ax1 = plt.subplot(2, 4, 1)

data = np.loadtxt("./N=1/UP_population.dat")

plt.plot(data[:,0], data[:,1], '-', label = "UP population", color = 'red', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 1.0     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.5)
y_minor_locator = MultipleLocator(0.1)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'Population', font = 'Times New Roman', size = 20)
ax.set_title(r'$N = 1$', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'lower right', frameon = False, prop = font, markerscale = 1)
# plt.legend()

# ==============================================================================================
#                                      Fig 1b    
# ==============================================================================================

ax2 = plt.subplot(2, 4, 5)

data = np.loadtxt("./N=1/Evib_avg.dat")

plt.plot(data[:,0], data[:,1], '-', label = r"$E_\mathrm{vib}$ per molecule", color = 'navy', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 0.065     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.02)
y_minor_locator = MultipleLocator(0.01)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$E_\mathrm{vib}$ (eV)', font = 'Times New Roman', size = 20)
# ax.set_title('No Vibrational Relaxation', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper right', frameon = False, prop = font, markerscale = 1)

# ==============================================================================================
#                                      Fig 1c    
# ==============================================================================================

ax1 = plt.subplot(2, 4, 2)

data = np.loadtxt("./N=2/UP_population.dat")

plt.plot(data[:,0], data[:,1], '-', label = "UP population", color = 'red', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 1.0     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.5)
y_minor_locator = MultipleLocator(0.1)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
# ax.set_ylabel(r'Population', font = 'Times New Roman', size = 20)
ax.set_title(r'$N = 2$', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'lower right', frameon = False, prop = font, markerscale = 1)
# plt.legend()

# ==============================================================================================
#                                      Fig 1d    
# ==============================================================================================

ax2 = plt.subplot(2, 4, 6)

data = np.loadtxt("./N=2/Evib_avg.dat")

plt.plot(data[:,0], data[:,1], '-', label = r"$E_\mathrm{vib}$ per molecule", color = 'navy', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 0.065     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.02)
y_minor_locator = MultipleLocator(0.01)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
# ax.set_ylabel(r'$E_\mathrm{vib}$ (eV)', font = 'Times New Roman', size = 20)
# ax.set_title('No Vibrational Relaxation', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'upper right', frameon = False, prop = font, markerscale = 1)

# ==============================================================================================
#                                      Fig 1e    
# ==============================================================================================

ax1 = plt.subplot(2, 4, 3)

data = np.loadtxt("./N=4/UP_population.dat")

plt.plot(data[:,0], data[:,1], '-', label = "UP population", color = 'red', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 1.0     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.5)
y_minor_locator = MultipleLocator(0.1)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
# ax.set_ylabel(r'Population', font = 'Times New Roman', size = 20)
ax.set_title(r'$N = 4$', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'lower right', frameon = False, prop = font, markerscale = 1)
# plt.legend()

# ==============================================================================================
#                                      Fig 1f    
# ==============================================================================================

ax2 = plt.subplot(2, 4, 7)

data = np.loadtxt("./N=4/Evib_avg.dat")

plt.plot(data[:,0], data[:,1], '-', label = r"$E_\mathrm{vib}$ per molecule", color = 'navy', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 0.065     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.02)
y_minor_locator = MultipleLocator(0.01)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
# ax.set_ylabel(r'$E_\mathrm{vib}$ (eV)', font = 'Times New Roman', size = 20)
# ax.set_title('No Vibrational Relaxation', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'upper right', frameon = False, prop = font, markerscale = 1)

# ==============================================================================================
#                                      Fig 1g    
# ==============================================================================================

ax1 = plt.subplot(2, 4, 4)

data = np.loadtxt("./N=8/UP_population.dat")

plt.plot(data[:,0], data[:,1], '-', label = "UP population", color = 'red', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 1.0     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.5)
y_minor_locator = MultipleLocator(0.1)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
# ax.set_ylabel(r'Population', font = 'Times New Roman', size = 20)
ax.set_title(r'$N = 8$', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'lower right', frameon = False, prop = font, markerscale = 1)
# plt.legend()

# ==============================================================================================
#                                      Fig 1h    
# ==============================================================================================

ax2 = plt.subplot(2, 4, 8)

data = np.loadtxt("./N=8/Evib_avg.dat")

plt.plot(data[:,0], data[:,1], '-', label = r"$E_\mathrm{vib}$ per molecule", color = 'navy', linewidth = 2.0)

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 0.065     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(0.02)
y_minor_locator = MultipleLocator(0.01)

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
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
# ax.set_ylabel(r'$E_\mathrm{vib}$ (eV)', font = 'Times New Roman', size = 20)
# ax.set_title('No Vibrational Relaxation', font = 'Times New Roman', size = 20)

# legend location, font & markersize
# ax.legend(loc = 'upper right', frameon = False, prop = font, markerscale = 1)




plt.savefig("Population.pdf", bbox_inches='tight')
