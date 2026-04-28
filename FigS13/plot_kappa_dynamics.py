import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import ScalarFormatter
from matplotlib.pyplot import MultipleLocator

# ==============================================================================================
#                                       Font setup (Helvetica throughout)
# ==============================================================================================

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

plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["mathtext.default"] = "regular"
set_helvetica()

# ==============================================================================================
#                                   Global style constants
# ==============================================================================================

lw          = 2.5
lsize       = 24
offsetsize  = 16
legendsize  = 48          # panel label size (Helvetica, from rcParams)
legend_x    = -0.28       # panel label anchor x (axes fraction, outside left)
legend_y    = 0.92        # panel label anchor y (axes fraction, just above top)

font_legend = {'size': 16}   # inherits Helvetica from rcParams

# vib_level_pop.dat columns with vib_trunc = 4:
#   0:time  1:P_g_n0  2:P_g_n1  3:P_g_n2  4:P_g_n3
#           5:P_e_n0  6:P_e_n1  7:P_e_n2  8:P_e_n3
COL_G1 = 2   # P_{G, v=1}
COL_G2 = 3   # P_{G, v=2}
COL_E1 = 6   # P_{E, v=1}
COL_E2 = 7   # P_{E, v=2}

BASE = os.path.dirname(os.path.abspath(__file__))
kappa_cases = [
    (r"lossless",                  "0.20_kappa=0",   "#44C2B0"),  # teal
    (r"$\kappa = 0.5$ ps$^{-1}$", "0.20_kappa=0.5", "#F5A623"),  # orange
    (r"$\kappa = 1$ ps$^{-1}$",   "0.20_kappa=1",   "#7ED321"),  # green
    (r"$\kappa = 2$ ps$^{-1}$",   "0.20_kappa=2",   "#B8860B"),  # dark golden
    (r"$\kappa = 5$ ps$^{-1}$",   "0.20_kappa=5",   "#E879A0"),  # pink
    (r"$\kappa = 10$ ps$^{-1}$",  "0.20_kappa=10",  "#C0392B"),  # dark red
    (r"$\kappa = 20$ ps$^{-1}$",  "0.20_kappa=20",  "#7B241C"),  # deeper red
]

# ==============================================================================================
#                              Figure layout  (2 rows × 3 columns)
# ==============================================================================================

fig = plt.figure(figsize=(21, 14), dpi=128)
fig.subplots_adjust(hspace=0.35, wspace=0.30)

# ==============================================================================================
#  Helpers
# ==============================================================================================

def apply_sci_y(ax, y_major, y_minor, ylim):
    ax.yaxis.set_major_locator(MultipleLocator(y_major))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor))
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax.yaxis.get_offset_text().set_size(offsetsize)
    ax.yaxis.get_offset_text().set_fontname('Times New Roman')
    ax.set_ylim(*ylim)

def apply_x(ax, xlim=(0, 2000)):
    ax.xaxis.set_major_locator(MultipleLocator(500))
    ax.xaxis.set_minor_locator(MultipleLocator(100))
    ax.set_xlim(*xlim)

def mirror_ticks(ax2, y_major, y_minor, ylim):
    ax2.yaxis.set_major_locator(MultipleLocator(y_major))
    ax2.yaxis.set_minor_locator(MultipleLocator(y_minor))
    ax2.tick_params(which='major', length=8, direction='in')
    ax2.tick_params(which='minor', length=4, direction='in')
    ax2.set_ylim(*ylim)
    ax2.axes.yaxis.set_ticklabels([])

def set_tnr_labels(ax):
    """Set Times New Roman on all tick labels of ax."""
    [lbl.set_fontname('Times New Roman') for lbl in ax.get_xticklabels()]
    [lbl.set_fontname('Times New Roman') for lbl in ax.get_yticklabels()]

def finish_panel(ax, ax2, label, y_major, y_minor, ylim):
    """Mirror ticks on ax2 and place panel label outside upper-left of ax."""
    mirror_ticks(ax2, y_major, y_minor, ylim)
    plt.tick_params(which='both', direction='in')
    ax.text(legend_x, legend_y, label, transform=ax.transAxes,
            fontsize=legendsize, va='bottom', ha='left')

# ==============================================================================================
#  Panel (a): P_UP(t) — max ~6.6e-6
# ==============================================================================================

plt.subplot(2, 3, 1)
for lbl, folder, color in kappa_cases:
    d = np.loadtxt(os.path.join(BASE, folder, "UP_LP_GS_DS_population.dat"))
    plt.plot(d[:, 0], d[:, 1], '-', linewidth=lw, color=color, label=lbl)

ax = plt.gca()
apply_x(ax)
apply_sci_y(ax, y_major=2e-6, y_minor=5e-7, ylim=(0, 8e-6))
ax.tick_params(which='major', length=8, labelsize=lsize)
ax.tick_params(which='minor', length=4)
plt.tick_params(which='both', direction='in', pad=6)
set_tnr_labels(ax)
ax.set_xlabel(r'$t$ (fs)', size=lsize, fontfamily='Times New Roman')
ax.set_ylabel(r'$P_{\mathrm{UP}}(t)$', size=lsize, labelpad=20, fontfamily='Times New Roman')

ax2 = ax.twinx()
finish_panel(ax, ax2, '(a)', y_major=2e-6, y_minor=5e-7, ylim=(0, 8e-6))

# ==============================================================================================
#  Panel (b): P_{E,v=1}(t) — max ~1.7e-6  [col 6 with vib_trunc=4]
# ==============================================================================================

plt.subplot(2, 3, 2)
for lbl, folder, color in kappa_cases:
    d = np.loadtxt(os.path.join(BASE, folder, "vib_level_pop.dat"))
    plt.plot(d[:, 0], d[:, COL_E1], '-', linewidth=lw, color=color, label=lbl)

ax = plt.gca()
apply_x(ax)
apply_sci_y(ax, y_major=5e-7, y_minor=1e-7, ylim=(0, 2e-6))
ax.tick_params(which='major', length=8, labelsize=lsize)
ax.tick_params(which='minor', length=4)
plt.tick_params(which='both', direction='in', pad=6)
set_tnr_labels(ax)
ax.set_xlabel(r'$t$ (fs)', size=lsize, fontfamily='Times New Roman')
ax.set_ylabel(r'$P_{E,\,v=1}(t)$', size=lsize, labelpad=20, fontfamily='Times New Roman')

ax2 = ax.twinx()
finish_panel(ax, ax2, '(b)', y_major=5e-7, y_minor=1e-7, ylim=(0, 2e-6))

# ==============================================================================================
#  Panel (c): P_{G,v=1}(t) — max ~3.6e-17 (machine-precision zero)
#  Legend placed here: lower center, 2 columns
# ==============================================================================================

plt.subplot(2, 3, 3)
for lbl, folder, color in kappa_cases:
    d = np.loadtxt(os.path.join(BASE, folder, "vib_level_pop.dat"))
    plt.plot(d[:, 0], d[:, COL_G1], '-', linewidth=lw, color=color, label=lbl)

ax = plt.gca()
apply_x(ax)
apply_sci_y(ax, y_major=1e-17, y_minor=2e-18, ylim=(-1e-17, 5e-17))
ax.tick_params(which='major', length=8, labelsize=lsize)
ax.tick_params(which='minor', length=4)
plt.tick_params(which='both', direction='in', pad=6)
set_tnr_labels(ax)
ax.set_xlabel(r'$t$ (fs)', size=lsize, fontfamily='Times New Roman')
ax.set_ylabel(r'$P_{G,\,v=1}(t)$', size=lsize, labelpad=20, fontfamily='Times New Roman')
ax.legend(loc='lower center', frameon=False, prop=font_legend, ncol=2, handlelength=1.5)

ax2 = ax.twinx()
finish_panel(ax, ax2, '(c)', y_major=1e-17, y_minor=2e-18, ylim=(-1e-17, 5e-17))

# ==============================================================================================
#  Panel (d): P_LP(t) — max ~1.3e-5
# ==============================================================================================

plt.subplot(2, 3, 4)
for lbl, folder, color in kappa_cases:
    d = np.loadtxt(os.path.join(BASE, folder, "UP_LP_GS_DS_population.dat"))
    plt.plot(d[:, 0], d[:, 2], '-', linewidth=lw, color=color, label=lbl)

ax = plt.gca()
apply_x(ax)
apply_sci_y(ax, y_major=5e-6, y_minor=1e-6, ylim=(0, 1.5e-5))
ax.tick_params(which='major', length=8, labelsize=lsize)
ax.tick_params(which='minor', length=4)
plt.tick_params(which='both', direction='in', pad=6)
set_tnr_labels(ax)
ax.set_xlabel(r'$t$ (fs)', size=lsize, fontfamily='Times New Roman')
ax.set_ylabel(r'$P_{\mathrm{LP}}(t)$', size=lsize, labelpad=20, fontfamily='Times New Roman')

ax2 = ax.twinx()
finish_panel(ax, ax2, '(d)', y_major=5e-6, y_minor=1e-6, ylim=(0, 1.5e-5))

# ==============================================================================================
#  Panel (e): P_{E,v=2}(t) — max ~4.1e-9  [col 7 with vib_trunc=4]
# ==============================================================================================

plt.subplot(2, 3, 5)
for lbl, folder, color in kappa_cases:
    d = np.loadtxt(os.path.join(BASE, folder, "vib_level_pop.dat"))
    plt.plot(d[:, 0], d[:, COL_E2], '-', linewidth=lw, color=color, label=lbl)

ax = plt.gca()
apply_x(ax)
apply_sci_y(ax, y_major=1e-9, y_minor=2e-10, ylim=(0, 5e-9))
ax.tick_params(which='major', length=8, labelsize=lsize)
ax.tick_params(which='minor', length=4)
plt.tick_params(which='both', direction='in', pad=6)
set_tnr_labels(ax)
ax.set_xlabel(r'$t$ (fs)', size=lsize, fontfamily='Times New Roman')
ax.set_ylabel(r'$P_{E,\,v=2}(t)$', size=lsize, labelpad=20, fontfamily='Times New Roman')

ax2 = ax.twinx()
finish_panel(ax, ax2, '(e)', y_major=1e-9, y_minor=2e-10, ylim=(0, 5e-9))

# ==============================================================================================
#  Panel (f): P_{G,v=2}(t) — max ~5e-20 (machine-precision zero)
# ==============================================================================================

plt.subplot(2, 3, 6)
for lbl, folder, color in kappa_cases:
    d = np.loadtxt(os.path.join(BASE, folder, "vib_level_pop.dat"))
    plt.plot(d[:, 0], d[:, COL_G2], '-', linewidth=lw, color=color, label=lbl)

ax = plt.gca()
apply_x(ax)
apply_sci_y(ax, y_major=1e-20, y_minor=2e-21, ylim=(-1e-20, 6e-20))
ax.tick_params(which='major', length=8, labelsize=lsize)
ax.tick_params(which='minor', length=4)
plt.tick_params(which='both', direction='in', pad=6)
set_tnr_labels(ax)
ax.set_xlabel(r'$t$ (fs)', size=lsize, fontfamily='Times New Roman')
ax.set_ylabel(r'$P_{G,\,v=2}(t)$', size=lsize, labelpad=20, fontfamily='Times New Roman')

ax2 = ax.twinx()
finish_panel(ax, ax2, '(f)', y_major=1e-20, y_minor=2e-21, ylim=(-1e-20, 6e-20))

# ==============================================================================================
#  Save
# ==============================================================================================

plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["mathtext.default"] = "regular"
plt.savefig(os.path.join(BASE, "FigS13.pdf"), bbox_inches='tight')
# plt.savefig(os.path.join(BASE, "FigS13.png"), bbox_inches='tight', dpi=150)
print("Saved FigS13.pdf and FigS13.png")
