import PyQt5.QtWidgets as pq5
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl

mpl.use('qt5agg')

class mplWidget(pq5.QWidget):
    def __init__(self, parent = None):
        pq5.QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure(facecolor='white'))
        vertical_layout = pq5.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)       
        self.canvas.axes = self.canvas.figure.add_subplot()

        self.canvas.axes.set_xlim(0, 1)
        self.canvas.axes.set_ylim(0, 1)
        self.canvas.axes.xaxis.set_visible(False)
        self.canvas.axes.yaxis.set_visible(False)
        self.canvas.axes.spines['top'].set_color('none')
        self.canvas.axes.spines['bottom'].set_color('none')
        self.canvas.axes.spines['left'].set_color('none')
        self.canvas.axes.spines['right'].set_color('none')
        self.canvas.axes.set_facecolor('white')

        latex_string = r'$u=\frac{u´+v}{1+\frac{u´*v}{c^2}}$'
        self.canvas.axes.text(0.3, 0.95, latex_string, fontsize=18)

        self.canvas.axes.plot()
        self.setLayout(vertical_layout)

