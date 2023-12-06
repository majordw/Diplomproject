from time import sleep
import PyQt5.QtWidgets as pq5
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.animation import FuncAnimation
from threading import Thread
from PyQt5.QtGui import QDoubleValidator
import mainMenu as Menu
from model.tim import interfaceV2_schrWurf_end as Tim2
from model.tim import interfaceV2_waWurf_end as Tim3


""" 
My GUI:
GUI klasse für die grafischen Darstellung für die Oberfläche. Diese nimmt die Daten aus der UI-Datei und initialisiert 
diese. Anschließend werden dann einzelne Knöpfe bzw Eingaberestriktionen hinzugefügt. Es folgen die beiden Methoden menu
und prüfen. In menu wird ein Seitenmenü erstellt. In Prüfen werden die Eingaben auf ihre Richtigkeit überprüft. Das 
Seitenmenü wurde von Herrn Grasl erstellt. 
"""


class MyGUI(pq5.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MyGUI, self).__init__()
        uic.loadUi("model/tim/Models/base_frFall.ui", self)

        # Initialisierung der Elemente
        self.angabeTextEdit = self.findChild(QTextEdit, "angabeTextEdit")
        self.checkButton = self.findChild(QPushButton, "checkButton")
        self.eingabeGeschwindigkeit = self.findChild(QLineEdit, "eingabeGeschwindigkeit")
        self.eingabeGeschwindigkeit.setValidator(QDoubleValidator(-0.99, 99.999, 3))
        self.eingabeWurfdauer = self.findChild(QLineEdit, "eingabeWurfdauer")
        self.eingabeWurfdauer.setValidator(QDoubleValidator(0.99, 99.999, 3))
        self.loesungTextEdit = self.findChild(QTextEdit, "loesungTextEdit")
        self.animationWidget = self.findChild(QWidget, "animationWidget")

        self.berechnung = FallWurf(self)
        self.berechnung.solve()
        self.menuButton.clicked.connect(self.menu)
        self.angabeTextEdit.setPlainText(self.berechnung.textangabe)
        self.checkButton.clicked.connect(self.pruefen)
        self.btn_back.clicked.connect(lambda: self.changeUI(Menu.MainMenu))
        self.pushButton.clicked.connect(lambda: self.changeUI(Tim2.MyGUI))
        self.pushButton_2.clicked.connect(lambda: self.changeUI(Tim3.MyGUI))
        self.setWindowTitle('Lernprogramm')
    
    def changeUI(self, gui):
        self.window = gui()
        self.window.show()
        self.close()

    def menu(self):
        width = self.leftS.width()
        if width == 0:
            newWidth = 200
            self.menuButton.setIcon(QtGui.QIcon(u"model/ferdi/source/icons8-loeschen-30.png"))
        else:
            newWidth = 0
            self.menuButton.setIcon(QtGui.QIcon(u"model/ferdi/source/icons8-menue-30.png"))

        self.animation = QPropertyAnimation(self.leftS, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.start()

    def pruefen(self):
        pwgeschwindigikeit = self.eingabeGeschwindigkeit.text()
        pwzeit = self.eingabeWurfdauer.text()
        self.berechnung.wgeschwindigkeit = str(self.berechnung.wgeschwindigkeit)
        self.berechnung.wgeschwindigkeit = self.berechnung.wgeschwindigkeit.replace(".", ",")
        self.berechnung.wzeitvariable = str(self.berechnung.wzeitvariable)
        self.berechnung.wzeitvariable = self.berechnung.wzeitvariable.replace(".", ",")
        if self.berechnung.wgeschwindigkeit == pwgeschwindigikeit:
            geschwindigkeit = "Geschwindigkeit korrekt berechnet"
            print("Geschwindigkeit Korrekt")
        else:
            geschwindigkeit = "Geschwindigkeit falsch berechnet"
            print("Geschwindigkeit Falsch")
        if self.berechnung.wzeitvariable == pwzeit:
            zeit = "Zeit korrekt berechnet."
            print("Zeit korrekt")
        else:
            zeit = "Zeit falsch berechnet."
            print("Zeit falsch")
        if self.berechnung.wgeschwindigkeit == pwgeschwindigikeit and self.berechnung.wzeitvariable == pwzeit:
            self.loesungTextEdit.setPlainText(self.berechnung.textloesung)
            print("Gut gemacht")
        else:
            self.loesungTextEdit.setPlainText(f"Leider falsch! {geschwindigkeit}, {zeit}")
            print("Leider Falsch")


"""
FallWurf:
Die Klasse FallWurf enthält alle Methoden, die zur Berechnung der Eingaben nötig sind. Es werden alle Werte entweder 
zufällig erstellt oder, wie z.B. die Gravitation hardcoded. Das hat den Grund, dass sonst sehr extreme Werte 
herausgekommen wären, bzw. bei der Gravitation ist es nicht notwendig den Wert zufällig zu erstellen. 

Es wird in dieser klasse zwei Dinge getan: Die Animation und die Berechnung der Lösung.

Die Animation besteht aus der Methode wgleichungberechnung, plot, init, animate, draw, draw_new.
    Die Gleichungsberechnung erstellt mir zwei Listen, eine für die x-Koordinaten und die andere für die y-Koordinaten.
    Mit Plot wir ein schwarzes Rechteck erstellt um die Höhe zu darzustellen.
    Die letzten Drei erstellen dann die eigentliche Animation. Es wird dafür ein thread erstellt. Es wird der canvas 
    der bereits das Rechteck enthält einfach übermalt.      

Die Berechnung der Lösung verwendet die Methoden wzeit, wweite. Damit werden die Wurfdauer und 
die Wurfweite ermittelt. 
"""


class FallWurf:
    def __init__(self, gui_class: MyGUI):
        self.y = 0
        self.parent_gui = gui_class  # GUI in die Klasse laden, damit wir Zugriff auf das QWidget haben
        self.yListe = np.empty(0)
        self.wurfListe = np.empty(0)
        self.hoehe = np.random.randint(30, 101)
        self.gravitation = 9.81
        self.wurfgleichung = self.hoehe
        self.line = 0
        self.wgeschwindigkeit = 0
        self.wzeitvariable = 0
        self.textangabe = 0
        self.textloesung = 0

    def wgleichungberechnung(self):
        anhoehe = self.hoehe
        while self.wurfgleichung >= 0:
            self.wurfgleichung = anhoehe
            self.yListe = np.append(self.yListe, 0.5)
            self.wurfListe = np.append(self.wurfListe, self.wurfgleichung)
            anhoehe = anhoehe - 1
            self.y = self.y + 1

    def plot(self):  # Initiieren des Plots
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.line, = self.ax.plot([], [])
        ax.set(xlim=(-4, 50), ylim=(0, 100))
        ax.set_xlabel('Weite')
        ax.set_ylabel('Höhe')
        ax.set_title(f'Wurfparabel')
        layout = QVBoxLayout()  # Leeres Layout
        self.canvas = FigureCanvasQTAgg(fig)  # Canvas = fig als backend
        self.canvas.resize(50, 100)
        layout.addWidget(self.canvas)  # Einbetten des canvas in das leere Layout
        widget = self.parent_gui.animationWidget
        widget.setLayout(layout)  # setzen das Layout von unserem animationWidget

    def wweite(self):
        self.wgeschwindigkeit = round(-np.sqrt(2 * self.hoehe * self.gravitation), 3)
        print(f'Der Ball flog mit {self.wgeschwindigkeit}m/s.')

    def wzeit(self):
        self.wzeitvariable = round(np.sqrt(2 * self.hoehe / self.gravitation), 3)
        print(f'Der Ball flog {self.wzeitvariable} sek lang.')

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.line.set_data(self.xListe[:i], self.wurfListe[:i])
        return self.line,  # Beistrich für Iteration

    def draw(self):
        anim = FuncAnimation(self.fig, self.animate, frames=range(len(self.yListe) + 1), blit=True)
        anim.save()
        print("Speichern erfolgreich.")

    def draw_new(self):
        for i in range(len(self.yListe) + 1):
            self.line.set_xdata(self.yListe[:i])
            self.line.set_ydata(self.wurfListe[:i])
            sleep(0.1)
            self.canvas.draw()
            self.canvas.flush_events()

    def angabe(self):
        self.textangabe = f"Es wird ein Hammer aus {self.hoehe} m Höhe fallen gelassen. Die Gravitation beträgt " \
                          f"{self.gravitation} m/s.\nErmittlen Sie auf zwei Kommastellen genau die " \
                          f"Fallgeschwindigkeit in m/s, sowie die Falldauer in sek."

        print(
            f"Es wird ein Hammer aus {self.hoehe} m Höhe fallen gelassen. Die Gravitation beträgt " \
            f"{self.gravitation} m/s.\nErmittlen Sie auf zwei Kommastellen genau die " \
            f"Fallgeschwindigkeit in m/s, sowie die Falldauer in sek.")

    def loesung(self):
        self.textloesung = f"Die Fallgeschwindigkeit beträgt {self.wgeschwindigkeit}m/s und die Wurfdauer dauert " \
                           f"{self.wzeitvariable}sek."

        print(
            f"Die Fallgeschwindigkeit beträgt {self.wgeschwindigkeit}m/s und die Wurfdauer dauert"
            f"{self.wzeitvariable}sek.")

    def solve(self):
        self.angabe()
        self.wgleichungberechnung()
        self.plot()
        self.wweite()
        self.wzeit()
        self.loesung()
        thr = Thread(target=self.draw_new)  # , args=(1,))
        thr.start()


def main():
    app = pq5.QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
