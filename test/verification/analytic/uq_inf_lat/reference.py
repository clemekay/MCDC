import numpy as np
import h5py

import h5py
import numpy as np
import matplotlib.pyplot as plt

n_runs = 100
p = np.array([[2, 0], [5, 0], [1, 1], [5, 1], [1, 2], [1, 3], [2, 3]])
b = np.array([[5, 3], [2, 3], [1, 3], [2, 2], [1, 2], [1, 1], [5, 0]])

assert len(p) == len(b), "Number of runs not equal."
with h5py.File('p16b11/combined_results.h5','r') as g:
        x = g['tally/grid/x'][:]
        dx = (x[1:] - x[:-1])[0]
        xmid = 0.5 * (x[:-1] + x[1:])
        phi_ref = g['tally/flux/mean'][:]
        var_ref = g['tally/flux/varp'][:] / (dx**2)

n_eta = np.zeros(len(p))
n_xi = n_eta.copy()
run_tot = n_eta.copy()
run_prep = n_eta.copy()
run_out = n_eta.copy()
varp_norm = n_eta.copy()
vart_norm = varp_norm.copy()
for i in range(len(p)):
    n_eta[i] = p[i][0] * (10**p[i][1])
    n_xi[i] = n_runs * b[i][0] * (10**b[i][1])
    outdir = 'p' + str(p[i][0]) + str(p[i][1]) + 'b' + str(b[i][0]) + str(b[i][1])
    with h5py.File(outdir+'/combined_results.h5','r') as f:
        phi = f['tally/flux/mean'][:]
        varp = f['tally/flux/varp'][:] / (dx**2)
        vart = f['tally/flux/vart'][:] / (dx**2)
        run_tot[i] = f['runtime/total'][:]
        run_prep[i] = f['runtime/preparation'][:]
        run_out[i] = f['runtime/output'][:]

        varp_err = (varp - var_ref)/var_ref
        varp_norm[i] = np.sqrt(np.sum(np.square(varp_err)))
        vart_err = (vart - var_ref)/var_ref
        vart_norm[i] = np.sqrt(np.sum(np.square(vart_err)))

cost_tot = n_eta * n_xi
run_time = run_tot - (run_prep+run_out)/100*99
varp_fom = 1/(varp_norm**2)/run_time
vart_fom = 1/(vart_norm**2)/run_time
