import numpy as np

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
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

        self.show()

    def assign_widgets(self):               # Widgets
        self.ui.pushButton_exit.clicked.connect(self.ExitApp)
        self.ui.pushButton_GetFlowSystemFile.clicked.connect(self.GetPipe)

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

    def GetPipe(self):
        filename = QFileDialog.getOpenFileName()[0]     # Read Filename
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