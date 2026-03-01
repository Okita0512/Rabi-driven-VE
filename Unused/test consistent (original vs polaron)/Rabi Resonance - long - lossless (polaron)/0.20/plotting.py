import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _load_rabi_values(rabi_path: Path) -> dict:
    values = {}
    text = rabi_path.read_text(encoding="utf-8")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("def pulse_drive"):
            break
        if "=" not in line:
            continue
        left, right = line.split("=", 1)
        name = left.strip()
        if not re.match(r"^[A-Za-z_]\w*$", name):
            continue
        expr = right.split("#", 1)[0].strip()
        if not expr:
            continue
        try:
            values[name] = eval(expr, {"np": np, "math": math}, values)
        except Exception:
            # Skip lines that require objects or imports we haven't built yet.
            continue

    return values


def _build_pulse(values: dict):
    hbar_eVfs = values.get("HBAR_eVfs", 0.658211951)

    pulse_t0_fs = values["pulse_t0_fs"]
    pulse_sigma_fs = values["pulse_sigma_fs"]
    pulse_omega_eV = values["pulse_omega_eV"]
    pulse_amp_eV = values["pulse_amp_eV"]
    omega_d_eV = values.get("omega_d_eV", 0.0)

    def eV_to_rate(e_eV):
        return e_eV / hbar_eVfs

    omega_0 = eV_to_rate(pulse_amp_eV)
    delta_p = eV_to_rate(pulse_omega_eV - omega_d_eV)

    def pulse_drive(t):
        if omega_0 == 0.0:
            return 0.0
        envelope = np.exp(-0.5 * ((t - pulse_t0_fs) / pulse_sigma_fs) ** 2)
        return omega_0 * envelope * np.exp(-1j * delta_p * t)

    return pulse_drive


def main() -> None:
    rabi_path = Path(__file__).with_name("Rabi.py")
    if not rabi_path.exists():
        raise FileNotFoundError(f"Could not find {rabi_path}")

    values = _load_rabi_values(rabi_path)
    pulse_drive = _build_pulse(values)

    t0 = values.get("t0", 0.0)
    t1 = values.get("t1", 2000.0)
    num_pts = int(values.get("num_pts", 40001))
    t = np.linspace(t0, t1, num_pts)

    drive = pulse_drive(t)

    plt.figure(figsize=(8, 4.5))
    plt.plot(t, drive.real, label="Re[pulse_drive(t)]")
    plt.plot(t, drive.imag, label="Im[pulse_drive(t)]")
    plt.plot(t, np.abs(drive), label="|pulse_drive(t)|", linewidth=2)
    plt.xlabel("t (fs)")
    plt.ylabel("Pulse drive (1/fs)")
    plt.title("pulse_drive(t) from Rabi.py")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
