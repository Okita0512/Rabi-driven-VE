import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, kron, identity
from scipy.sparse.linalg import expm_multiply

# -------------------- Unit conversion --------------------
EV_PER_HARTREE = 27.211386245988         # eV / Hartree
FS_PER_AUT     = 0.024188843265857       # fs / atomic unit of time

def eV_to_Hartree(x_eV: float) -> float:
    return x_eV / EV_PER_HARTREE

def fs_to_aut(t_fs: np.ndarray) -> np.ndarray:
    return t_fs / FS_PER_AUT

# -------------------- Hamiltonian builder --------------------
def htc_hamiltonian(
    N: int,
    omega_c: float,    # Hartree
    omega_0: float,    # Hartree
    omega_v: float,    # Hartree
    g_c: float,        # Hartree
    c_v: float,        # Hartree
    vib_trunc: int = 2,
    dtype=np.complex128,
):
    """
    Holstein–Tavis–Cummings Hamiltonian in the single-excitation subspace.
    Returns: H (CSR), dims, Hvib_full = I_e ⊗ (omega_v * Σ b†b).
    """
    dim_e = N + 1  # |C>, |1>,...,|N>
    def proj_e(idx):
        e = np.zeros((dim_e, 1), dtype=dtype); e[idx, 0] = 1.0
        return csr_matrix(e @ e.conj().T)

    P_c = proj_e(0)
    P_n = [proj_e(j) for j in range(1, N + 1)]
    P_exc = sum(P_n, start=csr_matrix((dim_e, dim_e), dtype=dtype))

    def flip_cn(n):
        """|C><n| + |n><C| in electronic subspace."""
        e_c = np.zeros((dim_e, 1), dtype=dtype); e_c[0, 0] = 1.0
        e_n = np.zeros((dim_e, 1), dtype=dtype); e_n[n, 0] = 1.0
        return csr_matrix(e_c @ e_n.conj().T) + csr_matrix(e_n @ e_c.conj().T)

    # Vibrational local operators (truncated to vib_trunc)
    d = vib_trunc
    a = np.zeros((d, d), dtype=dtype)
    for m in range(1, d):
        a[m-1, m] = np.sqrt(m)
    adag  = a.conj().T
    n_op  = adag @ a
    I_v1  = identity(d, dtype=dtype, format='csr')

    def vib_local(op, j):
        """Embed single-mode operator `op` on mode j (0..N-1) across N modes."""
        out = None
        for k in range(N):
            block = op if k == j else I_v1
            out = block if out is None else kron(out, block, format='csr')
        return out if N > 0 else csr_matrix((1, 1), dtype=dtype)

    b_list  = [vib_local(csr_matrix(a),    j) for j in range(N)]
    bd_list = [vib_local(csr_matrix(adag), j) for j in range(N)]
    n_list  = [vib_local(csr_matrix(n_op), j) for j in range(N)]
    I_v     = identity(d**N, dtype=dtype, format='csr') if N > 0 else identity(1, dtype=dtype, format='csr')

    # Vibrational level projectors (marginal, summed over modes)
    P_vib_levels = [csr_matrix(np.diag([1 if m == n else 0 for m in range(d)]), dtype=dtype) for n in range(d)]
    P_vib_level_sums = []
    for n in range(d):
        accum = csr_matrix((I_v.shape[0], I_v.shape[0]), dtype=dtype)
        for j in range(N):
            accum += vib_local(P_vib_levels[n], j)
        P_vib_level_sums.append(accum)

    # Assemble H on (electronic ⊗ vibrational) space
    H = csr_matrix(((N+1)*I_v.shape[0], (N+1)*I_v.shape[0]), dtype=dtype)
    H += kron(omega_c * P_c, I_v, format='csr')                     # cavity energy
    for n in range(N): H += kron(omega_0 * P_n[n], I_v, format='csr')  # exciton site energy
    for n in range(N): H += kron(g_c * flip_cn(n + 1), I_v, format='csr')  # light-matter coupling
    for n in range(N): H += kron(c_v * P_n[n], b_list[n] + bd_list[n], format='csr')  # Holstein coupling

    vib_number_sum = sum(n_list, start=csr_matrix((I_v.shape[0], I_v.shape[0]), dtype=dtype))
    Hvib_full = kron(identity(N+1, dtype=dtype, format='csr'), omega_v * vib_number_sum, format='csr')  # I_e ⊗ ωv Σ n_j
    H += Hvib_full  # add vibrational energy into H

    return (
        H,
        {"dim_elec": N+1, "dim_vib": I_v.shape[0], "dim_total": (N+1)*I_v.shape[0]},
        Hvib_full,
        P_c,
        P_exc,
        vib_number_sum,
        P_vib_level_sums,
    )

# -------------------- Upper polariton --------------------
# -------------------- Upper/Lower polaritons --------------------
def polariton_states_and_projectors(N, omega_c, omega_0, g_c, vib_trunc=2, dtype=np.complex128):
    """
    返回：psi0(取UP⊗|0...0>作为初态)、P_UP、P_LP
    Energies: Hartree; 在 {|C>, |B>} 的 2x2 子空间内对角化得到 UP/LP。
    """
    dim_e = N + 1
    e_c = np.zeros((dim_e,), dtype=dtype); e_c[0] = 1.0
    e_b = np.zeros((dim_e,), dtype=dtype); e_b[1:] = 1.0 / np.sqrt(N)  # |B>

    # 2×2 Rabi 块
    H_2 = np.array([[omega_c, g_c*np.sqrt(N)],
                    [g_c*np.sqrt(N), omega_0]], dtype=float)
    vals, vecs = np.linalg.eigh(H_2)   # 升序：vals[0]=LP, vals[1]=UP
    lp_vec = vecs[:, 0]
    up_vec = vecs[:, 1]

    # 嵌回电子基（|C>, |1>,...,|N|）
    eLP = lp_vec[0]*e_c + lp_vec[1]*e_b
    eUP = up_vec[0]*e_c + up_vec[1]*e_b

    # 投影算符（电子子空间）
    P_LP_e = np.outer(eLP, eLP.conj())
    P_UP_e = np.outer(eUP, eUP.conj())

    # 振动真空 |0...0>
    d = vib_trunc
    v0 = np.zeros((d,), dtype=dtype); v0[0] = 1.0
    vib0 = v0.copy()
    for _ in range(N - 1):
        vib0 = np.kron(vib0, v0)

    # 初态：UP ⊗ |0...0>
    psi0 = np.kron(eUP, vib0).astype(dtype)
    psi0 /= np.linalg.norm(psi0)

    # 张量到总空间
    dim_v = d**N if N > 0 else 1
    P_UP = kron(csr_matrix(P_UP_e), identity(dim_v, dtype=dtype, format='csr'))
    P_LP = kron(csr_matrix(P_LP_e), identity(dim_v, dtype=dtype, format='csr'))
    return psi0, P_UP, P_LP

# -------------------- Schrödinger propagation --------------------
def schrodinger_propagate(H, psi0, times_aut: np.ndarray) -> np.ndarray:
    """
    psi(t) = exp(-i H t) psi0 for a vector of times (atomic units).
    Returns array shape (len(times), dim).
    """
    A = (-1j) * H
    Y = expm_multiply(A, psi0, start=0.0, stop=times_aut[-1], num=len(times_aut), endpoint=True)
    return np.vstack([y for y in Y])

# -------------------- Main: parameters & run --------------------
if __name__ == "__main__":
    # Model size & truncation
    N = 2
    vib_trunc = 10

    # Energies given in eV (converted to Hartree)
    omega_c = eV_to_Hartree(2.0)
    omega_0 = eV_to_Hartree(2.0)
    omega_v = eV_to_Hartree(0.2)
    g_c     = eV_to_Hartree(0.2 / (2 * np.sqrt(N)))  # your choice here
    # g_c     = eV_to_Hartree(0.05)  # your choice here
    c_v     = eV_to_Hartree(0.02)

    # Build Hamiltonian (now returns Hvib_full, projectors, vib number operator)
    H, info, Hvib_full, P_c, P_exc, vib_number_sum, P_vib_level_sums = htc_hamiltonian(
        N, omega_c, omega_0, omega_v, g_c, c_v, vib_trunc=vib_trunc
    )
    print(f"H dims: {info}")

    # Initial state & UP projector
    psi0, P_UP, P_LP = polariton_states_and_projectors(N, omega_c, omega_0, g_c, vib_trunc=vib_trunc)

    # Time grid
    t_total_fs = 2000.0
    dt_fs = 0.025
    times_fs = np.arange(0.0, t_total_fs + 1e-12, dt_fs)
    times_aut = fs_to_aut(times_fs)

    # Propagate
    Psi_t = schrodinger_propagate(H, psi0, times_aut)

    # ---------- (1) Upper-polariton population ----------
    P_UP_t = np.array([np.real(np.vdot(Psi_t[i], P_UP.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Pt = np.zeros((len(P_UP_t), 2), dtype=float)
    Pt[:, 0] = times_fs
    Pt[:, 1] = P_UP_t
#    np.savetxt("UP_population.dat", Pt)

    # ---------- (1b) Lower-polariton population ----------
    P_LP_t = np.array([np.real(np.vdot(Psi_t[i], P_LP.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Lt = np.zeros((len(P_LP_t), 2), dtype=float)
    Lt[:, 0] = times_fs
    Lt[:, 1] = P_LP_t
#    np.savetxt("LP_population.dat", Lt)

    # （可选）同时保存合并文件，便于后续统一绘图
    Combo = np.column_stack([times_fs, P_UP_t, P_LP_t])
    np.savetxt("UP_LP_population.dat", Combo, header="time_fs  P_UP  P_LP")

    # ---------- (2) Average vibrational energy per mode ----------
    # Evib_total(t) = <ψ(t)| Hvib_full |ψ(t)>  (Hartree)
    Evib_total = np.array([np.real(np.vdot(Psi_t[i], Hvib_full.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Evib_avg_eV = (Evib_total / N) * EV_PER_HARTREE   # convert to eV per mode
    Et = np.zeros((len(times_fs), 2), dtype=float)
    Et[:, 0] = times_fs
    Et[:, 1] = Evib_avg_eV
    np.savetxt("Evib_avg.dat", Et)

    # ---------- (3) Vib population/energy on ground vs excited electronic surfaces ----------
    # Ground surface corresponds to the cavity |C> manifold (all molecules in electronic ground).
    Nvib_ground_op = kron(P_c, vib_number_sum, format='csr')
    Nvib_excited_op = kron(P_exc, vib_number_sum, format='csr')
    Nvib_ground = np.array([np.real(np.vdot(Psi_t[i], Nvib_ground_op.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Nvib_excited = np.array([np.real(np.vdot(Psi_t[i], Nvib_excited_op.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Evib_ground_eV = omega_v * Nvib_ground * EV_PER_HARTREE   # total vib energy on ground surface
    Evib_excited_eV = omega_v * Nvib_excited * EV_PER_HARTREE # total vib energy on excited surfaces

    Vsplit = np.column_stack([times_fs, Nvib_ground, Evib_ground_eV, Nvib_excited, Evib_excited_eV])
    np.savetxt(
        "vib_ground_excited.dat",
        Vsplit,
        header="time_fs  Nvib_ground  Evib_ground_eV  Nvib_excited  Evib_excited_eV",
    )

    # ---------- (4) Vib level-resolved populations/energies (marginal over modes) ----------
    pop_g_levels = np.zeros((len(times_fs), vib_trunc), dtype=float)
    pop_e_levels = np.zeros((len(times_fs), vib_trunc), dtype=float)
    for n in range(vib_trunc):
        Pg_n = kron(P_c, P_vib_level_sums[n], format='csr')
        Pe_n = kron(P_exc, P_vib_level_sums[n], format='csr')
        pop_g_levels[:, n] = [
            np.real(np.vdot(Psi_t[i], Pg_n.dot(Psi_t[i]))) for i in range(len(times_fs))
        ]
        pop_e_levels[:, n] = [
            np.real(np.vdot(Psi_t[i], Pe_n.dot(Psi_t[i]))) for i in range(len(times_fs))
        ]

    level_indices = np.arange(vib_trunc, dtype=float)
    Evib_g_levels_eV = omega_v * level_indices[None, :] * pop_g_levels * EV_PER_HARTREE
    Evib_e_levels_eV = omega_v * level_indices[None, :] * pop_e_levels * EV_PER_HARTREE

    pop_table = np.column_stack([times_fs, pop_g_levels, pop_e_levels])
    header_pop = "time_fs " + " ".join(
        [f"P_g_n{n}" for n in range(vib_trunc)] + [f"P_e_n{n}" for n in range(vib_trunc)]
    )
    np.savetxt("vib_level_pop.dat", pop_table, header=header_pop)

    energy_table = np.column_stack([times_fs, Evib_g_levels_eV, Evib_e_levels_eV])
    header_energy = "time_fs " + " ".join(
        [f"Evib_g_n{n}_eV" for n in range(vib_trunc)] + [f"Evib_e_n{n}_eV" for n in range(vib_trunc)]
    )
    np.savetxt("vib_level_energy.dat", energy_table, header=header_energy)

    print("Saved: UP_population.dat, Evib_avg.dat (eV per mode), vib_ground_excited.dat, vib_level_pop.dat, vib_level_energy.dat")
