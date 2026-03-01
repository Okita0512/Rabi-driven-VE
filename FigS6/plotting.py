import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager as fm
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoLocator, AutoMinorLocator, ScalarFormatter


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
DATA_020_DIR = os.path.join(BASE_DIR, "0.20")
Q_FOLDERS = ["0.16", "0.18", "0.20", "0.22", "0.24"]


def main():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=128)

    # (a) Exciton and photon population dynamics (0.20 folder)
    photon = np.loadtxt(os.path.join(DATA_020_DIR, "Photon_number.dat"))
    exciton = np.loadtxt(os.path.join(DATA_020_DIR, "Excited_population.dat"))

    ax = axes[0]
    ax.plot(photon[:, 0], photon[:, 1], label="photon")
    ax.plot(exciton[:, 0], 10000 * exciton[:, 1], label="exciton")
    ax.set_xlabel("time (fs)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel("population", fontname="Helvetica", fontsize=20)
    ax.set_xlim(0.0, 1000.0)
    ax.set_ylim(-0.001, 0.029)
    sci_formatter = ScalarFormatter(useMathText=True)
    sci_formatter.set_scientific(True)
    sci_formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(sci_formatter)
    ax.yaxis.get_offset_text().set_fontname("Times New Roman")
    ax.yaxis.get_offset_text().set_fontsize(16)
    legend_prop = FontProperties(family="Helvetica", size=24)
    ax.legend(frameon=False, prop=legend_prop)
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

    # (b) Q(t) for multiple nu folders
    ax = axes[1]
    for folder in Q_FOLDERS:
        q_data = np.loadtxt(os.path.join(BASE_DIR, folder, "Q.dat"))
        ax.plot(q_data[:, 0], q_data[:, 1], label=rf"$\nu = {folder}$ eV")
    ax.set_xlabel("time (fs)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel("Q(t)", fontname="Helvetica", fontsize=20)
    ax.set_xlim(0.0, 2000.0)
    ax.set_ylim(-4.5e-6, 5e-6)
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
        "(b)",
        transform=ax.transAxes,
        fontsize=48,
        fontname="Helvetica",
        va="top",
        ha="left",
    )

    # (c) Evib vs nu
    evib_path = os.path.join(BASE_DIR, "Evib_per_molecule_avg.csv")
    evib = np.loadtxt(evib_path, delimiter=",", skiprows=1)
    x = evib[:, 0]
    y = evib[:, 1]

    ax = axes[2]
    ax.yaxis.set_major_locator(AutoLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.plot(x, y, marker="o")
    ax.set_xlabel(r"$\nu$ (eV)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel(r"$\langle E_\mathrm{vib} \rangle$ (eV)", fontname="Helvetica", fontsize=20)
    ax.set_xlim(0.16, 0.24)
    ax.grid(True, alpha=0.3)
    sci_formatter = ScalarFormatter(useMathText=True)
    sci_formatter.set_scientific(True)
    sci_formatter.set_powerlimits((0, 0))
    ax.yaxis.set_major_formatter(sci_formatter)
    ax.yaxis.get_offset_text().set_fontname("Times New Roman")
    ax.yaxis.get_offset_text().set_fontsize(16)
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

    for axis in list(axes):
        axis.xaxis.set_minor_locator(AutoMinorLocator())
        axis.yaxis.set_minor_locator(AutoMinorLocator())
        axis.tick_params(which="major", length=8, labelsize=20, direction="in")
        axis.tick_params(which="minor", length=1.6, direction="in")
        for label in axis.get_xticklabels() + axis.get_yticklabels():
            label.set_fontname("Times New Roman")

    plt.tight_layout()
    plt.savefig("FigS6.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
