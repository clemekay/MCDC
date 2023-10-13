import h5py
import numpy as np

f = h5py.File('output.h5','r')
Nb = 1E4
mean = f['tally']['exit']['mean'][:][1]
sdev = f['tally']['exit']['sdev'][:][1]
varp = f['tally']['exit']['uq_var'][:][1]

exact = 5.504/1000

print('Var param: ' + str(varp))
total = (sdev**2)*Nb
print('Var total: ' +  str(total))
print('param error: ' + str(abs(exact-varp)))
print('total error: ' + str(abs(exact-total)))

f.close()
