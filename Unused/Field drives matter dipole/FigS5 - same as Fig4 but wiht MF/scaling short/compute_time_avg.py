import os
import re
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(__file__)
ENERGY_OUT = os.path.join(BASE_DIR, "energy_summary.csv")
POP_OUT = os.path.join(BASE_DIR, "pop_summary.csv")
TIME_START_FS = 100.0


def intensity_from_name(name: str):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)meV", name)
    return float(m.group(1)) if m else None


def read_table(path, names=None):
    df = pd.read_csv(path, delim_whitespace=True, comment="#", header=None)
    if names:
        df.columns = names
    else:
        df.columns = ["time_fs"] + [f"col_{i}" for i in range(1, df.shape[1])]
    return df


def filter_time(df, time_col="time_fs", tmin=TIME_START_FS):
    return df[df[time_col] > tmin]


def main():
    entries = []
    for entry in os.listdir(BASE_DIR):
        full = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full):
            inten = intensity_from_name(entry)
            if inten is not None:
                entries.append((inten, full))

    entries.sort(key=lambda x: x[0])

    energy_rows = []
    pop_rows = []

    for inten, folder in entries:
        # Energy averages
        vib_energy_path = os.path.join(folder, "Evib_per_molecule.dat")
        if not os.path.isfile(vib_energy_path):
            print(f"Skip {folder}: missing Evib_per_molecule.dat")
            continue
        vib_energy_cols = ["time_fs", "Evib_total_eV", "Evib_ground_eV", "Evib_excited_eV"]
        vib_energy = read_table(vib_energy_path, vib_energy_cols)
        vib_energy = filter_time(vib_energy)
        avg_g = vib_energy["Evib_ground_eV"].mean()
        avg_e = vib_energy["Evib_excited_eV"].mean()
        avg_tot = vib_energy["Evib_total_eV"].mean()
        energy_rows.append({
            "intensity_meV": inten,
            "Evib_ground_avg_eV": avg_g,
            "Evib_excited_avg_eV": avg_e,
            "Evib_total_avg_eV": avg_tot,
        })

        # Population averages
        pop_g_path = os.path.join(folder, "Vib_pops_g.dat")
        pop_e_path = os.path.join(folder, "Vib_pops_e.dat")
        if os.path.isfile(pop_g_path) and os.path.isfile(pop_e_path):
            pop_g = read_table(pop_g_path)
            pop_e = read_table(pop_e_path)
            pop_g.columns = ["time_fs"] + [f"P_g_n{i}" for i in range(pop_g.shape[1] - 1)]
            pop_e.columns = ["time_fs"] + [f"P_e_n{i}" for i in range(pop_e.shape[1] - 1)]
            pop_g = filter_time(pop_g)
            pop_e = filter_time(pop_e)

            row = {"intensity_meV": inten}
            for col in pop_g.columns[1:]:
                row[f"{col}_avg"] = pop_g[col].mean()
            for col in pop_e.columns[1:]:
                row[f"{col}_avg"] = pop_e[col].mean()
            pop_rows.append(row)
        else:
            missing = []
            if not os.path.isfile(pop_g_path):
                missing.append("Vib_pops_g.dat")
            if not os.path.isfile(pop_e_path):
                missing.append("Vib_pops_e.dat")
            print(f"Skip {folder}: missing {', '.join(missing)}")

    if energy_rows:
        pd.DataFrame(energy_rows).to_csv(ENERGY_OUT, index=False)
        print(f"Wrote {ENERGY_OUT}")
    if pop_rows:
        pd.DataFrame(pop_rows).to_csv(POP_OUT, index=False)
        print(f"Wrote {POP_OUT}")


if __name__ == "__main__":
    main()
