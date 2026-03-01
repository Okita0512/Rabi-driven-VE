import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(__file__)
ENERGY_FILE = os.path.join(BASE_DIR, "energy_summary.csv")
POP_FILE = os.path.join(BASE_DIR, "pop_summary.csv")


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


def plot_energy(df):
    df = df.sort_values("intensity_meV")
    plt.figure(figsize=(6,6))
    legend_entries = []
    for col, lbl, marker, color in [
        ("Evib_total_avg_eV", "Total vib energy", "o", "#1f77b4"),
        ("Evib_ground_avg_eV", "Ground vib energy", "s", "#ff7f0e"),
        ("Evib_excited_avg_eV", "Excited vib energy", "^", "#2ca02c"),
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
            legend_entries.append(f"{lbl} fit: y={m:.3f}x+{b:.3f}, R^2={r2:.4f}")
    plt.xlabel(r"$\log_{10}$ (pulse intensity / meV)")
    plt.ylabel(r"$\log_{10}\;\langle E_{\rm vib}\rangle$ (eV)")
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend(title="Series", loc="best")
    if legend_entries:
        plt.tight_layout()
        # add fit text box
        text = "\n".join(legend_entries)
        plt.gca().text(
            0.35, 0.06, text,
            transform=plt.gca().transAxes,
            fontsize=8,
            verticalalignment="center",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
        )
    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "energy_vs_intensity.png")
    plt.savefig(out_path, dpi=300)
    print(f"Saved {out_path}")


def plot_pop(df):
    df = df.sort_values("intensity_meV")
    plt.figure(figsize=(6,6))
    legend_entries = []
    for col, lbl, marker, color in [
        ("P_g_n1_avg", "P_g_1", "o", "#1f77b4"),
        ("P_g_n2_avg", "P_g_2", "s", "#ff7f0e"),
        ("P_e_n1_avg", "P_e_1", "^", "#2ca02c"),
        ("P_e_n2_avg", "P_e_2", "D", "#d62728"),
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
            legend_entries.append(f"{lbl} fit: y={m:.3f}x+{b:.3f}, R^2={r2:.4f}")
    plt.xlabel(r"$\log_{10}$ (pulse intensity / meV)")
    plt.ylabel(r"$\log_{10}\;\langle P_{\rm vib}\rangle$ (per mode)")
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend(title="Series", loc="best")
    if legend_entries:
        plt.tight_layout()
        text = "\n".join(legend_entries)
        plt.gca().text(
            0.48, 0.03, text,
            transform=plt.gca().transAxes,
            fontsize=8,
            verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
        )
    plt.tight_layout()
    out_path = os.path.join(BASE_DIR, "pop_vs_intensity.png")
    plt.savefig(out_path, dpi=300)
    print(f"Saved {out_path}")


def main():
    if os.path.isfile(ENERGY_FILE):
        df_energy = pd.read_csv(ENERGY_FILE)
        plot_energy(df_energy)
    else:
        print(f"Missing {ENERGY_FILE}")

    if os.path.isfile(POP_FILE):
        df_pop = pd.read_csv(POP_FILE)
        plot_pop(df_pop)
    else:
        print(f"Missing {POP_FILE}")


if __name__ == "__main__":
    main()
