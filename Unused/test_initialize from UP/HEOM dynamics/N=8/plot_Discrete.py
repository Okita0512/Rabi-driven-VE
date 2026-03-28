import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, tick_params
import numpy as np
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"

fig, ax = plt.subplots()

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(7, 7), dpi = 128)

# ================= global ====================

conv = 27.211397                            # 1 a.u. = 27.211397 eV
fs_to_au = 41.341                           # 1 fs = 41.341 a.u.
cm_to_au = 4.556335e-06                     # 1 cm^-1 = 4.556335e-06 a.u.
au_to_K = 3.1577464e+05                     # 1 au = 3.1577464e+05 K
kcal_to_au = 1.5936e-03                     # 1 kcal/mol = 1.5936e-3 a.u.

nmol = 8
NStates = nmol + 1
U = np.loadtxt("unitary.txt", dtype = complex)

# data = np.loadtxt("N=5_ntier=2.dat", dtype = float)
data = np.loadtxt("prop-rho.dat", dtype = float)
rhot = np.zeros((len(data[:,0]), NStates, NStates), dtype = complex)
rhot_p = np.zeros((len(data[:,0]), NStates, NStates), dtype = complex)
for j in range(len(data[:,0])):
    for m in range(NStates):
        for n in range(NStates):
            rhot[j, m, n] = data[j, 2 * (NStates * m + n) + 1] + 1.0j * data[j, 2 * (NStates * m + n) + 2]

    rhot_p[j,:,:] = U.conjugate().T @ rhot[j,:,:] @ U

print(rhot_p[0,-1,-1])

plt.plot(data[:,0] / fs_to_au, np.real(rhot_p[:,0,0]), '-', label = "LP")
plt.plot(data[:,0] / fs_to_au, np.real(rhot_p[:, NStates - 1, NStates - 1]), '-', label = "UP")

dark_pop = rhot_p[:, 1, 1]
for j in range(2, NStates - 1):
    dark_pop += rhot_p[:, j, j]

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 1000             # x-axis range: (0, time)
y1, y2 = 0.0, 1.0     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(200)
x_minor_locator = MultipleLocator(40)
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
# ax.set_title('No Vibrational Relaxation', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'center right', prop = font, markerscale = 1)
plt.legend(frameon = False)

# plt.show()

plt.savefig("N=8.pdf", bbox_inches='tight')
