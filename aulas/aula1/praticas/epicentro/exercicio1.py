import sys
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Square
from fatiando.seismic import epicenter, traveltime
from fatiando import vis, utils, inversion, gridder, ui

import cPickle as pickle

area = (0, 100000, 0, 100000)
vp, vs = 2000, 1000
model = [Square(area, props={'vp':vp, 'vs':vs})]

pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Escolha as estacoes")
rec_points = ui.picker.points(area, ax, marker='^', color='r')

pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Escolha o evento")
vis.map.points(rec_points, '^r')
src = ui.picker.points(area, ax, marker='*', color='y')
    
srcs, recs = utils.connect_points(src, rec_points)
ptime = traveltime.straight_ray_2d(model, 'vp', srcs, recs)
stime = traveltime.straight_ray_2d(model, 'vs', srcs, recs)
error_level = 0.0
ttr_true = stime - ptime
ttr, error = utils.contaminate(ttr_true, error_level, percent=True,
                               return_stddev=True)
                               
pyplot.figure(figsize=(14,6))
pyplot.subplot(1, 2, 1)
pyplot.title('Epicentro + estacoes')
pyplot.axis('scaled')
vis.map.points(recs, '^r', label="Stations")
vis.map.points(src, '*y', label="True")
vis.map.set_area(area)
pyplot.xlabel("X")
pyplot.ylabel("Y")
ax = pyplot.subplot(1, 2, 2)
pyplot.title('Tempo de percurso')
s = numpy.arange(len(ttr)) + 1
width = 0.2
pyplot.bar(s - 0.5*width, ttr, width, color='y', label="Observed")
ax.set_xticks(s)
pyplot.xlabel("Estacao")
pyplot.ylabel("Tempo de percurso")
pyplot.show()
