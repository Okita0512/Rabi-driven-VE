import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
ENERGY_OUT = os.path.join(BASE_DIR, "energy_summary.csv")
POP_OUT = os.path.join(BASE_DIR, "pop_summary.csv")
TIME_START_FS = 100.0


def cv_from_name(name: str):
    # Accept either bare numeric folder names (e.g., 0.20) or legacy N=0.20
    m = re.fullmatch(r"(?:N=)?(\d+(?:\.\d+)?)", name)
    return float(m.group(1)) if m else None


def read_table(path):
    return pd.read_csv(path, sep=r"\s+", comment="#", header=None)


def filter_time(df, time_col=0, tmin=TIME_START_FS):
    return df[df.iloc[:, time_col] > tmin]


def mean_if_exists(df, col_idx):
    return df.iloc[:, col_idx].mean() if df.shape[1] > col_idx else float("nan")


def main():
    entries = []
    for entry in os.listdir(BASE_DIR):
        full = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full):
            cv = cv_from_name(entry)
            if cv is not None:
                entries.append((cv, full))

    entries.sort(key=lambda x: x[0])

    energy_rows = []
    pop_rows = []

    for cv, folder in entries:
        # Energy averages from Evib_per_molecule.dat:
        # time, Evib_ground, Evib_excited, Evib_total
        evib_path = os.path.join(folder, "Evib_per_molecule.dat")
        if not os.path.isfile(evib_path):
            print(f"Skip {folder}: missing Evib_per_molecule.dat")
            continue

        evib = filter_time(read_table(evib_path))
        if evib.empty or evib.shape[1] < 3:
            print(f"Skip {folder}: insufficient data in Evib_per_molecule.dat")
            continue

        avg_g = evib.iloc[:, 1].mean()
        avg_e = evib.iloc[:, 2].mean()
        if evib.shape[1] >= 4:
            avg_tot = evib.iloc[:, 3].mean()
        else:
            avg_tot = (evib.iloc[:, 1] + evib.iloc[:, 2]).mean()

        energy_rows.append({
            "cv": cv,
            "Evib_ground_avg_eV": avg_g,
            "Evib_excited_avg_eV": avg_e,
            "Evib_total_avg_eV": avg_tot,
        })

        # Population averages from Vib_pops_g/e.dat:
        # time, n0, n1, n2, ...
        pg_path = os.path.join(folder, "Vib_pops_g.dat")
        pe_path = os.path.join(folder, "Vib_pops_e.dat")

        if os.path.isfile(pg_path) and os.path.isfile(pe_path):
            pop_g = filter_time(read_table(pg_path))
            pop_e = filter_time(read_table(pe_path))

            pop_rows.append({
                "cv": cv,
                "P_g_n1_avg": mean_if_exists(pop_g, 2),
                "P_g_n2_avg": mean_if_exists(pop_g, 3),
                "P_e_n1_avg": mean_if_exists(pop_e, 2),
                "P_e_n2_avg": mean_if_exists(pop_e, 3),
            })
        else:
            print(f"Skip {folder}: missing Vib_pops_g.dat and/or Vib_pops_e.dat")

    if energy_rows:
        pd.DataFrame(energy_rows).to_csv(ENERGY_OUT, index=False)
        print(f"Wrote {ENERGY_OUT}")
    if pop_rows:
        pd.DataFrame(pop_rows).to_csv(POP_OUT, index=False)
        print(f"Wrote {POP_OUT}")


if __name__ == "__main__":
    main()
