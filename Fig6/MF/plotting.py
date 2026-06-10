import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
REFERENCE_FILE = ROOT / "Evib_per_molecule_avg.csv"
KAPPA_SWEEP_DIR = ROOT / "kappa_sweep"
RESONANCE_EV = 0.19866


def load_reference_curve():
    data = np.loadtxt(REFERENCE_FILE, delimiter=",", skiprows=1)
    return data[:, 0], data[:, 2]


def format_kappa_ratio(kappa_ratio):
    label = f"{kappa_ratio:.3f}".rstrip("0").rstrip(".")
    if "." not in label:
        label += ".0"
    return label


def load_lossy_curves():
    curves = []
    for path in sorted(KAPPA_SWEEP_DIR.glob("kappa_ratio_*.csv")):
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            continue

        kappa_ratio = float(rows[0]["kappa_ratio"])
        if np.isclose(kappa_ratio, 0.0):
            continue

        nu_vals = np.array([float(row["nu_eV"]) for row in rows])
        evib_vals = np.array([float(row["Evib_per_molecule_g_avg_eV"]) for row in rows])
        order = np.argsort(nu_vals)
        curves.append((kappa_ratio, nu_vals[order], evib_vals[order]))
    return curves


def main():
    nu_ref, evib_ref = load_reference_curve()
    lossy_curves = load_lossy_curves()
    y_values = [evib_ref]
    y_values.extend(evib_vals for _, _, evib_vals in lossy_curves)
    positive_y = np.concatenate([vals[vals > 0.0] for vals in y_values])
    y_min = positive_y.min() * 0.8
    y_max = positive_y.max() * 1.2

    fig, ax = plt.subplots()
    ax.semilogy(nu_ref, evib_ref, marker="o", linestyle="-", color="black", label="lossless")

    if lossy_curves:
        cmap = plt.get_cmap("turbo")
        if len(lossy_curves) == 1:
            colors = [cmap(0.75)]
        else:
            colors = [cmap(i / (len(lossy_curves) - 1)) for i in range(len(lossy_curves))]

        for color, (kappa_ratio, nu_vals, evib_vals) in zip(colors, lossy_curves):
            ax.semilogy(
                nu_vals,
                evib_vals,
                linestyle="-",
                linewidth=2.0,
                color=color,
                label=rf"lossy, $\kappa/\Omega={format_kappa_ratio(kappa_ratio)}$",
            )

    ax.vlines(
        RESONANCE_EV,
        ymin=y_min,
        ymax=y_max,
        colors="r",
        linestyles="dashed",
        label=rf"resonance at $\nu = {RESONANCE_EV}$ eV",
    )

    ax.set_xlabel(r"$\nu$ (eV)")
    ax.set_ylabel(r"$\langle E_{vib,g} \rangle$ (eV)")
    ax.set_ylim(y_min, y_max)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
