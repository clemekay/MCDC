import numpy as np
import os, sys, argparse
from task import task

# Option parser
parser = argparse.ArgumentParser(description="MC/DC verification test")
parser.add_argument("--mpiexec", type=int, default=0)
parser.add_argument("--srun", type=int, default=0)
args, unargs = parser.parse_known_args()
mpiexec = args.mpiexec
srun = args.srun


# =============================================================================
# Functions
# =============================================================================


def run(N_hist, name, N_batch=1):
    """
    N_hist: number of histories
    name: name for the job
    N_batch: number of batches
    """
    if N_batch == 1:
        output = "output_%i" % N_hist
    else:
        output = "output_%i_%i" % (N_hist, N_batch)

    if srun > 1:
        os.system(
            "srun -n %i python input.py --mode=numba --N_particle=%i --output=%s"
            % (srun, N_hist, output)
        )
    elif mpiexec > 1:
        os.system(
            "mpiexec -n %i python input.py --mode=numba --N_particle=%i --output=%s"
            % (mpiexec, N_hist, output)
        )
    else:
        os.system(
            "python input.py --mode=numba --N_particle=%i --output=%s --N_batch=%i"
            % (N_hist, output, N_batch)
        )


# =============================================================================
# Select and run tests
# =============================================================================

for name in task.keys():
    os.chdir(name)
    N = task[name]["N"]
    if "N_batch" in task[name]:
        N_hist = int(10**int(task[name]["N_lim"][0]))
        N_min = task[name]["N_batch"][0]
        N_max = task[name]["N_batch"][1]
        for N_batch in np.logspace(N_min, N_max, N):
            N_batch = int(N_batch)
            print("N_batch %i" % N_batch)
            run(N_hist, name, N_batch)
        N_batch = int(10**int(task[name]["N_batch"][0]))
        N_min = task[name]["N_lim"][0]
        N_max = task[name]["N_lim"][1]
        hist_list = np.logspace(N_min, N_max, N)
        for i in range(1, N):
            N_hist = int(hist_list[i])
            print("N_hist %i" % N_hist)
            run(N_hist, name, N_batch)
    else:
        N_min = task[name]["N_lim"][0]
        N_max = task[name]["N_lim"][1]
        for N_hist in np.logspace(N_min, N_max, N):
            N_hist = int(N_hist)
            print(name, N_hist)
            run(N_hist, name)
    os.chdir(r"..")
