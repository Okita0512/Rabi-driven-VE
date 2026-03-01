import os
import re
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(__file__)
ENERGY_OUT = os.path.join(BASE_DIR, "P_g_1.csv")
POP_OUT = os.path.join(BASE_DIR, "P_e_1.csv")
TIME_START_FS = 100.0

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

    P_g = []
    P_e = []

    for inten, folder in entries:
        # Energy averages
        vg_path = os.path.join(folder, "Vib_pops_g.dat")
        if not os.path.isfile(vg_path):
            print(f"Skip {folder}: missing Vib_pops_g.dat")
            continue
        vg_cols = ["time_fs", "P_g_0", "P_g_1", "P_g_2", "P_g_3"]
        vg = read_table(vg_path, vg_cols)
        vg = filter_time(vg)
        P_g.append({
                "Rabi_meV": inten,
                "P_g_0_avg": vg["P_g_0"].mean(),
                "P_g_1_avg": vg["P_g_1"].mean(),
                "P_g_2_avg": vg["P_g_2"].mean(),
                "P_g_3_avg": vg["P_g_3"].mean(),
            })

        # Population averages
        pop_path = os.path.join(folder, "Vib_pops_e.dat")
        if os.path.isfile(pop_path):
            pop_cols = ["time_fs", "P_e_0", "P_e_1", "P_e_2", "P_e_3"]
            pop = read_table(pop_path, pop_cols)
            pop = filter_time(pop)
            P_e.append({
                "Rabi_meV": inten,
                "P_e_0_avg": pop["P_e_0"].mean(),
                "P_e_1_avg": pop["P_e_1"].mean(),
                "P_e_2_avg": pop["P_e_2"].mean(),
                "P_e_3_avg": pop["P_e_3"].mean(),
            })
        else:
            print(f"Skip {folder}: missing Vib_pops_e.dat")

    if P_g:
        pd.DataFrame(P_g).to_csv(ENERGY_OUT, index=False)
        print(f"Wrote {ENERGY_OUT}")
    if P_e:
        pd.DataFrame(P_e).to_csv(POP_OUT, index=False)
        print(f"Wrote {POP_OUT}")


if __name__ == "__main__":
    main()
