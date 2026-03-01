import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import ScalarFormatter
from matplotlib.pyplot import MultipleLocator, tick_params
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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

font = {'family':'Times New Roman', 'weight': 'roman', 'size':14}
fig = plt.figure(figsize=(15, 5), dpi = 128)
fig.subplots_adjust(wspace = 0.43)

legend_x, legend_y = - 0.43, 1.03
transparency = .4
legendsize = 48         # size for legend

# ==============================================================================================
#                                      Fig 3a     
# ==============================================================================================
plt.subplot(1, 3, 1)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20050/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20050 eV")

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20100/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20100 eV")

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20110/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20110 eV")

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20120/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20120 eV")

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20125/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20125 eV")

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20130/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20130 eV")

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20134/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20134 eV")

# ==============================================================================================

# x and y range of plotting 
time = 20              # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = -1e-14, 7e-13      # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(5)
x_minor_locator = MultipleLocator(1)
y_major_locator = MultipleLocator(2e-13)
y_minor_locator = MultipleLocator(1e-13)

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

# format left y-axis in scientific notation like panel (a)
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel('time (ps)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{g}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)
# ax.set_title(r'', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
plt.legend(title = '(a)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig 3b     
# ==============================================================================================
plt.subplot(1, 3, 2)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20050/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20050 eV", alpha = 1.0)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20100/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20100 eV", alpha = 0.85)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20110/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20110 eV", alpha = 0.70)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20120/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20120 eV", alpha = 0.55)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20125/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20125 eV", alpha = 0.40)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20130/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20130 eV", alpha = 0.25)

data = np.loadtxt("./Rabi Resonance - short - lossless/0.20134/Vib_pops_e.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\Omega$ = 0.20134 eV", alpha = 0.10)

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 20              # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 2.5e-10       # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(5)
x_minor_locator = MultipleLocator(1)
y_major_locator = MultipleLocator(5e-11)
y_minor_locator = MultipleLocator(1e-11)

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

# format left y-axis in scientific notation like panel (a)
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel('time (ps)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{e}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)
plt.legend(title = '(b)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig 3c     
# ==============================================================================================
plt.subplot(1, 3, 3)

data = np.loadtxt("./Rabi Resonance - short - lossless/P_g_1.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,2], 'o-', markersize = 4, color = 'navy')

plt.vlines(0.20134, 0, 1e-12, colors = 'darkred', linestyles = 'dashed')
plt.text(0.20020, 2.2e-13, r'$\Omega = 0.20134$ eV', color = 'darkred', fontsize = 16, fontname = 'Times New Roman')

# x and y range of plotting 
y1, y2 = 0, 2.5e-13     # y-axis range: (y1, y2)

plt.xlim(0.20000, 0.20200)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(0.001)
x_minor_locator = MultipleLocator(0.0002)
y_major_locator = MultipleLocator(5e-14)
y_minor_locator = MultipleLocator(1e-14)

# x-axis and LHS y-axis
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 8, labelsize = 10, color = 'navy')
ax.tick_params(which = 'minor', length = 4, color = 'navy')
ax.spines['left'].set_color('navy')
ax.spines['left'].set_linewidth(2)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

# format left y-axis in scientific notation like panel (a)
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel(r'$\Omega$ (eV)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$\langle P_{\mathrm{g}, \nu = 1} \rangle$', font = 'Times New Roman', size = 20, labelpad = 20, color = 'navy')

# legend location, font & markersize
# ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
plt.legend(title = '(c)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================

plt.savefig("FigS4.pdf", bbox_inches='tight')
