from os import path
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import SquareMesh
from fatiando.seismic import traveltime, srtomo
from fatiando import vis, logger, utils, inversion
import cPickle as pickle

params = __import__('exercicio6_entrada')
with open(params.dados) as f:
    model, src_loc, rec_loc, tts, error = pickle.load(f)
shape = model.shape
area = (0, 5, 0, 5)
vmin, vmax = model.props['vp'].min(), model.props['vp'].max()
mesh = SquareMesh(area, shape)
with open('exercicio6-modelo.pickle') as f:
    estimate = pickle.load(f)

pyplot.figure(figsize=(14, 5))
pyplot.subplot(1, 2, 1)
pyplot.axis('scaled')
pyplot.title('Tomografia')
vis.map.squaremesh(mesh, estimate, vmin=1./vmax, vmax=1./vmin,
    cmap=pyplot.cm.seismic_r)
cb = pyplot.colorbar()
cb.set_label('Vagarosidade')
pyplot.subplot(1, 2, 2)
pyplot.axis('scaled')
pyplot.title('Verdadeiro')
vis.map.squaremesh(model, model.props['vp'], cmap=pyplot.cm.seismic)
cb = pyplot.colorbar()
cb.set_label('Velocidade')
pyplot.show()
