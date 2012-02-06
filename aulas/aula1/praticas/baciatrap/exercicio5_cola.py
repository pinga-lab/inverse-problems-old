from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import Polygon
from fatiando import vis
import cPickle as pickle

with open('exercicio4.pickle') as f:
    data = pickle.load(f)
    xp = data['xp']
    zp = data['zp']
    nodes = data['nodes']
    gz = data['gz']
    density = data['density']
        
with open('exercicio5.pickle') as f:
    data = pickle.load(f)
    nodes_model = data['nodes']

true = Polygon(nodes)
seu = Polygon(nodes_model)
    
pyplot.figure(figsize=(14, 5))
vis.map.polygon(seu, 'o-r', linewidth=2, fill='r', alpha=0.3,
                label='Seu')
vis.map.polygon(true, 'o--b', linewidth=2, label='Verdadeiro')
pyplot.legend(loc='lower right', numpoints=1)
pyplot.xlabel("X")
pyplot.ylabel("Z")
vis.map.set_area((0, 100000, 5000, 0))
pyplot.show()
