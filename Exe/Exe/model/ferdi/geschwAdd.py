import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
from PyQt5 import uic
import mainMenu as Menu
from model.ferdi import ZeitGui as Ferdi

class MyGUI(qw.QWidget):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("model/ferdi/source/GesAdd2.ui", self)
        self.setWindowTitle('Lernprogramm')
        # Eventfilter
        self.lineEdit_u2.installEventFilter(self)
        self.lineEdit_v.installEventFilter(self)
        self.lineEdit_u2.setValidator(qg.QIntValidator())
        self.lineEdit_v.setValidator(qg.QIntValidator())
        # Timer für schrittweise Berrechnung
        self.step = 1
        self.QTimer = qc.QTimer()
        self.QTimer.setInterval(500)        #1/2 sekunde
        self.QTimer.timeout.connect(lambda: self.calc(self.lineEdit_u2.text(), self.lineEdit_v.text()))
        # btn connection
        self.menuButton.clicked.connect(self.sideBar)
        self.btn_action.clicked.connect(self.QTimer.start)
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
                    self.QTimer.start()
                    return True
        return super().eventFilter(source, event)
    
    def checkInput(self, n):
        if n == '':
            n=0
        else:
            n=float(n)
        return n 

    # schrittweise berrechnung (mittels QTimer)
    def calc(self, u2, v):
        u2 = self.checkInput(u2)
        v = self.checkInput(v)
        c = 299792458
        erg1 = u2+v
        erg2 = u2*v
        erg3 = erg2/c**2
        erg4 = 1+erg3
        erg5 = erg1/erg4
        if self.step == 0:
            self.mplWidget.canvas.axes.clear()
            self.step = self.step +1
            latexString = r'$u=\frac{u´+v}{1+\frac{u´*v}{c^2}}$'
            self.draw(0.3, 0.95, latexString)
        elif self.step == 1:
            self.step = self.step +1
            latexString = r'$u=\frac{'f'{u2}'r'+'f'{v}'r'}{1+\frac{'f'{u2}'r'*'f'{v}'r'}{'f'{c}'r'^2}}$'
            self.draw(0, 0.75, latexString)
        elif self.step == 2:
            self.step = self.step +1
            latexString = r'$u=\frac{'f'{erg1}'r'}{1+\frac{'f'{erg2}'r'}{'f'{c}'r'^2}}$'
            self.draw(0, 0.55, latexString)
        elif self.step == 3:
            self.step = self.step +1
            latexString = r'$u=\frac{'f'{erg1}'r'}{1+'f'{erg3}'r'}$'
            self.draw(0, 0.35, latexString)
        elif self.step == 4:
            self.step = self.step +1
            latexString = r'$u=\frac{'f'{erg1}'r'}{'f'{erg4}'r'}$'
            self.draw(0, 0.15, latexString)
        elif self.step == 5:
            self.step = 0
            latexString = r'$u='f'{erg5}'r'm/s$'
            self.draw(0, -0.05, latexString)
            # Stoppt den Timer 
            self.QTimer.stop()

    # Ausgabe im matplotlib Widget
    def draw(self, x, y, latexString):
        self.mplWidget.canvas.axes.text(x, y, latexString, fontsize=18)
        self.mplWidget.canvas.draw()

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