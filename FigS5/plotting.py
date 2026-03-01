import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager as fm
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoLocator, AutoMinorLocator, MultipleLocator, ScalarFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


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


def tukey_envelope(t, t0_fs, duration_fs, alpha):
    if duration_fs <= 0.0:
        return 0.0
    t_start = t0_fs - 0.5 * duration_fs
    t_end = t0_fs + 0.5 * duration_fs
    if t < t_start or t > t_end:
        return 0.0
    x = (t - t_start) / duration_fs
    alpha = np.clip(alpha, 0.0, 1.0)
    if alpha == 0.0:
        return 1.0
    if x < alpha / 2.0:
        return 0.5 * (1.0 + np.cos(np.pi * (2.0 * x / alpha - 1.0)))
    if x > 1.0 - alpha / 2.0:
        return 0.5 * (1.0 + np.cos(np.pi * (2.0 * x / alpha - 2.0 / alpha + 1.0)))
    return 1.0


def main():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=128)

    # (a) Tukey window: amplitude and real/imag parts
    # Parameters matched to 0.20/Rabi.py
    hbar_ev_fs = 0.658211951
    n_mol = 100
    g_ev = 0.01
    omega_d_ev = 2.0
    pulse_t0_fs = 250.0
    pulse_duration_fs = 200.0
    pulse_taper_alpha = 0.01
    pulse_amp_ev = 1.0e-3
    pulse_omega_ev = 2.0 + np.sqrt(n_mol) * g_ev

    omega_0 = pulse_amp_ev / hbar_ev_fs
    delta_p = (pulse_omega_ev - omega_d_ev) / hbar_ev_fs

    t_fs = np.linspace(0.0, 1000.0, 5001)
    envelope = np.array(
        [tukey_envelope(t, pulse_t0_fs, pulse_duration_fs, pulse_taper_alpha) for t in t_fs]
    )
    amp = omega_0 * envelope
    real_part = amp * np.cos(delta_p * t_fs)
    imag_part = -amp * np.sin(delta_p * t_fs)

    ax = axes[0]
    ax.yaxis.set_major_locator(MultipleLocator(0.001))
    ax.yaxis.set_minor_locator(MultipleLocator(0.0002))
    ax.plot(t_fs, amp, label="Amplitude")
    ax.plot(t_fs, real_part, label="Re")
    ax.plot(t_fs, imag_part, label="Im")
    ax.set_xlim(0.0, 1000.0)
    ax.set_xlabel("time (fs)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel("drive (1/fs)", fontname="Helvetica", fontsize=20)
    legend_prop = FontProperties(family="Helvetica", size=18)
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

    ax_in = inset_axes(ax, width="40%", height="35%", loc="lower right", borderpad=2.0)
    mask = (t_fs >= 145.0) & (t_fs <= 155.0)
    ax_in.plot(t_fs[mask], amp[mask], label="Amplitude")
    ax_in.plot(t_fs[mask], real_part[mask], label="Re")
    ax_in.plot(t_fs[mask], imag_part[mask], label="Im")
    ax_in.set_xlim(147.0, 153.0)

    # (b) Exciton and photon population dynamics
    photon = np.loadtxt(os.path.join(DATA_020_DIR, "Photon_number.dat"))
    exciton = np.loadtxt(os.path.join(DATA_020_DIR, "Excited_population.dat"))

    ax = axes[1]
    ax.plot(photon[:, 0], photon[:, 1], label="photon")
    ax.plot(exciton[:, 0], 100.0 * exciton[:, 1], label="exciton")
    ax.set_xlabel("time (fs)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel("population", fontname="Helvetica", fontsize=20)
    ax.set_xlim(0.0, 2000.0)
    legend_prop = FontProperties(family="Helvetica", size=24)
    ax.legend(frameon=False, prop=legend_prop)
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

    # (c) P_g_1 population vs intensity
    pop_summary = pd.read_csv(os.path.join(BASE_DIR, "pop_summary.csv"))
    x = pop_summary["intensity_meV"].to_numpy()
    y = pop_summary["P_g_n1_avg"].to_numpy()

    ax = axes[2]
    ax.yaxis.set_major_locator(AutoLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.plot(x, y, marker="o")
    ax.set_xlabel(r"$\Omega$ (eV)", fontname="Helvetica", fontsize=20)
    ax.set_ylabel(r"$\langle P_{\mathrm{g},\nu=1}\rangle$", fontname="Helvetica", fontsize=20)
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

    for axis in list(axes) + [ax_in]:
        axis.xaxis.set_minor_locator(AutoMinorLocator())
        axis.yaxis.set_minor_locator(AutoMinorLocator())
        axis.tick_params(which="major", length=8, labelsize=20, direction="in")
        axis.tick_params(which="minor", length=1.6, direction="in")
        for label in axis.get_xticklabels() + axis.get_yticklabels():
            label.set_fontname("Times New Roman")

    ax_in.tick_params(which="major", length=5, labelsize=10, direction="in")

    plt.tight_layout()
    plt.savefig("FigS5.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
