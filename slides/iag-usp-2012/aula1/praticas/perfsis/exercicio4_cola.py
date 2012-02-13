from matplotlib import pyplot
import numpy
from fatiando.seismic import profile
from fatiando import vis, utils, ui
import cPickle as pickle

area = (0, 10000, 0, 600)
vmin, vmax, zmin, zmax = area

with open('exercicio4.pickle') as f:
    data = pickle.load(f)
    thickness = data['thickness']
    velocity = data['velocity']

with open('exercicio4-modelo.pickle') as f:
    data = pickle.load(f)
    thickness_model = data['thickness']
    velocity_model = data['velocity']

pyplot.figure(figsize=(6,5))
pyplot.grid()
pyplot.title("Perfil de velocidades")
vis.map.layers(thickness, velocity, '--b', linewidth=2, label="Verdadeiro")
vis.map.layers(thickness_model, velocity_model, 'o-r', linewidth=2, label="Seu")
pyplot.ylim(zmax, zmin)
pyplot.xlim(vmin, vmax)
pyplot.xlabel("Velocidade (m/s)")
pyplot.ylabel("Profundidade (m)")
pyplot.show()
