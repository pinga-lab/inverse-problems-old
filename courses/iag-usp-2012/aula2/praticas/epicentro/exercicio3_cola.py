import sys
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Square
from fatiando.seismic import epicenter, traveltime
from fatiando import vis, utils, inversion, gridder, ui
import cPickle as pickle

with open('exercicio3.pickle') as f:
    recs, src, ttr, error = pickle.load(f)
with open('exercicio3-modelo.pickle') as f:
    estimate = pickle.load(f)

area = (0, 100000, 0, 100000)
shape = (50, 50)
xs, ys = gridder.regular(area, shape)
vp, vs = 2000, 1000
goals = epicenter.mapgoal(xs, ys, ttr, recs, vp, vs)
                               
pyplot.figure(figsize=(7,6))
pyplot.title('Epicentro + estacoes')
pyplot.axis('scaled')
vis.map.contourf(xs, ys, goals, shape, 30)
vis.map.points(recs, '^r', label="Estacaoes")
vis.map.points(src, '*y', label="Verdadeiro")
vis.map.points([estimate], '*g', label="Estimado")
vis.map.set_area(area)
leg = pyplot.legend(loc='lower right', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.xlabel("X")
pyplot.ylabel("Y")
pyplot.show()
