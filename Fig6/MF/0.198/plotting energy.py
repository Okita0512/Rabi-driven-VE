import numpy as np
import matplotlib.pyplot as plt


def load_two_col(path):
    data = np.loadtxt(path)
    return data[:, 0], data[:, 1]


t_total, e_total = load_two_col("Total_energy.dat")
t_exc, e_exc = load_two_col("Exciton_energy.dat")
t_vib, e_vib = load_two_col("Vibrational_energy.dat")
t_ph, e_ph = load_two_col("Photon_energy.dat")

plt.figure(figsize=(8, 5))
plt.plot(t_total, e_total, label="Total energy", linewidth=2.0, color="black")
plt.plot(t_vib, e_vib, label="Vibrational energy")

# plt.plot(t_exc, e_exc, label="Exciton energy")
#plt.plot(t_ph, e_ph, label="Photon energy")

plt.plot(t_vib, e_exc + e_ph, label="electronic + photonic energy")


plt.xlabel("Time (fs)")
plt.ylabel("Energy (eV)")
plt.legend()
plt.tight_layout()
plt.show()
