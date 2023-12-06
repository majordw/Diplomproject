import sys

from time import sleep
import PyQt5.QtWidgets as pq5
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QWidget, QLabel, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from threading import Thread


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MyGUI(pq5.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MyGUI, self).__init__()
        # uic.loadUi("interface2.ui", self)
        uic.loadUi("base_topic.ui", self)

        # Initialisierung der Elemente
        self.horizWurfButton = self.findChild(QPushButton, "horizWurfButton")
        self.schrWurfButton = self.findChild(QPushButton, "schrWurfButton")
        self.fallButton = self.findChild(QPushButton, "fallButton")

        self.angabeTextEdit = self.findChild(QTextEdit, "angabeTextEdit")
        self.checkButton = self.findChild(QPushButton, "checkButton")
        self.eingabeWurfweite = self.findChild(QLineEdit, "eingabeWurfweite")
        self.eingabeWurfdauer = self.findChild(QLineEdit, "eingabeWurfdauer")
        self.eingabeAufprallgeschwindigkeit = self.findChild(QLineEdit, "eingabeAufprallgeschwindigkeit")
        self.eingabeAufprallwinkel = self.findChild(QLineEdit, "eingabeAufprallwinkel")
        self.loesungTextEdit = self.findChild(QTextEdit, "loesungTextEdit")
        self.animationWidget = self.findChild(QWidget, "animationWidget")
        

        # Elemente mit der Funktion vernknüpfen
        # self.horizWurfButton.clicked.connect(open("interfaceV2_topic_end.py"))

        self.berechnung = WaagWurf(self)
        self.berechnung.solve()
        self.menuButton.clicked.connect(self.menu)
        self.angabeTextEdit.setPlainText(self.berechnung.textangabe)
        self.checkButton.clicked.connect(self.pruefen)

    def menu(self):
        width = self.leftS.width()
        if width == 0:
            newWidth = 200
            self.menuButton.setIcon(QtGui.QIcon(u"icons8-löschen-30.png"))
        else:
            newWidth = 0
            self.menuButton.setIcon(QtGui.QIcon(u"icons8-menü-30.png"))

        self.animation = QPropertyAnimation(self.leftS, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.start()

    def pruefen(self):
        pwweite = self.eingabeWurfweite.text()
        pwzeit = self.eingabeWurfdauer.text()
        pvauftreff = self.eingabeAufprallgeschwindigkeit.text()
        pwauftreff = self.eingabeAufprallwinkel.text()
        self.berechnung.wweitevariable = str(self.berechnung.wweitevariable)
        self.berechnung.wzeitvariable = str(self.berechnung.wzeitvariable)
        self.berechnung.vauftreffvariable = str(self.berechnung.vauftreffvariable)
        self.berechnung.wauftreffvariable = str(self.berechnung.wauftreffvariable)
        if self.berechnung.wweitevariable == pwweite and self.berechnung.wzeitvariable == pwzeit and \
                self.berechnung.vauftreffvariable == pvauftreff and self.berechnung.wauftreffvariable == pwauftreff:
            self.loesungTextEdit.setPlainText(self.berechnung.textloesung)
            print("Gut gemacht")
        else:
            self.loesungTextEdit.setPlainText("Leider falsch")
            print("Leider Falsch")


class WaagWurf:
    def __init__(self, gui_class: MyGUI):
        self.x = 0
        self.parent_gui = gui_class # GUI in die Klasse laden, damit wir Zugriff auf das QWidget haben
        self.xListe = np.empty(0)
        self.wurfListe = np.empty(0)
        self.hoehe = np.random.randint(30, 101)
        self.gravitation = 10
        self.vAnfang = np.random.randint(1, 11)
        self.wurfgleichung = -1 / 2 * self.gravitation / (self.vAnfang ** 2) * (self.x ** 2) + self.hoehe
        self.line = 0
        self.wweitevariable = 0
        self.wzeitvariable = 0
        self.vauftreffvariable = 0
        self.vauftreffkmhvariable = 0
        self.wauftreffvariable = 0
        self.textangabe = 0
        self.textloesung = 0

    def wgleichungberechnung(self):
        while self.wurfgleichung >= 0:
            self.wurfgleichung = -1 / 2 * self.gravitation / (self.vAnfang ** 2) * (self.x ** 2) + self.hoehe
            self.xListe = np.append(self.xListe, self.x)
            self.wurfListe = np.append(self.wurfListe, self.wurfgleichung)
            self.x = self.x + 1

    def plot(self): # Initiieren des Plots
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.line, = self.ax.plot([], [])
        ax.add_patch(patches.Rectangle((-4, 0), 4, self.hoehe, edgecolor='black', fill=False))
        ax.set(xlim=(-4, 50), ylim=(0, 100))
        ax.set_xlabel('Weite')
        ax.set_ylabel('Höhe')
        ax.set_title(f'Wurfparabel')
        layout = QVBoxLayout()                   # Leeres Layout
        self.canvas = FigureCanvasQTAgg(fig)     # Canvas = fig als backend
        self.canvas.resize(100, 100)
        layout.addWidget(self.canvas)            # Einbetten des canvas in das leere Layout
        widget = self.parent_gui.animationWidget
        widget.setLayout(layout)                 # setzen das Layout von unserem animationWidget

        #plt.show()
        # debug: plot angabe
        # self.line.set_xdata(self.xListe)
        # self.line.set_ydata(self.wurfListe)

    def wweite(self):
        self.wweitevariable = round(self.vAnfang * np.sqrt(2 * self.hoehe / self.gravitation), 3)
        print(f'Der Ball flog {self.wweitevariable}m weit.')

    def wzeit(self):
        self.wzeitvariable = round(np.sqrt(2 * self.hoehe / self.gravitation), 3)
        print(f'Der Ball flog {self.wzeitvariable} sek lang.')

    def vauftreff(self):
        self.vauftreffvariable = round(np.sqrt(self.vAnfang ** 2 + 2 * self.gravitation * self.hoehe), 3)
        self.vauftreffkmhvariable = round(self.vauftreffvariable * 3.6, 3)
        print(
            f'Der Ball hatte eine Auftreffgeschwindigkeit von {self.vauftreffvariable} m/sek. oder '
            f'{self.vauftreffkmhvariable} km/h.')

    def wauftreff(self):
        self.wauftreffvariable = round(
            np.degrees(np.arctan(-np.sqrt(2 * self.gravitation * self.hoehe) / self.vAnfang)), 3)
        print(f'Der Ball landete in einem Winkel von {self.wauftreffvariable}°.')

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.line.set_data(self.xListe[:i], self.wurfListe[:i])
        return self.line,  # Beistrich für Iteration

    def draw(self):
        # fig = plt.figure()
        # axis = plt.axes(xlim=(-4, 50), ylim=(0, 100))
        # self.line, = axis.plot([], [], lw=3)
        self.ax.add_patch(patches.Rectangle((-4, 0), 4, self.hoehe, edgecolor='black', fill=False))
        anim = FuncAnimation(self.fig, self.animate, frames=range(len(self.xListe) + 1), blit=True)
        anim.save()
        print("Speichern erfolgreich.")

    def draw_new(self):
        for i in range(len(self.xListe)):
            self.line.set_xdata(self.xListe[:i])
            self.line.set_ydata(self.wurfListe[:i])
            sleep(0.1)
            self.canvas.draw()
            self.canvas.flush_events()

    def angabe(self):
        self.textangabe = f"Das sind die Angaben: Höhe: {self.hoehe} m, Anfangsgeschwindigkeit: {self.vAnfang} m/s " \
                          f"und Gravitation ist {self.gravitation} m/s.\nErmittlen Sie auf zwei Kommastellen genau " \
                          f"die Wurfweite in m, die Wurfdauer in sek, die Aufprallgeschwindigkeit in m/sek und den " \
                          f"Aufprallwinkel in Grad."

        print(
            f"Das sind die Angaben: Höhe: {self.hoehe} m, Anfangsgeschwindigkeit: {self.vAnfang} m/s und Gravitation "
            f"ist {self.gravitation} m/s.\nErmittlen Sie auf zwei Kommastellen genau die Wurfweite in m, die Wurfdauer "
            f"in sek, die Aufprallgeschwindigkeit in m/sek und den Aufprallwinkel in Grad.")

    def loesung(self):
        self.textloesung = f"Wurfweite ist {self.wweitevariable}m, die Wurfdauer ist {self.wzeitvariable} sek lang." \
                           f" Die Aufprallgeschwindigkeit ist {self.vauftreffvariable} m/sek oder " \
                           f"{self.vauftreffkmhvariable} km/h. Der Aufprallwinkel ist {self.wauftreffvariable}."

        print(
            f"Wurfweite ist {self.wweitevariable}m, die Wurfdauer ist {self.wzeitvariable} sek lang. "
            f"Die Aufprallgeschwindigkeit ist {self.vauftreffvariable} m/sek oder {self.vauftreffkmhvariable} km/h. "
            f"Der Aufprallwinkel ist {self.wauftreffvariable}.")

    def solve(self):
        self.angabe()
        self.wgleichungberechnung()
        self.plot()
        self.wweite()
        self.wzeit()
        self.vauftreff()
        self.wauftreff()
        self.loesung()
        #self.draw_new()
        thr = Thread(target=self.draw_new) #, args=(1,))
        thr.start()


def main():
    app = pq5.QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
