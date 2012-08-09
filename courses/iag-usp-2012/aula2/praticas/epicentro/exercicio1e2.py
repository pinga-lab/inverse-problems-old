import sys
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Square
from fatiando.seismic import epicenter, traveltime
from fatiando import vis, utils, inversion, gridder, ui
import cPickle as pickle

params = __import__('exercicio1e2_entrada')

area = (0, 100000, 0, 100000)
vp, vs = params.vp, params.vs
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

pyplot.figure()
ax = pyplot.subplot(1, 1, 1)
pyplot.axis('scaled')
pyplot.suptitle("Escolha a estimativa inicial")
vis.map.points(rec_points, '^r')
vis.map.points(src, '*y')
inicial = ui.picker.points(area, ax, marker='*', color='k')[0]

srcs, recs = utils.connect_points(src, rec_points)
ptime = traveltime.straight_ray_2d(model, 'vp', srcs, recs)
stime = traveltime.straight_ray_2d(model, 'vs', srcs, recs)
error_level = params.ruido
ttr_true = stime - ptime
ttr, error = utils.contaminate(ttr_true, error_level, percent=True,
                               return_stddev=True)
solver = inversion.gradient.newton(initial=inicial)
result = epicenter.flat_earth(ttr, recs, vp, vs, solver)
estimate, residuals = result
predicted = ttr - residuals
                               
pyplot.figure(figsize=(14,6))
pyplot.subplot(1, 2, 1)
pyplot.title('Epicentro + estacoes')
pyplot.axis('scaled')
vis.map.points(recs, '^r', label="Estacaoes")
vis.map.points(src, '*y', label="Verdadeiro")
vis.map.points([inicial], '*k', label="Inicial")
vis.map.points([estimate], '*g', label="Estimado")
vis.map.set_area(area)
leg = pyplot.legend(loc='lower right', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.xlabel("X")
pyplot.ylabel("Y")
ax = pyplot.subplot(1, 2, 2)
pyplot.title('Tempo de percurso')
s = numpy.arange(len(ttr)) + 1
width = 0.3
pyplot.bar(s - width, ttr, width, color='g', label="Observado",
           yerr=error)
pyplot.bar(s, predicted, width, color='r', label="Predito")
ax.set_xticks(s)
leg = pyplot.legend(loc='lower right')
leg.get_frame().set_alpha(0.5)
pyplot.xlabel("Estacao")
pyplot.ylabel("Tempo de percurso")
pyplot.show()
