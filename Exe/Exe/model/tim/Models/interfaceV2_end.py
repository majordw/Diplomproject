import PyQt5.QtWidgets as pq5
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QPropertyAnimation


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




def main():
    app = pq5.QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
