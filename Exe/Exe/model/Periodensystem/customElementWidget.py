from PyQt5.QtWidgets import QWidget,QGridLayout,QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QMetaObject,Qt

#Diese Klasse ist aus einem QtDesigner Element umgewandelt um leichter Änderungen vornehmen zu können.
#Sie bildet ein einzelnes Feld im Periodensystem ab(z.B. Wasserstoff) und ordnet Positionen der einzelnen Elemente
# zu, setzt Größe, etc. und setzt den Objectnamen der Positionen um sie später aus dem JSON zuordnen zu können.
class ElementWidget(QWidget):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setStyleSheet("background-color:#b5deff; border-style:outset; border-width:1px; border-color:#ffffff; padding:0 0 0 0; margin: 0px;")
        self.gridLayout = QGridLayout(self)
        self.setMaximumHeight(90)
        self.setMaximumWidth(83)

        self.ordinalNumber = QLabel(self)
        self.ordinalNumber.setText("?")  
        font = QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.ordinalNumber.setFont(font)
        self.ordinalNumber.setAlignment(Qt.AlignLeft)
        self.ordinalNumber.setObjectName("ordinalNumber")
        self.gridLayout.addWidget(self.ordinalNumber, 1, 0, 1, 1)
                
        self.atomicMass = QLabel(self)
        self.atomicMass.setText("????")
        font = QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.atomicMass.setFont(font)
        self.atomicMass.setAlignment(Qt.AlignRight)
        self.atomicMass.setObjectName("atomicMass")
        self.gridLayout.addWidget(self.atomicMass, 1, 1, 1, 1)

        self.symbol = QLabel(self)
        self.symbol.setText("?")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.symbol.setFont(font)
        self.symbol.setAlignment(Qt.AlignCenter)
        self.symbol.setObjectName("symbol")
        self.gridLayout.addWidget(self.symbol, 2, 0, 1, 2)

        self.fullName = QLabel(self)
        self.fullName.setText("???????")
        font = QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.fullName.setFont(font)
        self.fullName.setAlignment(Qt.AlignCenter)
        self.fullName.setObjectName("fullName")
        self.gridLayout.addWidget(self.fullName, 3, 0, 1, 2)

        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.setLayout(self.gridLayout)


    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(400, 297)
        self.fullName = QWidget(self.gridLayoutWidget)
        self.fullName.setAlignment(Qt.AlignCenter)
        self.fullName.setObjectName("fullName")
        self.gridLayout.addWidget(self.fullName, 3, 0, 1, 2)

        self.retranslateUi(widget)
        QMetaObject.connectSlotsByName(widget)
