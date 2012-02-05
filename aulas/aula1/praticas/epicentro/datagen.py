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
pyplot.suptitle("Choose the location of the receivers")
rec_points = ui.picker.points(area, ax, marker='^', color='r')

pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Choose the location of the source")
vis.map.points(rec_points, '^r')
src = ui.picker.points(area, ax, marker='*', color='y')
    
srcs, recs = utils.connect_points(src, rec_points)
ptime = traveltime.straight_ray_2d(model, 'vp', srcs, recs)
stime = traveltime.straight_ray_2d(model, 'vs', srcs, recs)
error_level = 0.05
ttr_true = stime - ptime
ttr, error = utils.contaminate(ttr_true, error_level, percent=True,
                               return_stddev=True)

with open('exercicio3.pickle', 'w') as f:
    data = {'ttr':ttr, 'recs':recs, 'src':src, 'error':error}
    pickle.dump(data, f)
                               
pyplot.figure(figsize=(14,4))
pyplot.subplot(1, 3, 1)
pyplot.title('Epicenter + %d recording stations' % (len(rec_points)))
pyplot.axis('scaled')
vis.map.points(recs, '^r', label="Stations")
vis.map.points(src, '*y', label="True")
vis.map.set_area(area)
pyplot.legend(loc='upper left', shadow=True, numpoints=1, prop={'size':10})
pyplot.xlabel("X")
pyplot.ylabel("Y")
ax = pyplot.subplot(1, 3, 2)
pyplot.title('Travel-time residuals + %g%s error' % (100.*error_level, '%'))
s = numpy.arange(len(ttr)) + 1
width = 0.2
pyplot.bar(s - 2*width, ttr, width, color='y', label="Observed")
ax.set_xticks(s)
pyplot.legend(loc='lower right', shadow=True, prop={'size':10})
pyplot.xlabel("Station number")
pyplot.ylabel("Travel-time residual")
pyplot.show()
