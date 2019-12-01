import numpy as np

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

# standard OpenGL imports
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PipeDrawingClass import gl2D, gl2DText, gl2DCircle

from Final_Gui import Ui_Dialog
from Pipe_Class import Pipe

class main_window(QDialog):                     # Main Window standard stuff
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.assign_widgets()
        self.setupGLWindows()

        self.Pipe = Pipe()                      # Declare variables
        self.selected = "Q"
        self.show()
        self.flowrate = 0.0
        self.pressure = 0.0
        #self.filename = 'None'


    def assign_widgets(self):               # Widgets
        self.ui.pushButton_exit.clicked.connect(self.ExitApp)
        self.ui.pushButton_GetFlowSystemFile.clicked.connect(self.GetPipe)
        self.ui.pushButton_AnalyzeFlow.clicked.connect(self.AnalyzeFlow)
        self.ui.pushButton_GenerateCurves.clicked.connect(self.GenerateCurves)
        #self.ui.pushButton_RefreshSketch(self.RefreshSketch)
        #self.ui.pushButton_Save(self.Save)
        #self.ui.pushButton_SaveAs(self.SaveAs)

        self.ui.radioButton_ConstantFlowrateSource.clicked.connect(self.RadioChanged)
        self.ui.radioButton_ConstantPressureSource.clicked.connect(self.RadioChanged)
        self.ui.radioButton_PumpSource.clicked.connect(self.RadioChanged)

        self.ui.checkBox_Length.clicked.connect(self.Length)

        self.ui.Pump_Selection.currentTextChanged.connect(self.PumpChanged)
        self.ui.Pump_Selection.addItem('Taco Pump 4 (006b)')
        self.ui.Pump_Selection.addItem('Taco Pump 8 (010)')
        self.ui.Pump_Selection.addItem('Taco Pump 6 (008)')

    def GetPipe(self):
        filename = QFileDialog.getOpenFileName()[0]     # Read Filename
        #self.filename = filename
        if len(filename)==0:
            no_file()
            return
        self.ui.textEdit_filepath.setText(filename)     # Output filename
        app.processEvents()

        f1 = open(filename, 'r')                        # Open and read file
        data = f1.readlines()
        f1.close()

        self.Pipe = Pipe()

        self.Pipe.ReadPipeData(data)

        [xmin, xmax, ymin, ymax] = self.Pipe.DrawingSize
        dx = xmax - xmin
        dy = ymax - ymin
        xmin -= .05*dx
        xmax += .05*dx
        ymin -= .05*dy
        ymax += .05*dy
        self.glwindow1.setViewSize(xmin, xmax, ymin, ymax, allowDistortion=False)
        self.glwindow1.glUpdate()

        rpt = self.Pipe.GenerateReport(data)
        self.ui.textEdit_report.setText(rpt)

    def Length(self):
        """Doesnt work yet but trying to print the pipe lengths when the check for it is clicked"""
        #self.Pipe.Length()

    def PumpChanged(self):
        text = self.ui.Pump_Selection.currentText()     # text equals whichever pump is selected
        # need to assign other pump properties (coefficients) to variables
        # so we can pass them to def Generate Curves to plot a pump curve
        # and find where it intersects with system curve for overall Q and H
        pass

    def setupGLWindows(self):
        self.glwindow1 = gl2D(self.ui.openGLWidget, self.DrawingCallback)
        self.glwindow1.setViewSize(-10, 500, -10, 500, allowDistortion=False)
        self.ui.horizontalSlider_zoom.valueChanged.connect(self.glZoomSlider)

    def glZoomSlider(self):  # I used a slider to control GL zooming
        zoomval = float((self.ui.horizontalSlider_zoom.value()) / 200 + 0.25)
        self.glwindow1.glZoom(zoomval)  # set the zoom value
        self.glwindow1.glUpdate()  # update the GL image

    def DrawingCallback(self):
        self.Pipe.DrawPipePicture()

    def RadioChanged(self):
        # This is where I'm trying to update Pipe.supply so in the class we can call
        # and print self.supply for the report but it's printing the original val of None
        if self.ui.radioButton_ConstantFlowrateSource.isChecked():
            Pipe.supply = "Constant Flowrate"
            self.flowrate = float(self.ui.lineEdit_SourceFlowrate.text())

        elif self.ui.radioButton_ConstantPressureSource.isChecked():
            Pipe.supply = "Constant Pressure"
            self.pressure = float(self.ui.lineEdit_SourcePressure.text())

        elif self.ui.radioButton_PumpSource.isChecked():
            self.pumpID = self.ui.Pump_Selection.currentText()
            Pipe.supply = 'Pump - {}'.format(self.pumpID)
        return

    def AnalyzeFlow(self):
        self.ui.lineEdit_Flowrate.setText('{:.2f}'.format(self.flowrate))
        self.ui.lineEdit_Pressure.setText('{:.2f}'.format(self.pressure))
        self.power = self.flowrate * self.pressure
        self.ui.lineEdit_FluidPower.setText('{:.2f}'.format(self.power))
        # the rest of analyze flow will be here

    def GenerateCurves(self):
        self.minFlow = float(self.ui.lineEdit_MinFlow.text())
        self.maxFlow = float(self.ui.lineEdit_MaxFlow.text())
        #the rest of generate curves will be here

    def RefreshSketch(self):
        """code"""

    def Save(self):
        """save"""

    def SaveAs(self):
        """does this need to be a separate function or can it be part of the Save?"""



    def ExitApp(self):
        app.exit()


def no_file():
    msg = QMessageBox()
    msg.setText('There was no file selected')       # No file specified
    msg.setWindowTitle("No File")
    retval = msg.exec_()
    return None

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)            # Standard Stuff
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())