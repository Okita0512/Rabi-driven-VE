import os

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
FILE_A = os.path.join(BASE_DIR, "energy_summary.csv")
FILE_B = os.path.join(BASE_DIR, "energy_summary_2.csv")


def main():
    df_a = pd.read_csv(FILE_A)
    df_b = pd.read_csv(FILE_B)

    merged = df_a.merge(df_b, on="intensity_meV", suffixes=("_a", "_b"))
    x = merged["intensity_meV"].to_numpy()

    cols = ["Evib_ground_avg_eV", "Evib_excited_avg_eV", "Evib_total_avg_eV"]
    for col in cols:
        merged[f"{col}_diff"] = merged[f"{col}_a"] - merged[f"{col}_b"]

    fig, ax = plt.subplots()
    for col in cols:
        y = merged[f"{col}_diff"].to_numpy()
        ax.plot(x, y, marker="o", label=f"{col} diff")

    ax.set_xlabel(r"$\nu$ (eV)")
    ax.set_ylabel("energy difference (eV)")
    ax.set_title("energy_summary - energy_summary_2")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
