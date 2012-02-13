from matplotlib import pyplot
import numpy
from fatiando.seismic import profile
from fatiando.inversion import linear
from fatiando import vis, utils, ui

params = __import__('exercicio1e2_entrada')

area = (0, 10000, 0, 600)
vmin, vmax, zmin, zmax = area
figure = pyplot.figure()
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
thickness, velocity = ui.picker.draw_layers(area, figure.gca())

zp = numpy.arange(zmin + 1, zmax, 1)
tts, error = utils.contaminate(profile.vertical(thickness, velocity, zp),
    params.ruido, percent=True, return_stddev=True)
    
pyplot.figure(figsize=(6, 5))
pyplot.title("Dados observados")
pyplot.plot(tts, zp, '.k')
pyplot.xlabel("Tempo de chegada (s)")
pyplot.ylabel("Profundidade (m)")
pyplot.ylim(sum(thickness), 0)
pyplot.show()

solver = linear.overdet(len(thickness))
p, residuals = profile.invert_vertical(tts, zp, thickness, solver)

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
vis.map.layers(thickness, 1./p, 'o-r', linewidth=2, label='Estimado')
leg = pyplot.legend(loc='lower right', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.ylim(zmax, zmin)
pyplot.xlim(vmin, vmax)
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
pyplot.show()
