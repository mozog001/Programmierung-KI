from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton
from PyQt5 import uic
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graph_utils import genGraph, calculate_sma
import sys


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("gui/mainScreen.ui", self)
        self.test_data = []
        self.show()

        self.layout = QVBoxLayout(self.centralwidget)        
        self.layout.addWidget(self.pushButtonGenGraph)
        self.layout.addWidget(self.pushButtonCalcSma)
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.centralwidget.setLayout(self.layout)

        # Connect button clicks to the respective functions
        self.pushButtonGenGraph.clicked.connect(self.on_pushButtonGenGraph_clicked)
        self.pushButtonCalcSma.clicked.connect(self.on_pushButtonCalcSma_clicked)

    def on_pushButtonGenGraph_clicked(self):
        self.ax.clear()
        self.test_data = genGraph(self.ax, self.canvas)
        self.ax.plot(self.test_data)
        self.canvas.draw()

    def on_pushButtonCalcSma_clicked(self):
        sma_values = calculate_sma(self.ax, self.canvas, self.test_data)
        self.ax.plot(sma_values)
        self.canvas.draw()
        

def main():
    app = QApplication(sys.argv)
    window = MyGui()
    app.exec_()

if __name__ == '__main__':
    main()

