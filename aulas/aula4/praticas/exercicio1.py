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

with open('dados.pickle') as f:
    src, rec_points, ttr, error, ttr_true = pickle.load(f)
    
srcs, recs = utils.connect_points(src, rec_points)
                               
shape = (50, 50)
xs, ys = gridder.regular(area, shape)
goals = epicenter.mapgoal(xs, ys, ttr, recs, vp, vs)
    
pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Escolha a estimativa inicial")
vis.map.contourf(xs, ys, goals, shape, 50)
vis.map.points(rec_points, '^r')
vis.map.points(src, '*y')
initial = ui.picker.points(area, ax, marker='*', color='k')
if len(initial) > 1:
    log.error("Don't be greedy! Pick only one initial estimate")
    sys.exit()
initial = initial[0]
    
nsolver = inversion.gradient.newton(initial)
newton = [initial]
iterator = epicenter.flat_earth(ttr, recs, vp, vs, nsolver, iterate=True)
for e, r in iterator:
    newton.append(e)
newton_predicted = ttr - r

sdsolver = inversion.gradient.steepest(initial)
steepest = [initial]
iterator = epicenter.flat_earth(ttr, recs, vp, vs, sdsolver, iterate=True)
for e, r in iterator:
    steepest.append(e)
steepest_predicted = ttr - r

pyplot.figure()
pyplot.axis('scaled')
vis.map.contourf(xs, ys, goals, shape, 50)
vis.map.points(recs, '^r')
vis.map.points(newton, '.-r', size=5, label="Gauss-Newton")
vis.map.points([newton[-1]], '*r')
vis.map.points(steepest, '.-m', size=5, label="Steepest")
vis.map.points([steepest[-1]], '*m')
vis.map.points(src, '*y')
vis.map.set_area(area)
leg = pyplot.legend(loc='upper left', shadow=True, numpoints=1, prop={'size':10})
leg.get_frame().set_alpha(0.5)
pyplot.xlabel("X")
pyplot.ylabel("Y")
pyplot.figure(figsize=(8,4))
ax = pyplot.subplot(1, 2, 1)
pyplot.title('Tempos de chegada')
s = numpy.arange(len(ttr)) + 1
width = 0.2
pyplot.bar(s - 2*width, ttr, width, color='y', label="Observado", yerr=error)
pyplot.bar(s - width, newton_predicted, width, color='r', label="Gauss-Newton")
pyplot.bar(s, steepest_predicted, width, color='m', label="Steepest")
pyplot.plot(s - 1.5*width, ttr_true, '^-y', linewidth=2, label="Sem ruido")
ax.set_xticks(s)
leg = pyplot.legend(loc='lower right', shadow=True, prop={'size':10})
leg.get_frame().set_alpha(0.5)
pyplot.ylim(0, 4.5)
pyplot.xlabel("Estacao")
pyplot.ylabel("Tempo de chegada")
ax = pyplot.subplot(1, 2, 2)
pyplot.title('Numero de iteracoes')
width = 0.5
pyplot.bar(1, len(newton), width, color='r', label="Gauss-Newton")
pyplot.bar(2, len(steepest), width, color='m', label="Steepest")
ax.set_xticks([])
pyplot.grid()
leg = pyplot.legend(loc='lower right', shadow=True, prop={'size':10})
leg.get_frame().set_alpha(0.5)
pyplot.show()
