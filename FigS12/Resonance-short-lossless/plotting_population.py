import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


FOLDERS = ["0.20", "0.201", "0.2011", "0.2012", "0.2013", "0.2014"]
DATA_FILE = "vib_level_pop.dat"


def load_pe_n1(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(path, comments="#")
    t_fs = data[:, 0]
    p_e_n1 = data[:, 5]
    return t_fs, p_e_n1


def main() -> None:
    plt.figure(figsize=(9, 6))

    for folder in FOLDERS:
        file_path = Path(folder) / DATA_FILE
        if not file_path.exists():
            print(f"Skipping missing file: {file_path}")
            continue

        t_fs, p_e_n1 = load_pe_n1(file_path)
        plt.plot(t_fs, p_e_n1, linewidth=1.6, label=folder)

    plt.xlabel("time_fs")
    plt.ylabel("P_e_n1")
    plt.title("Population Dynamics of P_e_n1")
    plt.grid(True, alpha=0.3)
    plt.legend(title="Folder", fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
