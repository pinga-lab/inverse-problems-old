import sys
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Square
from fatiando.seismic import epicenter, traveltime
from fatiando import vis, logger, utils, inversion, gridder, ui
import cPickle as pickle

area = (0, 10, 0, 10)
vp, vs = 2, 1
model = [Square(area, props={'vp':vp, 'vs':vs})]

pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Escolha os receptores")
rec_points = ui.picker.points(area, ax, marker='^', color='r')

pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Escolha a fonte")
vis.map.points(rec_points, '^r')
src = ui.picker.points(area, ax, marker='*', color='y')
if len(src) > 1:
    log.error("Don't be greedy! Pick only one point as the source")
    sys.exit()
    
srcs, recs = utils.connect_points(src, rec_points)
ptime = traveltime.straight_ray_2d(model, 'vp', srcs, recs)
stime = traveltime.straight_ray_2d(model, 'vs', srcs, recs)
error_level = 0.1
ttr_true = stime - ptime
ttr, error = utils.contaminate(ttr_true, error_level, percent=True,
                               return_stddev=True)
with open("dados.pickle", 'w') as f:
    data = [src, rec_points, ttr, error, ttr_true]
    pickle.dump(data, f)
                               
shape = (50, 50)
xs, ys = gridder.regular(area, shape)
goals = epicenter.mapgoal(xs, ys, ttr, recs, vp, vs)
    
pyplot.figure()
pyplot.axis('scaled')
pyplot.suptitle("Funcao objetivo")
vis.map.contourf(xs, ys, goals, shape, 50)
vis.map.points(rec_points, '^r')
vis.map.points(src, '*y')
pyplot.show()
