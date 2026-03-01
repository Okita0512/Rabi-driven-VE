import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, ScalarFormatter


def set_helvetica():
    candidates = []
    direct_path = r"C:\\Windows\\Fonts\\Helvetica.ttf"
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
set_helvetica()

BASE_DIR = os.path.dirname(__file__)
QUANTUM_DIR = os.path.join(BASE_DIR, "Quantum nuclei")
QUANTUM2_DIR = os.path.join(BASE_DIR, "Quantum nuclei-2")
CLASSICAL_DIR = os.path.join(BASE_DIR, "Classical nuclei")
RESONANCE_DIR = os.path.join(BASE_DIR, "Resonance peak")
KAPPA_FOLDERS = [
    ("lossless", "0.20 - lossless"),
    ("0.5", "0.20 - lossy - kappa=0.5"),
    ("1", "0.20 - lossy - kappa=1"),
    ("2", "0.20 - lossy - kappa=2"),
    ("5", "0.20 - lossy - kappa=5"),
    ("10", "0.20 - lossy - kappa=10"),
    ("20", "0.20 - lossy - kappa=20"),
]
KAPPA_FOLDERS_Q2 = [
    ("lossless", "0.20134 - lossless"),
    ("0.5", "0.20134 - lossy - kappa=0.5"),
    ("1", "0.20134 - lossy - kappa=1"),
    ("2", "0.20134 - lossy - kappa=2"),
    ("5", "0.20134 - lossy - kappa=5"),
    ("10", "0.20134 - lossy - kappa=10"),
    ("20", "0.20134 - lossy - kappa=20"),
]
RESONANCE_FOLDERS = [
    ("lossless", "Rabi Resonance - short - lossless"),
    ("0.5", "Rabi Resonance - short - kappa=0.5"),
    ("1", "Rabi Resonance - short - kappa=1"),
]


def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 12), dpi=128)

    # (a) Quantum results: P_g,nu=1 for different kappa
    ax = axes[0, 0]
    for kappa_value, folder in KAPPA_FOLDERS:
        data = np.loadtxt(os.path.join(QUANTUM_DIR, folder, "Vib_pops_g.dat"))
        label = (
            "lossless"
            if kappa_value == "lossless"
            else rf"$\kappa$ = {kappa_value} ps$^{{-1}}$"
        )
        ax.plot(data[:, 0] / 1000.0, data[:, 2], "-", label=label)
    ax.set_xlabel("time (ps)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel(r"$P_{\mathrm{g}, \nu = 1}$", fontname="Helvetica", fontsize=20, labelpad=10)
    ax.set_xlim(0.0, 20.0)
    ax.set_ylim(0.0, 2.9e-15)
    sci_formatter = ScalarFormatter(useMathText=True)
    sci_formatter.set_scientific(True)
    sci_formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(sci_formatter)
    ax.yaxis.get_offset_text().set_fontname("Times New Roman")
    ax.yaxis.get_offset_text().set_fontsize(16)
    legend_prop = FontProperties(family="Helvetica", size=16)
    ax.legend(frameon=False, prop=legend_prop, ncol=2, loc="upper left")
    ax.text(
        -0.24,
        1.04,
        "(a)",
        transform=ax.transAxes,
        fontsize=48,
        fontname="Helvetica",
        va="top",
        ha="left",
    )

    # (b) Quantum-2 results: P_g,nu=1 for different kappa
    ax = axes[0, 1]
    y_max_b = 0.0
    for kappa_value, folder in KAPPA_FOLDERS_Q2:
        data = np.loadtxt(os.path.join(QUANTUM2_DIR, folder, "Vib_pops_g.dat"))
        y_max_b = max(y_max_b, float(np.max(data[:, 2])))
        label = (
            "lossless"
            if kappa_value == "lossless"
            else rf"$\kappa$ = {kappa_value} ps$^{{-1}}$"
        )
        ax.plot(data[:, 0] / 1000.0, data[:, 2], "-", label=label)
    ax.set_xlabel("time (ps)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel(r"$P_{\mathrm{g}, \nu = 1}$", fontname="Helvetica", fontsize=20, labelpad=10)
    ax.set_xlim(0.0, 20.0)
    ax.set_ylim(0.0, y_max_b * 1.05 if y_max_b > 0 else 1.0)
    sci_formatter = ScalarFormatter(useMathText=True)
    sci_formatter.set_scientific(True)
    sci_formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(sci_formatter)
    ax.yaxis.get_offset_text().set_fontname("Times New Roman")
    ax.yaxis.get_offset_text().set_fontsize(16)
    legend_prop = FontProperties(family="Helvetica", size=16)
    ax.legend(frameon=False, prop=legend_prop, ncol=1, loc="upper left")
    ax.text(
        -0.24,
        1.04,
        "(b)",
        transform=ax.transAxes,
        fontsize=48,
        fontname="Helvetica",
        va="top",
        ha="left",
    )

    # (c) Resonance scan: P_g,nu=1 averaged vs Rabi_meV
    ax = axes[1, 0]
    y_max_c = 0.0
    for kappa_value, folder in RESONANCE_FOLDERS:
        csv_path = os.path.join(RESONANCE_DIR, folder, "P_g_1.csv")
        data = np.genfromtxt(csv_path, delimiter=",", names=True)
        x = np.asarray(data["Rabi_meV"], dtype=float)
        y = np.asarray(data["P_g_1_avg"], dtype=float)
        order = np.argsort(x)
        x = x[order]
        y = y[order]
        y_max_c = max(y_max_c, float(np.max(y)))
        label = (
            "lossless"
            if kappa_value == "lossless"
            else rf"$\kappa$ = {kappa_value} ps$^{{-1}}$"
        )
        ax.plot(x, y, "-", label=label)
    ax.set_xlabel(r"$\Omega$ (eV)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel(r"$\langle P_{\mathrm{g}, \nu = 1} \rangle$", fontname="Helvetica", fontsize=20, labelpad=10)
    ax.set_xlim(0.200, 0.203)
    ax.set_ylim(-2e-15, 2.9e-14)
    sci_formatter = ScalarFormatter(useMathText=True)
    sci_formatter.set_scientific(True)
    sci_formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(sci_formatter)
    ax.yaxis.get_offset_text().set_fontname("Times New Roman")
    ax.yaxis.get_offset_text().set_fontsize(16)
    legend_prop = FontProperties(family="Helvetica", size=16)
    ax.legend(frameon=False, prop=legend_prop, ncol=1, loc="upper right")
    ax.text(
        -0.24,
        1.04,
        "(c)",
        transform=ax.transAxes,
        fontsize=48,
        fontname="Helvetica",
        va="top",
        ha="left",
    )

    # (d) Classical results: Q(t) for different kappa
    ax = axes[1, 1]
    for kappa_value, folder in KAPPA_FOLDERS:
        q_data = np.loadtxt(os.path.join(CLASSICAL_DIR, folder, "Q.dat"))
        label = (
            "lossless"
            if kappa_value == "lossless"
            else rf"$\kappa$ = {kappa_value} ps$^{{-1}}$"
        )
        ax.plot(q_data[:, 0], q_data[:, 1], label=label)
    ax.set_xlabel("time (fs)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel("Q(t)", fontname="Helvetica", fontsize=20)
    ax.set_xlim(0.0, 2000.0)
    ax.set_ylim(-4.4e-6, 6e-6)
    sci_formatter = ScalarFormatter(useMathText=True)
    sci_formatter.set_scientific(True)
    sci_formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(sci_formatter)
    ax.yaxis.get_offset_text().set_fontname("Times New Roman")
    ax.yaxis.get_offset_text().set_fontsize(16)
    legend_prop = FontProperties(family="Helvetica", size=16)
    ax.legend(frameon=False, prop=legend_prop, ncol=2, loc="upper left")
    ax.text(
        -0.24,
        1.04,
        "(d)",
        transform=ax.transAxes,
        fontsize=48,
        fontname="Helvetica",
        va="top",
        ha="left",
    )

    for axis in axes.ravel():
        axis.xaxis.set_minor_locator(AutoMinorLocator())
        axis.yaxis.set_minor_locator(AutoMinorLocator())
        axis.tick_params(which="major", length=8, labelsize=20, direction="in")
        axis.tick_params(which="minor", length=1.6, direction="in")
        for label in axis.get_xticklabels() + axis.get_yticklabels():
            label.set_fontname("Times New Roman")

    plt.tight_layout()
    plt.savefig("FigS7.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
