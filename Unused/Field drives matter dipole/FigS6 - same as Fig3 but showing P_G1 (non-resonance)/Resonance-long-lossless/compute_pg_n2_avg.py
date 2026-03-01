import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
SUMMARY_OUT = os.path.join(BASE_DIR, "pg_n2_summary.csv")
TIME_START_FS = 1000.0
TARGET_BASENAME = "vib_level_pop.dat"
TARGET_COL = "P_g_n2"


def intensity_from_folder(path):
    name = os.path.basename(path)
    m = re.fullmatch(r"\d+(?:\.\d+)?", name)
    return float(m.group(0)) if m else None


def read_table(path):
    return pd.read_csv(path, delim_whitespace=True, comment="#", header=None)


def filter_time(df, time_col=0, tmin=TIME_START_FS):
    return df[df[time_col] > tmin]


def extract_header(path):
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                return line.lstrip("#").strip().split()
            break
    return None


def iter_pop_files():
    for entry in os.listdir(BASE_DIR):
        full = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full):
            target = os.path.join(full, TARGET_BASENAME)
            if os.path.isfile(target):
                yield target


def main():
    rows = []
    for full in iter_pop_files():
        folder = os.path.dirname(full)
        inten = intensity_from_folder(folder)
        if inten is None:
            print(f"Skip {full}: folder is not a numeric label")
            continue

        header = extract_header(full)
        if not header or TARGET_COL not in header:
            print(f"Skip {full}: missing {TARGET_COL} header")
            continue

        col_idx = header.index(TARGET_COL)
        df = read_table(full)
        if df.shape[1] <= col_idx:
            print(f"Skip {full}: data has fewer columns than header")
            continue

        df = filter_time(df)
        if df.empty:
            print(f"Skip {full}: no rows after time filter")
            continue

        rows.append({
            "intensity": inten,
            "P_g_n2_avg": df[col_idx].mean(),
        })

    if rows:
        out = pd.DataFrame(rows).sort_values("intensity")
        out.to_csv(SUMMARY_OUT, index=False)
        print(f"Wrote {SUMMARY_OUT}")
    else:
        print("No data to write.")


if __name__ == "__main__":
    main()
