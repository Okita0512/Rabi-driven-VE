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
fig = plt.figure(figsize=(6, 6), dpi = 128)
# fig.subplots_adjust(hspace = 0.2, wspace = 0.35)

legend_x, legend_y = - 0.35, 1.03
transparency = .4
legendsize = 48         # size for legend

# ==============================================================================================
#                                      Fig s4     
# ==============================================================================================

data = np.loadtxt("./0.20 - lossless/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"lossless")

data = np.loadtxt("./0.20 - lossy - kappa=1/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\kappa$ = 1 fs$^{-1}$")

data = np.loadtxt("./0.20 - lossy - kappa=2/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\kappa$ = 2 fs$^{-1}$")

data = np.loadtxt("./0.20 - lossy - kappa=5/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\kappa$ = 5 fs$^{-1}$")

data = np.loadtxt("./0.20 - lossy - kappa=10/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\kappa$ = 10 fs$^{-1}$")

data = np.loadtxt("./0.20 - lossy - kappa=20/Vib_pops_g.dat")

plt.plot(data[:,0] / 1000, data[:,2], '-', label = r"$\kappa$ = 20 fs$^{-1}$")

# ==============================================================================================

# x and y range of plotting 
time = 20              # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 2.4e-15      # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(5)
x_minor_locator = MultipleLocator(1)
y_major_locator = MultipleLocator(1e-15)
y_minor_locator = MultipleLocator(2e-16)

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
ax.set_ylabel(r'$P_{\mathrm{g}, \nu = 1}$', font = 'Times New Roman', size = 20, labelpad = 20)
# ax.set_title(r'', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1, ncol = 2)
# plt.legend(title = '(a)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================

plt.savefig("FigS4.pdf", bbox_inches='tight')
