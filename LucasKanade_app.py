import os
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from Lucas_Kanade import izberiDatoteko, izracunPomikov
from matplotlib.patches import Rectangle
import scipy.signal
import numpy as np
from scipy.fft import fft

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #levi del
        self.leviGlavniLayout = QtWidgets.QVBoxLayout()
        self.leviGlavniLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.leviGlavniLayout.setObjectName("leviGlavniLayout")

        self.figure = plt.Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.figure.clear()

        self.NavigatorWidget = NavigationToolbar(self.canvas, self.centralwidget)
        self.NavigatorWidget.setObjectName("NavigatorWidget")
        self.leviGlavniLayout.addWidget(self.NavigatorWidget)

        self.RefSlikaWidget = self.canvas
        self.RefSlikaWidget.setObjectName("RefSlikaWidget")
        self.leviGlavniLayout.addWidget(self.RefSlikaWidget)
        self.horizontalLayout.addLayout(self.leviGlavniLayout)

        #desni del
        self.desniGlavniLayout = QtWidgets.QVBoxLayout()
        self.desniGlavniLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.desniGlavniLayout.setContentsMargins(0, -1, 0, -1)
        self.desniGlavniLayout.setObjectName("desniGlavniLayout")

            #izberi datoteko
        self.izberiDatotekoLayout = QtWidgets.QVBoxLayout()
        self.izberiDatotekoLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.izberiDatotekoLayout.setObjectName("izberiDatotekoLayout")
        self.izberiDatotekoButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.izberiDatotekoButton.sizePolicy().hasHeightForWidth())
        self.izberiDatotekoButton.setSizePolicy(sizePolicy)
        self.izberiDatotekoButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.izberiDatotekoButton.setBaseSize(QtCore.QSize(0, 0))
        self.izberiDatotekoButton.setObjectName("izberiDatotekoButton")
        self.izberiDatotekoButton.clicked.connect(self.odpri_datoteko)
        self.izberiDatotekoLayout.addWidget(self.izberiDatotekoButton)
        self.izbranaDatotekaLine = QtWidgets.QLineEdit(self.centralwidget)
        self.izbranaDatotekaLine.setMaximumSize(QtCore.QSize(400, 16777215))
        self.izbranaDatotekaLine.setReadOnly(True)
        self.izbranaDatotekaLine.setObjectName("izbranaDatotekaLine")
        self.izberiDatotekoLayout.addWidget(self.izbranaDatotekaLine)
        self.desniGlavniLayout.addLayout(self.izberiDatotekoLayout)



            #parametri
        self.ParametriBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ParametriBox.sizePolicy().hasHeightForWidth())
        self.ParametriBox.setSizePolicy(sizePolicy)
        self.ParametriBox.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ParametriBox.setFont(font)
        self.ParametriBox.setObjectName("ParametriBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.ParametriBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.parametriLayout = QtWidgets.QVBoxLayout()
        self.parametriLayout.setObjectName("parametriLayout")

                #tocka
        self.TockaBox = QtWidgets.QGroupBox(self.ParametriBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TockaBox.sizePolicy().hasHeightForWidth())
        self.TockaBox.setSizePolicy(sizePolicy)
        self.TockaBox.setBaseSize(QtCore.QSize(0, 0))
        self.TockaBox.setObjectName("TockaBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.TockaBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.xLabel = QtWidgets.QLabel(self.TockaBox)
        self.xLabel.setObjectName("xLabel")
        self.horizontalLayout_4.addWidget(self.xLabel)
        self.xLine = QtWidgets.QLineEdit(self.TockaBox)
        self.xLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.xLine.setObjectName("xLine")
        self.horizontalLayout_4.addWidget(self.xLine)
        spacerItem = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.yLabel = QtWidgets.QLabel(self.TockaBox)
        self.yLabel.setObjectName("yLabel")
        self.horizontalLayout_4.addWidget(self.yLabel)
        self.yLine = QtWidgets.QLineEdit(self.TockaBox)
        self.yLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.yLine.setObjectName("yLine")
        self.horizontalLayout_4.addWidget(self.yLine)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.parametriLayout.addWidget(self.TockaBox)

                #ROI
        self.ROIBox = QtWidgets.QGroupBox(self.ParametriBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ROIBox.sizePolicy().hasHeightForWidth())
        self.ROIBox.setSizePolicy(sizePolicy)
        self.ROIBox.setObjectName("ROIBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ROIBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.wLabel = QtWidgets.QLabel(self.ROIBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wLabel.sizePolicy().hasHeightForWidth())
        self.wLabel.setSizePolicy(sizePolicy)
        self.wLabel.setObjectName("wLabel")
        self.horizontalLayout_3.addWidget(self.wLabel)
        self.wLine = QtWidgets.QLineEdit(self.ROIBox)
        self.wLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.wLine.setObjectName("wLine")
        self.horizontalLayout_3.addWidget(self.wLine)
        spacerItem2 = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.hLabel = QtWidgets.QLabel(self.ROIBox)
        self.hLabel.setObjectName("hLabel")
        self.horizontalLayout_3.addWidget(self.hLabel)
        self.hLine = QtWidgets.QLineEdit(self.ROIBox)
        self.hLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.hLine.setObjectName("hLine")
        self.horizontalLayout_3.addWidget(self.hLine)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.TockaBox.raise_()
        self.wLabel.raise_()
        self.hLabel.raise_()
        self.hLine.raise_()
        self.wLine.raise_()
        self.parametriLayout.addWidget(self.ROIBox)

                #merilo
        self.MeriloBox = QtWidgets.QGroupBox(self.ParametriBox)
        self.MeriloBox.setObjectName("MeriloBox")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.MeriloBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.meriloLine = QtWidgets.QLineEdit(self.MeriloBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meriloLine.sizePolicy().hasHeightForWidth())
        self.meriloLine.setSizePolicy(sizePolicy)
        self.meriloLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.meriloLine.setBaseSize(QtCore.QSize(0, 0))
        self.meriloLine.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.meriloLine.setText("")
        self.meriloLine.setObjectName("meriloLine")
        self.horizontalLayout_5.addWidget(self.meriloLine)
        self.pxLabel = QtWidgets.QLabel(self.MeriloBox)
        self.pxLabel.setObjectName("pxLabel")
        self.horizontalLayout_5.addWidget(self.pxLabel)
        self.mmLine = QtWidgets.QLineEdit(self.MeriloBox)
        self.mmLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.mmLine.setText("")
        self.mmLine.setObjectName("mmLine")
        self.horizontalLayout_5.addWidget(self.mmLine)
        self.mmLabel = QtWidgets.QLabel(self.MeriloBox)
        self.mmLabel.setObjectName("mmLabel")
        self.horizontalLayout_5.addWidget(self.mmLabel)
        spacerItem4 = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.ROIBox.raise_()
        self.meriloLine.raise_()
        self.pxLabel.raise_()
        self.mmLine.raise_()
        self.mmLabel.raise_()
        self.parametriLayout.addWidget(self.MeriloBox)


        self.st_interpLayout = QtWidgets.QHBoxLayout()
        self.st_interpLayout.setObjectName("st_interpLayout")
        self.st_interpLabel = QtWidgets.QLabel(self.ParametriBox)
        self.st_interpLabel.setObjectName("st_interpLabel")
        self.st_interpLayout.addWidget(self.st_interpLabel)
        self.st_interpLine = QtWidgets.QLineEdit(self.ParametriBox)
        self.st_interpLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.st_interpLine.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.st_interpLine.setObjectName("st_interpLine")
        self.st_interpLine.setValidator(QtGui.QIntValidator(bottom=1, top=5))
        self.st_interpLayout.addWidget(self.st_interpLine)
        spacerItem5 = QtWidgets.QSpacerItem(128, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.st_interpLayout.addItem(spacerItem5)
        self.parametriLayout.addLayout(self.st_interpLayout)
        self.maxiterLayout = QtWidgets.QHBoxLayout()
        self.maxiterLayout.setObjectName("maxiterLayout")
        self.maxiterLabel = QtWidgets.QLabel(self.ParametriBox)
        self.maxiterLabel.setObjectName("maxiterLabel")
        self.onlyInt_maxiter = QtGui.QIntValidator()
        self.st_interpLine.setValidator(self.onlyInt_maxiter)
        self.maxiterLayout.addWidget(self.maxiterLabel)
        self.maxiterLine = QtWidgets.QLineEdit(self.ParametriBox)
        self.maxiterLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.maxiterLine.setInputMask("")
        self.maxiterLine.setText("")
        self.maxiterLine.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.maxiterLine.setPlaceholderText("")
        self.maxiterLine.setObjectName("maxiterLine")
        self.maxiterLayout.addWidget(self.maxiterLine)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.maxiterLayout.addItem(spacerItem6)
        self.parametriLayout.addLayout(self.maxiterLayout)
        self.tolerancaLayout = QtWidgets.QHBoxLayout()
        self.tolerancaLayout.setObjectName("tolerancaLayout")
        self.tolerancaLabel = QtWidgets.QLabel(self.ParametriBox)
        self.tolerancaLabel.setObjectName("tolerancaLabel")
        self.tolerancaLayout.addWidget(self.tolerancaLabel)
        self.tolerancaLine = QtWidgets.QLineEdit(self.ParametriBox)
        self.tolerancaLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.tolerancaLine.setText("")
        self.tolerancaLine.setObjectName("tolerancaLine")
        self.tolerancaLayout.addWidget(self.tolerancaLine)
        spacerItem7 = QtWidgets.QSpacerItem(128, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.tolerancaLayout.addItem(spacerItem7)
        self.parametriLayout.addLayout(self.tolerancaLayout)

                #preveri parametre
        self.preveriParametreButton = QtWidgets.QPushButton(self.ParametriBox)
        self.preveriParametreButton.setEnabled(False)
        self.preveriParametreButton.setObjectName("preveriParametreButton")
        self.preveriParametreButton.clicked.connect(self.preveri_parametre)
        self.parametriLayout.addWidget(self.preveriParametreButton)
        self.horizontalLayout_2.addLayout(self.parametriLayout)
        self.desniGlavniLayout.addWidget(self.ParametriBox)

            #izracunaj pomike
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem8 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem8)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_6.addWidget(self.checkBox)
        self.desniGlavniLayout.addLayout(self.horizontalLayout_6)

        self.izracunajPomikeButton = QtWidgets.QPushButton(self.centralwidget)
        self.izracunajPomikeButton.setEnabled(False)
        self.izracunajPomikeButton.setMaximumSize(QtCore.QSize(400, 16777215))
        self.izracunajPomikeButton.setObjectName("izracunajPomikeButton")
        self.izracunajPomikeButton.clicked.connect(self.izracunaj_pomike)
        self.desniGlavniLayout.addWidget(self.izracunajPomikeButton)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.desniGlavniLayout.addWidget(self.line_2)

            #izvedi frekvencno analiuo
        self.izvediFrekAnalizoButton = QtWidgets.QPushButton(self.centralwidget)
        self.izvediFrekAnalizoButton.setEnabled(False)
        self.izvediFrekAnalizoButton.setMaximumSize(QtCore.QSize(400, 16777215))
        self.izvediFrekAnalizoButton.setObjectName("izvediFrekAnalizoButton")
        self.desniGlavniLayout.addWidget(self.izvediFrekAnalizoButton)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.desniGlavniLayout.addWidget(self.line_3)
        self.izvediFrekAnalizoButton.clicked.connect(self.fourierjevaTrans)

            #shrani pomike
        self.shraniPomikeButton = QtWidgets.QPushButton(self.centralwidget)
        self.shraniPomikeButton.setEnabled(False)
        self.shraniPomikeButton.setMaximumSize(QtCore.QSize(400, 16777215))
        self.shraniPomikeButton.setObjectName("shraniPomikeButton")
        self.desniGlavniLayout.addWidget(self.shraniPomikeButton)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.desniGlavniLayout.addWidget(self.line_4)
        self.shraniPomikeButton.clicked.connect(self.shrani)

            #progressBar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setMaximumSize(QtCore.QSize(400, 16777215))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()
        self.desniGlavniLayout.addWidget(self.progressBar)

            #messageBox
        self.messageboxLabel = QtWidgets.QLabel(self.centralwidget)
        self.messageboxLabel.setMaximumSize(QtCore.QSize(400, 16777215))
        self.messageboxLabel.setAutoFillBackground(False)
        self.messageboxLabel.setInputMethodHints(QtCore.Qt.ImhNone)
        self.messageboxLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.messageboxLabel.setWordWrap(True)
        self.messageboxLabel.setObjectName("messageboxLabel")
        self.desniGlavniLayout.addWidget(self.messageboxLabel)
        self.horizontalLayout.addLayout(self.desniGlavniLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.izberiDatotekoButton.setText(_translate("MainWindow", "Izberi datoteko"))
        self.ParametriBox.setTitle(_translate("MainWindow", "Parametri"))
        self.TockaBox.setTitle(_translate("MainWindow", "Točka:"))
        self.xLabel.setText(_translate("MainWindow", "x:"))
        self.yLabel.setText(_translate("MainWindow", "y:"))
        self.ROIBox.setTitle(_translate("MainWindow", "Območje zanimanja:"))
        self.wLabel.setText(_translate("MainWindow", "w:"))
        self.hLabel.setText(_translate("MainWindow", "h:"))
        self.MeriloBox.setTitle(_translate("MainWindow", "Merilo"))
        self.pxLabel.setText(_translate("MainWindow", "px     =  "))
        self.mmLabel.setText(_translate("MainWindow", "mm"))
        self.st_interpLabel.setText(_translate("MainWindow", "Stopnja interpolacije:"))
        self.st_interpLine.setPlaceholderText(_translate('', '3'))
        self.maxiterLabel.setText(_translate("MainWindow", "Maksimalno število iteracij:"))
        self.maxiterLine.setPlaceholderText(_translate('', '25'))
        self.tolerancaLabel.setText(_translate("MainWindow", "Toleranca konvergence:"))
        self.tolerancaLine.setPlaceholderText(_translate('', '10e-8'))
        self.preveriParametreButton.setText(_translate("MainWindow", "Preveri parametre"))
        self.izracunajPomikeButton.setText(_translate("MainWindow", "Izračunaj pomike"))
        self.izvediFrekAnalizoButton.setText(_translate("MainWindow", "Izvedi frekvenčno analizo"))
        self.shraniPomikeButton.setText(_translate("MainWindow", "Shrani pomike"))
        self.messageboxLabel.setText(_translate("MainWindow", " "))
        self.checkBox.setText(_translate("MainWindow", "Premik na izhodišče"))

    def odpri_datoteko(self):
        dialog = QtWidgets.QFileDialog()
        self.datoteka = QtWidgets.QFileDialog.getOpenFileName(dialog, 'Odpri datoteko', filter=("cih (*.cih)"))
        if self.datoteka != ('', ''):
            self.izbranaDatotekaLine.setText(self.datoteka[0])
            self.video, self.FPS, self.shape = izberiDatoteko(self.datoteka[0])
            self.izrisRefSlike(self.video)
            self.xLine.setText("")
            self.yLine.setText("")
            self.wLine.setText("")
            self.hLine.setText("")
            self.meriloLine.setText("")
            self.mmLine.setText("")
            self.st_interpLine.setText("")
            self.maxiterLine.setText("")
            self.tolerancaLine.setText("")
            self.preveriParametreButton.setEnabled(True)
            self.t = np.linspace(0, self.shape[0] / self.FPS, self.shape[0])
        else:
            pass

    def izrisRefSlike(self, video):
        for i in reversed(range(self.leviGlavniLayout.count())):
            self.leviGlavniLayout.itemAt(i).widget().deleteLater()

        self.figure = plt.Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.figure.clear()

        self.refSlika = self.figure.add_subplot(111)
        self.refSlika.imshow(video[0], 'gray')
        self.refSlika.plot()
        self.canvas.draw()

        self.NavigatorWidget = NavigationToolbar(self.canvas, self.centralwidget)
        self.NavigatorWidget.setObjectName("NavigatorWidget")
        self.leviGlavniLayout.addWidget(self.NavigatorWidget)

        self.RefSlikaWidget = self.canvas
        self.RefSlikaWidget.setObjectName("RefSlikaWidget")
        self.leviGlavniLayout.addWidget(self.RefSlikaWidget)
        self.horizontalLayout.addLayout(self.leviGlavniLayout)

    def preveri_parametre(self):
        napake = []
        parametriOK = True
        shape = self.video.shape
        x = self.xLine.text()
        y = self.yLine.text()
        w = self.wLine.text()
        h = self.hLine.text()
        red = self.st_interpLine.text()

        if x == '':
            napake.append("Vpiši vrednost 'x'! \n")
            parametriOK = False
        else:
            self.x = int(x)
            if 0 < self.x < shape[2]:
                pass
            else:
                napake.append("Vrednost 'x' je izven obsega! \n")
                parametriOK = False

        if y == '':
            napake.append("Vpiši vrednost 'y'! \n")
            parametriOK = False
        else:
            self.y = int(y)
            if 0 < self.y < shape[1]:
                pass
            else:
                napake.append("Vrednost 'y' je izven obsega! \n")
                parametriOK = False

        if w == '':
            self.w = 15
        else:
            self.w = int(w)
            if self.w >= 9:
                pass
            else:
                napake.append("Vrednost 'w' naj bo večja od 9! \n")
                parametriOK = False

        if h == '':
            self.h = 15
        else:
            self.h = int(h)
            if self.h >= 9:
                pass
            else:
                napake.append("Vrednost 'h' naj bo večja od 9! \n")
                parametriOK = False

        if red == '':
            self.red = 3
        else:
            self.red = int(red)
            if self.red in range(1,6):
                pass
            else:
                napake.append("Stopnja interpolacije mora biti med 1 in 5. \n")
                parametriOK = False

        napake = ''.join(napake)
        self.messageboxLabel.setText(napake)

        if parametriOK == True:
            for i in reversed(range(self.leviGlavniLayout.count())):
                self.leviGlavniLayout.itemAt(i).widget().deleteLater()

            self.figure = plt.Figure()
            self.canvas = FigureCanvasQTAgg(self.figure)
            self.figure.clear()

            self.refSlika = self.figure.add_subplot(111)
            self.refSlika.imshow(self.video[0], 'gray')
            self.refSlika.plot()
            self.refSlika.scatter(self.x, self.y)
            rect = Rectangle((self.x - self.w / 2, self.y - self.h / 2), self.w, self.h, linewidth=2, edgecolor='r', facecolor='none')
            self.refSlika.add_patch(rect)
            self.refSlika.plot()
            self.canvas.draw()

            self.NavigatorWidget = NavigationToolbar(self.canvas, self.centralwidget)
            self.NavigatorWidget.setObjectName("NavigatorWidget")
            self.leviGlavniLayout.addWidget(self.NavigatorWidget)

            self.RefSlikaWidget = self.canvas
            self.RefSlikaWidget.setObjectName("RefSlikaWidget")
            self.leviGlavniLayout.addWidget(self.RefSlikaWidget)
            self.horizontalLayout.addLayout(self.leviGlavniLayout)

            self.izracunajPomikeButton.setEnabled(True)

    def izracunaj_pomike(self):
        px = self.meriloLine.text()
        if px == '':
            self.px = 1.
        else:
            self.px = float(px)

        mm = self.mmLine.text()
        if mm == '':
            self.mm = 1.
        else:
            self.mm = float(mm)

        maxiter = self.maxiterLine.text()
        if maxiter == '':
            self.maxiter = 25
        else:
            self.maxiter = int(maxiter)

        tol = self.tolerancaLine.text()
        if tol == '':
            self.tol = 10e-8
        else:
            self.tol = float(tol)

        self.progressBar.show()
        self.data, self.napaka = izracunPomikov(self.video,
                                   tocka=[self.x, self.y],
                                   ROI=(self.w, self.h),
                                   stopnjaInterp=self.red,
                                   maxiter=self.maxiter,
                                   tol=self.tol,
                                   piksli=self.px,
                                   dolzina=self.mm,
                                   progressBar=self.progressBar,
                                   messageBox=self.messageboxLabel)
        for i in reversed(range(self.leviGlavniLayout.count())):
            self.leviGlavniLayout.itemAt(i).widget().deleteLater()

        if self.napaka == True:
            self.messageboxLabel.setText(f'Med izračunom je prišlo do napake. Spremeni parametre!!')

        if self.checkBox.isChecked() == True:
            self.data = self.premik()
        else:
            pass

        self.plot_data_x(self.data)
        self.plot_data_y(self.data)
        self.izvediFrekAnalizoButton.setEnabled(True)
        self.shraniPomikeButton.setEnabled(True)

    def premik(self):
        if self.napaka == True:
            self.messageboxLabel.setText(
                f'Med izračunom je prišlo do napake. Spremeni parametre!! \nPremik ni bil izveden!')
            self.data = self.data
            return self.data
        else:
            for i in range(2):
                data = self.data[:, i]
                if data[1] < data[0]:
                    peaks = scipy.signal.argrelmin(data)[0]
                else:
                    peaks = scipy.signal.find_peaks(data)[0]

                povprecje = np.average(data[peaks[1]:peaks[-1]])
                self.data[:, i] = self.data[:, i] - povprecje
            return self.data

    def plot_data_x(self, data):
        self.Xfigure = plt.Figure()
        self.Xfigure.clear()
        self.Xcanvas = FigureCanvasQTAgg(self.Xfigure)

        self.XNavigatorWidget = NavigationToolbar(self.Xcanvas, self.centralwidget)
        self.XNavigatorWidget.setObjectName("NavigatorWidget")
        self.leviGlavniLayout.addWidget(self.XNavigatorWidget)
        ax = self.Xfigure.add_subplot(111)
        ax.plot(self.t, data[:, 0].T)
        ax.set_title("Pomiki v smeri x")
        ax.set_ylabel("amplituda [mm]")
        ax.set_xlabel("t [s]")
        ax.grid()
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        self.Xfigure.set_tight_layout(True)
        self.XgrafWidget = self.Xcanvas
        self.XgrafWidget.setObjectName("XgrafWidget")
        self.leviGlavniLayout.addWidget(self.XgrafWidget)

    def plot_data_y(self, data):
        self.Yfigure = plt.Figure()
        self.Yfigure.clear()
        self.Ycanvas = FigureCanvasQTAgg(self.Yfigure)

        self.YNavigatorWidget = NavigationToolbar(self.Ycanvas, self.centralwidget)
        self.YNavigatorWidget.setObjectName("YNavigatorWidget")
        self.leviGlavniLayout.addWidget(self.YNavigatorWidget)
        ay = self.Yfigure.add_subplot(111)
        ay.plot(self.t, data[:, 1].T)
        ay.set_title("Pomiki v smeri y")
        ay.set_ylabel("amplituda [mm]")
        ay.set_xlabel("t [s]")
        ay.grid()
        ay.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        self.Yfigure.set_tight_layout(True)
        self.YgrafWidget = self.Ycanvas
        self.YgrafWidget.setObjectName("YgrafWidget")
        self.leviGlavniLayout.addWidget(self.YgrafWidget)

    def fourierjevaTrans(self):
        N = self.video.shape[0]
        FPS = float(self.FPS)
        T = 1/FPS
        t = np.linspace(0.0, N*T, N)

        x = self.data[:, 0]
        Amp_x = fft(x)
        freq_x = np.linspace(0.0, 1.0/(2.0*T), N//2)

        y = self.data[:, 1]
        Amp_y = fft(y)
        freq_y = np.linspace(0.0, 1.0/(2.0*T), N//2)


        for i in reversed(range(self.leviGlavniLayout.count())):
            self.leviGlavniLayout.itemAt(i).widget().deleteLater()

        self.Xfigure = plt.Figure()
        self.Xfigure.clear()
        self.Xcanvas = FigureCanvasQTAgg(self.Xfigure)

        self.XNavigatorWidget = NavigationToolbar(self.Xcanvas, self.centralwidget)
        self.XNavigatorWidget.setObjectName("NavigatorWidget")
        self.leviGlavniLayout.addWidget(self.XNavigatorWidget)
        freqAnalizax = self.Xfigure.add_subplot(111)
        freqAnalizax.plot(freq_x, 2.0/N * np.abs(Amp_x[0:N//2]))
        freqAnalizax.set_title("Frekvenčni spekter v smeri x")
        freqAnalizax.set_ylabel("amplituda [mm]")
        freqAnalizax.set_xlabel("frekvenca [Hz]")
        freqAnalizax.set_xlim(0, 25)
        freqAnalizax.grid()
        self.Xfigure.set_tight_layout(True)
        self.XgrafWidget = self.Xcanvas
        self.XgrafWidget.setObjectName("XgrafWidget")
        self.leviGlavniLayout.addWidget(self.XgrafWidget)
        self.Xfigure = plt.Figure()
        self.Xfigure.clear()
        self.Xcanvas = FigureCanvasQTAgg(self.Xfigure)

        self.Yfigure = plt.Figure()
        self.Yfigure.clear()
        self.Ycanvas = FigureCanvasQTAgg(self.Yfigure)

        self.YNavigatorWidget = NavigationToolbar(self.Ycanvas, self.centralwidget)
        self.YNavigatorWidget.setObjectName("YNavigatorWidget")
        self.leviGlavniLayout.addWidget(self.YNavigatorWidget)
        freqAnalizay = self.Yfigure.add_subplot(111)
        freqAnalizay.plot(freq_y, 2.0/N * np.abs(Amp_y[0:N//2]))
        freqAnalizay.set_title("Frekvenčni spekter v smeri y")
        freqAnalizay.set_ylabel("amplituda [mm]")
        freqAnalizay.set_xlabel("frekvenca [Hz]")
        freqAnalizay.set_xlim(0, 25)
        freqAnalizay.grid()
        self.Yfigure.set_tight_layout(True)
        self.YgrafWidget = self.Ycanvas
        self.YgrafWidget.setObjectName("YgrafWidget")
        self.leviGlavniLayout.addWidget(self.YgrafWidget)


    def shrani(self):
        root_ext = os.path.splitext(self.datoteka[0])
        koren = root_ext[0]
        txt = koren + f'_x{self.x}_y{self.y}.txt'
        with open(txt, 'w', newline='') as txt:
            glava_tabele = ['x', 'y']
            zapis = csv.DictWriter(txt, delimiter= ' ', fieldnames=glava_tabele)
            zapis.writeheader()
            for line in self.data:
                zapis.writerow(dict(zip(glava_tabele, line)))
        self.messageboxLabel.setText("Podatki so uspešno shranjeni.")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

