# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_LeastSquares.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(954, 693)
        self.group_input = QtWidgets.QGroupBox(Dialog)
        self.group_input.setGeometry(QtCore.QRect(20, 10, 681, 151))
        self.group_input.setObjectName("group_input")
        self.pushButton_calculate = QtWidgets.QPushButton(self.group_input)
        self.pushButton_calculate.setGeometry(QtCore.QRect(230, 110, 141, 28))
        self.pushButton_calculate.setObjectName("pushButton_calculate")
        self.radioButton_linear = QtWidgets.QRadioButton(self.group_input)
        self.radioButton_linear.setGeometry(QtCore.QRect(30, 80, 95, 20))
        self.radioButton_linear.setObjectName("radioButton_linear")
        self.radioButton_quadratic = QtWidgets.QRadioButton(self.group_input)
        self.radioButton_quadratic.setGeometry(QtCore.QRect(200, 80, 111, 20))
        self.radioButton_quadratic.setObjectName("radioButton_quadratic")
        self.radioButton_cubic = QtWidgets.QRadioButton(self.group_input)
        self.radioButton_cubic.setGeometry(QtCore.QRect(380, 80, 95, 20))
        self.radioButton_cubic.setObjectName("radioButton_cubic")
        self.radioButton_exponential = QtWidgets.QRadioButton(self.group_input)
        self.radioButton_exponential.setGeometry(QtCore.QRect(550, 80, 111, 20))
        self.radioButton_exponential.setObjectName("radioButton_exponential")
        self.lineEdit_filename = QtWidgets.QLineEdit(self.group_input)
        self.lineEdit_filename.setGeometry(QtCore.QRect(90, 40, 541, 22))
        self.lineEdit_filename.setObjectName("lineEdit_filename")
        self.label = QtWidgets.QLabel(self.group_input)
        self.label.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label.setObjectName("label")
        self.group_output = QtWidgets.QGroupBox(Dialog)
        self.group_output.setGeometry(QtCore.QRect(20, 170, 911, 511))
        self.group_output.setObjectName("group_output")
        self.lineEdit_equation = QtWidgets.QLineEdit(self.group_output)
        self.lineEdit_equation.setGeometry(QtCore.QRect(90, 30, 811, 22))
        self.lineEdit_equation.setObjectName("lineEdit_equation")
        self.label_2 = QtWidgets.QLabel(self.group_output)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 55, 16))
        self.label_2.setObjectName("label_2")
        self.graphicsView_plot = QtWidgets.QGraphicsView(self.group_output)
        self.graphicsView_plot.setGeometry(QtCore.QRect(10, 60, 891, 441))
        self.graphicsView_plot.setObjectName("graphicsView_plot")
        self.pushButton_exit = QtWidgets.QPushButton(Dialog)
        self.pushButton_exit.setGeometry(QtCore.QRect(780, 120, 93, 28))
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.group_input.setTitle(_translate("Dialog", "Input"))
        self.pushButton_calculate.setText(_translate("Dialog", "Load and Calculate"))
        self.radioButton_linear.setText(_translate("Dialog", "Linear Fit"))
        self.radioButton_quadratic.setText(_translate("Dialog", "Quadratic Fit"))
        self.radioButton_cubic.setText(_translate("Dialog", "Cubic Fit"))
        self.radioButton_exponential.setText(_translate("Dialog", "Exponential Fit"))
        self.label.setText(_translate("Dialog", "Filename:"))
        self.group_output.setTitle(_translate("Dialog", "Output"))
        self.label_2.setText(_translate("Dialog", "Equation"))
        self.pushButton_exit.setText(_translate("Dialog", "Exit"))

