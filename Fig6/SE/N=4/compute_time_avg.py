import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
ENERGY_OUT = os.path.join(BASE_DIR, "energy_summary_N4.csv")
TIME_START_FS = 0.0


def intensity_from_name(name: str):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)meV", name)
    if m:
        return float(m.group(1))
    try:
        return float(name)
    except ValueError:
        return None


def read_table(path, names):
    return pd.read_csv(path, sep=r"\s+", comment="#", header=None, names=names)


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
    for inten, folder in entries:
        # Energy averages
        evib_path = os.path.join(folder, "Evib_avg.dat")
        if not os.path.isfile(evib_path):
            print(f"Skip {folder}: missing Evib_avg.dat")
            continue
        evib_cols = ["time_fs", "Evib_eV"]
        evib = read_table(evib_path, evib_cols)
        evib = filter_time(evib)
        avg_evib = evib["Evib_eV"].mean()
        energy_rows.append({
            "intensity_meV": inten,
            "Evib_avg_eV": avg_evib,
        })

    if energy_rows:
        pd.DataFrame(energy_rows).to_csv(ENERGY_OUT, index=False)
        print(f"Wrote {ENERGY_OUT}")


if __name__ == "__main__":
    main()
