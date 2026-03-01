import os
import re
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(__file__)
EVIB_OUT = os.path.join(BASE_DIR, "Evib_per_molecule_avg.csv")
TIME_START_FS = 1000.0

def intensity_from_name(name: str):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)", name)
    return float(m.group(1)) if m else None

def read_table(path, names):
    # Files include extra columns; read only the requested leading columns.
    return pd.read_csv(
        path,
        sep=r"\s+",
        comment="#",
        header=None,
        names=names,
        usecols=range(len(names)),
    )

def filter_time(df, time_col="time_fs", tmin=TIME_START_FS):
    return df[df[time_col] >= tmin]

def main():
    entries = []
    for entry in os.listdir(BASE_DIR):
        full = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full):
            inten = intensity_from_name(entry)
            if inten is not None:
                entries.append((inten, full))

    entries.sort(key=lambda x: x[0])

    E_vib = []

    for inten, folder in entries:

        # Vibrational energy averages
        evib_path = os.path.join(folder, "Evib_per_molecule.dat")
        if os.path.isfile(evib_path):
            evib_cols = ["time_fs", "Evib_per_molecule"]
            evib = read_table(evib_path, evib_cols)
            evib = filter_time(evib)
            E_vib.append({
                "Rabi_meV": inten,
                "Evib_per_molecule_avg": evib["Evib_per_molecule"].mean(),
            })
        else:
            print(f"Skip {folder}: missing Evib_per_molecule.dat")

    if E_vib:
        pd.DataFrame(E_vib).to_csv(EVIB_OUT, index=False)
        print(f"Wrote {EVIB_OUT}")


if __name__ == "__main__":
    main()
