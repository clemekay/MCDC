import numpy as np
import h5py

import mcdc


# =========================================================================
# Set model and run
# =========================================================================

lib = h5py.File("c5g7.h5", "r")

def set_mat(mat):
    return mcdc.material(
        capture=mat["capture"][:],
        scatter=mat["scatter"][:],
        fission=mat["fission"][:],
        nu_p=mat["nu_p"][:],
        nu_d=mat["nu_d"][:],
        chi_p=mat["chi_p"][:],
        chi_d=mat["chi_d"][:],
        speed=mat["speed"],
        decay=mat["decay"],
    )


def uq_mat(mat, param, c):
    return c*mat[param][:]


mat_uo2 = set_mat(lib["uo2"])  # Fuel: UO2
mat_mod = set_mat(lib["mod"])  # Moderator
mat_cr = set_mat(lib["cr"])  # Control rod

s1 = mcdc.surface("plane-x", x=0.0, bc="reflective")
s2 = mcdc.surface("plane-x", x=0.5)
s3 = mcdc.surface("plane-x", x=1.5)
s4 = mcdc.surface("plane-x", x=2.0, bc="reflective")

mcdc.cell([+s1, -s2], mat_uo2)
mcdc.cell([+s2, -s3], mat_mod)
mcdc.cell([+s3, -s4], mat_cr)

mcdc.source(point=[1.0, 0.0, 0.0], energy=[1, 0, 0, 0, 0, 0, 0], isotropic=True)

scores = ["flux"]
grid = 200
mcdc.tally(scores=scores, x=np.linspace(0.0, 2.0, grid+1), g=[-.5, 3.5, 6.5])

mcdc.setting(N_particle=1E2, N_batch=1E2)

mcdc.uq(material=mat_mod, distribution='uniform',
         capture=uq_mat(lib["mod"], 'capture', 0.8),
         scatter=uq_mat(lib["mod"], 'scatter', 0.8),
         )

mcdc.uq(material=mat_cr, distribution='uniform',
        capture=uq_mat(lib["cr"], 'capture', 0.8),
        scatter=uq_mat(lib["cr"], 'scatter', 0.8),
        )

mcdc.run()



