from os import path
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import SquareMesh
from fatiando.seismic import traveltime
from fatiando import vis, logger, utils, inversion
import cPickle as pickle

params = __import__('exercicio1_entrada')

imgfile = params.imagem
area = (0, 5, 0, 5)
shape = params.tamanho
model = SquareMesh(area, shape)
model.img2prop(imgfile, params.vmin, params.vmax, 'vp')

src_loc = utils.random_points(area, params.epicentros)
rec_loc = utils.circular_points(area, params.sismometros, random=True)
srcs, recs = utils.connect_points(src_loc, rec_loc)
tts, error = utils.contaminate(
    traveltime.straight_ray_2d(model, 'vp', srcs, recs), params.ruido, percent=True,
    return_stddev=True)

with open(params.dados, 'w') as f:
    data = [model, src_loc, rec_loc, tts, error]
    pickle.dump(data, f)

pyplot.figure(figsize=(7, 5))
pyplot.axis('scaled')
pyplot.title('Modelo de velocidades')
vis.map.squaremesh(model, model.props['vp'], cmap=pyplot.cm.seismic)
cb = pyplot.colorbar()
cb.set_label('Velocidade')
vis.map.points(src_loc, '*y', label="Epicentros")
vis.map.points(rec_loc, '^r', label="Sismometros")
leg = pyplot.legend(loc='lower left', shadow=True, numpoints=1)
leg.get_frame().set_alpha(0.5)
pyplot.show()
