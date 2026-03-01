import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.pyplot import MultipleLocator, tick_params
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
fig, ax = plt.subplots()

def set_helvetica():
    candidates = []
    direct_path = r"C:\Windows\Fonts\Helvetica.ttf"
    if os.path.exists(direct_path):
        candidates.append(direct_path)
    for font_entry in fm.fontManager.ttflist:
        if font_entry.name.lower().startswith("helvetica"):
            candidates.append(font_entry.fname)
    for path in fm.findSystemFonts():
        if "helvetica" in os.path.basename(path).lower():
            candidates.append(path)
    if not candidates:
        return
    def font_score(path):
        name = os.path.basename(path).lower()
        score = 0
        if "regular" in name or "roman" in name:
            score -= 2
        if "bold" in name or "black" in name:
            score += 2
        if "italic" in name or "oblique" in name:
            score += 1
        return (score, len(name))
    best_path = sorted(candidates, key=font_score)[0]
    fm.fontManager.addfont(best_path)
    font_name = fm.FontProperties(fname=best_path).get_name()
    plt.rcParams["font.family"] = font_name

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"
set_helvetica()
# ==============================================================================================
#                                       Global Parameters     
# ==============================================================================================

conv = 27.211397                            # 1 a.u. = 27.211397 eV
fs_to_au = 41.341                           # 1 fs = 41.341 a.u.
cm_to_au = 4.556335e-06                     # 1 cm^-1 = 4.556335e-06 a.u.
au_to_K = 3.1577464e+05                     # 1 au = 3.1577464e+05 K
kcal_to_au = 1.5936e-03                     # 1 kcal/mol = 1.5936e-3 a.u.

# ==============================================================================================
#                                       Global Constants     
# ==============================================================================================
lw = 3.0
legendsize = 48         # size for legend
font_legend = {'family':'Times New Roman', 'weight': 'roman', 'size': 24}
# axis label size
lsize = 30             
txtsize = 32
# tick length
lmajortick = 15
lminortick = 5
legend_x, legend_y = - 0.08, 1.03
transparency = .4

unitlen = 7
fig = plt.figure(figsize=(3.6 * unitlen, 3.0 * unitlen), dpi = 128)
gs = fig.add_gridspec(5, 2, height_ratios = [1, 1, 0.65, 1, 1], hspace = 0.0, wspace = 0.15)

# ==============================================================================================
#                           Fig 2a-upper 
# ==============================================================================================

fig.add_subplot(gs[0, 0])

def W(t,w):
    # global parameters
    lamF = 0.04 / conv
    t0 = 10 * fs_to_au
    sigma = 2 * fs_to_au
    wc = 2.0 / conv
    a = 0
    return (np.sqrt(np.pi) / 2) * lamF**2 * sigma * np.exp(- ((t - t0) / sigma)**2 - sigma**2 * (w - wc - 2 * a * (t - t0))**2)

t_plot = np.linspace(0 * fs_to_au, 20 * fs_to_au, 300)
w_plot = np.linspace(1.5 / conv, 2.5 / conv, 200)
x, y = np.meshgrid(t_plot, w_plot)
Wigner = W(x, y)

# ==============================================================================================

# RHS y-axis
ax = plt.gca()
cp = ax.contourf(x / fs_to_au, y * conv, Wigner, cmap = 'jet') # binary_r magma summer, RdYlBu_r

ax.plot([0, 20], [1.9, 1.9], '--', linewidth = lw, color = 'white', label = 'LP')
ax.plot([0, 20], [2.1, 2.1], '--', linewidth = lw, color = 'white', label = 'UP')
ax.text(15, 1.8, r'LP', fontsize = 28, color = 'white')
ax.text(15, 2.15, r'UP', fontsize = 28, color = 'white')

x_major_locator = MultipleLocator(5)
x_minor_locator = MultipleLocator(1)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 0, color = 'white')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'white')
plt.xlim(0, 20)
y1, y2 = 1.5, 2.5
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'white')
plt.ylim(y1, y2)

# ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'$\omega$ (eV)', size = 32)
# ax.legend(loc = 'upper left', frameon = False, prop = font_legend)
ax.set_title(r"Ultrashort pulse", size = 48, pad = 20)
legend = plt.legend(title = '(a)', loc = 'upper left', frameon = False, title_fontsize = legendsize)
plt.setp(legend.get_title(), color = 'white')

# ==============================================================================================
#                           Fig 2a-lower 
# ==============================================================================================

fig.add_subplot(gs[1, 0])

data1 = np.loadtxt("./Ultrashort/Excited_population.dat")
plt.plot(data1[:,0], 100 * data1[:,1], '-', linewidth = lw, color = 'tab:blue', label = "Exciton")

data2 = np.loadtxt("./Ultrashort/Photon_number.dat")
plt.plot(data2[:,0], data2[:,1], '-', linewidth = lw, color = 'tab:red', label = "Photon")

# ==============================================================================================

# x and y range of plotting 
time = 20             # x-axis range: (0, time)
y1, y2 = -0.05, 1.05     # y-axis range: (y1, y2)

plt.xlim(0, 20)
plt.ylim(y1, y2)

# RHS y-axis
ax = plt.gca()
x_major_locator = MultipleLocator(5)
x_minor_locator = MultipleLocator(1)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 30, color = 'k')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'k')

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'k')
plt.ylim(y1, y2)

ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'Population', size = 32)
ax.legend(loc = 'upper right', frameon = False, prop = font_legend, ncol = 2)
# ax.set_title(r"Ultrashort pulse", size = 48, pad = 20)
# legend = plt.legend(title = '(a)', loc = 'upper left', frameon = False, title_fontsize = legendsize)
# plt.setp(legend.get_title(), color = 'white')

# Inset: long-time dynamics (0-2000 fs) inside the blank area
ax_main = plt.gca()
ax_inset = inset_axes(ax_main, width = "32%", height = "55%", loc = "center left", borderpad = 6.4)
ax_inset.plot(data1[:,0], 100 * data1[:,1], '-', linewidth = lw, color = 'tab:blue')
ax_inset.plot(data2[:,0], data2[:,1], '-', linewidth = lw, color = 'tab:red')

ax_inset.set_xlim(0, 2000)
ax_inset.set_ylim(y1, y2)
ax_inset.xaxis.set_major_locator(MultipleLocator(500))
ax_inset.xaxis.set_minor_locator(MultipleLocator(100))
ax_inset.yaxis.set_major_locator(y_major_locator)
ax_inset.yaxis.set_minor_locator(y_minor_locator)
ax_inset.tick_params(which = 'major', length = 10, pad = 6)
ax_inset.tick_params(which = 'minor', length = 4)
ax_inset.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 18, color = 'k')
ax_inset.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 18, color = 'k')

inset_x_labels = ax_inset.get_xticklabels()
[label.set_fontname('Times New Roman') for label in inset_x_labels]
inset_y_labels = ax_inset.get_yticklabels()
[label.set_fontname('Times New Roman') for label in inset_y_labels]

ax_inset.set_xlabel(r't (fs)', size = 16)
ax_inset.set_ylabel(r'Population', size = 16)

# ==============================================================================================
#                           Fig 2b 
# ==============================================================================================

fig.add_subplot(gs[0, 1])

def W(t,w):
    # global parameters
    lamF = 0.04 / conv
    t0 = 250 * fs_to_au
    sigma = 50 * fs_to_au
    wc = 2.0 / conv
    a = 0
    return (np.sqrt(np.pi) / 2) * lamF**2 * sigma * np.exp(- ((t - t0) / sigma)**2 - sigma**2 * (w - wc - 2 * a * (t - t0))**2)

t_plot = np.linspace(0 * fs_to_au, 500 * fs_to_au, 300)
w_plot = np.linspace(1.75 / conv, 2.25 / conv, 200)
x, y = np.meshgrid(t_plot, w_plot)
Wigner = W(x, y)

# ==============================================================================================

# RHS y-axis
ax = plt.gca()
cp = ax.contourf(x / fs_to_au, y * conv, Wigner, cmap = 'jet') # binary_r magma summer, RdYlBu_r

ax.plot([0, 500], [1.9, 1.9], '--', linewidth = lw, color = 'white', label = 'LP')
ax.plot([0, 500], [2.1, 2.1], '--', linewidth = lw, color = 'white', label = 'UP')
ax.text(370, 1.84, r'LP', fontsize = 28, color = 'white')
ax.text(370, 2.12, r'UP', fontsize = 28, color = 'white')

x_major_locator = MultipleLocator(100)
x_minor_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 0, color = 'white')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'white')
plt.xlim(0, 500)
y1, y2 = 1.75, 2.25
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'white')
plt.ylim(y1, y2)

# ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'$\omega$ (eV)', size = 32)
# ax.legend(loc = 'upper left', frameon = False, prop = font_legend)
ax.set_title(r"Long pulse", size = 48, pad = 20)
legend = plt.legend(title = '(b)', loc = 'upper left', frameon = False, title_fontsize = legendsize)
plt.setp(legend.get_title(), color = 'white')

# ==============================================================================================
#                           Fig 2b-lower 
# ==============================================================================================

fig.add_subplot(gs[1, 1])

data = np.loadtxt("./2.0eV/Excited_population.dat")
plt.plot(data[:,0], 100 * data[:,1], '-', linewidth = lw, color = 'tab:blue', label = "Exciton")

data = np.loadtxt("./2.0eV/Photon_number.dat")
plt.plot(data[:,0], data[:,1], '-', linewidth = lw, color = 'tab:red', label = "Photon")

# ==============================================================================================

# x and y range of plotting 
time = 500             # x-axis range: (0, time)
y1, y2 = -0.05, 1.05     # y-axis range: (y1, y2)

plt.xlim(0, 500)
plt.ylim(y1, y2)

# RHS y-axis
ax = plt.gca()
x_major_locator = MultipleLocator(100)
x_minor_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 30, color = 'k')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'k')

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'k')
plt.ylim(y1, y2)

ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'Population', size = 32)
# ax.legend(loc = 'upper right', frameon = False, prop = font_legend)
# ax.set_title(r"Ultrashort pulse", size = 48, pad = 20)
# legend = plt.legend(title = '(a)', loc = 'upper left', frameon = False, title_fontsize = legendsize)
# plt.setp(legend.get_title(), color = 'white')

# ==============================================================================================
#                           Fig 2c-upper 
# ==============================================================================================

fig.add_subplot(gs[3, 0])

def W(t,w):
    # global parameters
    lamF = 0.04 / conv
    t0 = 250 * fs_to_au
    sigma = 50 * fs_to_au
    wc = 1.9 / conv
    a = 0
    return (np.sqrt(np.pi) / 2) * lamF**2 * sigma * np.exp(- ((t - t0) / sigma)**2 - sigma**2 * (w - wc - 2 * a * (t - t0))**2)

t_plot = np.linspace(0 * fs_to_au, 500 * fs_to_au, 300)
w_plot = np.linspace(1.75 / conv, 2.25 / conv, 200)
x, y = np.meshgrid(t_plot, w_plot)
Wigner = W(x, y)

# ==============================================================================================

# RHS y-axis
ax = plt.gca()
cp = ax.contourf(x / fs_to_au, y * conv, Wigner, cmap = 'jet') # binary_r magma summer, RdYlBu_r

ax.plot([0, 500], [1.9, 1.9], '--', linewidth = lw, color = 'white', label = 'LP')
ax.plot([0, 500], [2.1, 2.1], '--', linewidth = lw, color = 'white', label = 'UP')
ax.text(370, 1.84, r'LP', fontsize = 28, color = 'white')
ax.text(370, 2.12, r'UP', fontsize = 28, color = 'white')

x_major_locator = MultipleLocator(100)
x_minor_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 0, color = 'white')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'white')
plt.xlim(0, 500)
y1, y2 = 1.75, 2.25
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'white')
plt.ylim(y1, y2)

# ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'$\omega$ (eV)', size = 32)
# ax.legend(loc = 'upper left', frameon = False, prop = font_legend)
ax.set_title(r"Pump the LP", size = 48, pad = 20)
legend = plt.legend(title = '(c)', loc = 'upper left', frameon = False, title_fontsize = legendsize)
plt.setp(legend.get_title(), color = 'white')

# ==============================================================================================
#                           Fig 2c-lower 
# ==============================================================================================

fig.add_subplot(gs[4, 0])

data1 = np.loadtxt("./1.9eV/Excited_population.dat")
plt.plot(data1[:,0], 100 * data1[:,1], '-', linewidth = lw, color = 'tab:blue', label = "Exciton")

data2 = np.loadtxt("./1.9eV/Photon_number.dat")
plt.plot(data2[:,0], data2[:,1], '-', linewidth = lw, color = 'tab:red', label = "Photon")
# ==============================================================================================

# x and y range of plotting 
time = 500             # x-axis range: (0, time)
y1, y2 = -0.05, 1.05     # y-axis range: (y1, y2)

plt.xlim(0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax = plt.gca()
x_major_locator = MultipleLocator(100)
x_minor_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 30, color = 'k')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'k')

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'k')
plt.ylim(y1, y2)

ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'Population', size = 32)
# ax.legend(loc = 'upper right', frameon = False, prop = font_legend, ncol = 2)

# Inset: long-time dynamics (0-1000 fs) inside the blank area
ax_main = plt.gca()
ax_inset = inset_axes(ax_main, width = "32%", height = "55%", loc = "center left", borderpad = 6.4)
ax_inset.plot(data1[:,0], 100 * data1[:,1], '-', linewidth = lw, color = 'tab:blue')
ax_inset.plot(data2[:,0], data2[:,1], '-', linewidth = lw, color = 'tab:red')

ax_inset.set_xlim(0, 2000)
ax_inset.set_ylim(y1, y2)
ax_inset.xaxis.set_major_locator(MultipleLocator(500))
ax_inset.xaxis.set_minor_locator(MultipleLocator(100))
ax_inset.yaxis.set_major_locator(y_major_locator)
ax_inset.yaxis.set_minor_locator(y_minor_locator)
ax_inset.tick_params(which = 'major', length = 10, pad = 6)
ax_inset.tick_params(which = 'minor', length = 4)
ax_inset.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 18, color = 'k')
ax_inset.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 18, color = 'k')

inset_x_labels = ax_inset.get_xticklabels()
[label.set_fontname('Times New Roman') for label in inset_x_labels]
inset_y_labels = ax_inset.get_yticklabels()
[label.set_fontname('Times New Roman') for label in inset_y_labels]

ax_inset.set_xlabel(r't (fs)', size = 16)
ax_inset.set_ylabel(r'Population', size = 16)

# ==============================================================================================
#                           Fig 2d-upper 
# ==============================================================================================

fig.add_subplot(gs[3, 1])

def W(t,w):
    # global parameters
    lamF = 0.04 / conv
    t0 = 250 * fs_to_au
    sigma = 50 * fs_to_au
    wc = 2.1 / conv
    a = 0
    return (np.sqrt(np.pi) / 2) * lamF**2 * sigma * np.exp(- ((t - t0) / sigma)**2 - sigma**2 * (w - wc - 2 * a * (t - t0))**2)

t_plot = np.linspace(0 * fs_to_au, 500 * fs_to_au, 300)
w_plot = np.linspace(1.75 / conv, 2.25 / conv, 200)
x, y = np.meshgrid(t_plot, w_plot)
Wigner = W(x, y)

# ==============================================================================================

# RHS y-axis
ax = plt.gca()
cp = ax.contourf(x / fs_to_au, y * conv, Wigner, cmap = 'jet') # binary_r magma summer, RdYlBu_r

ax.plot([0, 500], [1.9, 1.9], '--', linewidth = lw, color = 'white', label = 'LP')
ax.plot([0, 500], [2.1, 2.1], '--', linewidth = lw, color = 'white', label = 'UP')
ax.text(370, 1.84, r'LP', fontsize = 28, color = 'white')
ax.text(370, 2.12, r'UP', fontsize = 28, color = 'white')

x_major_locator = MultipleLocator(100)
x_minor_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 0, color = 'white')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'white')
plt.xlim(0, 500)
y1, y2 = 1.75, 2.25
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'white')
plt.ylim(y1, y2)

# ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'$\omega$ (eV)', size = 32)
# ax.legend(loc = 'upper left', frameon = False, prop = font_legend)
ax.set_title(r"Pump the UP", size = 48, pad = 20)
legend = plt.legend(title = '(d)', loc = 'upper left', frameon = False, title_fontsize = legendsize)
plt.setp(legend.get_title(), color = 'white')

# ==============================================================================================
#                           Fig 2d-lower 
# ==============================================================================================

fig.add_subplot(gs[4, 1])

data1 = np.loadtxt("./2.1eV/Excited_population.dat")
plt.plot(data1[:,0], 100 * data1[:,1], '-', linewidth = lw, color = 'tab:blue', label = "Exciton")

data2 = np.loadtxt("./2.1eV/Photon_number.dat")
plt.plot(data2[:,0], data2[:,1], '-', linewidth = lw, color = 'tab:red', label = "Photon")
# ==============================================================================================

# x and y range of plotting 
time = 500             # x-axis range: (0, time)
y1, y2 = -0.05, 1.05     # y-axis range: (y1, y2)

plt.xlim(0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax = plt.gca()
x_major_locator = MultipleLocator(100)
x_minor_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.2)
y_minor_locator = MultipleLocator(0.1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 15, pad = 10)
ax.tick_params(which = 'minor', length = 5)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 30, color = 'k')
plt.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 30, color = 'k')

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 15)
ax2.tick_params(which = 'minor', length = 5)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in', color = 'k')
plt.ylim(y1, y2)

ax.set_xlabel(r't (fs)', size = 32)
ax.set_ylabel(r'Population', size = 32)
# ax.legend(loc = 'upper right', frameon = False, prop = font_legend, ncol = 2)

# Inset: long-time dynamics (0-1000 fs) inside the blank area
ax_main = plt.gca()
ax_inset = inset_axes(ax_main, width = "32%", height = "55%", loc = "center left", borderpad = 6.4)
ax_inset.plot(data1[:,0], 100 * data1[:,1], '-', linewidth = lw, color = 'tab:blue')
ax_inset.plot(data2[:,0], data2[:,1], '-', linewidth = lw, color = 'tab:red')

ax_inset.set_xlim(0, 2000)
ax_inset.set_ylim(y1, y2)
ax_inset.xaxis.set_major_locator(MultipleLocator(500))
ax_inset.xaxis.set_minor_locator(MultipleLocator(100))
ax_inset.yaxis.set_major_locator(y_major_locator)
ax_inset.yaxis.set_minor_locator(y_minor_locator)
ax_inset.tick_params(which = 'major', length = 10, pad = 6)
ax_inset.tick_params(which = 'minor', length = 4)
ax_inset.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 18, color = 'k')
ax_inset.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 18, color = 'k')

inset_x_labels = ax_inset.get_xticklabels()
[label.set_fontname('Times New Roman') for label in inset_x_labels]
inset_y_labels = ax_inset.get_yticklabels()
[label.set_fontname('Times New Roman') for label in inset_y_labels]

ax_inset.set_xlabel(r't (fs)', size = 16)
ax_inset.set_ylabel(r'Population', size = 16)

# ==============================================================================================

plt.savefig("FigS2.pdf", bbox_inches='tight')
