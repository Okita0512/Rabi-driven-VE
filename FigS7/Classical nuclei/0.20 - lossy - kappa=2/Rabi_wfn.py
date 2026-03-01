import numpy as np
import numpy as np
from numpy import kron
from scipy.integrate import solve_ivp

# ---------------- constants ----------------
HBAR_eVfs = 0.658211951  # hbar [eV*fs]
def eV_to_rate(e_eV):    # energy [eV] -> angular frequency [1/fs]
    return e_eV / HBAR_eVfs

# ---------------- user parameters ----------------
N           = 10000      # number of identical, uncorrelated molecules
omega_c_eV  = 2.000      # cavity frequency [eV]
omega_0_eV  = 2.000      # exciton frequency [eV]
omega_v_eV  = 0.200      # vibrational frequency [eV]
g_eV        = 0.10 / np.sqrt(N)      # light-matter coupling [eV]
c_v_eV      = 0.02       # Holstein coupling [eV], set 0 for clean Rabi

# rotating frame frequency (pick equal to cavity/exciton for resonance)
omega_d_eV  = 2.000      # choose =omega_c_eV=omega_0_eV for ?=0 (resonant Rabi)

# no dissipation, no external drive:
kappa_rate     = 0.002     # cavity loss [1/fs]
eta            = 0.0 + 0.0j  # external cavity drive [1/fs]; keep 0

# pulse excitation (seed + drive)
seed_alpha     = 0.0         # tiny seed to trigger Rabi in mean-field

# Pulse (cavity drive)
# pulse_t0_fs     = 10.0      # pulse center [fs]
# pulse_sigma_fs  = 2.0       # pulse width [fs]
pulse_t0_fs       = 250.0      # pulse center [fs]
pulse_sigma_fs    = 50.0       # Gaussian width [fs]
pulse_shape       = "tukey"  # "gaussian" or "tukey"
# pulse_shape       = "gaussian"  # "gaussian" or "tukey"
pulse_duration_fs = 200.0      # Tukey total duration [fs]
pulse_taper_alpha = 0.01        # Tukey taper fraction in [0, 1]
# pulse_omega_eV  = 2.1        # pulse carrier [eV]
pulse_omega_eV  = 2.0 + np.sqrt(N) * g_eV        # always pump the UP
# print("Pulse frequency = UP frequency:", pulse_omega_eV)
pulse_amp_eV    = 1.0e-3     # field amplitude [eV] (Rabi energy scale)

# classical vibration initial conditions (dimensionless)
q0 = 0.0
p0 = 0.0

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
Omega_0 = eV_to_rate(pulse_amp_eV)
Delta_p = eV_to_rate(pulse_omega_eV - omega_d_eV)

# ---------------- electronic Hilbert space (two-level only) ----------------
# electronic operators
sig_minus = np.array([[0,1],[0,0]], dtype=complex)  # |g><e|
sig_plus  = sig_minus.conj().T
proj_g    = np.array([[1,0],[0,0]], dtype=complex)  # |g><g|
proj_e    = np.array([[0,0],[0,1]], dtype=complex)  # |e><e|

SigmaMinus = sig_minus
SigmaPlus  = sig_plus
Proj_g     = proj_g
Proj_e     = proj_e

# Hamiltonian for one molecule in rotating frame at ?_d (?=1 in rate units)
# H = ?x |e><e| + c_v q |e><e| + g( ? ?^+ + ?* ?^- )
def _tukey_envelope(t):
    if pulse_duration_fs <= 0.0:
        return 0.0
    t_start = pulse_t0_fs - 0.5 * pulse_duration_fs
    t_end = pulse_t0_fs + 0.5 * pulse_duration_fs
    if t < t_start or t > t_end:
        return 0.0
    x = (t - t_start) / pulse_duration_fs  # 0..1
    alpha = np.clip(pulse_taper_alpha, 0.0, 1.0)
    if alpha == 0.0:
        return 1.0
    if x < alpha / 2.0:
        return 0.5 * (1.0 + np.cos(np.pi * (2.0 * x / alpha - 1.0)))
    if x > 1.0 - alpha / 2.0:
        return 0.5 * (1.0 + np.cos(np.pi * (2.0 * x / alpha - 2.0 / alpha + 1.0)))
    return 1.0

def _gaussian_envelope(t):
    return np.exp(-0.5 * ((t - pulse_t0_fs) / pulse_sigma_fs)**2)

def pulse_drive(t):
    if Omega_0 == 0.0:
        return 0.0
    if pulse_shape.lower() == "gaussian":
        envelope = _gaussian_envelope(t)
    elif pulse_shape.lower() == "tukey":
        envelope = _tukey_envelope(t)
    else:
        raise ValueError(f"Unknown pulse_shape: {pulse_shape}")
    return Omega_0 * envelope * np.exp(-1j * Delta_p * t)

def H_mol(alpha, q):
    H = Delta_x * Proj_e
    if c_v != 0.0:
        H = H + c_v * q * Proj_e
    H = H + g * (alpha * SigmaPlus + np.conj(alpha) * SigmaMinus)
    return H

def expect(op, psi):
    return np.vdot(psi, op @ psi)

# ---------------- ODE: y = [alpha, psi(2), q, p] ----------------
def rhs(t, y):
    alpha = y[0]
    psi   = y[1:3]
    q     = y[3]
    p     = y[4]

    # molecule Schr?dinger equation
    H  = H_mol(alpha, q)
    dpsi = -1j * (H @ psi)

    # cavity mean-field amplitude
    sigma_minus = expect(SigmaMinus, psi)
    eta_t = eta + pulse_drive(t)
    dalpha = -(kappa_rate/2 + 1j*Delta_c)*alpha - 1j * g * N * sigma_minus + eta_t

    # classical vibration (dimensionless q,p)
    pe = np.real(expect(Proj_e, psi))
    dq = omega_v * p
    dp = -omega_v * q - c_v * pe

    return np.concatenate(([dalpha], dpsi, [dq, dp]))

# ---------------- initial condition: molecule in |g>, cavity tiny seed ----------------
ket_e = np.array([0,1], dtype=complex)
ket_g = np.array([1,0], dtype=complex)

psi0 = ket_g
alpha0 = seed_alpha

y0 = np.concatenate(([alpha0], psi0, [q0, p0]))

# ---------------- integrate ----------------
sol = solve_ivp(rhs, (t0, t1), y0, t_eval=t_eval, rtol=1e-8, atol=1e-10, method="RK45")
alpha_t = sol.y[0, :]
psi_t   = sol.y[1:3, :].T  # shape (len(t), 2)
q_t     = np.real(sol.y[3, :])
p_t     = np.real(sol.y[4, :])

# ---------------- observables & save ----------------
excited_pop = np.real([expect(Proj_e, psi) for psi in psi_t])
photon_num  = np.abs(alpha_t)**2

# classical vibrational energy (per molecule, above zero-point), in eV
Evib_per_mol_eV = (0.5 * omega_v * (q_t**2 + p_t**2)) * HBAR_eVfs
Evib_total_eV   = N * Evib_per_mol_eV

np.savetxt("Excited_population.dat", np.column_stack([sol.t, excited_pop]))
np.savetxt("Photon_number.dat",      np.column_stack([sol.t, photon_num]))
np.savetxt("Q.dat",                 np.column_stack([sol.t, q_t]))
np.savetxt("P.dat",                 np.column_stack([sol.t, p_t]))
np.savetxt("Evib_per_molecule.dat", np.column_stack([sol.t, Evib_per_mol_eV]))
