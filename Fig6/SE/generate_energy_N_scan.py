"""
Generate energy_summary_N{N}.csv for N = 1, 2, 4 using the full HTC TDSE.

Parameters match the existing Fig3 SE data:
  sqrt(N)*gc = 0.10 eV  (collective coupling fixed)
  cv = 20 meV
  omega0 = omegac = 2.0 eV
  vib_trunc = 5
  T_total = 2000 fs, dt = 0.025 fs
  Initial state: |C, vac_vib> (one photon, electronic ground, vibrational vacuum)

Output:
  SE/energy_summary_N1.csv
  SE/energy_summary_N2.csv
  SE/energy_summary_N4.csv  (re-generated for verification)
"""

import os
import numpy as np
from scipy.sparse import csr_matrix, kron, identity
from scipy.sparse.linalg import expm_multiply

# -------------------- Unit conversion --------------------
EV_PER_HARTREE = 27.211386245988
FS_PER_AUT     = 0.024188843265857

def eV_to_Hartree(x): return x / EV_PER_HARTREE
def fs_to_aut(t):     return t / FS_PER_AUT

# -------------------- HTC Hamiltonian --------------------
def htc_hamiltonian(N, omega_c, omega_0, omega_v, g_c, c_v, vib_trunc=5, dtype=np.complex128):
    dim_e = N + 2
    def proj_e(idx):
        e = np.zeros((dim_e, 1), dtype=dtype); e[idx, 0] = 1.0
        return csr_matrix(e @ e.conj().T)

    P_c   = proj_e(1)
    P_n   = [proj_e(j + 2) for j in range(N)]

    def flip_cn(e_idx):
        e_c = np.zeros((dim_e, 1), dtype=dtype); e_c[1, 0] = 1.0
        e_n = np.zeros((dim_e, 1), dtype=dtype); e_n[e_idx, 0] = 1.0
        return csr_matrix(e_c @ e_n.conj().T) + csr_matrix(e_n @ e_c.conj().T)

    d = vib_trunc
    a = np.zeros((d, d), dtype=dtype)
    for m in range(1, d):
        a[m-1, m] = np.sqrt(m)
    adag = a.conj().T
    I_v1 = identity(d, dtype=dtype, format='csr')

    def vib_local(op, j):
        out = None
        for k in range(N):
            block = op if k == j else I_v1
            out = block if out is None else kron(out, block, format='csr')
        return out

    b_list  = [vib_local(csr_matrix(a),    j) for j in range(N)]
    bd_list = [vib_local(csr_matrix(adag), j) for j in range(N)]
    n_list  = [vib_local(csr_matrix(adag @ a), j) for j in range(N)]
    I_v     = identity(d**N, dtype=dtype, format='csr')

    H = csr_matrix((dim_e * d**N, dim_e * d**N), dtype=dtype)
    H += kron(omega_c * P_c, I_v, format='csr')
    for n in range(N):
        H += kron(eV_to_Hartree(0.0) * P_n[n], I_v, format='csr')  # omega_0 * P_n added below
    for n in range(N):
        H += kron(omega_0 * P_n[n], I_v, format='csr')
    for n in range(N):
        H += kron(g_c * flip_cn(n + 2), I_v, format='csr')
    for n in range(N):
        H += kron(c_v * P_n[n], b_list[n] + bd_list[n], format='csr')

    vib_number_sum = sum(n_list, start=csr_matrix((d**N, d**N), dtype=dtype))
    Hvib_full = kron(identity(dim_e, dtype=dtype, format='csr'), omega_v * vib_number_sum, format='csr')
    H += Hvib_full
    return H, Hvib_full, dim_e, d**N


def htc_hamiltonian_clean(N, omega_c, omega_0, omega_v, g_c, c_v, vib_trunc=5, dtype=np.complex128):
    """Clean version without double-counting omega_0."""
    dim_e = N + 2
    def proj_e(idx):
        e = np.zeros((dim_e, 1), dtype=dtype); e[idx, 0] = 1.0
        return csr_matrix(e @ e.conj().T)

    P_c = proj_e(1)
    P_n = [proj_e(j + 2) for j in range(N)]

    def flip_cn(e_idx):
        e_c = np.zeros((dim_e, 1), dtype=dtype); e_c[1, 0] = 1.0
        e_n = np.zeros((dim_e, 1), dtype=dtype); e_n[e_idx, 0] = 1.0
        return csr_matrix(e_c @ e_n.conj().T) + csr_matrix(e_n @ e_c.conj().T)

    d = vib_trunc
    a = np.zeros((d, d), dtype=dtype)
    for m in range(1, d):
        a[m-1, m] = np.sqrt(m)
    adag = a.conj().T
    I_v1 = identity(d, dtype=dtype, format='csr')

    def vib_local(op, j):
        out = None
        for k in range(N):
            block = op if k == j else I_v1
            out = block if out is None else kron(out, block, format='csr')
        return out

    b_list  = [vib_local(csr_matrix(a),    j) for j in range(N)]
    bd_list = [vib_local(csr_matrix(adag), j) for j in range(N)]
    n_list  = [vib_local(csr_matrix(adag @ a), j) for j in range(N)]
    I_v     = identity(d**N, dtype=dtype, format='csr')

    H = csr_matrix((dim_e * d**N, dim_e * d**N), dtype=dtype)
    H += kron(omega_c * P_c, I_v, format='csr')
    for n in range(N):
        H += kron(omega_0 * P_n[n], I_v, format='csr')
    for n in range(N):
        H += kron(g_c * flip_cn(n + 2), I_v, format='csr')
    for n in range(N):
        H += kron(c_v * P_n[n], b_list[n] + bd_list[n], format='csr')

    vib_number_sum = sum(n_list, start=csr_matrix((d**N, d**N), dtype=dtype))
    Hvib_full = kron(identity(dim_e, dtype=dtype, format='csr'), omega_v * vib_number_sum, format='csr')
    H += Hvib_full
    return H, Hvib_full, dim_e, d**N


def compute_evib_avg(N, nu_eV, vib_trunc=5, t_total_fs=2000.0, dt_fs=0.025):
    """Compute time-averaged Evib per molecule for given N and nu."""
    omega_c = eV_to_Hartree(2.0)
    omega_0 = eV_to_Hartree(2.0)
    omega_v = eV_to_Hartree(nu_eV)
    g_c     = eV_to_Hartree(0.2 / (2.0 * np.sqrt(N)))   # sqrt(N)*gc = 0.10 eV
    c_v     = eV_to_Hartree(0.02)

    H, Hvib_full, dim_e, dim_v = htc_hamiltonian_clean(
        N, omega_c, omega_0, omega_v, g_c, c_v, vib_trunc=vib_trunc
    )

    # Initial state: |C, vib_vacuum>  (index 1 in electronic space)
    d = vib_trunc
    v0 = np.zeros((d,), dtype=np.complex128); v0[0] = 1.0
    vib0 = v0.copy()
    for _ in range(N - 1):
        vib0 = np.kron(vib0, v0)
    psi0_e = np.zeros((dim_e,), dtype=np.complex128); psi0_e[1] = 1.0
    psi0 = np.kron(psi0_e, vib0).astype(np.complex128)

    times_fs  = np.arange(0.0, t_total_fs + 1e-12, dt_fs)
    times_aut = fs_to_aut(times_fs)

    A = (-1j) * H
    Psi_t = expm_multiply(A, psi0, start=0.0, stop=times_aut[-1],
                          num=len(times_aut), endpoint=True)
    Psi_t = np.vstack([y for y in Psi_t])

    Evib_total = np.array([
        np.real(np.vdot(Psi_t[i], Hvib_full.dot(Psi_t[i])))
        for i in range(len(times_fs))
    ])
    Evib_avg_eV = (Evib_total / N) * EV_PER_HARTREE
    return float(np.mean(Evib_avg_eV))


if __name__ == "__main__":
    # nu values matching the existing Fig3 SE energy_summary.csv
    NU_VALUES = [
        0.16, 0.17, 0.18, 0.19, 0.195, 0.196, 0.197, 0.198,
        0.199, 0.20, 0.201, 0.202, 0.203, 0.21, 0.22, 0.23, 0.24,
    ]

    N_LIST = [1, 2, 4]

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for N in N_LIST:
        print(f"\n=== N = {N} ===")
        rows = []
        for nu in NU_VALUES:
            evib = compute_evib_avg(N, nu)
            rows.append((nu, evib))
            print(f"  nu = {nu:.3f} eV  ->  <Evib_E> = {evib:.6e} eV")

        out_path = os.path.join(script_dir, f"energy_summary_N{N}.csv")
        with open(out_path, "w") as f:
            f.write("intensity_meV,Evib_avg_eV\n")
            for nu, evib in rows:
                f.write(f"{nu},{evib}\n")
        print(f"  Saved: {out_path}")
