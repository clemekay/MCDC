import h5py
import numpy as np
import math

f = h5py.File('output.h5','r')
Nb = f['input_deck']['setting']['N_batch'][()]
Np = f['input_deck']['setting']['N_particle'][()]
seed = f['input_deck']['setting']['rng_seed'][()]
mean = f['tally']['exit']['mean'][:][1]
sdev = f['tally']['exit']['sdev'][:][1]
varp = f['tally']['exit']['uq_var'][:][1]

exact = 5.504/1000

print('(N_particle,N_batch) = (' + str(Np) + ',' + str(Nb) + ') = 2e' + str(int(math.log10(Nb*Np))))
print('Analytic UQ variance: ' + str(exact))
print('With variance deconv: ' + str(varp))
total = (sdev**2)*Nb
print('Brute-force approach: ' +  str(total))
print('\n')
print('Error of var-d: ' + str(abs(exact-varp)))
print('Error of brute: ' + str(abs(exact-total)))
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
