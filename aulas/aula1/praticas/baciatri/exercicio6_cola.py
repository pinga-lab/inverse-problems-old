from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Polygon
from fatiando import vis
import cPickle as pickle

with open('exercicio6.pickle') as f:
    data = pickle.load(f)
    xp = data['xp']
    zp = data['zp']
    nodes = data['nodes']
    gz = data['gz']
    density = data['density']
        
with open('exercicio6-modelo.pickle') as f:
    data = pickle.load(f)
    nodes_model = data['nodes']

true = [Polygon(n) for n in nodes]
seu = Polygon(nodes_model)
    
pyplot.figure(figsize=(14, 5))
vis.map.polygon(seu, 'o-r', linewidth=2, fill='r', alpha=0.3,
            label='Seu')
vis.map.polygon(true[0], 'o--b', linewidth=2, label='Verdadeiro')
vis.map.polygon(true[1], 'o--b', linewidth=2)
pyplot.legend(loc='lower left', numpoints=1)
pyplot.xlabel("X")
pyplot.ylabel("Z")
vis.map.set_area((0, 100000, 5000, 0))
pyplot.show()
