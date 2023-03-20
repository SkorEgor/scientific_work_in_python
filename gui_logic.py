from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_Dialog

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

class GuiProgram(Ui_Dialog):
    ''' A class which takes care of user interaction. '''

    def __init__(self, dialog):
        ''' This method gets called when the window is created. '''
        Ui_Dialog.__init__(self)              # Initialize Window
        self.setupUi(dialog)                  # Set up the UI
        # Initialize the figure in our window
        figure = Figure()                     # Prep empty figure
        axis = figure.add_subplot(111)        # Prep empty plot
        self.initialize_figure(figure, axis)  # Initialize!
        self.initialize_figure2(figure, axis)  # Initialize!
        # Connect our button with plotting function
        self.pushButton.clicked.connect(self.change_plot)

    def change_plot(self):
        ''' Plots something new in the figure. '''
        # Clear whatever was in the plot before
        self.ax.clear()
        # Plot data, add labels, change colors, ...
        self.ax.set_xlabel('time spent learning Qt (minutes)')
        self.ax.set_ylabel('skill (a.u.)')
        self.ax.plot([0,1,2,3,4,5], [1,5,6,9,15,22])
        # Make sure everything fits inside the canvas
        self.fig.tight_layout()
        # Show the new figure in the interface
        self.canvas.draw()

        self.ax2.clear()
        # Plot data, add labels, change colors, ...
        self.ax2.set_xlabel('time spent learning Qt (minutes)')
        self.ax2.set_ylabel('skill (a.u.)')
        self.ax2.plot([0,1,2,3,4,5,10,20], [1,5,6,9,15,22,40,50])
        # Make sure everything fits inside the canvas
        self.fig2.tight_layout()
        # Show the new figure in the interface
        self.canvas2.draw()

    def initialize_figure(self, fig, ax):
        ''' Initializes a matplotlib figure inside a GUI container.
            Only call this once when initializing.
        '''
        # Figure creation (self.fig and self.ax)
        self.fig = fig
        self.ax = ax
        # Canvas creation
        self.canvas = FigureCanvas(self.fig)
        self.plotLayout.addWidget(self.canvas)
        self.canvas.draw()
        # Toolbar creation
        self.toolbar = NavigationToolbar(self.canvas, self.plotWindow,
                                         coordinates=True)
        self.plotLayout.addWidget(self.toolbar)

    def initialize_figure2(self, fig, ax):
        ''' Initializes a matplotlib figure inside a GUI container.
            Only call this once when initializing.
        '''
        # Figure creation (self.fig and self.ax)
        self.fig2 = fig
        self.ax2 = ax
        # Canvas creation
        self.canvas2 = FigureCanvas(self.fig2)
        self.plotLayout2.addWidget(self.canvas2)
        self.canvas2.draw()
        # Toolbar creation
        self.toolbar2 = NavigationToolbar(self.canvas2, self.plotWindow2,
                                         coordinates=True)
        self.plotLayout2.addWidget(self.toolbar2)