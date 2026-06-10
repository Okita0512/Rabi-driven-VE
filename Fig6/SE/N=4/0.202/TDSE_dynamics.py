import numpy as np
from scipy.sparse import csr_matrix, kron, identity
from scipy.sparse.linalg import expm_multiply

# -------------------- Unit conversion --------------------
EV_PER_HARTREE = 27.211386245988         # eV / Hartree
FS_PER_AUT     = 0.024188843265857       # fs / atomic unit of time

def eV_to_Hartree(x_eV: float) -> float:
    return x_eV / EV_PER_HARTREE

def fs_to_aut(t_fs: np.ndarray) -> np.ndarray:
    return t_fs / FS_PER_AUT

def vibrational_vacuum(N: int, vib_trunc: int, dtype=np.complex128) -> np.ndarray:
    """Tensor-product vibrational vacuum |0...0> across N modes."""
    d = vib_trunc
    v0 = np.zeros((d,), dtype=dtype); v0[0] = 1.0
    vib0 = v0.copy()
    for _ in range(max(N - 1, 0)):
        vib0 = np.kron(vib0, v0)
    return vib0

# -------------------- Hamiltonian builder --------------------
def htc_hamiltonian(
    N: int,
    omega_c: float,
    omega_0: float,
    omega_v: float,
    g_c: float,
    c_v: float,
    vib_trunc: int = 2,
    dtype=np.complex128,
):
    """
    Holstein-Tavis-Cummings Hamiltonian in the zero/one-excitation manifold.
    Basis order: |G>, |C>, |1>,...,|N>, each tensored with vibrational space.
    """
    dim_e = N + 2
    def proj_e(idx):
        e = np.zeros((dim_e, 1), dtype=dtype); e[idx, 0] = 1.0
        return csr_matrix(e @ e.conj().T)

    P_g = proj_e(0)
    P_c = proj_e(1)
    P_n = [proj_e(j + 2) for j in range(N)]
    P_exc = sum(P_n, start=csr_matrix((dim_e, dim_e), dtype=dtype))

    def flip_cn(e_idx):
        e_c = np.zeros((dim_e, 1), dtype=dtype); e_c[1, 0] = 1.0
        e_n = np.zeros((dim_e, 1), dtype=dtype); e_n[e_idx, 0] = 1.0
        return csr_matrix(e_c @ e_n.conj().T) + csr_matrix(e_n @ e_c.conj().T)

    d = vib_trunc
    a = np.zeros((d, d), dtype=dtype)
    for m in range(1, d):
        a[m-1, m] = np.sqrt(m)
    adag  = a.conj().T
    n_op  = adag @ a
    I_v1  = identity(d, dtype=dtype, format='csr')

    def vib_local(op, j):
        out = None
        for k in range(N):
            block = op if k == j else I_v1
            out = block if out is None else kron(out, block, format='csr')
        return out if N > 0 else csr_matrix((1, 1), dtype=dtype)

    b_list  = [vib_local(csr_matrix(a), j) for j in range(N)]
    bd_list = [vib_local(csr_matrix(adag), j) for j in range(N)]
    n_list  = [vib_local(csr_matrix(n_op), j) for j in range(N)]
    I_v     = identity(d**N, dtype=dtype, format='csr') if N > 0 else identity(1, dtype=dtype, format='csr')

    P_vib_levels = [csr_matrix(np.diag([1 if m == n else 0 for m in range(d)]), dtype=dtype) for n in range(d)]
    P_vib_level_sums = []
    for n in range(d):
        accum = csr_matrix((I_v.shape[0], I_v.shape[0]), dtype=dtype)
        for j in range(N):
            accum += vib_local(P_vib_levels[n], j)
        P_vib_level_sums.append(accum)

    H = csr_matrix((dim_e*I_v.shape[0], dim_e*I_v.shape[0]), dtype=dtype)
    H += kron(omega_c * P_c, I_v, format='csr')
    for n in range(N): H += kron(omega_0 * P_n[n], I_v, format='csr')
    for n in range(N): H += kron(g_c * flip_cn(n + 2), I_v, format='csr')
    for n in range(N): H += kron(c_v * P_n[n], b_list[n] + bd_list[n], format='csr')

    vib_number_sum = sum(n_list, start=csr_matrix((I_v.shape[0], I_v.shape[0]), dtype=dtype))
    Hvib_full = kron(identity(dim_e, dtype=dtype, format='csr'), omega_v * vib_number_sum, format='csr')
    H += Hvib_full

    return (
        H,
        {"dim_elec": dim_e, "dim_vib": I_v.shape[0], "dim_total": dim_e*I_v.shape[0]},
        Hvib_full,
        P_g,
        P_c,
        P_exc,
        vib_number_sum,
        P_vib_level_sums,
    )

def polariton_projectors(N, omega_c, omega_0, g_c, vib_trunc=2, dtype=np.complex128):
    dim_e = N + 2
    e_c = np.zeros((dim_e,), dtype=dtype); e_c[1] = 1.0
    e_b = np.zeros((dim_e,), dtype=dtype); e_b[2:] = 1.0 / np.sqrt(N)

    H_2 = np.array([[omega_c, g_c*np.sqrt(N)],
                    [g_c*np.sqrt(N), omega_0]], dtype=float)
    vals, vecs = np.linalg.eigh(H_2)
    lp_vec = vecs[:, 0]
    up_vec = vecs[:, 1]

    eLP = lp_vec[0]*e_c + lp_vec[1]*e_b
    eUP = up_vec[0]*e_c + up_vec[1]*e_b

    P_LP_e = np.outer(eLP, eLP.conj())
    P_UP_e = np.outer(eUP, eUP.conj())

    dim_v = vib_trunc**N if N > 0 else 1
    P_UP = kron(csr_matrix(P_UP_e), identity(dim_v, dtype=dtype, format='csr'))
    P_LP = kron(csr_matrix(P_LP_e), identity(dim_v, dtype=dtype, format='csr'))
    return P_UP, P_LP

def schrodinger_propagate(H, psi0, times_aut: np.ndarray) -> np.ndarray:
    A = (-1j) * H
    Y = expm_multiply(A, psi0, start=0.0, stop=times_aut[-1], num=len(times_aut), endpoint=True)
    return np.vstack([y for y in Y])

if __name__ == "__main__":
    N = 4
    vib_trunc = 5

    omega_c = eV_to_Hartree(2.0)
    omega_0 = eV_to_Hartree(2.0)
    omega_v = eV_to_Hartree(0.202)
    g_c     = eV_to_Hartree(0.2 / (2 * np.sqrt(N)))
    c_v     = eV_to_Hartree(0.02)

    H, info, Hvib_full, P_g, P_c, P_exc, vib_number_sum, P_vib_level_sums = htc_hamiltonian(
        N, omega_c, omega_0, omega_v, g_c, c_v, vib_trunc=vib_trunc
    )
    print(f"H dims: {info}")

    P_UP, P_LP = polariton_projectors(N, omega_c, omega_0, g_c, vib_trunc=vib_trunc)

    dim_e = info["dim_elec"]
    vib0 = vibrational_vacuum(N, vib_trunc, dtype=np.complex128)
    psi0_e = np.zeros((dim_e,), dtype=np.complex128); psi0_e[1] = 1.0  # |G,1>
    psi0 = np.kron(psi0_e, vib0).astype(np.complex128)

    I_v = identity(info["dim_vib"], dtype=np.complex128, format='csr')
    e_b = np.zeros((dim_e,), dtype=np.complex128); e_b[2:] = 1.0 / np.sqrt(N)

    P_gs = kron(P_g, I_v, format='csr')
    P_bright_e = csr_matrix(np.outer(e_b, e_b.conj()))
    P_ds = kron(P_exc - P_bright_e, I_v, format='csr')

    t_total_fs = 2000.0
    dt_fs = 2.5
    times_fs = np.arange(0.0, t_total_fs + 1e-12, dt_fs)
    times_aut = fs_to_aut(times_fs)

    Psi_t = schrodinger_propagate(H, psi0, times_aut)

    P_UP_t = np.array([np.real(np.vdot(Psi_t[i], P_UP.dot(Psi_t[i]))) for i in range(len(times_fs))])
    P_LP_t = np.array([np.real(np.vdot(Psi_t[i], P_LP.dot(Psi_t[i]))) for i in range(len(times_fs))])
    P_GS_t = np.array([np.real(np.vdot(Psi_t[i], P_gs.dot(Psi_t[i]))) for i in range(len(times_fs))])
    P_DS_t = np.array([np.real(np.vdot(Psi_t[i], P_ds.dot(Psi_t[i]))) for i in range(len(times_fs))])
    np.savetxt(
        "UP_LP_GS_DS_population.dat",
        np.column_stack([times_fs, P_UP_t, P_LP_t, P_GS_t, P_DS_t]),
        header="time_fs  P_UP  P_LP  P_GS  P_DS",
    )

    P_photon = kron(P_c, I_v, format='csr')
    P_exciton = kron(P_exc, I_v, format='csr')
    P_exciton_t = np.array([np.real(np.vdot(Psi_t[i], P_exciton.dot(Psi_t[i]))) for i in range(len(times_fs))])
    P_photon_t = np.array([np.real(np.vdot(Psi_t[i], P_photon.dot(Psi_t[i]))) for i in range(len(times_fs))])
    np.savetxt(
        "exciton_photon_population.dat",
        np.column_stack([times_fs, P_exciton_t, P_photon_t]),
        header="time_fs  P_exc  P_photon",
    )

    Evib_total = np.array([np.real(np.vdot(Psi_t[i], Hvib_full.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Evib_avg_eV = (Evib_total / N) * EV_PER_HARTREE
    np.savetxt("Evib_avg.dat", np.column_stack([times_fs, Evib_avg_eV]))

    Nvib_ground_op = kron(P_g, vib_number_sum, format='csr')
    Nvib_excited_op = kron(P_c + P_exc, vib_number_sum, format='csr')
    Nvib_ground = np.array([np.real(np.vdot(Psi_t[i], Nvib_ground_op.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Nvib_excited = np.array([np.real(np.vdot(Psi_t[i], Nvib_excited_op.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Evib_ground_eV = omega_v * Nvib_ground * EV_PER_HARTREE
    Evib_excited_eV = omega_v * Nvib_excited * EV_PER_HARTREE
    np.savetxt(
        "vib_ground_excited.dat",
        np.column_stack([times_fs, Nvib_ground, Evib_ground_eV, Nvib_excited, Evib_excited_eV]),
        header="time_fs  Nvib_ground  Evib_ground_eV  Nvib_excited  Evib_excited_eV",
    )

    pop_g_levels = np.zeros((len(times_fs), vib_trunc), dtype=float)
    pop_e_levels = np.zeros((len(times_fs), vib_trunc), dtype=float)
    for n in range(vib_trunc):
        Pg_n = kron(P_g, P_vib_level_sums[n], format='csr')
        Pe_n = kron(P_c + P_exc, P_vib_level_sums[n], format='csr')
        pop_g_levels[:, n] = [np.real(np.vdot(Psi_t[i], Pg_n.dot(Psi_t[i]))) / N for i in range(len(times_fs))]
        pop_e_levels[:, n] = [np.real(np.vdot(Psi_t[i], Pe_n.dot(Psi_t[i]))) / N for i in range(len(times_fs))]

    level_indices = np.arange(vib_trunc, dtype=float)
    Evib_g_levels_eV = omega_v * level_indices[None, :] * pop_g_levels * EV_PER_HARTREE
    Evib_e_levels_eV = omega_v * level_indices[None, :] * pop_e_levels * EV_PER_HARTREE

    np.savetxt(
        "vib_level_pop.dat",
        np.column_stack([times_fs, pop_g_levels, pop_e_levels]),
        header="time_fs " + " ".join([f"P_g_n{n}" for n in range(vib_trunc)] + [f"P_e_n{n}" for n in range(vib_trunc)]),
    )
    np.savetxt(
        "vib_level_energy.dat",
        np.column_stack([times_fs, Evib_g_levels_eV, Evib_e_levels_eV]),
        header="time_fs " + " ".join([f"Evib_g_n{n}_eV" for n in range(vib_trunc)] + [f"Evib_e_n{n}_eV" for n in range(vib_trunc)]),
    )

    print("Saved: UP_LP_GS_DS_population.dat, exciton_photon_population.dat, Evib_avg.dat (eV per mode), vib_ground_excited.dat, vib_level_pop.dat, vib_level_energy.dat")
