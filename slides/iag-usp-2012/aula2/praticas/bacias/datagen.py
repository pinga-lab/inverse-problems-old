import numpy
from fatiando.ui.gui import Moulder
import cPickle as pickle

area = (0, 100000, 0, 5000)
xp = numpy.arange(0, 100000, 1000)
zp = numpy.zeros_like(xp)
nodes = [[20000, 1], [80000, 1]]
app = Moulder(area, xp, zp)
app.run()

with open('exercicio5e6.pickle', 'w') as f:
    #data = {'xp':xp, 'zp':zp, 'nodes':1000*numpy.array(app.polygons[0]),
            #'gz':app.get_data(),
            #'density':app.densities[0]}
    data = {'xp':xp, 'zp':zp, 'nodes':[1000*numpy.array(p) for p in app.polygons],
            'gz':app.get_data(),
            'density':app.densities[0]}
    pickle.dump(data, f)
