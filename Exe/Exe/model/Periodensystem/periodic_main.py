from PyQt5.QtWidgets import QApplication
from model.Periodensystem.periocdic_gui import Gui
from model.Periodensystem.periodic_manager import Manager
import sys

def main():

    app = QApplication([])
    window = Gui()
    window.show()
    manager = Manager(window)
    manager.initConectors()
    manager.mainGameLoop()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()