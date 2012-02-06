from matplotlib import pyplot
import numpy
from fatiando.heat import climatesignal
from fatiando.inversion.gradient import levmarq
from fatiando import vis, utils

params = __import__('exercicio1e2_entrada')
zp = numpy.arange(0, 100, 1)
temp, error = utils.contaminate(climatesignal.abrupt(params.amplitude,
    params.idade, zp), params.ruido, percent=True, return_stddev=True)
solver = levmarq(initial=params.inicial)
p, residuals = climatesignal.invert_abrupt(temp, zp, solver)
est_amp, est_age = p

pyplot.figure(figsize=(12,5))
pyplot.subplot(1, 2, 1)
pyplot.title("Sinal climatico")
pyplot.plot(temp, zp, 'ok', label='Observado')
pyplot.plot(temp - residuals, zp, '--r', linewidth=3, label='Predito')
pyplot.legend(loc='lower right', numpoints=1)
pyplot.xlabel("Temperatura (C)")
pyplot.ylabel("Z")
pyplot.ylim(100, 0)
ax = pyplot.subplot(1, 2, 2)
ax2 = pyplot.twinx()
pyplot.title("Idade e amplitude")
width = 0.3
ax.bar([1 - width], [params.idade], width, color='b', label="Verdadeiro")
ax.bar([1], [est_age], width, color='r', label="Estimado")
ax2.bar([2 - width], [params.amplitude], width, color='b')
ax2.bar([2], [est_amp], width, color='r')
ax.legend(loc='upper center', numpoints=1)
ax.set_ylabel("Idade (anos)")
ax2.set_ylabel("Amplitude (C)")
ax.set_xticks([1, 2])
ax.set_xticklabels(['Idade', 'Amplitude'])
ax.set_ylim(0, 150)
ax2.set_ylim(0, 4)
pyplot.show()
