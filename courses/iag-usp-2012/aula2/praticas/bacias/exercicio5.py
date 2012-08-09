import numpy
import cPickle as pickle
from matplotlib import pyplot
from fatiando.potential import basin2d
from fatiando.inversion import gradient
from fatiando.mesher.dd import Polygon
from fatiando import vis

area = (0, 100000, 0, 5000)
with open('exercicio5e6.pickle') as f:
    data = pickle.load(f)
    xp = data['xp']
    zp = data['zp']
    nodes = data['nodes'][0]
    gz = data['gz']
    dens = data['density']
model = Polygon(nodes)
dm = basin2d.TriangularGzDM(xp, zp, gz, prop=dens, verts=nodes[0:2])
solver = gradient.levmarq(initial=(2500, 2500))
p, residuals = basin2d.triangular([dm], solver)
estimate = Polygon([nodes[0], nodes[1], p])

pyplot.figure()
pyplot.subplot(2, 1, 1)
pyplot.title("Anomalia de gravidade")
pyplot.plot(xp, gz, 'ok', label='Observada')
pyplot.plot(xp, gz - residuals[0], '-r', linewidth=2, label='Predita')
leg = pyplot.legend(loc='lower left', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.ylabel("mGal")
pyplot.xlim(0, 100000)
pyplot.subplot(2, 1, 2)
vis.map.polygon(estimate, 'o-r', linewidth=2, fill='r', alpha=0.3,
                label='Estimado')
vis.map.polygon(model, '--k', linewidth=2, label='Verdadeiro')
leg = pyplot.legend(loc='lower left', numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.xlabel("X")
pyplot.ylabel("Z")
vis.map.set_area((0, 100000, 5000, 0))
pyplot.show()
