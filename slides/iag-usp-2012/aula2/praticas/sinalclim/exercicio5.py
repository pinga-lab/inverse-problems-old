from matplotlib import pyplot
import numpy
import cPickle as pickle
from fatiando.heat import climatesignal
from fatiando.inversion.gradient import levmarq
from fatiando import vis, utils

params = __import__('exercicio5_entrada')
with open('exercicio5.pickle') as f:
    zp, temp = pickle.load(f)
solver = levmarq(initial=params.inicial)
p, resabr = climatesignal.invert_abrupt(temp, zp, solver)
ampabr, ageabr = p
solver = levmarq(initial=params.inicial)
p, reslin = climatesignal.invert_linear(temp, zp, solver)
amplin, agelin = p

pyplot.figure(figsize=(12,5))
pyplot.subplot(1, 2, 1)
pyplot.title("Sinal climatico")
pyplot.plot(temp, zp, 'ok', label='Observado')
pyplot.plot(temp - reslin, zp, '-b', linewidth=3, label='Linear')
pyplot.plot(temp - resabr, zp, '-r', linewidth=3, label='Abrupto')
pyplot.legend(loc='lower right', numpoints=1)
pyplot.xlabel("Temperatura (C)")
pyplot.ylabel("Z")
pyplot.ylim(110, 10)
ax = pyplot.subplot(1, 2, 2)
ax2 = pyplot.twinx()
pyplot.title("Idade e amplitude")
width = 0.3
ax.bar([1 - width], [agelin], width, color='b', label="Linear")
ax.bar([1], [ageabr], width, color='r', label="Abrupto")
ax2.bar([2 - width], [amplin], width, color='b')
ax2.bar([2], [ampabr], width, color='r')
ax.legend(loc='lower left', numpoints=1)
ax.set_ylabel("Idade (anos)")
ax2.set_ylabel("Amplitude (C)")
ax.set_xticks([1, 2])
ax.set_xticklabels(['Idade', 'Amplitude'])
pyplot.show()
