import os
import re
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(__file__)
ENERGY_OUT = os.path.join(BASE_DIR, "energy_summary.csv")
TIME_START_FS = 10.0


def intensity_from_name(name: str):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)", name)
    return float(m.group(1)) if m else None


def read_table(path, names):
    return pd.read_csv(path, delim_whitespace=True, comment="#", header=None, names=names)


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
        vg_path = os.path.join(folder, "vib_ground_excited.dat")
        if not os.path.isfile(vg_path):
            print(f"Skip {folder}: missing vib_ground_excited.dat")
            continue
        vg_cols = ["time_fs", "Nvib_ground", "Evib_ground_eV", "Nvib_excited", "Evib_excited_eV"]
        vg = read_table(vg_path, vg_cols)
        vg = filter_time(vg)
        avg_g = vg["Evib_ground_eV"].mean()
        avg_e = vg["Evib_excited_eV"].mean()
        avg_tot = (vg["Evib_ground_eV"] + vg["Evib_excited_eV"]).mean()
        energy_rows.append({
            "intensity_meV": inten,
            "Evib_ground_avg_eV": avg_g,
            "Evib_excited_avg_eV": avg_e,
            "Evib_total_avg_eV": avg_tot,
        })

    if energy_rows:
        pd.DataFrame(energy_rows).to_csv(ENERGY_OUT, index=False)
        print(f"Wrote {ENERGY_OUT}")


if __name__ == "__main__":
    main()
