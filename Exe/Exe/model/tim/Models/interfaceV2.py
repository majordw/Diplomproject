import PyQt5.QtWidgets as pq5
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QPropertyAnimation
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

class MyGUI(pq5.QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        # uic.loadUi("interface2.ui", self)
        uic.loadUi("base.ui", self)


        self.menuButton.clicked.connect(self.menu)
    
    def menu(self):
        width = self.leftS.width()
        if width == 0:
            newWidth = 200
            self.menuButton.setIcon(QtGui.QIcon(u"interface/icons8-löschen-30.png"))
        else:
            newWidth = 0
            self.menuButton.setIcon(QtGui.QIcon(u"interface/icons8-menü-30.png"))

        self.animation = QPropertyAnimation(self.leftS, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.start()

class WaagWurf:
    def __init__(self):
        self.x = 0
        self.xListe = np.empty(0)
        self.wurfListe = np.empty(0)
        self.hoehe = np.random.randint(30, 101)
        self.gravitation = 10
        self.vAnfang = np.random.randint(1, 11)
        self.wurfgleichung = -1 / 2 * self.gravitation / (self.vAnfang ** 2) * (self.x ** 2) + self.hoehe
        self.line = 0

    def wgleichung_berechnung(self):

        while self.wurfgleichung >= 0:
            self.wurfgleichung = -1 / 2 * self.gravitation / (self.vAnfang ** 2) * (self.x ** 2) + self.hoehe
            self.xListe = np.append(self.xListe, self.x)
            self.wurfListe = np.append(self.wurfListe, self.wurfgleichung)
            self.x = self.x + 1

    def plot(self):
        fig, ax = plt.subplots()
        ax.add_patch(patches.Rectangle((-4, 0), 4, self.hoehe, edgecolor='black', fill=False))
        ax.set(xlim=(-4, 50), ylim=(0, 100))
        ax.set_xlabel('Weite')
        ax.set_ylabel('Höhe')
        ax.set_title(f'Wurfparabel')
        plt.plot(self.xListe, self.wurfListe, color="black", linewidth=2)
        plt.show()

    def wweite(self):
        wweite = round(self.vAnfang * np.sqrt(2 * self.hoehe / self.gravitation), 3)
        print(f'Der Ball flog {wweite}m weit.')

    def wzeit(self):
        wzeit = round(np.sqrt(2 * self.hoehe / self.gravitation), 3)
        print(f'Der Ball flog {wzeit} sek lang.')
        return wzeit

    def vauftreff(self):
        vauftreff = round(np.sqrt(self.vAnfang ** 2 + 2 * self.gravitation * self.hoehe), 3)
        vauftreffkmh = round(vauftreff * 3.6, 3)
        print(f'Der Ball hatte eine Auftreffgeschwindigkeit von {self.wzeit()} m/sek. oder {vauftreffkmh} km/h.')

    def wauftreff(self):
        wauftreff = round(
            np.degrees(np.arctan(-np.sqrt(2 * self.gravitation * self.hoehe) / self.vAnfang)), 3)
        print(f'Der Ball landete in einem Winkel von {wauftreff}°.')

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.line.set_data(self.xListe[:i], self.wurfListe[:i])
        return self.line,  # Beistrich für Iteration

    def draw(self):
        fig = plt.figure()
        axis = plt.axes(xlim=(-4, 50), ylim=(0, 100))
        self.line, = axis.plot([], [], lw=3)
        axis.add_patch(patches.Rectangle((-4, 0), 4, self.hoehe, edgecolor='black', fill=False))
        anim = FuncAnimation(fig, self.animate, frames=range(len(self.xListe) + 1), blit=True)
        # plt.plot(self.xListe, self.wurfListe, color="black", linewidth=2)
        plt.show()
        anim.save('animation.gif', writer='ffmpeg', fps=30)

    def angabe(self):
        print(f"bla bla bla")

    def loesung(self):
        print(f'Der Ball flog {wweite}m weit.')
        print(f'Der Ball flog {wzeit} sek lang.')

    def solve(self):
        self.wgleichung_berechnung()
        # self.plot()
        self.wweite()
        self.wzeit()
        self.vauftreff()
        self.wauftreff()
        self.draw()


def main():
    app = pq5.QApplication([])
    window = MyGUI()
    window.show()
    solve = WaagWurf()
    solve.solve()
    app.exec_()



if __name__ == '__main__':
    main()