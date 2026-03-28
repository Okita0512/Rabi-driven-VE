#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan folders N=1..10, read Evib_avg.dat (2 columns: time_fs, Evib_avg),
compute time-average of column 2, and write Evib_avg_time_avg_vs_N.txt.

Usage:
  python collect_evib_avg.py \
      --base "." \
      --pattern "N={n}" \
      --filename "Evib_avg.dat" \
      --nmin 1 --nmax 10 \
      --out "Evib_avg_time_avg_vs_N.txt"
"""

import os
import argparse
import numpy as np

def load_time_average(filepath: str) -> float:
    """
    Load a 2-column DAT file and return the time average of column 2.
    Assumes uniform (or not) time grid; this does simple arithmetic mean
    requested by the user: mean over all time points of the second column.
    """
    data = np.loadtxt(filepath)
    if data.ndim == 1:
        # Single row file case: still return the only value in col 2
        return float(data[1])
    # col 1: time_fs, col 2: Evib_avg (eV)
    evib = data[:, 1]
    return float(np.mean(evib))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".", help="Base directory containing N=* folders")
    ap.add_argument("--pattern", default="N={n}", help="Folder name pattern, use {n} for N")
    ap.add_argument("--filename", default="Evib_avg.dat", help="File name inside each folder")
    ap.add_argument("--nmin", type=int, default=1, help="Minimum N")
    ap.add_argument("--nmax", type=int, default=10, help="Maximum N")
    ap.add_argument("--out", default="Evib_avg_time_avg_vs_N.txt", help="Output text file")
    args = ap.parse_args()

    rows = []
    missing = []

    for n in range(args.nmin, args.nmax + 1):
        folder = args.pattern.format(n=n)
        path = os.path.join(args.base, folder, args.filename)
        if not os.path.isfile(path):
            missing.append(path)
            continue
        try:
            avg = load_time_average(path)
            rows.append((n, avg))
        except Exception as e:
            print(f"[WARN] Failed to read {path}: {e}")

    # sort by N just in case
    rows.sort(key=lambda x: x[0])

    # write output
    with open(os.path.join(args.base, args.out), "w", encoding="utf-8") as f:
        f.write("# N    Evib_avg_time_mean(eV)\n")
        for n, avg in rows:
            f.write(f"{n:3d}  {avg:.10f}\n")

    print(f"[OK] Wrote {args.out} with {len(rows)} rows.")
    if missing:
        print("[INFO] Missing files (skipped):")
        for p in missing:
            print("   ", p)

if __name__ == "__main__":
    main()
