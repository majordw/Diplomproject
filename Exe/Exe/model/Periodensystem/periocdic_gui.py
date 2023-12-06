from PyQt5 import QtWidgets, QtCore , uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QTime
from model.Periodensystem.customElementWidget import ElementWidget
import sys

#Um ein Windows Problem mit der Auflösung zu fixen.(150%,200% der "Größe von Text,Apps und Elemente")
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class Gui(QMainWindow):

    def printToGui(self, text):
        self.textBrowser.append(text)
        
    def __init__(self):
        super().__init__()

        uic.loadUi("model/Periodensystem/periodic.ui", self)
        self.setWindowTitle("Periodensystem Lernprogramm ")
        self.resize(1208, 909)
        self.elementWidgets = []
        self.timerTime = QTime(00,00,00)
        self.timer = QTimer()
        self.timer.timeout.connect(self.time)

    # Funktionen zum hochzählen des Timers/ resetten des Timers und umwandeln der Asugabe in String damit es angezeigt werden kann    
    def time(self):
        self.timerTime = self.timerTime.addSecs(1)
        self.TimeLabel.setText(self.timerTime.toString())
    
    def resetTimer(self):
        self.timerTime = QTime(00,00,00)
        self.TimeLabel.setText(self.timerTime.toString())

    #Zuordnung der einzelnen Elementwidgets mit den dazugehörigen Daten der JSON, nachdem die Widgets im QtDesigner
    # den Namen "en"(n für eine Zahl, an der Stelle im Periodensystem an der sie stehen(=Ordunungszahl)) so z.B. für
    #  Wasserstoff "e1" lassen sich die Daten leicht verknüpfen.
    def assignElements(self, listOfElements):
        
        for i in range(1, len(listOfElements)):
            childElement = self.findChild(ElementWidget, "e" + str(i))
            childElement.ordinalNumber.setText(str(listOfElements[i-1].number))
            childElement.symbol.setText(str(listOfElements[i-1].symbol))
            childElement.atomicMass.setText(str(listOfElements[i-1].atomic_mass)[:5])
            childElement.fullName.setText(str(listOfElements[i-1].name))
            self.elementWidgets.append(childElement)

    #Funktion zum Ausblenden der Elemente, Textfelder werden auf "?" geändert, Farbe wird grau
    def hideElement(self, ordinalNumber):
        self.elementWidgets[ordinalNumber-1].setStyleSheet("background-color: lightgrey;border-style:outset; border-width:1px; border-color:grey;")
        self.elementWidgets[ordinalNumber-1].symbol.setText("?")
        self.elementWidgets[ordinalNumber-1].ordinalNumber.setText("?")
        self.elementWidgets[ordinalNumber-1].atomicMass.setText("?")
        self.elementWidgets[ordinalNumber-1].fullName.setText("?")

    #Funktion zum Anzeigen welches Element gesucht wird
    def displayTask(self, taskText):
        self.taskLineEdit.setText(taskText)

    app = QApplication(sys.argv)
