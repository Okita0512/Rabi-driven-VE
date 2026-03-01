import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
from matplotlib import font_manager as fm
from matplotlib.pyplot import MultipleLocator, tick_params

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
legendsize = 48         # size for panel labels

fig = plt.figure(figsize=(8, 6), dpi=128)
fig.subplots_adjust(left=0.15, right=0.92, top=0.92, bottom=0.15)

# ==============================================================================================
#                                      FigS9
#   P_g,v=1 vs time for varying N = 10^2, 10^3, 10^4, 10^5 (folders 2, 3, 4, 5)
# ==============================================================================================

ax = plt.gca()

# Curves truly overlap in value (N-convergence); distinguish by
# linestyle + marker shape + staggered marker positions along x.
# 40001 pts over 20 ps → markevery=(start, 4000) gives ~10 markers/curve
# stagger start by 1000 pts (0.5 ps) so markers fall at different x.
folders = [
    ("2", r"$N = 10^2$",  '-',   'C0', 'o', (0,    4000)),
    ("3", r"$N = 10^3$",  '--',  'C1', 's', (1000, 4000)),
    ("4", r"$N = 10^4$",  ':',   'C2', '^', (2000, 4000)),
    ("5", r"$N = 10^5$",  '-.',  'C3', 'D', (3000, 4000)),
]

for folder, label, ls, color, marker, markevery in folders:
    data = np.loadtxt(f"./{folder}/Vib_pops_g.dat")
    N = 10 ** int(folder)
    # time in column 0 (fs), convert to ps; P_g,v=1 in column 2, multiplied by N
    ax.plot(data[:, 0] / 1000, data[:, 2] * N**2, ls, color=color, label=label,
            marker=marker, markevery=markevery,
            markerfacecolor='none', markersize=7, markeredgewidth=1.5)

# ==============================================================================================
#                                      Axis setup
# ==============================================================================================

time = 20   # x-axis range in ps

ax.set_xlim(0.0, time)
ax.set_ylim(0.0, 2.0e-7)

# x-axis ticks
x_major_locator = MultipleLocator(5)
x_minor_locator = MultipleLocator(1)
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)

# y-axis ticks (ylim 0 to 2e-7)
y_major_locator = MultipleLocator(5e-8)
y_minor_locator = MultipleLocator(1e-8)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)

ax.tick_params(which='major', length=8, labelsize=20, direction='in')
ax.tick_params(which='minor', length=4, direction='in')

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

# format left y-axis in scientific notation
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# RHS y-axis: mirror ticks only, no labels
ax2 = ax.twinx()
ax2.set_ylim(0.0, 2.0e-7)
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.yaxis.set_major_formatter(NullFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
ax2.tick_params(which='major', length=8, direction='in')
ax2.tick_params(which='minor', length=4, direction='in')

# Axis labels
ax.set_xlabel('time (ps)', font='Times New Roman', size=20)
ax.set_ylabel(r'$N^2 \cdot P_{\mathrm{g}, \nu = 1}~(t)$', font='Times New Roman', size=20, labelpad=20)

# Legend
ax.legend(loc='upper left', frameon=False, prop=font, markerscale=1, ncol=2)

plt.savefig("FigS9.pdf", bbox_inches='tight')
plt.show()