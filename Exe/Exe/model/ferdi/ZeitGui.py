import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
from PyQt5 import uic
import numpy as np
import mainMenu as Menu
from model.ferdi import geschwAdd as Ferdi

class MyGUI(qw.QWidget):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("model/ferdi/source/zeitdil.ui", self)
        self.setWindowTitle('Lernprogramm')
        # Eventfilter
        self.lineEdit_t.installEventFilter(self)
        self.lineEdit_v.installEventFilter(self)
        self.lineEdit_t.setValidator(qg.QIntValidator())
        self.lineEdit_v.setValidator(qg.QIntValidator())
        # btn connection
        self.menuButton.clicked.connect(self.sideBar)
        self.btn_action.clicked.connect(lambda: self.calc(self.lineEdit_t.text(), self.lineEdit_v.text()))
        self.btn_back.clicked.connect(lambda: self.changeUI(Menu.MainMenu))
        self.pushButton.clicked.connect(lambda: self.changeUI(Ferdi.MyGUI))
    
    def changeUI(self, gui):
        self.window = gui()
        self.window.show()
        self.close()

    def eventFilter(self, source, event):
        if event.type() == qc.QEvent.KeyPress:
            key = event.key()
            try:
                Lat = chr(key)
            except:
                Lat = key
            match Lat:
                case "C":
                    source.setText('299792458')
                    return True
                case 16777220:  #Enter
                    self.calc(self.lineEdit_t.text(), self.lineEdit_v.text())
                    return True
        return super().eventFilter(source, event)
    
    def checkInput(self, n):
        if n == '':
            n=0
        else:
            n=float(n)
        return n 
    
    # Berechnung
    def calc(self,t,v):
        c = 299792458   #m/s
        t = self.checkInput(t)
        v = self.checkInput(v)
        t_bew = t*np.sqrt(1-(v/c)**2)
        latexString = r'$t´='f'{t_bew}'r's$'
        self.draw(latexString)
    
    # Ausgabe im matplotlib Widget
    def draw(self, latexString):
        self.mplWidget_2.ani.pause()
        self.mplWidget_2.canvas.axes.clear()
        self.mplWidget_2.drawBase()
        self.mplWidget_2.canvas.axes.text(1, 1, latexString, fontsize=12)
        self.mplWidget_2.canvas.draw()

    # Animation der Sidebar
    def sideBar(self):
            width = self.leftS.width()
            if width == 0:
                newWidth = 200
                self.menuButton.setIcon(qg.QIcon(u"model/ferdi/source/icons8-loeschen-30.png"))
            else:
                newWidth = 0
                self.menuButton.setIcon(qg.QIcon(u"model/ferdi/source/icons8-menue-30.png"))
            self.animation = qc.QPropertyAnimation(self.leftS, b"maximumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(newWidth)
            self.animation.start()

def main():
    app = qw.QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()