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

def gaussian_pulse(
    t_fs: float,
    center_fs: float,
    sigma_fs: float,
    amplitude: float,
    omega_p_eV: float,
) -> float:
    """
    Gaussian envelope A * exp(-(t-center)^2 / (2*sigma^2)) * cos(omega_p * t).
    omega_p is given in eV; t is in fs; result is in Hartree amplitude units.
    """
    env = amplitude * np.exp(-0.5 * ((t_fs - center_fs) / sigma_fs) ** 2)
    omega_p_H = eV_to_Hartree(omega_p_eV)  # Hartree
    t_aut = t_fs / FS_PER_AUT
    return env * np.cos(omega_p_H * t_aut)

def gaussian_envelope(
    t_fs: float,
    center_fs: float,
    sigma_fs: float,
    amplitude: float,
) -> float:
    """Gaussian envelope A * exp(-(t-center)^2 / (2*sigma^2))."""
    return amplitude * np.exp(-0.5 * ((t_fs - center_fs) / sigma_fs) ** 2)

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
    omega_c: float,    # Hartree
    omega_0: float,    # Hartree
    omega_v: float,    # Hartree
    g_c: float,        # Hartree
    c_v: float,        # Hartree
    vib_trunc: int = 2,
    dtype=np.complex128,
):
    """
    Holstein-Tavis-Cummings Hamiltonian in the zero/one-excitation manifold.
    Basis order: |G>, |C>, |1>,...,|N>, each tensored with vibrational space.
    Returns: H (CSR), dims, Hvib_full = I_e kron (omega_v * sum b^† b).
    """
    dim_e = N + 2  # |G>, |C>, |1>,...,|N>
    def proj_e(idx):
        e = np.zeros((dim_e, 1), dtype=dtype); e[idx, 0] = 1.0
        return csr_matrix(e @ e.conj().T)

    P_g = proj_e(0)
    P_c = proj_e(1)
    P_n = [proj_e(j + 2) for j in range(N)]
    P_exc = sum(P_n, start=csr_matrix((dim_e, dim_e), dtype=dtype))

    def flip_cn(e_idx):
        """|C><n| + |n><C| in electronic subspace."""
        e_c = np.zeros((dim_e, 1), dtype=dtype); e_c[1, 0] = 1.0
        e_n = np.zeros((dim_e, 1), dtype=dtype); e_n[e_idx, 0] = 1.0
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

    # Assemble H on (electronic x vibrational) space
    H = csr_matrix((dim_e*I_v.shape[0], dim_e*I_v.shape[0]), dtype=dtype)
    H += kron(omega_c * P_c, I_v, format='csr')                         # cavity energy
    for n in range(N): H += kron(omega_0 * P_n[n], I_v, format='csr')   # exciton site energy
    for n in range(N): H += kron(g_c * flip_cn(n + 2), I_v, format='csr')  # light-matter coupling
    for n in range(N): H += kron(c_v * P_n[n], b_list[n] + bd_list[n], format='csr')  # Holstein coupling

    vib_number_sum = sum(n_list, start=csr_matrix((I_v.shape[0], I_v.shape[0]), dtype=dtype))
    Hvib_full = kron(identity(dim_e, dtype=dtype, format='csr'), omega_v * vib_number_sum, format='csr')  # I_e kron omega_v sum n_j
    H += Hvib_full  # add vibrational energy into H

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

# -------------------- Upper/Lower polaritons --------------------
def polariton_states_and_projectors(N, omega_c, omega_0, g_c, vib_trunc=2, dtype=np.complex128):
    """
    Return: psi_UP (UP tensor |0...0>), P_UP, P_LP.
    Energies in Hartree; diagonalize the 2x2 span {|C>, |B>} to get UP/LP.
    """
    dim_e = N + 2
    e_c = np.zeros((dim_e,), dtype=dtype); e_c[1] = 1.0
    e_b = np.zeros((dim_e,), dtype=dtype); e_b[2:] = 1.0 / np.sqrt(N)  # |B>

    # 2x2 Rabi block in {|C>, |B>}
    H_2 = np.array([[omega_c, g_c*np.sqrt(N)],
                    [g_c*np.sqrt(N), omega_0]], dtype=float)
    vals, vecs = np.linalg.eigh(H_2)   # ascending: vals[0]=LP, vals[1]=UP
    lp_vec = vecs[:, 0]
    up_vec = vecs[:, 1]

    eLP = lp_vec[0]*e_c + lp_vec[1]*e_b
    eUP = up_vec[0]*e_c + up_vec[1]*e_b

    P_LP_e = np.outer(eLP, eLP.conj())
    P_UP_e = np.outer(eUP, eUP.conj())

    vib0 = vibrational_vacuum(N, vib_trunc, dtype=dtype)

    psi0 = np.kron(eUP, vib0).astype(dtype)
    psi0 /= np.linalg.norm(psi0)

    dim_v = vib0.size if N > 0 else 1
    P_UP = kron(csr_matrix(P_UP_e), identity(dim_v, dtype=dtype, format='csr'))
    P_LP = kron(csr_matrix(P_LP_e), identity(dim_v, dtype=dtype, format='csr'))
    return psi0, P_UP, P_LP

# -------------------- Schrodinger propagation --------------------
def schrodinger_propagate(H, psi0, times_aut: np.ndarray) -> np.ndarray:
    """
    psi(t) = exp(-i H t) psi0 for a vector of times (atomic units).
    Returns array shape (len(times), dim).
    """
    A = (-1j) * H
    Y = expm_multiply(A, psi0, start=0.0, stop=times_aut[-1], num=len(times_aut), endpoint=True)
    return np.vstack([y for y in Y])

def schrodinger_propagate_with_drive(
    H_base,
    drive_op,
    pulse_fn,
    psi0,
    times_fs: np.ndarray,
    dtype=np.complex128,
):
    """
    Midpoint Trotter: psi(t+dt) = exp[-i (H + E(t+dt/2) V) dt] psi(t).
    H_base, drive_op are CSR; pulse_fn takes time in fs and returns scalar amplitude in Hartree.
    """
    times_aut = fs_to_aut(times_fs)
    Psi_t = np.zeros((len(times_fs), psi0.size), dtype=dtype)
    Psi_t[0] = psi0
    psi = psi0.copy()
    for i in range(len(times_fs) - 1):
        dt = times_aut[i+1] - times_aut[i]
        t_mid = 0.5 * (times_fs[i+1] + times_fs[i])
        H_eff = H_base + pulse_fn(t_mid) * drive_op
        A = (-1j * dt) * H_eff
        psi = expm_multiply(A, psi)
        Psi_t[i+1] = psi
    return Psi_t

def schrodinger_propagate_with_drive_rwa(
    H_base,
    drive_op_plus,
    drive_op_minus,
    envelope_fn,
    omega_p_eV: float,
    psi0,
    times_fs: np.ndarray,
    dtype=np.complex128,
):
    """
    Midpoint Trotter with RWA drive:
    H_drive(t) = 0.5 * E0(t) * [e^{-i omega t} mu_plus + e^{+i omega t} mu_minus].
    """
    times_aut = fs_to_aut(times_fs)
    omega_p_H = eV_to_Hartree(omega_p_eV)
    Psi_t = np.zeros((len(times_fs), psi0.size), dtype=dtype)
    Psi_t[0] = psi0
    psi = psi0.copy()
    for i in range(len(times_fs) - 1):
        dt = times_aut[i+1] - times_aut[i]
        t_mid_fs = 0.5 * (times_fs[i+1] + times_fs[i])
        t_mid_aut = fs_to_aut(t_mid_fs)
        env = envelope_fn(t_mid_fs)
        phase = np.exp(1j * omega_p_H * t_mid_aut)
        H_drive = 0.5 * env * (phase * drive_op_plus + phase.conj() * drive_op_minus)
        H_eff = H_base + H_drive
        A = (-1j * dt) * H_eff
        psi = expm_multiply(A, psi)
        Psi_t[i+1] = psi
    return Psi_t

# -------------------- Main: parameters & run --------------------
if __name__ == "__main__":
    # Model size & truncation
    N = 4
    vib_trunc = 3

    # Energies given in eV (converted to Hartree)
    omega_c = eV_to_Hartree(2.0)
    omega_0 = eV_to_Hartree(2.0)
    omega_v = eV_to_Hartree(0.2)
    g_c     = eV_to_Hartree(0.2014 / (2 * np.sqrt(N)))  # your choice here
    # g_c     = eV_to_Hartree(0.05)  # your choice here
    c_v     = eV_to_Hartree(0.02)

    # Build Hamiltonian (now returns Hvib_full, projectors, vib number operator)
    H, info, Hvib_full, P_g, P_c, P_exc, vib_number_sum, P_vib_level_sums = htc_hamiltonian(
        N, omega_c, omega_0, omega_v, g_c, c_v, vib_trunc=vib_trunc
    )
    print(f"H dims: {info}")

    # Reference UP/LP projectors (UP state not used as initial state anymore)
    _, P_UP, P_LP = polariton_states_and_projectors(N, omega_c, omega_0, g_c, vib_trunc=vib_trunc)

    # Initial global ground state |G> kron |0...0>
    dim_e = info["dim_elec"]
    vib0 = vibrational_vacuum(N, vib_trunc, dtype=np.complex128)
    psi0_e = np.zeros((dim_e,), dtype=np.complex128); psi0_e[0] = 1.0
    psi0 = np.kron(psi0_e, vib0).astype(np.complex128)

    # Cavity-field coupling (drive the cavity mode)
    # H_pulse(t) = i*hbar*(-a*E_+(t) + a_dag*E_-(t))
    I_v = identity(info["dim_vib"], dtype=np.complex128, format='csr')
    e_g = psi0_e
    e_c = np.zeros((dim_e,), dtype=np.complex128); e_c[1] = 1.0  # |C>
    e_b = np.zeros((dim_e,), dtype=np.complex128); e_b[2:] = 1.0 / np.sqrt(N)
    a_op_elec = csr_matrix(np.outer(e_g, e_c))      # a = |G><C|
    a_dag_elec = csr_matrix(np.outer(e_c, e_g))     # a_dag = |C><G|
    drive_op_plus = (-1j) * kron(a_op_elec, I_v, format='csr')
    drive_op_minus = (1j) * kron(a_dag_elec, I_v, format='csr')

    # Projectors for global ground state and dark-state manifold
    P_gs = kron(P_g, I_v, format='csr')
    P_bright_e = csr_matrix(np.outer(e_b, e_b.conj()))
    P_ds = kron(P_exc - P_bright_e, I_v, format='csr')

    # Gaussian pulse parameters (fs)
    # === short pulse ===
    pulse_center_fs = 10.0
    pulse_sigma_fs = 2.0
    pulse_freq_eV = 2.0
    # === long pulse ===
    #pulse_center_fs = 250.0
    #pulse_sigma_fs = 50.0        # larger than 20 fs to avoid spectral broadening (overlap with DS and UP)
    #pulse_freq_eV = 2.1
    # ==================
    pulse_amplitude = eV_to_Hartree(1e-3)  # weak field (Hartree)
    # pulse_amplitude = eV_to_Hartree(0.525)  # 0.9 pi pulse
    # pulse_amplitude = eV_to_Hartree(0.023)  # pi pulse
    def pulse_envelope(t_fs):
        return gaussian_envelope(
            t_fs,
            center_fs=pulse_center_fs,
            sigma_fs=pulse_sigma_fs,
            amplitude=pulse_amplitude,
        )

    # Time grid
    t_total_fs = 2000.0
    dt_fs = 0.025
    times_fs = np.arange(0.0, t_total_fs + 1e-12, dt_fs)

    # Propagate
    Psi_t = schrodinger_propagate_with_drive_rwa(
        H,
        drive_op_plus,
        drive_op_minus,
        pulse_envelope,
        pulse_freq_eV,
        psi0,
        times_fs,
    )

    # ---------- (1) Upper-polariton population ----------
    P_UP_t = np.array([np.real(np.vdot(Psi_t[i], P_UP.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Pt = np.zeros((len(P_UP_t), 2), dtype=float)
    Pt[:, 0] = times_fs
    Pt[:, 1] = P_UP_t
#    np.savetxt("UP_population.dat", Pt)

    # ---------- (2) Lower-polariton population ----------
    P_LP_t = np.array([np.real(np.vdot(Psi_t[i], P_LP.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Lt = np.zeros((len(P_LP_t), 2), dtype=float)
    Lt[:, 0] = times_fs
    Lt[:, 1] = P_LP_t
#    np.savetxt("LP_population.dat", Lt)

    # ---------- (3) Ground-state and dark-state population ----------
    P_GS_t = np.array([np.real(np.vdot(Psi_t[i], P_gs.dot(Psi_t[i]))) for i in range(len(times_fs))])
    P_DS_t = np.array([np.real(np.vdot(Psi_t[i], P_ds.dot(Psi_t[i]))) for i in range(len(times_fs))])

    Combo = np.column_stack([times_fs, P_UP_t, P_LP_t, P_GS_t, P_DS_t])
    np.savetxt("UP_LP_GS_DS_population.dat", Combo, header="time_fs  P_UP  P_LP  P_GS  P_DS")

    # ---------- (4) Exciton and photon populations ----------
    P_photon = kron(P_c, I_v, format='csr')
    P_exciton = kron(P_exc, I_v, format='csr')
    P_photon_t = np.array([np.real(np.vdot(Psi_t[i], P_photon.dot(Psi_t[i]))) for i in range(len(times_fs))])
    P_exciton_t = np.array([np.real(np.vdot(Psi_t[i], P_exciton.dot(Psi_t[i]))) for i in range(len(times_fs))])
    exph = np.column_stack([times_fs, P_exciton_t, P_photon_t])
    np.savetxt("exciton_photon_population.dat", exph, header="time_fs  P_exc  P_photon")

    # ---------- (2) Average vibrational energy per mode ----------
    # Evib_total(t) = <psi(t)| Hvib_full |psi(t)>  (Hartree)
    Evib_total = np.array([np.real(np.vdot(Psi_t[i], Hvib_full.dot(Psi_t[i]))) for i in range(len(times_fs))])
    Evib_avg_eV = (Evib_total / N) * EV_PER_HARTREE   # convert to eV per mode
    Et = np.zeros((len(times_fs), 2), dtype=float)
    Et[:, 0] = times_fs
    Et[:, 1] = Evib_avg_eV
    np.savetxt("Evib_avg.dat", Et)

    # ---------- (3) Vib population/energy on ground vs excited electronic surfaces ----------
    # Ground surface corresponds to |G>; excited surfaces include |C> and |n>.
    Nvib_ground_op = kron(P_g, vib_number_sum, format='csr')
    Nvib_excited_op = kron(P_c + P_exc, vib_number_sum, format='csr')
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
        Pg_n = kron(P_g, P_vib_level_sums[n], format='csr')
        Pe_n = kron(P_c + P_exc, P_vib_level_sums[n], format='csr')
        pop_g_levels[:, n] = [
            np.real(np.vdot(Psi_t[i], Pg_n.dot(Psi_t[i]))) / N for i in range(len(times_fs))
        ]  # average per mode
        pop_e_levels[:, n] = [
            np.real(np.vdot(Psi_t[i], Pe_n.dot(Psi_t[i]))) / N for i in range(len(times_fs))
        ]  # average per mode

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

    print("Saved: UP_population.dat, UP_LP_GS_DS_population.dat, exciton_photon_population.dat, Evib_avg.dat (eV per mode), vib_ground_excited.dat, vib_level_pop.dat, vib_level_energy.dat")
