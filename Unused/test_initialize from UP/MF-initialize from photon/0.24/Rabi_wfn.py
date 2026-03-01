import numpy as np
from numpy import kron
from scipy.integrate import solve_ivp

# ---------------- constants ----------------
HBAR_eVfs = 0.658211951  # ħ [eV·fs]
def eV_to_rate(e_eV):    # energy [eV] -> angular frequency [1/fs]
    return e_eV / HBAR_eVfs

# ---------------- user parameters ----------------
N           = 10000      # number of identical, uncorrelated molecules
vib_trunc   = 5          # vibrational cutoff per molecule
omega_c_eV  = 2.000      # cavity frequency [eV]
omega_0_eV  = 2.000      # exciton frequency [eV]
omega_v_eV  = 0.240      # vibrational frequency [eV] (used if vib_trunc>=2)
g_eV        = 0.10 / np.sqrt(N)      # light–matter coupling [eV]
c_v_eV      = 0.02        # Holstein coupling [eV], set 0 for clean Rabi

# rotating frame frequency (pick equal to cavity/exciton for resonance)
omega_d_eV  = 2.000      # choose =omega_c_eV=omega_0_eV for Δ=0 (resonant Rabi)

# no dissipation, no external drive:
kappa_rate     = 0.0     # cavity loss [1/fs]
eta            = 0.0 + 0.0j  # external cavity drive [1/fs]; keep 0

# initial state: superposition of MF normal modes (LP/UP)
# |LP> = cosθ |1_ph> - sinθ |B_exc>, |UP> = sinθ |1_ph> + cosθ |B_exc>
# |psi0> = A |LP> + B e^{iφ} |UP>
A_lp = 1.0 / np.sqrt(2.0)   # LP weight
B_up = 1.0 / np.sqrt(2.0)   # UP weight
phi_rel = 0               # relative phase between LP and UP

# time window
t0, t1 = 0.0, 2000.0     # fs
num_pts = 40001
t_eval = np.linspace(t0, t1, num_pts)

# ---------------- derived (rates in 1/fs) ----------------
Delta_c = eV_to_rate(omega_c_eV - omega_d_eV)
Delta_x = eV_to_rate(omega_0_eV - omega_d_eV)
omega_v = eV_to_rate(omega_v_eV)
g       = eV_to_rate(g_eV)
c_v     = eV_to_rate(c_v_eV)

# ---------------- one-molecule vibronic Hilbert space ----------------
d_v = vib_trunc
Iv  = np.eye(d_v, dtype=complex)
# vib operators (if d_v=1, these are zeros)
a = np.zeros((d_v, d_v), dtype=complex)
for n in range(1, d_v):
    a[n-1, n] = np.sqrt(n)
adag = a.conj().T
n_op = adag @ a

# electronic operators
eg = np.array([[0,0],[0,1]], dtype=complex)  # |e><e|
gg = np.array([[1,0],[0,0]], dtype=complex)  # |g><g|
sig_minus = np.array([[0,1],[0,0]], dtype=complex)  # |g><e|
sig_plus  = sig_minus.conj().T

I_e  = np.eye(2, dtype=complex)
dim  = 2 * d_v

def E(op_e): return kron(op_e, Iv)   # electronic ⊗ I_v
def V(op_v): return kron(I_e, op_v)  # I_e ⊗ vibrational

SigmaMinus = E(sig_minus)
SigmaPlus  = E(sig_plus)
Proj_g     = E(gg)
Proj_e     = E(eg)
Nhat       = V(n_op)
B          = V(a)
Bd         = V(adag)

# projectors onto |g,n> and |e,n> vibrational states
P_gn = []
P_en = []
for n in range(d_v):
    n_proj = np.zeros((d_v, d_v), dtype=complex); n_proj[n, n] = 1.0
    P_gn.append(Proj_g @ V(n_proj))
    P_en.append(Proj_e @ V(n_proj))

# Hamiltonian for one molecule in rotating frame at ω_d (ħ=1 in rate units)
# H = Δx |e><e| + ωv b†b + c_v |e><e| (b+b†) + g( α σ^+ + α* σ^- )
def H_mol(alpha):
    H = Delta_x * Proj_e + omega_v * Nhat
    if c_v != 0.0:
        H = H + c_v * Proj_e @ (B + Bd)
    H = H + g * (alpha * SigmaPlus + np.conj(alpha) * SigmaMinus)
    return H

def expect(op, psi):
    return np.vdot(psi, op @ psi)

# ---------------- ODE: y = [alpha, psi] ----------------
def rhs(t, y):
    alpha = y[0]
    psi   = y[1:]

    # molecule Schrödinger equation
    H  = H_mol(alpha)
    dpsi = -1j * (H @ psi)

    # cavity mean-field amplitude
    sigma_minus = expect(SigmaMinus, psi)
    dalpha = -(kappa_rate/2 + 1j*Delta_c)*alpha - 1j * g * N * sigma_minus + eta

    return np.concatenate(([dalpha], dpsi))

# ---------------- initial condition: LP/UP superposition ----------------
ket_e = np.array([0,1], dtype=complex)
ket_g = np.array([1,0], dtype=complex)
ket_v0 = np.zeros((d_v,), dtype=complex); ket_v0[0] = 1.0
psie = kron(ket_e, ket_v0)            # |e,0>
psig = kron(ket_g, ket_v0)            # |g,0>

# mixing angle for LP/UP (use collective coupling g*sqrt(N))
g_coll = g * np.sqrt(N)
detuning = Delta_c - Delta_x
theta = 0.5 * np.arctan2(2.0 * g_coll, detuning)

# coefficients in {|1_ph>, |B_exc>} basis
C_ph = A_lp * np.cos(theta) + B_up * np.exp(1j * phi_rel) * np.sin(theta)
C_ex = -A_lp * np.sin(theta) + B_up * np.exp(1j * phi_rel) * np.cos(theta)

# set mean-field amplitudes: |alpha|^2 + N*|exciton|^2 = 1
photon_num = np.abs(C_ph)**2
exciton_pop_per_mol = np.abs(C_ex)**2 / N

# build molecular wavefunction with the bright-exciton amplitude
psi0 = np.sqrt(1.0 - exciton_pop_per_mol) * psig + C_ex * psie
alpha0 = C_ph
y0 = np.concatenate(([alpha0], psi0))

# ---------------- integrate ----------------
sol = solve_ivp(rhs, (t0, t1), y0, t_eval=t_eval, rtol=1e-8, atol=1e-10, method="RK45")
alpha_t = sol.y[0, :]
psi_t   = sol.y[1:, :].T  # shape (len(t), dim)

# ---------------- observables & save ----------------
excited_pop = np.real([expect(Proj_e, psi) for psi in psi_t])   # ⟨e|ρ|e⟩
photon_num  = np.abs(alpha_t)**2                                # |α|^2
n_avg       = np.real([expect(Nhat, psi) for psi in psi_t])     # ⟨b†b⟩

# vibrational occupation split by electronic surface
n_g_avg = np.real([expect(Proj_g @ Nhat, psi) for psi in psi_t])
n_e_avg = np.real([expect(Proj_e @ Nhat, psi) for psi in psi_t])

# vibrational energies (per molecule, above zero-point), in eV
Evib_per_mol_eV    = (omega_v * n_avg)   * HBAR_eVfs
Evib_g_per_mol_eV  = (omega_v * n_g_avg) * HBAR_eVfs
Evib_e_per_mol_eV  = (omega_v * n_e_avg) * HBAR_eVfs

# total (ensemble) vibrational energies [eV]
Evib_total_eV      = N * Evib_per_mol_eV
Evib_g_total_eV    = N * Evib_g_per_mol_eV
Evib_e_total_eV    = N * Evib_e_per_mol_eV

Xg_eV     = np.real([expect((B + Bd) @ Proj_g, psi) for psi in psi_t])
Vg_eV     = np.real([expect((B + Bd) @ (B + Bd) @ Proj_g, psi) for psi in psi_t])

# vib populations on g and e
vib_pops_g = np.empty((len(psi_t), d_v))
vib_pops_e = np.empty((len(psi_t), d_v))
for ti, psi in enumerate(psi_t):
    for n in range(d_v):
        vib_pops_g[ti, n] = np.real(expect(P_gn[n], psi))
        vib_pops_e[ti, n] = np.real(expect(P_en[n], psi))

# ---------------- save to disk ----------------
np.savetxt("Excited_population.dat", np.column_stack([sol.t, excited_pop]))
np.savetxt("Photon_number.dat",      np.column_stack([sol.t, photon_num]))
np.savetxt("Xg.dat",                 np.column_stack([sol.t, Xg_eV]))
np.savetxt("Vg.dat",                 np.column_stack([sol.t, Vg_eV]))

np.savetxt("Vib_pops_g.dat", np.column_stack([sol.t, vib_pops_g]))
np.savetxt("Vib_pops_e.dat", np.column_stack([sol.t, vib_pops_e]))

# (Optional) keep per-molecule file if you still want it
np.savetxt(
    "Evib_per_molecule.dat",
    np.column_stack([sol.t, Evib_per_mol_eV, Evib_g_per_mol_eV, Evib_e_per_mol_eV])
)
