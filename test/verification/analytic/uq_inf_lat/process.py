import numpy as np
import h5py
import sys
import ast

sys.path.append("../")
import tool

# Reference solution
with h5py.File("reference.h5","r") as f:
    x = f["tally/grid/x"][:]
    dx = (x[1:] - x[:-1])[0]
    xmid = 0.5 * (x[:-1] + x[1:])
    var_ref = f["tally/flux/varp"][:]

for i in range(1,6):
    sys.argv[i] = int(sys.argv[i])

hist_lim = [sys.argv[1], sys.argv[2]]
batch_lim = [sys.argv[3], sys.argv[4]]
N = int(sys.argv[5])

# Batch cases run
N_hist = 10**int(hist_lim[0])
N_batch_list = np.logspace(batch_lim[0], batch_lim[1], N)
error = np.zeros(N)
error_max = np.zeros(N)
for i, N_batch in enumerate(N_batch_list):
    # Get results
    with h5py.File("output_%i_%i.h5" % (int(N_hist), int(N_batch)),"r") as f:
        varp = f["tally/flux/uq_var"][:]
    error[i] = tool.error(varp, var_ref)
    error_max[i] = tool.error_max(varp, var_ref)
tool.plot_convergence("uq_inf_lat_batches", N_batch_list, error, error_max)

# History cases run
N_batch = 10**int(batch_lim[0])
N_hist_list = np.logspace(hist_lim[0], hist_lim[1], N)
for i, N_hist in enumerate(N_hist_list):
    # Get results
    with h5py.File("output_%i_%i.h5" % (int(N_hist), int(N_batch)),"r") as f:
        varp = f["tally/flux/uq_var"][:]
    error[i] = tool.error(varp, var_ref)
    error_max[i] = tool.error_max(varp, var_ref)
tool.plot_convergence("uq_inf_lat_hist", N_hist_list, error, error_max)
