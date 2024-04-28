import numpy as np
import os
from task import task


if not os.path.exists("results"):
    os.makedirs("results")

for name in task.keys():
    os.chdir(name)
    N = task[name]["N"]
    if "N_batch" in task[name]:
        N_h = task[name]["N_lim"]
        N_b = task[name]["N_batch"]
        os.system("python process.py %i %i %i %i %i" % (N_h[0], N_h[1], N_b[0], N_b[1], N))
    else:
        N_min = task[name]["N_lim"][0]
        N_max = task[name]["N_lim"][1]
        os.system("python process.py %i %i %i" % (N_min, N_max, N))
    os.chdir(r"..")
