import os
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
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

def _find_peaks_simple(y):
    """Return indices of simple local maxima (y[i] > neighbors)."""
    inds = []
    for i in range(1, len(y) - 1):
        if y[i] > y[i - 1] and y[i] > y[i + 1]:
            inds.append(i)
    return np.array(inds, dtype=int)

def estimate_period_from_time(t, y, min_prominence_frac=0.1):
    """Estimate oscillation period from time series (t, y).

    Strategy: find local maxima, filter by prominence threshold relative
    to (y.max()-y.min()), return median spacing between peak times.
    If insufficient peaks, return np.nan.
    """
    if len(t) < 3:
        return np.nan
    peaks = _find_peaks_simple(y)
    if peaks.size < 2:
        return np.nan
    # filter peaks by prominence relative to signal span
    span = np.nanmax(y) - np.nanmin(y)
    if span <= 0:
        return np.nan
    prominences = y[peaks] - (np.minimum(y[peaks - 1], y[peaks + 1]))
    thresh = max(min_prominence_frac * span, 1e-16)
    good = peaks[prominences >= thresh]
    if good.size < 2:
        # relax threshold once
        good = peaks
    if good.size < 2:
        return np.nan
    times = t[good]
    diffs = np.diff(times)
    # return median spacing as robust estimate
    return float(np.median(diffs))

def load_vib_file_try(path_base, n):
    """Try several filename variants and return loaded array or None."""
    candidates = [
        os.path.join(path_base, f"N={n}", "vib_level_pop.dat"),
        os.path.join(path_base, f"N={n}", "Vib_level_pop.dat"),
        os.path.join(path_base, f"N={n}", "vib_level_pop.dat".replace('v','V')),
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return np.loadtxt(p)
            except Exception:
                continue
    return None
font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
font2 = {'family':'Times New Roman', 'weight': 'roman', 'size':15}
fig = plt.figure(figsize=(19, 5), dpi = 128)
fig.subplots_adjust(hspace = 0.2, wspace = 0.4)

legend_x, legend_y = - 0.4, 1.03
transparency = .4
legendsize = 48         # size for legend
panel_label_size = 24   # size for panel labels inside axes



# ==============================================================================================
#                                      Fig 3a
# ==============================================================================================
plt.subplot(1, 3, 1)

data = np.loadtxt(os.path.join("Scaling short", "N=1", "Vib_level_pop.dat"))
plt.plot(data[:,0], 0 * 1e-5 + 1 * data[:,5], '-', label = r"$N$ = 1")

data = np.loadtxt(os.path.join("Scaling short", "N=2", "Vib_level_pop.dat"))
plt.plot(data[:,0], 1 * 1e-5 + 2 * data[:,5], '-', label = r"$N$ = 2")

data = np.loadtxt(os.path.join("Scaling short", "N=4", "Vib_level_pop.dat"))
plt.plot(data[:,0], 2 * 1e-5 + 4 * data[:,5], '-', label = r"$N$ = 4")

data = np.loadtxt(os.path.join("Scaling short", "N=8", "Vib_level_pop.dat"))
plt.plot(data[:,0], 3 * 1e-5 + 8 * data[:,5], '-', label = r"$N$ = 8")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 2000            # x-axis range: (0, time)
# y1, y2 = -0.2, 0.2     # y-axis range: (y1, y2)
y1, y2 = 0, 4.8e-5     # y-axis range: (y1, y2)

plt.xlim(0.0, time)
plt.ylim(y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(500)
x_minor_locator = MultipleLocator(100)
y_major_locator = MultipleLocator(1e-5)
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
ax.set_ylabel(r'$N \cdot P_{\mathrm{E}, \nu = 1}~(t)$', font = 'Times New Roman', size = 20, labelpad = 20)
ax.legend(loc = 'upper left', frameon = False, prop = font, ncol = 2)
plt.legend(title = '(a)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig 3b (main) - Oscillation period vs N
# ==============================================================================================
plt.subplot(1, 3, 2)
path_base = "Scaling short"
Ns = [1,2,3,4,5,6,7,8]

periods = []
for n in Ns:
    arr = load_vib_file_try(path_base, n)
    if arr is None:
        periods.append(np.nan)
        continue
    t = arr[:,0]
    # P_e_n1 corresponds to column index 5 in the vib files
    y = arr[:,5]
    # Two-pass envelope extraction: first estimate the fast oscillation period
    # from all raw peaks, then smooth by that scale to isolate the slow envelope.
    fast_peaks = _find_peaks_simple(y)
    if fast_peaks.size >= 2:
        fast_period_pts = float(np.median(np.diff(fast_peaks)))
    else:
        fast_period_pts = len(t) / 20.0
    sigma = max(fast_period_pts / 2.0, 1.0)
    y_env = gaussian_filter1d(y, sigma=sigma)
    # Find envelope peaks; apply height threshold (>= 20% of max) to exclude
    # spurious local maxima that appear at envelope minima after smoothing.
    env_peaks = _find_peaks_simple(y_env)
    ymax = y_env.max()
    if env_peaks.size >= 2 and ymax > 0:
        good = env_peaks[y_env[env_peaks] >= 0.2 * ymax]
        if good.size < 2:
            good = env_peaks
        period = float(np.median(np.diff(t[good])))
    else:
        period = np.nan
    periods.append(period)
periods = np.array(periods)

plt.plot(Ns, periods, marker='o', linestyle='none', color='#1f77b4')
ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')

# Least-squares power-law fit in log-log space
Ns_arr = np.array(Ns, dtype=float)
mask = ~np.isnan(periods)
slope, intercept = np.polyfit(np.log10(Ns_arr[mask]), np.log10(periods[mask]), 1)
N_fit = np.linspace(1, 8, 200)
T_fit = 10**intercept * N_fit**slope
plt.plot(N_fit, T_fit, '--', color='gray', linewidth=1.5)

# Print extracted periods and fit result
print("Fig5 panel b extracted periods:")
for n, p in zip(Ns, periods):
    if np.isnan(p):
        print(f"  N={n}: T=NaN")
    else:
        print(f"  N={n}: T={p:.2f} fs")
log_N = np.log10(Ns_arr[mask])
log_T = np.log10(periods[mask])
log_T_pred = slope * log_N + intercept
ss_res = np.sum((log_T - log_T_pred) ** 2)
ss_tot = np.sum((log_T - np.mean(log_T)) ** 2)
r2_b = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
print(f"Fig5 panel b fit result: y={slope:.3f}x+{intercept:.3f}, R^2={r2_b:.4f}")

ax.set_xlabel(r"$N$", font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$T$ (fs)', font = 'Times New Roman', size = 20)
ax.set_xlim(1, 8)
ax.set_xticks([1, 2, 3, 4, 6])
ax.set_xticklabels(['1','2','3','4','6'], fontname='Times New Roman', fontsize=20)
ax.set_yticks([200, 300, 400, 500, 600])
ax.set_yticklabels(['200','300','400','500','600'], fontname='Times New Roman', fontsize=20)

ax.tick_params(which='major', length=8, labelsize=20, direction='in')
ax.tick_params(which='minor', length=4, direction='in')
ax.annotate(rf'$T\propto N^{{{slope:.2f}}}$',
            xy=(0.97, 0.05), xycoords='axes fraction',
            ha='right', va='bottom', fontsize=36, fontfamily='Times New Roman')

plt.legend(title = '(b)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================
#                                      Fig 3c     
# ==============================================================================================
plt.subplot(1, 3, 3)

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
    ("Evib_ground_avg_eV", r"$\langle E_{\mathrm{vib,G}} \rangle$", "s", "#ff7f0e"),
    ("Evib_excited_avg_eV", r"$\langle E_{\mathrm{vib,E}} \rangle$", "^", "#2ca02c"),
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
plt.ylim(1e-18, 1e-5)

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

ax.set_xlabel(r"$N$", font = 'Times New Roman', size = 20)
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
    print("Fig5 panel c fit results:")
    for entry in fit_results:
        print("  " + entry)



plt.savefig("Fig5.pdf", bbox_inches='tight')
