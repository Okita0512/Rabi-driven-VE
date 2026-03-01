import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import ScalarFormatter, MultipleLocator
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

plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams["font.family"] = "Helvetica"
set_helvetica()
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["mathtext.default"] = "regular"

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(6, 5), dpi = 128)

legend_x, legend_y = - 0.45, 1.03
transparency = .4
legendsize = 48         # size for legend

# ==============================================================================================
#                                      Fig S12
# ==============================================================================================
ax = plt.subplot(1, 1, 1)

data = np.loadtxt("./Resonance-short-lossless/pe_n1_summary.csv", delimiter = ',', skiprows = 1)

plt.plot(data[:,0], data[:,1], '-o', markersize = 8, color = 'navy')

plt.vlines(0.201, ymin = 0.3e-6, ymax = 1.0e-6, colors = 'darkred', linestyles = 'dashed')
plt.text(0.2015, 0.5e-6, r'$\Omega = 0.201$ eV', verticalalignment='center', fontsize = 20, fontname = 'Times New Roman', color = 'darkred')


# x and y range of plotting
y1, y2 = 0.3e-6, 1.0e-6     # y-axis range: (y1, y2)

plt.xlim(0.19, 0.21)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(0.01)
x_minor_locator = MultipleLocator(0.002)
y_major_locator = MultipleLocator(5e-7)
y_minor_locator = MultipleLocator(1e-7)

# x-axis and LHS y-axis
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

# format left y-axis in scientific notation
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel(r'$\Omega$ (eV)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$\langle P_{\mathrm{E}, \nu = 1} \rangle$', font = 'Times New Roman', size = 20, labelpad = 20, color = 'navy')



plt.savefig("FigS12.pdf", bbox_inches='tight')
