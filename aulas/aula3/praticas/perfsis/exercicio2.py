from matplotlib import pyplot
import numpy
from fatiando.seismic import profile
from fatiando.inversion import linear
from fatiando import vis, utils, ui
import cPickle as pickle

params = __import__('exercicio2_entrada')
with open(params.dados) as f:
    zp, tts, thickness, velocity = pickle.load(f)
mu = params.norma_minima
area = (0, 10000, 0, 600)
vmin, vmax, zmin, zmax = area

thick = float(sum(thickness))/float(params.camadas)
model = params.camadas*[thick]
solver = linear.overdet(len(model))
p, residuals = profile.invert_vertical(tts, zp, model, solver, damping=mu)

pyplot.figure(figsize=(12,5))
pyplot.subplot(1, 2, 1)
pyplot.grid()
pyplot.title("Perfilagem sismica vertical")
pyplot.plot(tts, zp, 'ok', label='Observado')
pyplot.plot(tts - residuals, zp, '-r', label='Predito')
leg = pyplot.legend(loc='lower left', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.xlabel("Tempo de chegada (s)")
pyplot.ylabel("Profundidade (m)")
pyplot.ylim(sum(thickness), 0)
pyplot.subplot(1, 2, 2)
pyplot.grid()
pyplot.title("Perfil de velocidades")
vis.map.layers(thickness, velocity, '--b', linewidth=2, label='Verdadeiro')
vis.map.layers(model, 1./p, '-r', linewidth=2, label='Estimado')
leg = pyplot.legend(loc='lower right', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.ylim(zmax, zmin)
pyplot.xlim(vmin, vmax)
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
pyplot.show()
