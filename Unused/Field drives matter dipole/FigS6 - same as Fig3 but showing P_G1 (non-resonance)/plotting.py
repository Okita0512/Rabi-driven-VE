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

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(10, 10), dpi = 128)
fig.subplots_adjust(hspace = 0.2, wspace = 0.45)

legend_x, legend_y = - 0.45, 1.03
transparency = .4
legendsize = 48         # size for legend

# ==============================================================================================
#                                      Fig S6a     
# ==============================================================================================
plt.subplot(2, 2, 1)

data = np.loadtxt("./Resonance-short-lossless/0.16/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.16 eV")

data = np.loadtxt("./Resonance-short-lossless/0.18/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.18 eV")

data = np.loadtxt("./Resonance-short-lossless/0.20/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.20 eV")

data = np.loadtxt("./Resonance-short-lossless/0.22/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.22 eV")

data = np.loadtxt("./Resonance-short-lossless/0.24/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\Omega$ = 0.24 eV")

# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 2.5e-14     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(5e-15)
y_minor_locator = MultipleLocator(1e-15)

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
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{G}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)
# ax.set_title(r'', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
plt.legend(title = '(a)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig S6b     
# ==============================================================================================
plt.subplot(2, 2, 2)

data = np.loadtxt("./Resonance-short-lossless/pg_n1_summary.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,1], '-o', markersize = 8, color = 'navy')

plt.vlines(0.20, ymin = 0, ymax = 1.2e-14, colors = 'darkred', linestyles = 'dashed')
plt.text(0.204, 1e-14, r'$\Omega = \nu$', verticalalignment='center', fontsize = 20, fontname = 'Times New Roman', color = 'darkred')

plt.vlines(0.40, ymin = 0, ymax = 1.2e-14, colors = 'darkred', linestyles = 'dashed')
plt.text(0.304, 0.85e-14, r'$\Omega = 2\nu$', verticalalignment='center', fontsize = 20, fontname = 'Times New Roman', color = 'darkred')

# x and y range of plotting 
y1, y2 = 0.0, 1.2e-14     # y-axis range: (y1, y2)

plt.xlim(0.15, 0.45)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(0.1)
x_minor_locator = MultipleLocator(0.02)
y_major_locator = MultipleLocator(5e-15)
y_minor_locator = MultipleLocator(1e-15)

# x-axis and LHS y-axis
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 8, labelsize = 10, color = 'navy')
ax.tick_params(which = 'minor', length = 4, color = 'navy')
ax.spines['left'].set_color("navy")
ax.spines['left'].set_linewidth(2)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

# RHS y-axis
ax2 = ax.twinx()

data = np.loadtxt("./Resonance-short-lossless/pg_n2_summary.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,1], '-o', markersize = 8, color = 'red')

y1, y2 = 0.0, 1.2e-16     # y-axis range: (y1, y2)
plt.ylim(y1, y2)

y_major_locator = MultipleLocator(5e-17)
y_minor_locator = MultipleLocator(1e-17)
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8, labelsize = 10, color = 'red')
ax2.tick_params(which = 'minor', length = 4, color = 'red')
# ax2.axes.yaxis.set_ticklabels([])
ax2.spines['right'].set_color("red")
ax2.spines['right'].set_linewidth(2)

x1_label = ax2.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax2.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

# format left y-axis in scientific notation like panel (a)
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# format right y-axis in scientific notation like panel (a)
ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax2.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax2.yaxis.get_offset_text().set_size(16)
ax2.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel(r'$\Omega$ (eV)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$\langle P_{\mathrm{G}, \nu = 1} \rangle$', font = 'Times New Roman', size = 20, labelpad = 20, color = 'navy')
ax2.set_ylabel(r'$\langle P_{\mathrm{G}, \nu = 2} \rangle$', font = 'Times New Roman', size = 20, labelpad = 20, color = 'red')
plt.legend(title = '(b)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig S6c     
# ==============================================================================================
plt.subplot(2, 2, 3)

data = np.loadtxt("./Resonance-long-lossless/0.16/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.16 eV")

data = np.loadtxt("./Resonance-long-lossless/0.18/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.18 eV")

data = np.loadtxt("./Resonance-long-lossless/0.20/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.20 eV")

data = np.loadtxt("./Resonance-long-lossless/0.22/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.22 eV")

data = np.loadtxt("./Resonance-long-lossless/0.24/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.24 eV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 5e-10     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(1e-10)
y_minor_locator = MultipleLocator(2e-11)

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
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{G}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
plt.legend(title = '(c)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# Inset: long-time dynamics (0-1000 fs) inside the blank area
ax_main = plt.gca()
ax_inset = inset_axes(ax_main, width = "55%", height = "28%", loc = "lower right", borderpad = 2.8)
data = np.loadtxt("./Resonance-long-lossless/0.16/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.16 eV")

data = np.loadtxt("./Resonance-long-lossless/0.18/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.18 eV")

data = np.loadtxt("./Resonance-long-lossless/0.20/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.20 eV")

data = np.loadtxt("./Resonance-long-lossless/0.22/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.22 eV")

data = np.loadtxt("./Resonance-long-lossless/0.24/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\nu$ = 0.24 eV")

y1, y2 = 0, 2e-22
y_major_locator = MultipleLocator(1e-22)
y_minor_locator = MultipleLocator(2e-23)

ax_inset.set_xlim(500, 2000)
ax_inset.set_ylim(y1, y2)
ax_inset.xaxis.set_major_locator(MultipleLocator(500))
ax_inset.xaxis.set_minor_locator(MultipleLocator(100))
ax_inset.yaxis.set_major_locator(y_major_locator)
ax_inset.yaxis.set_minor_locator(y_minor_locator)
ax_inset.tick_params(which = 'major', length = 10, pad = 6)
ax_inset.tick_params(which = 'minor', length = 4)
ax_inset.tick_params(axis = 'x', which = 'both', direction = 'in', labelsize = 12, color = 'k')
ax_inset.tick_params(axis = 'y', which = 'both', direction = 'in', labelsize = 12, color = 'k')

inset_x_labels = ax_inset.get_xticklabels()
[label.set_fontname('Times New Roman') for label in inset_x_labels]
inset_y_labels = ax_inset.get_yticklabels()
[label.set_fontname('Times New Roman') for label in inset_y_labels]

# ax_inset.set_xlabel(r't (fs)', size = 12)
ax_inset.set_ylabel(r'$P_{\mathrm{G}, \nu = 1}$', size = 12)

# format left y-axis in scientific notation like panel (a)
ax_inset.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax_inset.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax_inset.yaxis.get_offset_text().set_size(12)
ax_inset.yaxis.get_offset_text().set_fontname('Times New Roman')

# ==============================================================================================
#                                      Fig S6d     
# ==============================================================================================
plt.subplot(2, 2, 4)

data = np.loadtxt("./Resonance-long-lossless/pg_n1_summary.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,1], '-o', label = r"$\langle P_{\mathrm{G}, \nu = 1} \rangle$", markersize = 8, color = 'navy')

plt.vlines(0.20, ymin = 0, ymax = 1.2e-19, colors = 'darkred', linestyles = 'dashed')
plt.text(0.204, 5e-20, r'$\nu = \Omega$', verticalalignment='center', fontsize = 20, fontname = 'Times New Roman', color = 'darkred')

plt.vlines(0.10, ymin = 0, ymax = 1.2e-19, colors = 'darkred', linestyles = 'dashed')
plt.text(0.104, 5e-20, r'$\nu = \frac{\Omega}{2}$', verticalalignment='center', fontsize = 20, fontname = 'Times New Roman', color = 'darkred')

# x and y range of plotting 
y1, y2 = 0.0, 1.2e-19     # y-axis range: (y1, y2)

plt.xlim(0.09, 0.25)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(0.1)
x_minor_locator = MultipleLocator(0.02)
y_major_locator = MultipleLocator(5e-20)
y_minor_locator = MultipleLocator(1e-20)

# x-axis and LHS y-axis
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 8, labelsize = 10, color = 'navy')
ax.tick_params(which = 'minor', length = 4, color = 'navy')
ax.spines['left'].set_color("navy")
ax.spines['left'].set_linewidth(2)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

# RHS y-axis
ax2 = ax.twinx()

data = np.loadtxt("./Resonance-long-lossless/pg_n2_summary.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,1], '-o', markersize = 8, color = 'red')

y1, y2 = 0.0, 1.2e-24     # y-axis range: (y1, y2)
plt.ylim(y1, y2)

y_major_locator = MultipleLocator(5e-25)
y_minor_locator = MultipleLocator(1e-25)
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8, labelsize = 10, color = 'red')
ax2.tick_params(which = 'minor', length = 4, color = 'red')
# ax2.axes.yaxis.set_ticklabels([])
ax2.spines['right'].set_color("red")
ax2.spines['right'].set_linewidth(2)

x1_label = ax2.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax2.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

# format left y-axis in scientific notation like panel (a)
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# format right y-axis in scientific notation like panel (a)
ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax2.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax2.yaxis.get_offset_text().set_size(16)
ax2.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel(r'$\Omega$ (eV)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$\langle P_{\mathrm{G}, \nu = 1} \rangle$', font = 'Times New Roman', size = 20, labelpad = 20, color = 'navy')
ax2.set_ylabel(r'$\langle P_{\mathrm{G}, \nu = 2} \rangle$', font = 'Times New Roman', size = 20, labelpad = 20, color = 'red')
plt.legend(title = '(d)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================

plt.savefig("FigS6.pdf", bbox_inches='tight')
