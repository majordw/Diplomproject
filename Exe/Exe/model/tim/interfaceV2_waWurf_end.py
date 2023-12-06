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
from model.tim import interfaceV2_schrWurf_end as Tim2


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
        uic.loadUi("model/tim/Models/base_waWurf.ui", self)

        # Initialisierung der Elemente

        self.angabeTextEdit = self.findChild(QTextEdit, "angabeTextEdit")
        self.checkButton = self.findChild(QPushButton, "checkButton")
        self.eingabeWurfweite = self.findChild(QLineEdit, "eingabeWurfweite")
        self.eingabeWurfweite.setValidator(QDoubleValidator(0.99, 99.999, 3))
        self.eingabeWurfdauer = self.findChild(QLineEdit, "eingabeWurfdauer")
        self.eingabeWurfdauer.setValidator(QDoubleValidator(0.99, 99.999, 3))
        self.eingabeAufprallgeschwindigkeit = self.findChild(QLineEdit, "eingabeAufprallgeschwindigkeit")
        self.eingabeAufprallgeschwindigkeit.setValidator(QDoubleValidator(0.99, 99.999, 3))
        self.eingabeAufprallwinkel = self.findChild(QLineEdit, "eingabeAufprallwinkel")
        self.eingabeAufprallwinkel.setValidator(QDoubleValidator(-99.99, 99.999, 3))
        self.loesungTextEdit = self.findChild(QTextEdit, "loesungTextEdit")
        self.animationWidget = self.findChild(QWidget, "animationWidget")

        self.berechnung = WaagWurf(self)
        self.berechnung.solve()
        self.menuButton.clicked.connect(self.menu)
        self.angabeTextEdit.setPlainText(self.berechnung.textangabe)
        self.checkButton.clicked.connect(self.pruefen)
        self.btn_back.clicked.connect(lambda: self.changeUI(Menu.MainMenu))
        self.pushButton.clicked.connect(lambda: self.changeUI(Tim2.MyGUI))
        self.pushButton_2.clicked.connect(lambda: self.changeUI(Tim2.MyGUI))
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
        pvauftreff = self.eingabeAufprallgeschwindigkeit.text()
        pwauftreff = self.eingabeAufprallwinkel.text()
        self.berechnung.wweitevariable = str(self.berechnung.wweitevariable)
        self.berechnung.wweitevariable = self.berechnung.wweitevariable.replace(".", ",")
        self.berechnung.wzeitvariable = str(self.berechnung.wzeitvariable)
        self.berechnung.wzeitvariable = self.berechnung.wzeitvariable.replace(".", ",")
        self.berechnung.vauftreffvariable = str(self.berechnung.vauftreffvariable)
        self.berechnung.vauftreffvariable = self.berechnung.vauftreffvariable.replace(".", ",")
        self.berechnung.winkauftreffvariable = str(self.berechnung.winkauftreffvariable)
        self.berechnung.winkauftreffvariable = self.berechnung.winkauftreffvariable.replace(".", ",")
        if self.berechnung.wweitevariable == pwweite:
            weite = "Weite Korrekt"
            print("Weite Korrekt")
        else:
            weite = "Weite Falsch"
            print("Weite Falsch")
        if self.berechnung.wzeitvariable == pwzeit:
            zeit = "Zeit korrekt"
            print("Zeit korrekt")
        else:
            zeit = "Zeit falsch"
            print("Zeit falsch")
        if self.berechnung.vauftreffvariable == pvauftreff:
            auftreff = "Auftreffgeschwindigkeit korrekt"
            print("Auftreffgeschwindigkeit korrekt")
        else:
            auftreff = "Auftreffgeschwindigkeit Falsch"
            print("Auftreffgeschwindigkeit Falsch")
        if self.berechnung.winkauftreffvariable == pwauftreff:
            winkel = "Winkel korrekt"
            print("Winkel korrekt")
        else:
            winkel = "Winkel falsch"
            print("Winkel falsch")
        if self.berechnung.wweitevariable == pwweite and self.berechnung.wzeitvariable == pwzeit and \
                self.berechnung.vauftreffvariable == pvauftreff and self.berechnung.winkauftreffvariable == pwauftreff:
            self.loesungTextEdit.setPlainText(self.berechnung.textloesung)
            print("Gut gemacht")
        else:
            self.loesungTextEdit.setPlainText(f"Leider falsch. {weite}, {zeit}, {auftreff}, {winkel} bitte überprüfen "
                                              f"Sie die eingegeben Zahlen.")
            print("Leider Falsch")


"""
WaagWurf:
Die Klasse WaagWurf enthält alle Methoden, die zur Berechnung der Eingaben nötig sind. Es werden alle Werte entweder 
zufällig erstellt oder, wie z.B. die Gravitation hardcoded. Das hat den Grund, dass sonst sehr extreme Werte 
herausgekommen wären, bzw. bei der Gravitation nicht notwendig ist den Wert zufällig zu erstellen. 

Es wird in dieser klasse zwei Dinge getan: Die Animation und die Berechnung der Lösung.

Die Animation besteht aus der Methode wgleichungberechnung, plot, init, animate, draw, draw_new.
    Die Gleichungsberechnung erstellt mir zwei Listen, eine für die x-Koordinaten und die andere für die y-Koordinaten.
    Mit Plot wir ein schwarzes Rechteck erstellt um die Höhe zu darzustellen.
    Die letzten Drei erstellen dann die eigentliche Animation. Es wird dafür ein thread erstellt. Es wird der canvas 
    der bereits das Rechteck enthält einfach übermalt.      

Die Berechnung der Lösung verwendet die Methoden wzeit, wweite, vauftreff, winauftreff. Damit werden die Wurfdauer, 
die Wurfweite, die Aufprallgeschwindigkeit und der Winkel, in dem das Objekt auftrifft, ermittelt.
"""


class WaagWurf:
    def __init__(self, gui_class: MyGUI):
        self.x = 0
        self.parent_gui = gui_class  # GUI in die Klasse laden, damit wir Zugriff auf das QWidget haben
        self.xListe = np.empty(0)
        self.wurfListe = np.empty(0)
        self.hoehe = np.random.randint(30, 101)
        self.gravitation = 9.81
        self.vAnfang = np.random.randint(1, 11)
        self.wurfgleichung = -1 / 2 * self.gravitation / (self.vAnfang ** 2) * (self.x ** 2) + self.hoehe
        self.line = 0
        self.wweitevariable = 0
        self.wzeitvariable = 0
        self.vauftreffvariable = 0
        self.vauftreffkmhvariable = 0
        self.winkauftreffvariable = 0
        self.textangabe = 0
        self.textloesung = 0

    def wgleichungberechnung(self):
        while self.wurfgleichung >= 0:
            self.wurfgleichung = -1 / 2 * self.gravitation / (self.vAnfang ** 2) * (self.x ** 2) + self.hoehe
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

    def winauftreff(self):
        self.winkauftreffvariable = round(
            np.degrees(np.arctan(-np.sqrt(2 * self.gravitation * self.hoehe) / self.vAnfang)), 3)
        print(f'Der Ball landete in einem Winkel von {self.winkauftreffvariable}°.')

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
        self.textangabe = f"Es wird eine Kanone horizontal in der Höhe {self.hoehe} m, mit der " \
                          f"Anfangsgeschwindigkeit {self.vAnfang} m/s abgefeuert. Die Gravitation beträgt " \
                          f"{self.gravitation} m/s.\nErmittlen Sie auf zwei Kommastellen genau die Schussweite in m," \
                          f" die Schussdauer in sek, die Aufprallgeschwindigkeit in m/sek und den Aufprallwinkel " \
                          f"in Grad."

        print(
            f"Es wird eine Kanone horizontal in der Höhe {self.hoehe} m, mit der " \
            f"Anfangsgeschwindigkeit {self.vAnfang} m/s abgefeuert. Die Gravitation beträgt " \
            f"{self.gravitation} m/s.\nErmittlen Sie auf zwei Kommastellen genau die Schussweite in m," \
            f" die Schussdauer in sek, die Aufprallgeschwindigkeit in m/sek und den Aufprallwinkel " \
            f"in Grad.")

    def loesung(self):
        self.textloesung = f"Die Schussweite beträgt {self.wweitevariable}m, die Schussdauer dauert " \
                           f"{self.wzeitvariable} sek. Die Aufprallgeschwindigkeit ist {self.vauftreffvariable} m/sek" \
                           f" oder{self.vauftreffkmhvariable} km/h. Der Aufprallwinkel beträgt " \
                           f"{self.winkauftreffvariable}°."

        print(
            f"Die Schussweite beträgt {self.wweitevariable}m, die Schussdauer dauert " \
            f"{self.wzeitvariable} sek. Die Aufprallgeschwindigkeit ist {self.vauftreffvariable} m/sek" \
            f" oder{self.vauftreffkmhvariable} km/h. Der Aufprallwinkel beträgt " \
            f"{self.winkauftreffvariable}°.")

    def solve(self):
        self.angabe()
        self.wgleichungberechnung()
        self.plot()
        self.wweite()
        self.wzeit()
        self.vauftreff()
        self.winauftreff()
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
