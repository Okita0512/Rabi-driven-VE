import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


CSV_PATH = Path("pe_n1_summary.csv")


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    x = df.iloc[:, 0].to_numpy()
    y = df.iloc[:, 1].to_numpy()

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o", linestyle="-", linewidth=1.5, markersize=4)
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    plt.title("Plot of First vs Second Column")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
