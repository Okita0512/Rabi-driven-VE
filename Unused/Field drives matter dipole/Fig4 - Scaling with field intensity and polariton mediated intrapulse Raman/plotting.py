import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib import font_manager as fm
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
font2 = {'family':'Times New Roman', 'weight': 'roman', 'size':15}
fig = plt.figure(figsize=(25, 10), dpi = 128)
fig.subplots_adjust(hspace = 0.2, wspace = 0.4)

legend_x, legend_y = - 0.4, 1.03
transparency = .4
legendsize = 48         # size for legend
panel_label_size = 24   # size for panel labels inside axes

# ==============================================================================================
#                                      Fig 3a     
# ==============================================================================================
plt.subplot(2, 4, 1)

data = np.loadtxt("./scaling short/1meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 1 meV")

data = np.loadtxt("./scaling short/2meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 2 meV")

data = np.loadtxt("./scaling short/4meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 4 meV")

data = np.loadtxt("./scaling short/8meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 8 meV")

# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 8e-11     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(2e-11)
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

# format left y-axis in scientific notation
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
#                                      Fig 3b     
# ==============================================================================================
plt.subplot(2, 4, 2)

data = np.loadtxt("./scaling short/1meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 1 meV")

data = np.loadtxt("./scaling short/2meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 2 meV")

data = np.loadtxt("./scaling short/4meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 4 meV")

data = np.loadtxt("./scaling short/8meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 8 meV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 1.8e-4     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(5e-5)
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

# format left y-axis in scientific notation like panel (a)
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{E}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)
plt.legend(title = '(b)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig 3c     
# ==============================================================================================
plt.subplot(2, 4, 3)

def fit_loglog(x, y):
    """Return slope, intercept, R^2 for log10-log10 linear fit."""
    mask = (x > 0) & (y > 0)
    xlog = np.log10(x[mask])
    ylog = np.log10(y[mask])
    if len(xlog) < 2:
        return None
    coeffs = np.polyfit(xlog, ylog, 1)
    slope, intercept = coeffs
    y_pred = slope * xlog + intercept
    ss_res = np.sum((ylog - y_pred) ** 2)
    ss_tot = np.sum((ylog - np.mean(ylog)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2

df_energy = pd.read_csv("Scaling short/energy_summary.csv")
df = df_energy.sort_values("intensity_meV")
fit_results = []
for col, lbl, marker, color in [
    ("Evib_total_avg_eV", "Total vib energy", "o", "#1f77b4"),
    ("Evib_ground_avg_eV", "Ground vib energy", "s", "#ff7f0e"),
    ("Evib_excited_avg_eV", "Excited vib energy", "^", "#2ca02c"),
]:
    x = df["intensity_meV"].to_numpy()
    y = df[col].to_numpy()
    if col == "Evib_total_avg_eV":
        plt.loglog(
            x, y, marker=marker, linestyle="none", color=color, label=lbl,
            markerfacecolor="none", markeredgewidth=1.5, markersize=12
        )
    else:
        plt.loglog(x, y, marker=marker, linestyle="none", color=color, label=lbl)
    fit = fit_loglog(x, y)
    if fit:
        m, b, r2 = fit
        xfit = np.linspace(np.log10(x.min()), np.log10(x.max()), 50)
        yfit = m * xfit + b
        plt.plot(10**xfit, 10**yfit, color=color, linewidth=1.5)
        fit_results.append(f"{lbl} fit: y={m:.3f}x+{b:.3f}, R^2={r2:.4f}")

plt.xlim(1, 8)
plt.ylim(1e-15, 1e-3)

ax = plt.gca()
ax.tick_params(which = 'major', length = 8, labelsize = 10)
ax.tick_params(which = 'minor', length = 4)
ax.tick_params(axis = 'y', right = True, labelright = False)
ax.yaxis.set_ticks_position('both')

x_ticks = [1, 2, 3, 4, 6]
ax.set_xticks(x_ticks)
ax.set_xticklabels([str(v) for v in x_ticks])

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')

ax.set_xlabel(r"$\lambda_F$ (meV)", font = 'Times New Roman', size = 20)
ax.set_ylabel(r"$\langle E_{\nu}\rangle$ (eV)", font = 'Times New Roman', size = 20)

ax.legend(loc = 'center left', frameon = False, prop = font)

ax2 = ax.twinx()
ax2.set_yscale('log')
ax2.set_ylim(ax.get_ylim())
ax2.yaxis.set_major_locator(ax.yaxis.get_major_locator())
ax2.yaxis.set_minor_locator(ax.yaxis.get_minor_locator())
ax2.tick_params(which = 'major', length = 8, labelright = False)
ax2.tick_params(which = 'minor', length = 4, labelright = False)

plt.tick_params(which = 'both', direction = 'in')

plt.legend(title = '(c)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)
if fit_results:
    print("Fig4 panel c fit results:")
    for entry in fit_results:
        print("  " + entry)

# ==============================================================================================
#                                      Fig 3d     
# ==============================================================================================
plt.subplot(2, 4, 4)

df_pop = pd.read_csv("Scaling short/pop_summary.csv")
df = df_pop.sort_values("intensity_meV")
fit_results = []
for col, lbl, marker, color in [
    ("P_g_n1_avg", r"$\langle P_{\mathrm{G}, \nu = 1} \rangle$", "o", "#1f77b4"),
    ("P_g_n2_avg", r"$\langle P_{\mathrm{G}, \nu = 2} \rangle$", "s", "#ff7f0e"),
    ("P_e_n1_avg", r"$\langle P_{\mathrm{E}, \nu = 1} \rangle$", "^", "#2ca02c"),
    ("P_e_n2_avg", r"$\langle P_{\mathrm{E}, \nu = 2} \rangle$", "D", "#d62728"),
]:
    x = df["intensity_meV"].to_numpy()
    y = df[col].to_numpy()
    plt.loglog(x, y, marker=marker, linestyle="none", color=color, label=lbl)
    fit = fit_loglog(x, y)
    if fit:
        m, b, r2 = fit
        xfit = np.linspace(np.log10(x.min()), np.log10(x.max()), 50)
        yfit = m * xfit + b
        plt.plot(10**xfit, 10**yfit, color=color, linewidth=1.5)
        fit_results.append(f"{lbl} fit: y={m:.3f}x+{b:.3f}, R^2={r2:.4f}")
plt.xlim(1, 8)
plt.ylim(1e-17, 1e0)
ax = plt.gca()
ax.set_xlabel(r"$\lambda_F$ (meV)", font = 'Times New Roman', size = 20)
ax.set_ylabel(r"Averaged Population     ", font = 'Times New Roman', size = 20)
ax.tick_params(which = 'major', length = 8, labelsize = 20)
ax.tick_params(which = 'minor', length = 4)
ax.tick_params(which = 'both', direction = 'in')
x_ticks = [1, 2, 3, 4, 6]
ax.set_xticks(x_ticks)
ax.set_xticklabels([str(v) for v in x_ticks])
x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]
ax.legend(loc = 'upper left', frameon = False, prop = font2, markerscale = 1, ncol = 2)

ax2 = ax.twinx()
ax2.set_yscale('log')
ax2.set_ylim(ax.get_ylim())
ax2.yaxis.set_major_locator(ax.yaxis.get_major_locator())
ax2.yaxis.set_minor_locator(ax.yaxis.get_minor_locator())
ax2.tick_params(which = 'major', length = 8, labelright = False)
ax2.tick_params(which = 'minor', length = 4, labelright = False)

plt.tick_params(which = 'both', direction = 'in')

plt.legend(title = '(d)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)
if fit_results:
    print("Fig4 panel d fit results:")
    for entry in fit_results:
        print("  " + entry)

# ==============================================================================================
#                                      Fig 3e     
# ==============================================================================================
plt.subplot(2, 4, 5)

data = np.loadtxt("./scaling long (pump UP)/1meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 1 meV")

data = np.loadtxt("./scaling long (pump UP)/2meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 2 meV")

data = np.loadtxt("./scaling long (pump UP)/4meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 4 meV")

data = np.loadtxt("./scaling long (pump UP)/8meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 8 meV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 2e-6     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(1e-6)
y_minor_locator = MultipleLocator(2e-7)

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

# format left y-axis in scientific notation
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{G}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1)
plt.legend(title = '(e)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# Inset: long-time dynamics (0-1000 fs) inside the blank area
ax_main = plt.gca()
ax_inset = inset_axes(ax_main, width = "55%", height = "32%", loc = "lower right", borderpad = 2.8)
data = np.loadtxt("./scaling long (pump UP)/1meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 1 meV")

data = np.loadtxt("./scaling long (pump UP)/2meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 2 meV")

data = np.loadtxt("./scaling long (pump UP)/4meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 4 meV")

data = np.loadtxt("./scaling long (pump UP)/8meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,2], '-', label = r"$\lambda_F$ = 8 meV")

y1, y2 = 0, 2e-19
y_major_locator = MultipleLocator(1e-19)
y_minor_locator = MultipleLocator(2e-20)

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

# format inset y-axis in scientific notation
ax_inset.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax_inset.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax_inset.yaxis.get_offset_text().set_size(10)
ax_inset.yaxis.get_offset_text().set_fontname('Times New Roman')

# ax_inset.set_xlabel(r't (fs)', size = 12)
ax_inset.set_ylabel(r'$P_{\mathrm{G}, \nu = 1}~(t)$', size = 12)

# ==============================================================================================
#                                      Fig 3f     
# ==============================================================================================
plt.subplot(2, 4, 6)

# data = np.loadtxt("Vg.dat")
data = np.loadtxt("./scaling long (pump UP)/1meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 1 meV")

data = np.loadtxt("./scaling long (pump UP)/2meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 2 meV")

data = np.loadtxt("./scaling long (pump UP)/4meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 4 meV")

data = np.loadtxt("./scaling long (pump UP)/8meV/Vib_level_pop.dat")

plt.plot(data[:,0], data[:,5], '-', label = r"$\lambda_F$ = 8 meV")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 7e-2     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(2e-2)
y_minor_locator = MultipleLocator(1e-2)

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

# format left y-axis in scientific notation
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 0))
ax.yaxis.get_offset_text().set_size(16)
ax.yaxis.get_offset_text().set_fontname('Times New Roman')

# name of x, y axis and the panel
ax.set_xlabel('time (fs)', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$P_{\mathrm{E}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)
plt.legend(title = '(f)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig 3g     
# ==============================================================================================
plt.subplot(2, 4, 7)

df_energy = pd.read_csv("Scaling long (pump UP)/energy_summary.csv")
df = df_energy.sort_values("intensity_meV")
fit_results = []
for col, lbl, marker, color in [
    ("Evib_total_avg_eV", "Total vib energy", "o", "#1f77b4"),
    ("Evib_ground_avg_eV", "Ground vib energy", "s", "#ff7f0e"),
    ("Evib_excited_avg_eV", "Excited vib energy", "^", "#2ca02c"),
]:
    x = df["intensity_meV"].to_numpy()
    y = df[col].to_numpy()
    if col == "Evib_total_avg_eV":
        plt.loglog(
            x, y, marker=marker, linestyle="none", color=color, label=lbl,
            markerfacecolor="none", markeredgewidth=1.5, markersize=12
        )
    else:
        plt.loglog(x, y, marker=marker, linestyle="none", color=color, label=lbl)
    fit = fit_loglog(x, y)
    if fit:
        m, b, r2 = fit
        xfit = np.linspace(np.log10(x.min()), np.log10(x.max()), 50)
        yfit = m * xfit + b
        plt.plot(10**xfit, 10**yfit, color=color, linewidth=1.5)
        fit_results.append(f"{lbl} fit: y={m:.3f}x+{b:.3f}, R^2={r2:.4f}")
plt.xlim(1, 8)
plt.ylim(1e-20, 1e0)
ax = plt.gca()
ax.set_xlabel(r"$\lambda_F$ (meV)", font = 'Times New Roman', size = 20)
ax.set_ylabel(r"$\langle E_{\nu}\rangle$ (eV)", font = 'Times New Roman', size = 20)
ax.tick_params(which = 'major', length = 8, labelsize = 20)
ax.tick_params(which = 'minor', length = 4)
ax.tick_params(which = 'both', direction = 'in')
x_ticks = [1, 2, 3, 4, 6]
ax.set_xticks(x_ticks)
ax.set_xticklabels([str(v) for v in x_ticks])
x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]
ax.legend(loc = 'center left', frameon = False, prop = font, markerscale = 1)

ax2 = ax.twinx()
ax2.set_yscale('log')
ax2.set_ylim(ax.get_ylim())
ax2.yaxis.set_major_locator(ax.yaxis.get_major_locator())
ax2.yaxis.set_minor_locator(ax.yaxis.get_minor_locator())
ax2.tick_params(which = 'major', length = 8, labelright = False)
ax2.tick_params(which = 'minor', length = 4, labelright = False)

plt.tick_params(which = 'both', direction = 'in')

plt.legend(title = '(g)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)
if fit_results:
    print("Fig4 panel g fit results:")
    for entry in fit_results:
        print("  " + entry)

# ==============================================================================================
#                                      Fig 3h     
# ==============================================================================================
plt.subplot(2, 4, 8)

df_pop = pd.read_csv("Scaling long (pump UP)/pop_summary.csv")
df = df_pop.sort_values("intensity_meV")
fit_results = []
for col, lbl, marker, color in [
    ("P_g_n1_avg", r"$\langle P_{\mathrm{G}, \nu = 1} \rangle$", "o", "#1f77b4"),
    ("P_g_n2_avg", r"$\langle P_{\mathrm{G}, \nu = 2} \rangle$", "s", "#ff7f0e"),
    ("P_e_n1_avg", r"$\langle P_{\mathrm{E}, \nu = 1} \rangle$", "^", "#2ca02c"),
    ("P_e_n2_avg", r"$\langle P_{\mathrm{E}, \nu = 2} \rangle$", "D", "#d62728"),
]:
    x = df["intensity_meV"].to_numpy()
    y = df[col].to_numpy()
    plt.loglog(x, y, marker=marker, linestyle="none", color=color, label=lbl)
    fit = fit_loglog(x, y)
    if fit:
        m, b, r2 = fit
        xfit = np.linspace(np.log10(x.min()), np.log10(x.max()), 50)
        yfit = m * xfit + b
        plt.plot(10**xfit, 10**yfit, color=color, linewidth=1.5)
        fit_results.append(f"{lbl} fit: y={m:.3f}x+{b:.3f}, R^2={r2:.4f}")
plt.xlim(1, 8)
plt.ylim(1e-23, 1e0)
ax = plt.gca()
ax.set_xlabel(r"$\lambda_F$ (meV)", font = 'Times New Roman', size = 20)
ax.set_ylabel(r"Averaged Population     ", font = 'Times New Roman', size = 20)
ax.tick_params(which = 'major', length = 8, labelsize = 20)
ax.tick_params(which = 'minor', length = 4)
ax.tick_params(which = 'both', direction = 'in')
x_ticks = [1, 2, 3, 4, 6]
ax.set_xticks(x_ticks)
ax.set_xticklabels([str(v) for v in x_ticks])
x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]
ax.legend(loc = 'center left', frameon = False, prop = font2, markerscale = 1, ncol = 2)

ax2 = ax.twinx()
ax2.set_yscale('log')
ax2.set_ylim(ax.get_ylim())
ax2.yaxis.set_major_locator(ax.yaxis.get_major_locator())
ax2.yaxis.set_minor_locator(ax.yaxis.get_minor_locator())
ax2.tick_params(which = 'major', length = 8, labelright = False)
ax2.tick_params(which = 'minor', length = 4, labelright = False)

plt.tick_params(which = 'both', direction = 'in')

plt.legend(title = '(h)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

if fit_results:
    print("Fig4 panel h fit results:")
    for entry in fit_results:
        print("  " + entry)



plt.savefig("Fig4.pdf", bbox_inches='tight')
