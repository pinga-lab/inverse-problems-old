from matplotlib import pyplot
import numpy
from fatiando.seismic import profile
from fatiando.inversion import linear
from fatiando import vis, utils, ui
import cPickle as pickle

params = __import__('datagen_entrada')

area = (0, 10000, 0, 600)
vmin, vmax, zmin, zmax = area
figure = pyplot.figure()
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
thickness, velocity = ui.picker.draw_layers(area, figure.gca())

zp = numpy.arange(zmin + 5, zmax, 5)
tts, error = utils.contaminate(profile.vertical(thickness, velocity, zp),
    params.ruido, percent=True, return_stddev=True)

with open('exercicio3.pickle', 'w') as f:
    pickle.dump([zp, tts, thickness, velocity], f)
    
pyplot.figure(figsize=(6, 5))
pyplot.title("Dados observados")
pyplot.plot(tts, zp, '.k')
pyplot.xlabel("Tempo de chegada (s)")
pyplot.ylabel("Profundidade (m)")
pyplot.ylim(sum(thickness), 0)
pyplot.show()

