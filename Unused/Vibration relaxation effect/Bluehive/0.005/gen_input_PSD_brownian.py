import sys
sys.path.append('../scripts')

import json
import numpy as np
import armadillo as arma
from bath_gen_Drude_PSD import generate

# ================= global ====================

conv = 27.211397                            # 1 a.u. = 27.211397 eV
fs_to_au = 41.341                           # 1 fs = 41.341 a.u.
cm_to_au = 4.556335e-06                     # 1 cm^-1 = 4.556335e-06 a.u.
au_to_K = 3.1577464e+05                     # 1 au = 3.1577464e+05 K
kcal_to_au = 1.5936e-03                     # 1 kcal/mol = 1.5936e-3 a.u.

def delta(m, n):
    return 1 if m == n else 0

def get_Hs(NStates, nmol, omega_c, omega_s, gc):

    RE = 0.0 / conv
    hams = np.zeros((NStates, NStates), dtype = complex)
    
    for i in range(nmol):
        hams[i,i] = omega_s + RE
        hams[i,NStates-1] = hams[NStates-1,i] = gc
    hams[NStates-1,NStates-1] = omega_c

    return hams

# remember to turn off the RE when bath is turned off

def get_Qs1(NStates, index):    # coupling to the system. s^+ s^-

    Qs1 = np.zeros((NStates, NStates), dtype=complex)
    
    Qs1[index,index] = 1

    return Qs1

def get_rho0(NStates, nfock, Hmat0):
    
    # for LP initial condition
    for i in range(NStates-1):
        Hmat0[i,i] = Hmat0[i,i] 
    eVal, eVec = np.linalg.eigh(Hmat0)
    print(eVal)
    np.savetxt("unitary.txt", eVec)
    
    # initialize from |+>
    rho0 = np.outer(eVec[:,NStates-1].conj(), eVec[:,NStates-1])
    # initialize from |->
#    rho0 = np.outer(eVec[:,0].conj(), eVec[:,0])

    return rho0

# ==============================================================================================================================

if __name__ == '__main__':

    with open('default.json') as f:
        ini = json.load(f)

    temp    = 300 / au_to_K                   # temperature
    
    nmol = 1 
    NStates = nmol + 1
    nfock = 1

    nmod    = nmol
    Om = 0.2 / conv 
    lam = (0.01 / conv)**2 / Om
    gam = 0.005 / conv

    # PSD scheme
    pade    = 1                            # 1 for [N-1/N], 2 for [N/N], 3 for [N+1/N]
    npsd    = 3                            # number of Pade terms

# ==============================================================================================================================

	# bath
    ini['bath']['temp'] = temp
    ini['bath']['nmod'] = nmod
    # ini['bath']['jomg'] = [{"jsdr":[(0.25,5.0,0.1)]} for i in xrange(nmod)] # Brownian oscillator
    # ini['bath']['jomg'] = [{"jdru":[(lambda_[i], gamma[i])]} for i in range(nmod)] # ,{"jdru":[(1.2,1.0)]}  # low temperature correction (Drude bath without bias)
    ini['bath']['jomg'] = [{"jsdr":[(lam, Om, gam)]} for i in range(nmod)]  # Brownian oscillator
    ini['bath']['pade'] = pade
    ini['bath']['npsd'] = npsd
    jomg = ini['bath']['jomg']
    
    nind = 0
    for m in range(nmod):       # one mode is treated by PFD
        try:
            ndru = len(jomg[m]['jdru'])
        except:
            ndru = 0
        try:
            nsdr = len(jomg[m]['jsdr'])
        except:
            nsdr = 0
        nper = ndru + 2 * nsdr + npsd
        nind += nper

    etal, etar, etaa, expn, delr = generate (temp, npsd, pade, jomg)

    mode = np.zeros((nind), dtype = int)
    for i in range(nmod):
        for j in range(npsd + 2):
            mode[(npsd + 2) * i + j] = i

    arma.arma_write(mode, 'inp_mode.mat')
    arma.arma_write(delr, 'inp_delr.mat')
    arma.arma_write(etal, 'inp_etal.mat')
    arma.arma_write(etar, 'inp_etar.mat')
    arma.arma_write(etaa, 'inp_etaa.mat')
    arma.arma_write(expn, 'inp_expn.mat')

# ==============================================================================================================================

    # system Hamiltonian and dissipation operators
    
    omega_c = 2.0 / conv # - 0.617 / conv
    omega_s = 2.0 / conv
    gc = (0.1 / conv) / np.sqrt(nmol)

    hams = get_Hs(NStates, nmol, omega_c, omega_s, gc)

    qmds = np.zeros((nmod, NStates * nfock, NStates * nfock), dtype=complex)
    for i in range(nmol):
        qmds[i,:,:] = get_Qs1(NStates, i)

    arma.arma_write (hams,ini['syst']['hamsFile'])
    arma.arma_write (qmds,ini['syst']['qmdsFile'])
    
# ==============================================================================================================================

    rho0 = get_rho0(NStates, nfock, hams)
    arma.arma_write (rho0,'inp_rho0.mat')

    # hidx
    ini['hidx']['trun'] = 0
    ini['hidx']['lmax'] = 100
    ini['hidx']['nmax'] = 1000000
    ini['hidx']['ferr'] = 1.0e-07

    dt = 0.005 * fs_to_au
    t = 1000 * fs_to_au
    nt = int(t / dt)

    # proprho
    jsonInit = {"deom":ini,
                "rhot":{
                    "dt": dt,
                    "nt": nt,
                    "nk": 100,
					"xpflag": 1,
					"staticErr": 0,
                    "rho0File": "inp_rho0.mat",
                    "sdipFile": "inp_sdip.mat",
                    "pdipFile": "inp_pdip.mat",
					"bdipFile": "inp_bdip.mat"
                },
            }

# ==============================================================================================================================

    # dipoles
    sdip = np.zeros((2,2),dtype=float)
    arma.arma_write(sdip,'inp_sdip.mat')

    pdip = np.zeros((nmod,2,2),dtype=float)
    pdip[0,0,1] = pdip[0,1,0] = 1.0
    arma.arma_write(pdip,'inp_pdip.mat')

    bdip = np.zeros(3,dtype=complex)
#    bdip[0]=-complex(5.00000000e-01,8.66025404e-01)
#    bdip[1]=-complex(5.00000000e-01,-8.66025404e-01)
#    bdip[2]=-complex(7.74596669e+00,0.00000000e+00)
    arma.arma_write(bdip,'inp_bdip.mat')

    with open('input.json','w') as f:
        json.dump(jsonInit,f,indent=4) 
