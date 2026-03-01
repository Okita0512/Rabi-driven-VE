import os

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "pop_summary.csv")


def main():
    df = pd.read_csv(DATA_FILE)
    x = df["intensity_meV"].to_numpy()
    y = df["P_g_n1_avg"].to_numpy()

    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o", label="P_g_n1_avg")

    ax.set_xlabel("intensity (meV)")
    ax.set_ylabel("P_g_n1_avg")
    ax.set_title("P_g_n1_avg vs intensity")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
