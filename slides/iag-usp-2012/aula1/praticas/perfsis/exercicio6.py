from matplotlib import pyplot
import numpy
from fatiando import ui
import cPickle as pickle

area = (0, 10000, 0, 600)
vmin, vmax, zmin, zmax = area

with open('exercicio5.pickle') as f:
    data = pickle.load(f)
    thickness = data['thickness']
    tts = data['tts']
    zp = data['zp']

vmin, vmax = 100, 10000
app = ui.gui.Lasagne(thickness, zp, vmin, vmax, tts)
app.run()

with open('exercicio6.pickle', 'w') as f:
    data = {'thickness':thickness, 'velocity':app.velocity,
            'tts':app.get_data(), 'zp':zp}
    pickle.dump(data, f)
