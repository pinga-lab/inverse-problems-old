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
    
with open('exercicio2-modelo.pickle') as f:
    data = pickle.load(f)
    ttr_model = data['ttr']
    src_model = data['src']
    
area = (0, 100000, 0, 100000)
vp, vs = 2000, 1000

pyplot.figure(figsize=(7, 6))
pyplot.title('Epicentros')
pyplot.axis('scaled')
vis.map.points(recs, '^r', label="Estacao")
vis.map.points(src_model, '*r', label="Seu")
vis.map.points(src, '*b', label="Verdadeiro")
vis.map.set_area(area)
pyplot.legend(loc='upper left', shadow=True, numpoints=1, prop={'size':10})
pyplot.xlabel("X")
pyplot.ylabel("Y")
pyplot.show()
