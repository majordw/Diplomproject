import sys
from time import sleep
import PyQt5.QtWidgets as pq5
import matplotlib.patches as patches
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
from model.tim import interfaceV2_Fall_end as Tim1
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
        uic.loadUi("model/tim/Models/base_schWurf_dyn.ui", self)

        # Initialisierung der Elemente
        self.angabeTextEdit = self.findChild(QTextEdit, "angabeTextEdit")
        self.checkButton = self.findChild(QPushButton, "checkButton")
        self.eingabeWurfweite = self.findChild(QLineEdit, "eingabeWurfweite")
        self.eingabeWurfweite.setValidator(QDoubleValidator(0.99, 99.999, 3))
        self.eingabeWurfdauer = self.findChild(QLineEdit, "eingabeWurfdauer")
        self.eingabeWurfdauer.setValidator(QDoubleValidator(0.99, 99.999, 3))
        self.eingabeAufprallgeschwindigkeit = self.findChild(QLineEdit, "eingabeAufprallgeschwindigkeit")
        self.eingabeAufprallwinkel = self.findChild(QLineEdit, "eingabeAufprallwinkel")
        self.loesungTextEdit = self.findChild(QTextEdit, "loesungTextEdit")
        self.animationWidget = self.findChild(QWidget, "animationWidget")

        """
        Aufrufen der Berechnungsklasse, damit diese bereits alle Berechnungen im Hintergrund ausgeführt werden. Es 
        verlangsamt den Aufbau des Programms aber, danach gibt es keine Probleme mehr. 
        """
        self.berechnung = SchraegWurf(self)
        self.berechnung.solve()
        self.menuButton.clicked.connect(self.menu)
        self.angabeTextEdit.setPlainText(self.berechnung.textangabe)
        self.checkButton.clicked.connect(self.pruefen)
        self.btn_back.clicked.connect(lambda: self.changeUI(Menu.MainMenu))
        self.pushButton.clicked.connect(lambda: self.changeUI(Tim1.MyGUI))
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
        pwweite = self.eingabeWurfweite.text()
        pwzeit = self.eingabeWurfdauer.text()
        print(self.berechnung.wweitevariable)
        print(self.berechnung.wzeitvariable)
        self.berechnung.wweitevariable = str(self.berechnung.wweitevariable)
        self.berechnung.wweitevariable = self.berechnung.wweitevariable.replace(".", ",")
        self.berechnung.wzeitvariable = str(self.berechnung.wzeitvariable)
        self.berechnung.wzeitvariable = self.berechnung.wzeitvariable.replace(".", ",")
        if self.berechnung.wweitevariable == pwweite:
            weite = "Weite Korrekt"
            print("Weite Korrekt")
        else:
            weite = "Weite Falsch"
            print("Weite Falsch")
        if self.berechnung.wzeitvariable == pwzeit:
            zeit = "Dauer korrekt"
            print("Zeit korrekt")
        else:
            zeit = "Dauer falsch"
            print("Zeit falsch")
        if self.berechnung.wweitevariable == pwweite and self.berechnung.wzeitvariable == pwzeit:
            self.loesungTextEdit.setPlainText(self.berechnung.textloesung)
            print("Gut gemacht")
        else:
            self.loesungTextEdit.setPlainText(f"Leider falsch! {weite}, {zeit}")
            print("Leider Falsch")


"""
SchraegWurf:
Die Klasse SchraegWurf enthält alle Methoden, die zur Berechnung der Eingaben nötig sind. Es werden alle Werte entweder 
zufällig erstellt oder, wie z.B. der Abwurfwinkel hardcoded. Das hat den Grund, dass sonst sehr extreme Werte 
herausgekommen wären. Auch eine Überschneidung mit dem waagrechten Wurf oder dem senkrechten Fall wäre möglich.

Es wird in dieser klasse zwei Dinge getan: Die Animation und die Berechnung der Lösung.

Die Animation besteht aus der Methode wgleichungberechnung, plot, init, animate, draw, draw_new.
    Die Gleichungsberechnung erstellt mir zwei Listen, eine für die x-Koordinaten und die andere für die y-Koordinaten.
    Mit Plot wir ein schwarzes Rechteck erstellt um die Höhe zu darzustellen.
    Die letzten Drei erstellen dann die eigentliche Animation. Es wird dafür ein thread erstellt. Es wird der canvas 
    der bereits das Rechteck enthält einfach übermalt.      

Die Berechnung der Lösung verwendet die Methoden wzeit und wweite. Damit werden die Wurfdauer und die Wurfweite 
ermittelt.
"""


class SchraegWurf:
    def __init__(self, gui_class: MyGUI):
        self.x = 0
        self.parent_gui = gui_class  # GUI in die Klasse laden, damit wir Zugriff auf das QWidget haben
        self.xListe = np.empty(0)
        self.wurfListe = np.empty(0)
        self.hoehe = np.random.randint(30, 100)
        self.alpha = 45
        self.radalpha = np.deg2rad(self.alpha)
        self.gravitation = 9.81
        self.vAnfang = np.random.randint(1, 10)
        self.vxAnfang = self.vAnfang * np.cos(self.radalpha)
        self.vyAnfang = self.vAnfang * np.sin(self.radalpha)
        self.wurfgleichung = self.x * np.tan(self.radalpha) - (self.gravitation * self.x ** 2) / (
                2 * self.vAnfang ** 2 * np.cos(self.radalpha) ** 2) + self.hoehe
        self.line = 0
        self.wweitevariable = 0
        self.wzeitvariable = 0
        self.vauftreffvariable = 0
        self.textangabe = 0
        self.textloesung = 0

    def wgleichungberechnung(self):
        while self.wurfgleichung >= 0:
            self.wurfgleichung = self.x * np.tan(self.radalpha) - (self.gravitation * self.x ** 2) / (
                    2 * self.vAnfang ** 2 * np.cos(self.radalpha) ** 2) + self.hoehe
            self.xListe = np.append(self.xListe, self.x)
            self.wurfListe = np.append(self.wurfListe, self.wurfgleichung)
            self.x = self.x + 1

    def plot(self):  # Initiieren des Plots
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.line, = self.ax.plot([], [])
        ax.add_patch(patches.Rectangle((-4, 0), 4, self.hoehe, edgecolor='black', fill=False))
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

    def wzeit(self):
        self.wzeitvariable = round(
            (self.vyAnfang + np.sqrt((self.vyAnfang ** 2) + 2 * self.gravitation * self.hoehe)) / self.gravitation, 3)
        print(f'Der Ball flog {self.wzeitvariable} sek lang.')

    def wweite(self):
        self.wweitevariable = round(self.vxAnfang * self.wzeitvariable, 3)
        print(f'Der Ball flog {self.wweitevariable}m weit.')

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.line.set_data(self.xListe[:i], self.wurfListe[:i])
        return self.line,  # Beistrich für Iteration

    def draw(self):
        self.ax.add_patch(patches.Rectangle((-4, 0), 4, self.hoehe, edgecolor='black', fill=False))
        anim = FuncAnimation(self.fig, self.animate, frames=range(len(self.xListe) + 1), blit=True)
        anim.save()
        print("Speichern erfolgreich.")

    def draw_new(self):
        for i in range(len(self.xListe) + 1):
            self.line.set_xdata(self.xListe[:i])
            self.line.set_ydata(self.wurfListe[:i])
            sleep(0.1)
            self.canvas.draw()
            self.canvas.flush_events()

    def angabe(self):
        self.textangabe = f"Es wird eine Kanone aus der Höhe {self.hoehe} m, mit der Anfangsgeschwindigkeit " \
                          f"{self.vAnfang} m/s abgefeuert. Die Gravitation ist {self.gravitation} m/s. " \
                          f"Der Wurfwinkel alpha beträgt {self.alpha}°.\nErmitteln Sie auf zwei Kommastellen genau die" \
                          f" Schussweite in m, sowie die Schussdauer in sek."

        print(
            f"Es wird eine Kanone aus der Höhe {self.hoehe} m, mit der Anfangsgeschwindigkeit ist " \
            f"{self.vAnfang} m/s abgefeuert. Die Gravitation ist {self.gravitation} m/s. " \
            f"Der Wurfwinkel alpha beträgt{self.alpha}°.\nErmitteln Sie auf zwei Kommastellen genau die" \
            f" Schussweite in m die Schussdauer in sek.")

    def loesung(self):
        self.textloesung = f"Die Schussweite beträgt {self.wweitevariable}m, die Schussdauer dauert " \
                           f"{self.wzeitvariable} sek."

        print(
            f"Die Schussweite beträgt {self.wweitevariable}m, die Schussdauer dauert " \
            f"{self.wzeitvariable} sek."
)

    def solve(self):
        self.angabe()
        self.wgleichungberechnung()
        self.plot()
        self.wzeit()
        self.wweite()
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
