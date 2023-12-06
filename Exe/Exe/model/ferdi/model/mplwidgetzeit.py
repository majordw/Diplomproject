import PyQt5.QtWidgets as pq5
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
import matplotlib.animation as animation
import matplotlib as mpl
import numpy as np

mpl.use('qt5agg')

class mplWidgetZeit(pq5.QWidget):
    def __init__(self, parent = None):
        pq5.QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure(facecolor='white'))
        vertical_layout = pq5.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)       
        self.canvas.axes = self.canvas.figure.add_subplot()

        self.drawBase()

        self.setLayout(vertical_layout)  

    def drawBase(self):
        self.canvas.axes.set_xlim(0, 7)
        self.canvas.axes.set_ylim(0, 10)
        self.canvas.axes.xaxis.set_visible(False)
        self.canvas.axes.yaxis.set_visible(False)

        self.delta_y = np.linspace(2,8)
        self.delta_x = np.linspace(4,6)

        self.point_red, = self.canvas.axes.plot([2], [2], marker='o', color='red')
        self.point_green, = self.canvas.axes.plot([4], [2], marker='o', color='green')

        arrow = FancyArrowPatch((1.5,2),(1.5,8),arrowstyle='-|>',mutation_scale=20)
        self.canvas.axes.add_patch(arrow)
        arrow = FancyArrowPatch((4,2),(4,8),arrowstyle='-|>',mutation_scale=20)
        self.canvas.axes.add_patch(arrow)
        arrow = FancyArrowPatch((4,8),(6,8),arrowstyle='-|>',mutation_scale=20)
        self.canvas.axes.add_patch(arrow)
        arrow = FancyArrowPatch((4,2),(6,8),arrowstyle='-|>',mutation_scale=20)
        self.canvas.axes.add_patch(arrow)

        latex_string = r'$v*t$'
        self.canvas.axes.text(4.5, 8.5, latex_string, fontsize=18)
        latex_string = r'$l$'
        self.canvas.axes.text(1, 5, latex_string, fontsize=18)
        self.canvas.axes.text(3.5, 5, latex_string, fontsize=18)

        self.ani = animation.FuncAnimation(self.canvas.figure, self.animate, repeat=True, frames=len(self.delta_y), interval=50)
        
    def animate(self,i):
        self.point_red.set_data([2], [self.delta_y[i]])
        self.point_green.set_data([self.delta_x[i]], [self.delta_y[i]])
        return self.point_red, self.point_green

