import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import MultipleLocator, ScalarFormatter


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

    regular_candidates = [
        path for path in candidates
        if os.path.basename(path).lower() in {"helvetica.ttf", "helvetica_0.ttf", "helvetica_1.ttf"}
    ]
    best_path = sorted(regular_candidates or candidates, key=font_score)[0]
    fm.fontManager.addfont(best_path)
    font_name = fm.FontProperties(fname=best_path).get_name()
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [font_name, "Helvetica", "Arial"]
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["axes.labelweight"] = "normal"
    plt.rcParams["axes.titleweight"] = "normal"
    plt.rcParams["mathtext.default"] = "regular"
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42


def set_linear_ticks(ax, set_x=True, set_y=True):
    if set_x:
        x0, x1 = ax.get_xlim()
        x_range = abs(x1 - x0)
        if np.isfinite(x_range) and x_range > 0:
            x_major = x_range / 5.0
            ax.xaxis.set_major_locator(MultipleLocator(x_major))
            ax.xaxis.set_minor_locator(MultipleLocator(x_major / 5.0))
    if set_y:
        y0, y1 = ax.get_ylim()
        y_range = abs(y1 - y0)
        if np.isfinite(y_range) and y_range > 0:
            y_major = y_range / 5.0
            ax.yaxis.set_major_locator(MultipleLocator(y_major))
            ax.yaxis.set_minor_locator(MultipleLocator(y_major / 5.0))


def resolve_existing_path(*candidate_paths):
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"None of the candidate paths exist: {candidate_paths}")


def load_se_vib_pop(nu_label):
    return np.loadtxt(
        resolve_existing_path(
            os.path.join("SE", "N=4", nu_label, "vib_level_pop.dat"),
            os.path.join("SE", nu_label, "vib_level_pop.dat"),
        ),
        comments="#",
    )


def load_se_summary(n_value):
    filename = f"energy_summary_N{n_value}.csv"
    return np.loadtxt(
        resolve_existing_path(
            os.path.join("SE", filename),
            os.path.join("SE", f"N={n_value}", filename),
        ),
        delimiter=",",
        skiprows=1,
    )


plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["mathtext.default"] = "regular"
set_helvetica()

MF_N_MOLECULES = 10000

se_vib_pop_199 = load_se_vib_pop("0.199")
se_vib_pop_195 = load_se_vib_pop("0.195")
se_vib_pop_19 = load_se_vib_pop("0.19")
se_summary_N1 = load_se_summary(1)
se_summary_N2 = load_se_summary(2)
se_summary_N4 = load_se_summary(4)
se_summary_N8 = load_se_summary(8)
mf_vib_pops_g_199 = np.loadtxt("MF/0.199/Vib_pops_g.dat")
mf_vib_pops_g_199_long = np.loadtxt("MF/0.199-long-time/Vib_pops_g.dat")
mf_vib_pops_g_195 = np.loadtxt("MF/0.195/Vib_pops_g.dat")
mf_vib_pops_g_19 = np.loadtxt("MF/0.19/Vib_pops_g.dat")
mf_evib_avg = np.loadtxt("MF/Evib_per_molecule_avg.csv", delimiter=",", skiprows=1)
mf_kappa_sweep = np.genfromtxt(
    "MF/kappa_sweep/kappa_sweep_summary.csv", delimiter=",", names=True, encoding="utf-8"
)

fig, axes = plt.subplots(2, 2, figsize=(14, 14), dpi=128)
plt.subplots_adjust(hspace=0.2, wspace=0.35)

# (a) SE P_e_1 only
ax = axes[0, 0]
ax.plot(se_vib_pop_199[:, 0], se_vib_pop_199[:, 7], color="navy", label=r"$\nu=0.199$ eV")
ax.plot(se_vib_pop_195[:, 0], se_vib_pop_195[:, 7], color="firebrick", label=r"$\nu=0.195$ eV")
ax.plot(se_vib_pop_19[:, 0], se_vib_pop_19[:, 7], color="forestgreen", label=r"$\nu=0.19$ eV")
ax.set_xlim(0, 1500)
ax.set_ylim(-0.005, 0.17)
ax.set_xlabel("time (fs)", fontsize=24)
ax.set_ylabel(r"$P_{\mathrm{E},\nu = 1}(t)$", fontsize=24)
ax.text(
    -0.3, 0.90, "(a)", transform=ax.transAxes, fontname="Helvetica", fontsize=48, clip_on=False
)
ax.xaxis.set_major_locator(MultipleLocator(500))
ax.xaxis.set_minor_locator(MultipleLocator(100))
ax.yaxis.set_major_locator(MultipleLocator(0.025))
ax.yaxis.set_minor_locator(MultipleLocator(0.005))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
ax.yaxis.get_offset_text().set_size(20)
set_linear_ticks(ax, set_x=False, set_y=False)
ax.tick_params(direction="in", labelsize=20, which="both")
ax.tick_params(axis="x", which="major", length=10)
ax.tick_params(axis="x", which="minor", length=5)
ax.tick_params(axis="y", which="major", length=10)
ax.tick_params(axis="y", which="minor", length=5)
ax.legend(frameon=False, fontsize=17, loc="upper right", ncol=2)

# (b) SE summary for N = 1, 2, 4, 8
ax = axes[0, 1]
se_N_data = [
    (1, se_summary_N1, "#7b2cbf", r"$N=1$"),
    (2, se_summary_N2, "#1f77b4", r"$N=2$"),
    (4, se_summary_N4, "#2ca02c", r"$N=4$"),
    (8, se_summary_N8, "#d62728", r"$N=8$"),
]
for N_val, data, color, label in se_N_data:
    ax.plot(data[:, 0], N_val * data[:, 1], "-", color=color, linewidth=3.0, label=label)
ax.set_xlim(0.16, 0.24)
ax.set_ylim(0.0005, 0.06)
ax.axvline(0.199, color="black", linestyle="--", linewidth=1.5)
ax.text(
    0.206,
    0.053,
    r"$\nu = 0.199$ eV",
    color="black",
    fontsize=24,
)
ax.set_xlabel(r"$\nu$ (eV)", fontsize=24)
ax.set_ylabel(r"$\langle E_{\mathrm{vib, E}}\rangle$ (eV)", fontsize=24)
ax.text(
    -0.3, 0.90, "(b)", transform=ax.transAxes, fontname="Helvetica", fontsize=48, clip_on=False
)
ax.xaxis.set_major_locator(MultipleLocator(0.02))
ax.xaxis.set_minor_locator(MultipleLocator(0.004))
ax.yaxis.set_major_locator(MultipleLocator(0.01))
ax.yaxis.set_minor_locator(MultipleLocator(0.002))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
ax.yaxis.get_offset_text().set_size(20)
set_linear_ticks(ax, set_x=False, set_y=False)
ax.tick_params(direction="in", labelsize=20, which="both")
ax.tick_params(axis="x", which="major", length=10)
ax.tick_params(axis="x", which="minor", length=5)
ax.tick_params(axis="y", which="major", length=10)
ax.tick_params(axis="y", which="minor", length=5)
ax.legend(frameon=False, fontsize=18, loc="upper left")

# (c) MF P_g_1 from the 3rd column
ax = axes[1, 0]
ax.plot(mf_vib_pops_g_199[:, 0], mf_vib_pops_g_199[:, 2], color="navy", label=r"$\nu=0.199$ eV")
ax.plot(mf_vib_pops_g_195[:, 0], mf_vib_pops_g_195[:, 2], color="firebrick", label=r"$\nu=0.195$ eV")
ax.plot(mf_vib_pops_g_19[:, 0], mf_vib_pops_g_19[:, 2], color="forestgreen", label=r"$\nu=0.19$ eV")
ax.set_xlim(0, 1500)
ax.set_ylim(-5e-8, 1.2e-6)
ax.set_xlabel("time (fs)", fontsize=24)
ax.set_ylabel(r"$P_{\mathrm{g},\nu = 1}(t)$", fontsize=24)
ax.text(
    -0.3, 0.90, "(c)", transform=ax.transAxes, fontname="Helvetica", fontsize=48, clip_on=False
)
ax.xaxis.set_major_locator(MultipleLocator(500))
ax.xaxis.set_minor_locator(MultipleLocator(100))
ax.yaxis.set_major_locator(MultipleLocator(0.5e-6))
ax.yaxis.set_minor_locator(MultipleLocator(0.1e-6))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
ax.yaxis.get_offset_text().set_size(20)
set_linear_ticks(ax, set_x=False, set_y=False)
ax.tick_params(direction="in", labelsize=20, which="both")
ax.tick_params(axis="x", which="major", length=10)
ax.tick_params(axis="x", which="minor", length=5)
ax.tick_params(axis="y", which="major", length=10)
ax.tick_params(axis="y", which="minor", length=5)
ax.legend(frameon=False, fontsize=16, loc="lower right", bbox_to_anchor=(1.0, 0.10))

# Inset for (c): long-time P_{g,v=1} for 0.199 eV (up to 100 ps)
ax_inset = ax.inset_axes([0.08, 0.56, 0.54, 0.38])
ax_inset.plot(
    mf_vib_pops_g_199_long[:, 0] / 1000,  # fs -> ps
    mf_vib_pops_g_199_long[:, 2],
    color="navy",
    linewidth=0.8,
)
ax_inset.set_xlim(0, 100)
ax_inset.set_ylim(-2e-6, 5.5e-5)
ax_inset.set_xlabel("time (ps)", fontsize=14)
# ax_inset.set_ylabel(r"$P_{\mathrm{g},\nu=1}$", fontsize=14)
ax_inset.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax_inset.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
ax_inset.yaxis.get_offset_text().set_size(12)
ax_inset.xaxis.set_major_locator(MultipleLocator(25))
ax_inset.xaxis.set_minor_locator(MultipleLocator(5))
ax_inset.yaxis.set_major_locator(MultipleLocator(1e-5))
ax_inset.yaxis.set_minor_locator(MultipleLocator(2e-6))
ax_inset.tick_params(direction="in", labelsize=12, which="both")
ax_inset.tick_params(axis="x", which="major", length=6)
ax_inset.tick_params(axis="x", which="minor", length=3)
ax_inset.tick_params(axis="y", which="major", length=6)
ax_inset.tick_params(axis="y", which="minor", length=3)

# (d) MF Evib_per_molecule_avg with cavity-loss sweep overlays
ax = axes[1, 1]

kappa_values = np.sort(np.unique(mf_kappa_sweep["kappa_ratio"]))
panel_d_colors = ["blue", "magenta", "limegreen", "cyan"]
colors = panel_d_colors[: len(kappa_values)]
if len(colors) < len(kappa_values):
    cmap = plt.get_cmap("viridis")
    extra_colors = [cmap(i / max(len(kappa_values) - len(colors) - 1, 1)) for i in range(len(kappa_values) - len(colors))]
    colors.extend(extra_colors)

mf_evib_total = MF_N_MOLECULES * mf_evib_avg[:, 2]

ax.semilogy(
    mf_evib_avg[:, 0],
    mf_evib_total,
    "--",
    color="black",
    linewidth=2.2,
    alpha=0.5,
    label="lossless",
    zorder=4,
)

finite_curve_values = [mf_evib_total]
for color, kappa_ratio in zip(colors, kappa_values):
    mask = np.isclose(mf_kappa_sweep["kappa_ratio"], kappa_ratio)
    nu_vals = mf_kappa_sweep["nu_eV"][mask]
    evib_vals = MF_N_MOLECULES * mf_kappa_sweep["Evib_per_molecule_g_avg_eV"][mask]
    order = np.argsort(nu_vals)
    nu_vals = nu_vals[order]
    evib_vals = evib_vals[order]
    finite_curve_values.append(evib_vals)
    ax.semilogy(
        nu_vals,
        evib_vals,
        "-",
        color=color,
        linewidth=3.0,
        label=rf"$\kappa/\Omega = {kappa_ratio:.2f}$",
        zorder=3,
    )

all_positive_values = np.concatenate([vals[vals > 0] for vals in finite_curve_values if np.any(vals > 0)])
ymin = 0.8 * all_positive_values.min()
ymax = 1.2 * all_positive_values.max()

ax.set_xlim(0.16, 0.24)
ax.set_ylim(ymin, 1e-3)
ax.axvline(0.199, color="black", linestyle="--", linewidth=1.5)
mf_peak_idx = np.argmin(np.abs(mf_evib_avg[:, 0] - 0.199))
ax.text(
    0.206,
    2e-4,
    r"$\nu = 0.199$ eV",
    color="black",
    fontsize=24,
)
ax.set_xlabel(r"$\nu$ (eV)", fontsize=24)
ax.set_ylabel(r"$\langle E_{\mathrm{vib,g}}\rangle$ (eV)", fontsize=24)
ax.text(
    -0.3, 0.90, "(d)", transform=ax.transAxes, fontname="Helvetica", fontsize=48, clip_on=False
)
# Keep panel (d) y-axis minor ticks as-is (log scale); only set x-axis spacing.
ax.xaxis.set_major_locator(MultipleLocator(0.02))
ax.xaxis.set_minor_locator(MultipleLocator(0.004))
set_linear_ticks(ax, set_x=False, set_y=False)
ax.tick_params(direction="in", labelsize=20, which="both")
ax.tick_params(axis="x", which="major", length=10)
ax.tick_params(axis="x", which="minor", length=5)
ax.legend(frameon=False, fontsize=16, loc="upper left")

plt.savefig("Fig6.pdf", bbox_inches="tight")
plt.savefig("Fig6.png", bbox_inches="tight", dpi=150)
print("Saved Fig6.pdf / Fig6.png")
