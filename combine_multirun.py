import h5py
import numpy as np
import math

N_runs = 0
mean = 0
tally_sq = 0
means_sq = 0
Nb = 0

#for file in ('multi1.h5', 'output.h5'):
for i in range(10):
    file = 'multi' + str(i) + '.h5'
    N_runs += 1
    with h5py.File(file,'r') as f:
        if N_runs == 1:
            Np = f['input_deck/setting/N_particle'][()]
            seed = f['input_deck/setting/rng_seed'][()]
        else:
            assert f['input_deck/setting/N_particle'][()] == Np, "Number of particles not constant."
            assert f['input_deck/setting/rng_seed'][()] != seed, "Same seed used."
        Nb += f['input_deck/setting/N_batch'][()]
        mean += f['tally/exit/mean'][:][1]
        tally_sq += f['tally/exit/tally_sq'][:][1]
        means_sq += f['tally/exit/mean_sq'][:][1]

mean /= N_runs
sdev = np.sqrt( (means_sq/Nb - np.square(mean)) / (Nb-1) )
mc_var = (tally_sq/Np - means_sq) / (Np-1) / Nb
tot_var = (means_sq - Nb*np.square(mean)) / (Nb-1)
varp = tot_var - mc_var

exact = 5.504/1000

print('(N_particle,N_batch) = ({:.0e},{:.0e}) = {:.0e}'.format(Np, Nb, Nb*Np))
print('Analytic UQ variance: {:5f}'.format(exact))
print('With variance deconv: {:5f}'.format(varp))
total = (sdev**2)*Nb
print('Brute-force approach: {:5f}'.format(tot_var))
print('\n')
print('Error of var-d: ' + str(abs(exact-varp)))
print('Error of brute: ' + str(abs(exact-tot_var)))
print('\n')
print('Analytic transmittance: ' + str(0.08378))
print('MC/DC transmittance: ' + str(mean) + ' +/- ' + str(sdev))
if mean+sdev > 0.08378 > mean-sdev:
    print('This is within 1 std dev')
else:
    error = np.abs(mean-0.08378)
    print('This is within ' + str(2) + ' standard deviations.')
print('seed: ' + str(seed))
f.close()
