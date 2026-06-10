import argparse
import csv
from pathlib import Path

import numpy as np
from numpy import kron
from scipy.integrate import solve_ivp


HBAR_eVfs = 0.658211951


def eV_to_rate(e_eV: float) -> float:
    return e_eV / HBAR_eVfs


def sanitize_float(value: float) -> str:
    return f"{value:.3f}".replace("-", "m").replace(".", "p")


def discover_omega_values(root: Path):
    omega_values = []
    for path in root.iterdir():
        if not path.is_dir():
            continue
        try:
            omega_values.append(float(path.name))
        except ValueError:
            continue
    return np.array(sorted(set(omega_values)), dtype=float)


def write_csv(path: Path, rows):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class MFKappaSweep:
    def __init__(
        self,
        n_molecules: int = 10000,
        vib_trunc: int = 5,
        omega_c_eV: float = 2.0,
        omega_0_eV: float = 2.0,
        omega_d_eV: float = 2.0,
        g_collective_eV: float = 0.10,
        c_v_eV: float = 0.02,
        eta: complex = 0.0 + 0.0j,
        a_lp: float = 1.0 / np.sqrt(2.0),
        b_up: float = 1.0 / np.sqrt(2.0),
        phi_rel: float = 0.0,
        t0_fs: float = 0.0,
        t1_fs: float = 20000.0,
        num_pts: int = 400001,
        time_avg_start_fs: float = 0.0,
        rtol: float = 1e-8,
        atol: float = 1e-10,
        method: str = "RK45",
    ):
        self.n_molecules = n_molecules
        self.vib_trunc = vib_trunc
        self.omega_c_eV = omega_c_eV
        self.omega_0_eV = omega_0_eV
        self.omega_d_eV = omega_d_eV
        self.g_collective_eV = g_collective_eV
        self.g_eV = g_collective_eV / np.sqrt(n_molecules)
        self.c_v_eV = c_v_eV
        self.eta = eta
        self.a_lp = a_lp
        self.b_up = b_up
        self.phi_rel = phi_rel
        self.t0_fs = t0_fs
        self.t1_fs = t1_fs
        self.num_pts = num_pts
        self.time_avg_start_fs = time_avg_start_fs
        self.rtol = rtol
        self.atol = atol
        self.method = method

        self.delta_c = eV_to_rate(omega_c_eV - omega_d_eV)
        self.delta_x = eV_to_rate(omega_0_eV - omega_d_eV)
        self.g = eV_to_rate(self.g_eV)
        self.c_v = eV_to_rate(c_v_eV)
        self.omega_rabi_eV = 2.0 * np.sqrt(n_molecules) * self.g_eV
        self.omega_rabi_rate = eV_to_rate(self.omega_rabi_eV)
        self.t_eval = np.linspace(t0_fs, t1_fs, num_pts)

        self._build_operators()
        self._build_initial_state()

    def _build_operators(self):
        d_v = self.vib_trunc
        iv = np.eye(d_v, dtype=complex)
        a = np.zeros((d_v, d_v), dtype=complex)
        for n in range(1, d_v):
            a[n - 1, n] = np.sqrt(n)
        adag = a.conj().T
        n_op = adag @ a

        eg = np.array([[0, 0], [0, 1]], dtype=complex)
        gg = np.array([[1, 0], [0, 0]], dtype=complex)
        sig_minus = np.array([[0, 1], [0, 0]], dtype=complex)

        i_e = np.eye(2, dtype=complex)

        def e_part(op_e):
            return kron(op_e, iv)

        def v_part(op_v):
            return kron(i_e, op_v)

        self.proj_g = e_part(gg)
        self.proj_e = e_part(eg)
        self.sigma_minus = e_part(sig_minus)
        self.sigma_plus = self.sigma_minus.conj().T
        self.nhat = v_part(n_op)
        self.b = v_part(a)
        self.bd = v_part(adag)

    def _build_initial_state(self):
        ket_e = np.array([0, 1], dtype=complex)
        ket_g = np.array([1, 0], dtype=complex)
        ket_v0 = np.zeros((self.vib_trunc,), dtype=complex)
        ket_v0[0] = 1.0
        psie = kron(ket_e, ket_v0)
        psig = kron(ket_g, ket_v0)

        g_coll = self.g * np.sqrt(self.n_molecules)
        detuning = self.delta_c - self.delta_x
        theta = 0.5 * np.arctan2(2.0 * g_coll, detuning)

        c_ph = self.a_lp * np.cos(theta) + self.b_up * np.exp(1j * self.phi_rel) * np.sin(theta)
        c_ex = -self.a_lp * np.sin(theta) + self.b_up * np.exp(1j * self.phi_rel) * np.cos(theta)

        exciton_pop_per_mol = np.abs(c_ex) ** 2 / self.n_molecules
        self.psi0 = np.sqrt(1.0 - exciton_pop_per_mol) * psig + c_ex * psie
        self.alpha0 = c_ph

    def _expect(self, op, psi):
        return np.vdot(psi, op @ psi)

    def _h_mol(self, alpha: complex, omega_v_rate: float):
        h_mol = self.delta_x * self.proj_e + omega_v_rate * self.nhat
        if self.c_v != 0.0:
            h_mol = h_mol + self.c_v * self.proj_e @ (self.b + self.bd)
        return h_mol + self.g * (alpha * self.sigma_plus + np.conj(alpha) * self.sigma_minus)

    def simulate(self, omega_v_eV: float, kappa_ratio: float):
        omega_v_rate = eV_to_rate(omega_v_eV)
        kappa_rate = kappa_ratio * self.omega_rabi_rate
        y0 = np.concatenate(([self.alpha0], self.psi0))

        def rhs(_, y):
            alpha = y[0]
            psi = y[1:]
            dpsi = -1j * (self._h_mol(alpha, omega_v_rate) @ psi)
            sigma_minus_exp = self._expect(self.sigma_minus, psi)
            dalpha = -(kappa_rate / 2.0 + 1j * self.delta_c) * alpha - 1j * self.g * self.n_molecules * sigma_minus_exp + self.eta
            return np.concatenate(([dalpha], dpsi))

        sol = solve_ivp(
            rhs,
            (self.t0_fs, self.t1_fs),
            y0,
            t_eval=self.t_eval,
            rtol=self.rtol,
            atol=self.atol,
            method=self.method,
        )
        psi_t = sol.y[1:, :].T
        n_g_avg = np.real([self._expect(self.proj_g @ self.nhat, psi) for psi in psi_t])
        mask = sol.t >= self.time_avg_start_fs
        evib_g_per_mol_eV = omega_v_eV * n_g_avg

        return {
            "nu_eV": omega_v_eV,
            "kappa_ratio": kappa_ratio,
            "kappa_rate_fs_inv": kappa_rate,
            "kappa_eV": kappa_rate * HBAR_eVfs,
            "omega_rabi_eV": self.omega_rabi_eV,
            "omega_rabi_rate_fs_inv": self.omega_rabi_rate,
            "time_avg_start_fs": self.time_avg_start_fs,
            "time_window_fs": self.t1_fs - self.t0_fs,
            "Evib_per_molecule_g_avg_eV": evib_g_per_mol_eV[mask].mean(),
            "Evib_per_molecule_g_max_eV": evib_g_per_mol_eV.max(),
        }


def parse_args():
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Generate Fig. 3d MF vibrational-energy sweeps for multiple cavity losses."
    )
    parser.add_argument(
        "--omega-v-values",
        type=float,
        nargs="+",
        default=None,
        help="Explicit nonuniform vibrational frequencies in eV. If omitted, numeric directory names in the script directory are used.",
    )
    parser.add_argument("--omega-v-min", type=float, default=0.16)
    parser.add_argument("--omega-v-max", type=float, default=0.24)
    parser.add_argument("--num-omega", type=int, default=41)
    parser.add_argument(
        "--kappa-ratios",
        type=float,
        nargs="+",
        # default=[0.00, 0.01, 0.05, 0.1],
        default=[0.2],
        help="Dimensionless cavity losses specified as kappa/Omega.",
    )
    parser.add_argument("--t1-fs", type=float, default=20000.0)
    parser.add_argument("--num-pts", type=int, default=400001)
    parser.add_argument("--time-avg-start-fs", type=float, default=0.0)
    parser.add_argument("--vib-trunc", type=int, default=5)
    parser.add_argument("--n-molecules", type=int, default=10000)
    parser.add_argument("--output-dir", type=Path, default=script_dir / "kappa_sweep")
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.omega_v_values is not None:
        omega_values = np.array(sorted(set(args.omega_v_values)), dtype=float)
    else:
        omega_values = discover_omega_values(Path(__file__).resolve().parent)
        if omega_values.size == 0:
            omega_values = np.linspace(args.omega_v_min, args.omega_v_max, args.num_omega)

    runner = MFKappaSweep(
        n_molecules=args.n_molecules,
        vib_trunc=args.vib_trunc,
        t1_fs=args.t1_fs,
        num_pts=args.num_pts,
        time_avg_start_fs=args.time_avg_start_fs,
    )

    all_rows = []
    for kappa_ratio in args.kappa_ratios:
        rows = []
        print(f"Running kappa/Omega = {kappa_ratio:.3f}")
        for idx, omega_v_eV in enumerate(omega_values, start=1):
            print(f"  [{idx:>3}/{len(omega_values):>3}] nu = {omega_v_eV:.6f} eV")
            row = runner.simulate(omega_v_eV=omega_v_eV, kappa_ratio=kappa_ratio)
            rows.append(row)
            all_rows.append(row)

        per_kappa_path = output_dir / f"kappa_ratio_{sanitize_float(kappa_ratio)}.csv"
        write_csv(per_kappa_path, rows)
        print(f"  Wrote {per_kappa_path}")

    write_csv(output_dir / "kappa_sweep_summary.csv", all_rows)
    print(f"Wrote {output_dir / 'kappa_sweep_summary.csv'}")


if __name__ == "__main__":
    main()
