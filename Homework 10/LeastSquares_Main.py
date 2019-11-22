import numpy as np

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from GUI_LeastSquares import Ui_Dialog
from LeastSquares import LeastSquares, LeastSquaresData, Exp

class PlotCanvas(FigureCanvas):
    def __init__(self, parent, width=None, height=None, dpi=100):       # Default Code
        if width == None: width = parent.width()/100
        if height == None: height = parent.height()/100
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def plot1(self, xvals, yvals, X, Y):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_title('Least Squares Curve Fitting')
        ax.plot(xvals, yvals, 'r-')
        ax.plot(X, Y, 'bo')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(['Curve Fit', 'Data Values'])

        self.draw()

class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()

        self.filename = None
        self.fit = 1

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.assign_widgets()

        plotwin = self.ui.graphicsView_plot
        self.m = PlotCanvas(plotwin)

        self.show()

    def assign_widgets(self):
        self.ui.pushButton_exit.clicked.connect(self.ExitApp)  # Widgets
        self.ui.pushButton_calculate.clicked.connect(self.Calculate)
        self.ui.radioButton_linear.clicked.connect(self.RadioChanged)
        self.ui.radioButton_quadratic.clicked.connect(self.RadioChanged)
        self.ui.radioButton_cubic.clicked.connect(self.RadioChanged)
        self.ui.radioButton_exponential.clicked.connect(self.RadioChanged)

    def RadioChanged(self, int):
        if self.ui.radioButton_linear.isChecked():                      # Change checked based on radio buttons
            self.fit = 1
        elif self.ui.radioButton_quadratic.isChecked():
            self.fit = 2
        elif self.ui.radioButton_cubic.isChecked():
            self.fit = 3
        elif self.ui.radioButton_exponential.isChecked():
            self.fit = 4
        return

    def Calculate(self):
        self.filename = self.ui.lineEdit_filename.text()
        X, Y = np.loadtxt(self.filename, skiprows=1, unpack=True)
        self.npoints = len(X)
        self.RadioChanged(1)

        if self.fit <= 4:
            c = LeastSquares(X, Y, self.fit)
            xvals, yvals = LeastSquaresData(X, Y, self.fit)     # Call functions to determine coefficient values
            exp = Exp(X, Y, [1,1,1])

            if self.fit == 1:                                   # Check which radio button is pressed to plot and print
                self.m.plot1(xvals, yvals, X, Y)
                strval = '{:.4f}*x + {:.4f}'.format(c[1], c[0])
            elif self.fit == 2:
                self.m.plot1(xvals, yvals, X, Y)
                strval = '{:.4f}*x^2 + {:.4f}*x + {:.4f}'.format(c[2], c[1], c[0])
            elif self.fit == 3:
                self.m.plot1(xvals, yvals, X, Y)
                strval = '{:.4f}*x^3 + {:.4f}*x^2 + {:.4f}*x + {:.4f}'.format(c[3], c[2],
                                                                            c[1], c[0])
            elif self.fit == 4:
                A = np.zeros_like(xvals) + exp[0]           # Create points for exponential function
                B = np.zeros_like(xvals) + exp[1]
                C = np.multiply(exp[2], xvals)
                C = np.exp(C)
                exppts = A + np.multiply(B, C)

                self.m.plot1(xvals, exppts, X, Y)           # Call plot class
                strval = 'A = {:.4f} B = {:.4f} C = {:.4f}'.format(exp[0], exp[1], exp[2])  # Print answers

        self.ui.lineEdit_equation.setText(strval)

    def ExitApp(self):
        app.exit()

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())