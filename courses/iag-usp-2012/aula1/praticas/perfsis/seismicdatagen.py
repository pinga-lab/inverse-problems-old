from matplotlib import pyplot
import numpy
from fatiando.seismic import profile
from fatiando import vis, utils, ui
import cPickle as pickle

area = (0, 10000, 0, 600)
vmin, vmax, zmin, zmax = area
figure = pyplot.figure()
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
thickness, velocity = ui.picker.draw_layers(area, figure.gca())

zp = numpy.arange(zmin + 5, zmax, 5)
tts, error = utils.contaminate(profile.vertical(thickness, velocity, zp), 0.02,
                               percent=True, return_stddev=True)

with open('exercicio5.pickle', 'w') as f:
    data = {'thickness':thickness, 'velocity':velocity,
            'tts':tts, 'zp':zp}
    pickle.dump(data, f)

    
pyplot.figure(figsize=(12,5))
pyplot.subplot(1, 2, 1)
pyplot.grid()
pyplot.title("Perfilagem sismica vertical")
pyplot.plot(tts, zp, '.k')
pyplot.xlabel("Tempo de chegada (s)")
pyplot.ylabel("Profundidade (m)")
pyplot.ylim(sum(thickness), 0)
pyplot.subplot(1, 2, 2)
pyplot.grid()
pyplot.title("Perfil de velocidades")
vis.map.layers(thickness, velocity, '--b', linewidth=2)
pyplot.ylim(zmax, zmin)
pyplot.xlim(vmin, vmax)
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
pyplot.show()
