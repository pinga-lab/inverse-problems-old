from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Square
from fatiando.seismic import epicenter, traveltime
from fatiando import vis, gridder, ui, utils
import cPickle as pickle

with open('exercicio2.pickle') as f:
    data = pickle.load(f)
    ttr = data['ttr']
    recs = data['recs']
    src = data['src']
    
area = (0, 100000, 0, 100000)
vp, vs = 2000, 1000
model = [Square(area, props={'vp':vp, 'vs':vs})]

pyplot.figure(figsize=(14, 6))
pyplot.suptitle("Escolha o epicentro")
ax = pyplot.subplot(1, 2, 1)
pyplot.axis('scaled')
vis.map.points(recs, '^r', label="Stations")
ax2 = pyplot.subplot(1, 2, 2)
pyplot.title('Tempos de chegada')
s = numpy.arange(len(ttr)) + 1
width = 0.2
pyplot.bar(s - width, ttr, width, color='r')
ax2.set_xticks(s)
pyplot.xlabel("Estacao")
pyplot.ylabel("Tempo de chegada")
src_model = ui.picker.points(area, ax, marker='*', color='y')
    
srcs, recs = utils.connect_points(src_model, recs)
ptime = traveltime.straight_ray_2d(model, 'vp', srcs, recs)
stime = traveltime.straight_ray_2d(model, 'vs', srcs, recs)
ttr_model = stime - ptime

with open('exercicio2-modelo.pickle', 'w') as f:
    data = {'ttr':ttr_model, 'recs':recs, 'src':src_model}
    pickle.dump(data, f)
                               
pyplot.figure(figsize=(14, 6))
pyplot.subplot(1, 2, 1)
pyplot.title('Epicentros')
pyplot.axis('scaled')
vis.map.points(recs, '^r', label="Estacao")
vis.map.points(src_model, '*y', label="Epicentro")
vis.map.set_area(area)
pyplot.legend(loc='upper left', shadow=True, numpoints=1, prop={'size':10})
pyplot.xlabel("X")
pyplot.ylabel("Y")
ax = pyplot.subplot(1, 2, 2)
pyplot.title('Tempos de chegada')
s = numpy.arange(len(ttr)) + 1
width = 0.2
pyplot.bar(s - width, ttr, width, color='r', label="Observado")
pyplot.bar(s, ttr_model, width, color='b', label="Seu")
ax.set_xticks(s)
pyplot.legend(loc='lower right', shadow=True, prop={'size':10})
pyplot.xlabel("Estacao")
pyplot.ylabel("Tempo de chegada")
pyplot.show()
