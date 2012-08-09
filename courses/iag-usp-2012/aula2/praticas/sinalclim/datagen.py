import numpy
from fatiando.heat import climatesignal
from fatiando import vis, utils
import cPickle as pickle

amplitude = 5
idade = 78
ruido = 0.05
zp = numpy.arange(10, 110, 1)
temp, error = utils.contaminate(climatesignal.linear(amplitude,
    idade, zp), ruido, percent=True, return_stddev=True)

with open('exercicio5.pickle', 'w') as f:
    pickle.dump([zp, temp], f)
