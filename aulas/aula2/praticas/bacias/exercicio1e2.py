import numpy
from matplotlib import pyplot
from fatiando.ui.gui import BasinTri
from fatiando.potential import basin2d
from fatiando.inversion import gradient
from fatiando.mesher.dd import Polygon
from fatiando import vis

area = (0, 100000, 0, 5000)
xp = numpy.arange(0, 100000, 1000)
zp = numpy.zeros_like(xp)
nodes = [[20000, 1], [80000, 1]]
app = BasinTri(area, nodes, xp, zp)
app.run()
gz = app.get_data()
dens = app.densities[0]
model = Polygon(1000*numpy.array(app.polygons[0]))
dm = basin2d.TriangularGzDM(xp, zp, gz, prop=dens, verts=nodes)
solver = gradient.levmarq(initial=(50000, 2500))
p, residuals = basin2d.triangular([dm], solver)
estimate = Polygon([nodes[0], nodes[1], p])

pyplot.figure()
pyplot.subplot(2, 1, 1)
pyplot.title("Anomalia de gravidade")
pyplot.plot(xp, gz, 'ok', label='Observada')
pyplot.plot(xp, gz - residuals[0], '-r', linewidth=2, label='Predita')
pyplot.legend(loc='lower left', numpoints=1)
pyplot.ylabel("mGal")
pyplot.xlim(0, 100000)
pyplot.subplot(2, 1, 2)
vis.map.polygon(estimate, 'o-r', linewidth=2, fill='r', alpha=0.3,
                label='Estimado')
vis.map.polygon(model, '--k', linewidth=2, label='Verdadeiro')
pyplot.legend(loc='lower left', numpoints=1)
pyplot.xlabel("X")
pyplot.ylabel("Z")
vis.map.set_area((0, 100000, 5000, 0))
pyplot.show()
