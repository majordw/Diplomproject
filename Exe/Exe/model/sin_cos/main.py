import sys
import math

import numpy as np

from matplotlib.backends.qt_compat import QtWidgets
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as plt_arc

from PyQt5.QtCore import Qt, QSize, QRect, QCoreApplication, QPropertyAnimation, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QIntValidator
from PyQt5.QtWidgets import QTextBrowser, QLineEdit, QLabel

import mainMenu
from model.sin_cos.canvas import Canvas, MplCanvas
import model.sin_cos.text as text


# http://schulphysikwiki.de/index.php/Animation:_Sinus_und_Cosinus_im_Einheitskreis


class ApplicationWindow(QtWidgets.QMainWindow):
    """
    This "window" is a QWidget.
    It will appear as a free-floating window.
    """

    def __init__(self, *args, **kwargs):
        self.frame_content = 0  # where we are now
        super().__init__(*args, **kwargs)
        self.text_content = text.first_word
        self.ankathete = None
        self.gegenkathete = None
        self.degrie = None


        #######################################################################################
        # matplotlib initialization
        #######################################################################################
        self.canvas = Canvas()

        #######################################################################################
        # qt5 initialization
        #######################################################################################
        self.qt5_init()

        # buttons in physic project
        self.rechtwinkliges_dreieck_button.clicked.connect(self.rechtwinkliges_dreieck)
        self.sinus_button.clicked.connect(self.sinus)
        self.animation_sinus_button.clicked.connect(self.animation_sinus)
        self.explain_button.clicked.connect(self.explain)

        # An animated button of the menu
        self.menuButton.clicked.connect(self.menu)
        # The buttons of the projects
        self.btn_back.clicked.connect(self.back_button)

    def qt5_init(self):

        """
        main window UI
        """
        self.setWindowTitle("Physic - Sinus and Cosinus")
        # main window: size width height and margin top left:
        top, left, width, height = 150, 100, 1194, 503
        self.setGeometry(left, top, width, height)
        self.setObjectName("MainWindow")

        #######################################################################################
        #  Main Widget (all objects are inside it)
        ####################################################################################### 
        self.centralwidget = QtWidgets.QWidget(self)
        # StyleSheet
        self.centralwidget.setStyleSheet(
            ".QWidget{\n"
            "    border: none;\n"
            "}\n"

            ".QFrame{\n"
            "    border: none;\n"
            "}\n"

            "#top_frame{\n"
            "    background-color: rgb(181, 222, 255);\n"
            "}\n"

            "#content_frame{\n"
            "    background-color: rgb(181, 222, 255);\n"
            "}")
        self.centralwidget.setObjectName("centralwidget")

        #######################################################################################
        #  Horizontal Layout- QHBoxLayout (the left menu)
        #######################################################################################

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        # margin window frame
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #######################################################################################
        #                     The frame is inside the central widget                        #
        #######################################################################################          
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        #######################################################################################
        #                       Horizontal Box 2 QHBoxLayout                                #
        ####################################################################################### 
        # HorizontalLayout_2 is added into the self.frame
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        # margin
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #######################################################################################
        #       The initialization of the leftS frame                                       #
        ####################################################################################### 
        self.leftS = QtWidgets.QFrame(self.frame)
        self.leftS.setMaximumSize(QSize(0, 16777215))
        self.leftS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftS.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftS.setObjectName("leftS")

        #######################################################################################
        #                    The initialization of the horizontal_Layout_3 (QHBoxLayout)    #
        ####################################################################################### 

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.leftS)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        #######################################################################################
        #                The initialization of the horizontal_Layout_3 (QHBoxLayout)        #
        ####################################################################################### 
        self.frame_4 = QtWidgets.QFrame(self.leftS)
        self.frame_4.setMinimumSize(QSize(200, 0))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        #######################################################################################
        # The initialization of the verticalLayout_3 (QVBoxLayout) for the buttons of the menu #
        ####################################################################################### 
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # label
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setMaximumSize(QSize(16777215, 36))
        font = QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        # The label is added into the verticalLayout_3
        self.verticalLayout_3.addWidget(self.label_2)

        #######################################################################################
        #              The initialization the left buttons of the menu                      #
        ####################################################################################### 

        # Spacer between buttons and button back
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # add spacer to VL3
        self.verticalLayout_3.addItem(spacerItem)

        self.btn_back = QtWidgets.QPushButton(self.frame_4)
        self.btn_back.setObjectName("btn_back")
        # add button to VL3
        self.verticalLayout_3.addWidget(self.btn_back)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.horizontalLayout_2.addWidget(self.leftS)

        #######################################################################################
        #           The initialization of the rightS frame                                   #
        ####################################################################################### 

        self.rightS = QtWidgets.QFrame(self.frame)
        self.rightS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rightS.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rightS.setObjectName("rightS")

        #######################################################################################
        #                       Vertical Box QVBoxLayout                                    #
        ####################################################################################### 
        self.verticalLayout = QtWidgets.QVBoxLayout(self.rightS)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_frame = QtWidgets.QFrame(self.rightS)
        self.top_frame.setMaximumSize(QSize(16777215, 36))
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName("top_frame")

        #######################################################################################
        #                       Horizontal Box 4 QHBoxLayout                                #
        ####################################################################################### 
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.top_frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        #######################################################################################
        #                       Frame 8                                                     #
        ####################################################################################### 
        self.frame_8 = QtWidgets.QFrame(self.top_frame)
        self.frame_8.setMinimumSize(QSize(36, 36))
        self.frame_8.setMaximumSize(QSize(36, 36))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")

        #######################################################################################
        #                      Vertical Box 2 QVBoxLayout                                   #
        ####################################################################################### 
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #######################################################################################
        #                   The initialization of one animated button for the menu          #
        ####################################################################################### 
        self.menuButton = QtWidgets.QPushButton(self.frame_8)
        self.menuButton.setMinimumSize(QSize(36, 36))
        self.menuButton.setMaximumSize(QSize(36, 36))
        self.menuButton.setText("")

        # init and add icon
        icon = QIcon()
        # from model.sin_cos.canvas
        icon.addPixmap(QPixmap("model/pictures/menu.png"), QIcon.Normal, QIcon.Off)
        self.menuButton.setIcon(icon)
        self.menuButton.setObjectName("menuButton")
        # add menu button to VL2
        self.verticalLayout_2.addWidget(self.menuButton)

        # add the horizontalLayout_4 into frame 8 (menu button)
        self.horizontalLayout_4.addWidget(self.frame_8)

        #  The initialization of then spacer
        spacerItem1 = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # add spaser item 1 to horizontalLayout 4
        self.horizontalLayout_4.addItem(spacerItem1)

        # label
        self.label = QtWidgets.QLabel(self.top_frame)
        font = QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        # add label to horizontalLayout 4
        self.horizontalLayout_4.addWidget(self.label)

        self.label_right = QtWidgets.QLabel(self.top_frame)
        font = QFont()
        font.setPointSize(24)
        self.label_right.setFont(font)
        self.label_right.setAlignment(Qt.AlignCenter)
        self.label_right.setObjectName("label")
        # add label to horizontalLayout 4
        self.horizontalLayout_4.addWidget(self.label_right)

        # spacer 2
        spacerItem2 = QtWidgets.QSpacerItem(179, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # add label to horizontalLayout 4
        self.horizontalLayout_4.addItem(spacerItem2)
        # add top_frame to verticalLayout
        self.verticalLayout.addWidget(self.top_frame)

        ##############################################################################################
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        #                                    Content Frame                                       #
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        ##############################################################################################

        self.frame_main = QtWidgets.QFrame(self.rightS)
        self.frame_main.setMinimumSize(QSize(0, 100))
        self.frame_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main.setObjectName("frame_main")

        #######################################################################################
        #                      Widget for right site (content)                              #
        ####################################################################################### 

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_main)
        self.horizontalLayoutWidget.setGeometry(QRect(70, -1, 1071, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        #######################################################################################
        #                       Horizontal Layout for Buttons QHBoxLayout                   #
        ####################################################################################### 
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_buttons.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")

        #######################################################################################
        #                       Buttons init and add                                        #
        ####################################################################################### 

        # rechtwinkliges Dreieck
        self.rechtwinkliges_dreieck_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.rechtwinkliges_dreieck_button.setObjectName("rechtwinkliges Dreieck")
        self.horizontalLayout_buttons.addWidget(self.rechtwinkliges_dreieck_button)

        # Erlärung
        self.explain_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.explain_button.setObjectName("explain")
        self.horizontalLayout_buttons.addWidget(self.explain_button)

        # sin button
        self.sinus_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.sinus_button.setObjectName("sinus_button")
        self.horizontalLayout_buttons.addWidget(self.sinus_button)

        # Animation Sinus
        self.animation_sinus_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.animation_sinus_button.setObjectName("Animation Sinus")
        self.horizontalLayout_buttons.addWidget(self.animation_sinus_button)

        #######################################################################################
        #                                  Widget for Content                              #
        #######################################################################################
        self.horizontalWidget_content = QtWidgets.QWidget(self.frame_main)

        #     +++++++++++++++++++++  geometry of main content   ++++++++++++++++++++++++++  #
        top, left, width, height = 50, 50, 1100, 380
        self.horizontalWidget_content.setGeometry(QRect(top, left, width, height))
        self.horizontalWidget_content.setObjectName("horizontalWidget_content")

        #######################################################################################
        #                       Horizontal Box layout for main content                      #
        ####################################################################################### 

        self.horizontalLayout_main = QtWidgets.QGridLayout(self.horizontalWidget_content)
        self.horizontalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_main.setObjectName("horizontalLayout_main")

        #######################################################################################
        #                                  Widget main for Content                          #
        #######################################################################################
        self.widget_main = QtWidgets.QWidget(self.horizontalWidget_content)
        self.widget_main.setObjectName("widget_main")

        #######################################################################################
        #                                  Widget 2 for Content                             #
        #######################################################################################
        self.widget_2 = QtWidgets.QWidget(self.widget_main)
        top1, left1, width1, height1 = 10, 100, 300, 300
        self.widget_2.setGeometry(QRect(top1, left1, width1, height1))
        self.widget_2.setObjectName("widget_2")

        # addWidget to main content
        self.horizontalLayout_main.addWidget(self.widget_main, 0, 0, 1, 1)

        self.verticalLayout.addWidget(self.frame_main)

        #######################################################################################
        #                                  frame for right site                            #
        #######################################################################################

        self.content_frame = QtWidgets.QFrame(self.rightS)
        self.content_frame.setMinimumSize(QSize(0, 36))
        self.content_frame.setMaximumSize(QSize(16777215, 36))
        self.content_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_frame.setObjectName("content_frame")

        # add verticalLayout to content_frame 
        self.verticalLayout.addWidget(self.content_frame)
        # add rightS frame to horizontalLayout_2
        self.horizontalLayout_2.addWidget(self.rightS)

        ##########################################################################
        # text_content
        self.text = QTextBrowser()
        self.text.setAcceptRichText(True)
        self.text.setOpenExternalLinks(True)
        # addWidget(*Widget, row, column, rowspan, colspan)
        self.horizontalLayout_main.addWidget(self.text, 0, 0, 4, 2)
        self.text_content = text.first_word
        self.text.setFixedWidth(1100)
        self.text.append(self.text_content)

        self.canvas.graph()

        # add rightS frame to horizontalLayout_2
        self.horizontalLayout.addWidget(self.frame)

        self.setCentralWidget(self.centralwidget)

        # The function for all labels, strings of text etc
        self.retranslateUi()

        # The initialization of the context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos):
        context = QtWidgets.QMenu(self)

        # The initialization of the sinus button
        sin = QtWidgets.QAction("Sinus", self)
        sin.triggered.connect(self.sinus)
        context.addAction(sin)
        # The initialization of the cosinus button
        cos = QtWidgets.QAction("Rechtwinkliges Dreieck", self)
        cos.triggered.connect(self.rechtwinkliges_dreieck)
        # maybe for the future
        # cos.triggered.connect(lambda: label.setText("cosinus button triggered"))
        context.addAction(cos)
        # The initialization of the folmeln button
        formeln = QtWidgets.QAction("Animation Sinus", self)
        formeln.triggered.connect(self.animation_sinus)
        context.addAction(formeln)

        explain = QtWidgets.QAction("Erklärungen", self)
        explain.triggered.connect(self.explain)
        context.addAction(explain)

        context.exec(self.mapToGlobal(pos))

    def retranslateUi(self):
        """
        Naming 
        """
        self._translate = QCoreApplication.translate
        # Window Name
        self.setWindowTitle(self._translate("MainWindow", "Sinus"))

        self.label_2.setText(self._translate("MainWindow", "Menu"))
        # TODO
        self.btn_back.setText(self._translate("MainWindow", "back"))
        self.label.setText(self._translate("MainWindow", "Sinus Cosinus title"))
        self.sinus_button.setText(self._translate("MainWindow", "Sinus und Cosinus"))
        self.rechtwinkliges_dreieck_button.setText(self._translate("MainWindow", "Rechtwinkliges Dreieck"))
        self.animation_sinus_button.setText(self._translate("MainWindow", "Animation Sinus"))
        self.explain_button.setText(self._translate("MainWindow", "Erklärung"))

    def explain(self):
        self.mouse_click_text = "der Erklärseite"
        self.remove_canvas()
        self.frame_content = 4
        # Set the window title and the main label
        self.setWindowTitle(self._translate("MainWindow", "Erlärung"))
        self.label.setText(self._translate("MainWindow", "Erklärung"))
        # text Feld size
        self.text.setFixedWidth(610)
        self.text.setFixedHeight(380)

        # sinus erklärung
        self.sinus_expain_button = QtWidgets.QPushButton()
        self.sinus_expain_button.setObjectName("Sinus Erklärung")
        self.sinus_expain_button.setText(self._translate("MainWindow", "Sinus Erklärung"))
        self.horizontalLayout_main.addWidget(self.sinus_expain_button, 1, 2, 1, 1)
        self.sinus_expain_button.clicked.connect(self.sinus_explain)

        # cosinus erklärung
        self.cosinus_expain_button = QtWidgets.QPushButton()
        self.cosinus_expain_button.setObjectName("Cosinus Erklärung")
        self.cosinus_expain_button.setText(self._translate("MainWindow", "Cosinus Erklärung"))
        self.horizontalLayout_main.addWidget(self.cosinus_expain_button, 2, 2, 1, 1)
        self.cosinus_expain_button.clicked.connect(self.cosinus_explain)

        # Tangens erklärung
        self.tan_expain_button = QtWidgets.QPushButton()
        self.tan_expain_button.setObjectName("Tangens Erklärung")
        self.tan_expain_button.setText(self._translate("MainWindow", "Tangens Erklärung"))
        self.horizontalLayout_main.addWidget(self.tan_expain_button, 3, 2, 1, 1)
        self.tan_expain_button.clicked.connect(self.tan_explain)

        # The initialization of the new canvas
        self.canvas.triangle_explain_main()
        # addWidget(*Widget, row, column, rowspan, colspan)
        self.horizontalLayout_main.addWidget(self.canvas.triangle_canvas_explain_main, 0, 2, 1, 1)

        self.text.clear()
        self.text.append(text.explain)
        self.canvas.triangle_canvas_explain_sinus = None
        self.canvas.triangle_canvas_explain_cosinus = None
        self.canvas.triangle_canvas_explain_tan = None

    def sinus_explain(self):
        self.text.clear()
        self.text.append(text.sinus_explain)
        self.remove_explain_canvases()
        self.canvas.triangle_explain_sinus()
        self.horizontalLayout_main.addWidget(self.canvas.triangle_canvas_explain_sinus, 0, 2, 1, 1)

    def cosinus_explain(self):
        self.text.clear()
        self.text.append(text.cosinus_explain)
        self.remove_explain_canvases()
        self.canvas.triangle_explain_cosinus()
        self.horizontalLayout_main.addWidget(self.canvas.triangle_canvas_explain_cosinus, 0, 2, 1, 1)

    def tan_explain(self):
        self.text.clear()
        self.text.append(text.tan_explain)
        self.remove_explain_canvases()
        self.canvas.triangle_explain_tan()
        self.horizontalLayout_main.addWidget(self.canvas.triangle_canvas_explain_tan, 0, 2, 1, 1)

    def remove_explain_canvases(self):

        if self.canvas.triangle_canvas_explain_main != None:
            self.horizontalLayout_main.removeWidget(self.canvas.triangle_canvas_explain_main)
            self.canvas.triangle_canvas_explain_main.deleteLater()
            self.canvas.triangle_canvas_explain_main = None

        if self.canvas.triangle_canvas_explain_sinus != None:
            self.horizontalLayout_main.removeWidget(self.canvas.triangle_canvas_explain_sinus)
            self.canvas.triangle_canvas_explain_sinus.deleteLater()
            self.canvas.triangle_canvas_explain_sinus = None

        if self.canvas.triangle_canvas_explain_cosinus != None:
            self.horizontalLayout_main.removeWidget(self.canvas.triangle_canvas_explain_cosinus)
            self.canvas.triangle_canvas_explain_cosinus.deleteLater()
            self.canvas.triangle_canvas_explain_cosinus = None

        if self.canvas.triangle_canvas_explain_tan != None:
            self.horizontalLayout_main.removeWidget(self.canvas.triangle_canvas_explain_tan)
            self.canvas.triangle_canvas_explain_tan.deleteLater()
            self.canvas.triangle_canvas_explain_tan = None

    def sinus(self):
        '''
        description
        '''
        self.mouse_click_text = "Animierte Erklärseite"
        # Set the window title and the main label
        self.setWindowTitle(self._translate("MainWindow", "Sinus und Cosinus"))
        self.label.setText(self._translate("MainWindow", "Sinus und Cosinus"))
        self.text.setFixedWidth(500)
        self.text.setFixedHeight(380)

        #########################################################################################
        #                                Canvas(matplotlib)                                   #
        #########################################################################################  

        # remove old
        self.remove_canvas()

        # init new
        if self.ankathete == None:
            self.text_content = text.sinus
            self.text.append(self.text_content)
            self.canvas.graph(x_hypotenuse=[0, .7], y_hypotenuse=[0, .7], x_gegenkathete=[.7, .7],
                              y_gegenkathete=[.7, 0], x_ankathete=[0, .7], y_ankathete=[0, 0])
        else:
            self.canvas.graph(x_hypotenuse=[0, self.gegenkathete], y_hypotenuse=[0, self.ankathete],
                              x_gegenkathete=[self.gegenkathete, self.gegenkathete], y_gegenkathete=[self.ankathete, 0],
                              x_ankathete=[0, self.gegenkathete], y_ankathete=[0, 0], arc=self.degrie)

            # addWidget(*Widget, row, column, rowspan, colspan)
        self.horizontalLayout_main.addWidget(self.canvas.dynamic_canvas, 0, 2, 4, 2)

        self.text.clear()
        self.text.append(self.text_content)

        # init input
        self.grad = QLineEdit()
        self.grad.setFixedWidth(90)
        self.grad.setAlignment(Qt.AlignRight)
        self.grad.setValidator(QIntValidator())
        self.grad.setFont(QFont("Arial", 20))
        # addWidget(*Widget, row, column, rowspan, colspan)
        self.horizontalLayout_main.addWidget(self.grad, 0, 4, 1, 1)

        self.label_grad = QLabel(self)
        self.label_grad.setText("<b>° Grad</b>")
        self.label_grad.setFont(QFont("Arial", 20))
        self.label_grad.setAlignment(Qt.AlignRight)
        self.label_grad.setBuddy(self.grad)

        self.horizontalLayout_main.addWidget(self.label_grad, 1, 4, 1, 1)

        self.grad.returnPressed.connect(self.update_text)
        # self.grad.textChanged.connect(self.update_text)    

        # change the frame_content into "1"
        self.frame_content = 1

    def rechtwinkliges_dreieck(self):
        '''
        Set the window title and the main label
        Run Matplotlib Canvas
        '''
        self.mouse_click_text = "der rechtwinkligen Dreieck Erklärseite"
        self.setWindowTitle(self._translate("MainWindow", "rechtwinkliges Dreieck"))
        self.label.setText(self._translate("MainWindow", "rechtwinkliges Dreieck"))
        self.text.setFixedWidth(550)
        self.text.setFixedHeight(380)
        # check if we are one the same Canvas
        if self.frame_content != 2:
            # delete the old canvas
            self.remove_canvas()
            # The initialization of the new canvas
            self.canvas.triangle()
            # add the new canvas
            # addWidget(*Widget, row, column, rowspan, colspan)
            self.horizontalLayout_main.addWidget(self.canvas.triangle_canvas, 0, 1, 1, 1)

            self.text.clear()
            self.text.append(text.rechtwinkliges_dreieck)

        # The initialization or changing of variable into "2"
        self.frame_content = 2

    def animation_sinus(self):
        '''
        description
        '''
        self.mouse_click_text = "der Sinus Animationsseite"
        # Set the window title and the main label
        self.setWindowTitle(self._translate("MainWindow", "Animation Sinus"))
        self.label.setText(self._translate("MainWindow", "Animation"))
        # text Feld width 200
        self.text.setFixedWidth(2)
        self.text.setFixedHeight(1)
        #########################################################################################
        #                                Canvas(matplotlib)                                   #
        ######################################################################################### 
        # remove old
        self.remove_canvas()

        self.text_content = """ """
        self.text.clear()
        self.text.append(self.text_content)

        # canvas
        self.animation_m = MplCanvas(self, width=5, height=5, dpi=80)
        self.horizontalLayout_main.addWidget(self.animation_m, 0, 0, 2, 4)

        self.xdata = np.arange(0, 6.4, 0.1)
        self.update_canvas()
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_canvas)
        self.timer.start()

        self.frame_content = 3

    def update_canvas(self):
        # Drop off the first y element, append a new one.
        if len(self.xdata) == 1:
            self.xdata = np.arange(start=0, stop=6.4, step=0.1)

        self.xdata = self.xdata[1:]

        if self.animation_m != None:
            self.animation_m.axes.cla()  # Clear the canvas.

            self.animation_m.axes.plot([0, np.cos(self.xdata[0])], [0, np.sin(self.xdata[0])], 'o-r', alpha=0.7, lw=5,
                                       mec='b', mew=2, ms=10)

            self.animation_m.axes.plot([self.xdata[0] + 1, np.cos(self.xdata[0])],
                                       [np.sin(self.xdata[0]), np.sin(self.xdata[0])],
                                       'o-g', alpha=0.7, lw=2, mew=1, ms=5)

            self.animation_m.axes.plot(self.xdata + 1, np.sin(self.xdata), 'r', alpha=0.7, lw=5, mec='b', mew=2, ms=10)

            self.animation_m.axes.set_ylim([-1, 1])
            self.animation_m.axes.set_xlim([-1, 7.3])
            self.animation_m.axes.set_title("Sinus")

            circle1 = plt.Circle((0, 0), 1, color='r', fill=False, alpha=0.7)
            self.animation_m.axes.add_patch(circle1)
            self.animation_m.axes.set_aspect('equal', 'box')

            arc_draw = plt_arc.Wedge(center=0, r=1, theta1=0, theta2=self.xdata[0] * 57, width=0.7, fill=True,
                                     color='orange', edgecolor="green", alpha=0.5)
            self.animation_m.axes.add_patch(arc_draw)

            # Устанавливаем интервал основных и вспомогательных делений:
            # steps major ticks and minor ticks
            self.animation_m.axes.xaxis.set_major_locator(ticker.MultipleLocator(1))
            self.animation_m.axes.xaxis.set_minor_locator(ticker.MultipleLocator(.1))
            self.animation_m.axes.yaxis.set_major_locator(ticker.MultipleLocator(1))
            self.animation_m.axes.yaxis.set_minor_locator(ticker.MultipleLocator(.1))

            self.animation_m.axes.set_xticks((-1, 0, 1, 2, 3, 4, 5, 6, 7))
            self.animation_m.axes.set_xticklabels(("-1", "0", "1 / 0", "1", "2", "3", "4", "5", "6"))

            self.animation_m.axes.set_yticks((-1, 0, 1))
            self.animation_m.axes.set_yticklabels(("-1", "0", "1"))

            self.animation_m.axes.tick_params(axis='both',  # Применяем параметры к обеим осям
                                              which='major',  # Применяем параметры к основным делениям
                                              direction='inout',  # Рисуем деления внутри и снаружи графика
                                              length=20,  # Длинна делений
                                              width=5,  # Ширина делений
                                              color='b',  # Цвет делений
                                              pad=10,  # Расстояние между черточкой и ее подписью
                                              labelsize=15,  # Размер подписи
                                              labelcolor='b',  # Цвет подписи
                                              bottom=True,  # Рисуем метки снизу
                                              top=True,  # сверху
                                              left=True,  # слева
                                              right=True,  # и справа
                                              labelbottom=True,  # Рисуем подписи снизу
                                              labeltop=True,  # сверху
                                              labelleft=True,  # слева
                                              labelright=True,  # и справа
                                              labelrotation=45)  # Поворот подписей

            self.animation_m.axes.tick_params(axis='both',  # Применяем параметры к обеим осям
                                              which='minor',  # Применяем параметры к вспомогательным делениям
                                              direction='out',  # Рисуем деления внутри и снаружи графика
                                              length=10,  # Длинна делений
                                              width=2,  # Ширина делений
                                              color='b',  # Цвет делений
                                              pad=10,  # Расстояние между черточкой и ее подписью
                                              labelsize=15,  # Размер подписи
                                              labelcolor='r',  # Цвет подписи
                                              bottom=True,  # Рисуем метки снизу
                                              top=True,  # сверху
                                              left=True,  # слева
                                              right=True)  # и справа

            #  Добавляем линии основной сетки:
            self.animation_m.axes.grid(axis='both', which='major', color='b')
            #  Включаем видимость вспомогательных делений:
            self.animation_m.axes.minorticks_on()
            #  Теперь можем отдельно задавать внешний вид вспомогательной сетки:
            self.animation_m.axes.grid(axis='both', which='minor', color='m', linestyle=':')

            # Trigger the canvas to update and redraw.
            self.animation_m.draw()

    def update_text(self):
        self.text_content = self.grad.text()
        self.text.clear()

        if self.text_content == '':
            self.degrie = 0
        else:
            self.degrie = int(self.text_content)  # with validator is always int. No need to proof it.
        self.counting()
        self.text_content = f"<div style='font-size: 22px'>\
                    <div style='text-align: right; margin-bottom: 20px;'>Sie haben {self.text_content}° angegeben.</div>\
                    <div style='text-align: right; color:green; margin-bottom: 20px;'>Sinus bzw die Länge von Gegenkathete von {self.degrie}° <br>= sin({self.degrie}) x radius <br>= {round(self.ankathete, 2)}</div>\
                    <div style='text-align: right; color:blue; margin-bottom: 20px;'>Cosinus bzw die Länge von Ankathete von {self.degrie}° <br>= cos({self.degrie}) x radius <br>= {round(self.gegenkathete, 2)}</div>\
                    <div style='text-align: right; color:red; margin-bottom: 20px;'>Die Hypotenuse ist der Radius = 1 </div>\
                            </div>"

        self.text.append(self.text_content)
        if self.frame_content == 1:
            self.sinus()

    def counting(self, r=1):
        self.ankathete = math.sin(math.radians(self.degrie))
        self.gegenkathete = math.cos(math.radians(self.degrie))

    def remove_canvas(self):
        """
        it will be removed, wenn we change fields
        """
        # It removes dynamic_canvas and input from Sinus field
        if self.frame_content == 1:
            self.horizontalLayout_main.removeWidget(self.canvas.dynamic_canvas)
            self.canvas.dynamic_canvas.deleteLater()
            self.canvas.dynamic_canvas = None

            self.horizontalLayout_main.removeWidget(self.grad)
            self.grad.deleteLater()
            self.grad = None

            self.horizontalLayout_main.removeWidget(self.label_grad)
            self.label_grad.deleteLater()
            self.label_grad = None

        # remove triangle_canvas from rechtwinkligen Dreieck field
        elif self.frame_content == 2:
            self.horizontalLayout_main.removeWidget(self.canvas.triangle_canvas)
            self.canvas.triangle_canvas.deleteLater()
            self.canvas.triangle_canvas = None

        # remove animation_m from Sinus Animation field
        elif self.frame_content == 3:
            self.horizontalLayout_main.removeWidget(self.animation_m)
            self.animation_m.deleteLater()
            self.animation_m = None

            # remove buttons from explain field
        elif self.frame_content == 4:

            # remove Button sinus_expain 
            self.horizontalLayout_main.removeWidget(self.sinus_expain_button)
            self.sinus_expain_button.deleteLater()
            self.sinus_expain_button = None

            # remove button cosinus_expain
            self.horizontalLayout_main.removeWidget(self.cosinus_expain_button)
            self.cosinus_expain_button.deleteLater()
            self.cosinus_expain_button = None

            # remove button tan_explain
            self.horizontalLayout_main.removeWidget(self.tan_expain_button)
            self.tan_expain_button.deleteLater()
            self.tan_expain_button = None

            # remove canvases
            self.remove_explain_canvases()

    def menu(self):
        '''
        description
        '''
        width = self.leftS.width()
        if width == 0:
            newWidth = 200
            self.menuButton.setIcon(QIcon(u"model/pictures/del.png"))
        else:
            newWidth = 0
            self.menuButton.setIcon(QIcon(u"model/pictures/menu.png"))

        self.animation = QPropertyAnimation(self.leftS, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.start()

    def back_button(self):
        '''
        back to main menu
        '''
        self.window = mainMenu.MainMenu()
        self.window.show()
        self.close()


def main():
    # Check whether there is already a running QApplication
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()


if __name__ == "__main__":
    main()
