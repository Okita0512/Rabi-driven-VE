import os
import sys
import re
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
SUMMARY_OUT = os.path.join(BASE_DIR, "time_avg_summary.csv")
TIME_START_FS = 100.0
DATA_EXTS = {".dat"}
TARGET_BASENAME = "vib_level_pop.dat"
POP_COL_NAMES = ["P_g_n0", "P_g_n1", "P_g_n2", "P_e_n0", "P_e_n1", "P_e_n2"]


def intensity_from_folder(path):
    name = os.path.basename(path)
    m = re.fullmatch(r"\d+(?:\.\d+)?", name)
    return float(m.group(0)) if m else None


def read_table(path):
    return pd.read_csv(path, delim_whitespace=True, comment="#", header=None)


def filter_time(df, time_col=0, tmin=TIME_START_FS):
    return df[df[time_col] > tmin]


def iter_pop_files(paths):
    if not paths:
        for entry in os.listdir(BASE_DIR):
            full = os.path.join(BASE_DIR, entry)
            if os.path.isdir(full):
                target = os.path.join(full, TARGET_BASENAME)
                if os.path.isfile(target):
                    yield target
        return

    for raw in paths:
        full = raw
        if not os.path.isabs(full):
            full = os.path.join(BASE_DIR, raw)
        if os.path.isdir(full):
            target = os.path.join(full, TARGET_BASENAME)
            if os.path.isfile(target):
                yield target
        elif os.path.isfile(full):
            if os.path.basename(full) == TARGET_BASENAME:
                yield full
        else:
            print(f"Skip {raw}: not found")


def main():
    rows = []
    targets = list(dict.fromkeys(iter_pop_files(sys.argv[1:])))
    for full in targets:
        folder = os.path.dirname(full)
        inten = intensity_from_folder(folder)
        if inten is None:
            print(f"Skip {full}: folder is not a numeric label")
            continue

        df = read_table(full)
        if df.shape[1] < 2:
            print(f"Skip {full}: need time + data columns")
            continue

        df = filter_time(df)
        if df.empty:
            print(f"Skip {full}: no rows after time filter")
            continue

        for col_idx in range(1, df.shape[1]):
            rows.append({
                "intensity": inten,
                "column_index": col_idx,
                "time_avg": df[col_idx].mean(),
            })

    if rows:
        out = pd.DataFrame(rows).sort_values(["intensity", "column_index"])
        wide = out.pivot(index="intensity", columns="column_index", values="time_avg")
        if len(wide.columns) == len(POP_COL_NAMES):
            wide = wide.rename(columns={i: name for i, name in zip(wide.columns, POP_COL_NAMES)})
        else:
            wide = wide.rename(columns={i: f"col_{i}" for i in wide.columns})
        wide.to_csv(SUMMARY_OUT, index=True)
        print(f"Wrote {SUMMARY_OUT}")
    else:
        print("No data to write.")


if __name__ == "__main__":
    main()
