import matplotlib
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()

# ================= global ====================

conv = 27.211397                            # 1 a.u. = 27.211397 eV
fs_to_au = 41.341374575751                  # 1 fs = 41.341 a.u.
cm_to_au = 4.556335e-06                     # 1 cm^-1 = 4.556335e-06 a.u.
au_to_K = 3.1577464e+05                     # 1 au = 3.1577464e+05 K
kcal_to_au = 1.5936e-03                     # 1 kcal/mol = 1.5936e-3 a.u.

# ==============================================================================================
#                                         data reading     
# ==============================================================================================

lamF = 0.04
sigma = 10
wc = 1.0
a = 0

def chirp(x):
    return (lamF / 2) * np.exp(- x**2 / (2 * sigma**2)) * np.cos(wc * x + a * x**2)

time = np.linspace(-50, 50, 10000)
ax.plot(time, chirp(time), 'k-', linewidth = 3.0)
ax.axis('off')

plt.savefig("chirp.pdf", bbox_inches='tight', pad_inches=0)

