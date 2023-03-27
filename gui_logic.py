from PyQt5.QtWidgets import QFileDialog
from gui import Ui_Dialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib

matplotlib.use("Qt5Agg")


class GuiProgram(Ui_Dialog):
    """ A class which takes care of user interaction. """

    def __init__(self, dialog):
        """ This method gets called when the window is created. """
        Ui_Dialog.__init__(self)  # Initialize Window

        self.ax1 = None
        self.fig1 = None
        self.canvas1 = None
        self.toolbar1 = None

        self.ax2 = None
        self.fig2 = None
        self.canvas2 = None
        self.toolbar2 = None

        self.setupUi(dialog)  # Set up the UI

        # Initialize the figure in our window
        figure1 = Figure()  # Prep empty figure
        axis1 = figure1.add_subplot(111)  # Prep empty plot
        self.initialize_figure(figure1, axis1)  # Initialize!

        # Initialize the figure in our window
        figure2 = Figure()  # Prep empty figure
        axis2 = figure2.add_subplot(111)  # Prep empty plot
        self.initialize_figure2(figure2, axis2)  # Initialize!

        # Connect our button with plotting function
        self.pushButton.clicked.connect(self.change_plot)

    def change_plot(self):
        # Вызов окна выбора файла
        filename, filetype = QFileDialog.getOpenFileName(None,
                                                         "Выбрать файл",
                                                         ".",
                                                         "Spectrometer Data(*.csv);;All Files(*)")

        # Чтение данных
        frequency = []
        gamma = []

        list_line = []
        with open(filename) as f:
            list_line = f.readlines()  # Читаем пустую строку

        self.parser(list_line, frequency, gamma)

        # Clear whatever was in the plot before
        self.ax1.clear()
        # Plot data, add labels, change colors, ...
        self.ax1.set_xlabel('time spent learning Qt (minutes)')
        self.ax1.set_ylabel('skill (a.u.)')
        self.ax1.plot(frequency, gamma)
        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()

        self.ax2.clear()
        # Plot data, add labels, change colors, ...
        self.ax2.set_xlabel('time spent learning Qt (minutes)')
        self.ax2.set_ylabel('skill (a.u.)')
        self.ax2.plot([0, 1, 2, 3, 4, 5, 10, 20], [1, 5, 6, 9, 15, 22, 40, 50])
        # Make sure everything fits inside the canvas
        self.fig2.tight_layout()
        # Show the new figure in the interface
        self.canvas2.draw()

    def initialize_figure(self, fig, ax):
        """ Initializes a matplotlib figure inside a GUI container.
            Only call this once when initializing.
        """
        # Figure creation (self.fig and self.ax)
        self.fig1 = fig
        self.ax1 = ax
        # Canvas creation
        self.canvas1 = FigureCanvas(self.fig1)
        self.plotLayout.addWidget(self.canvas1)
        self.canvas1.draw()
        # Toolbar creation
        self.toolbar1 = NavigationToolbar(self.canvas1, self.plotWindow,
                                          coordinates=True)
        self.plotLayout.addWidget(self.toolbar1)

    def initialize_figure2(self, fig, ax):
        """ Initializes a matplotlib figure inside a GUI container.
            Only call this once when initializing.
        """
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

    def parser(self, string_list, frequency_list, gamma_list):
        frequency_list.clear()
        gamma_list.clear()

        skipping_first_line = True
        for line in string_list:
            if skipping_first_line:
                skipping_first_line = False
                continue
            if line[0] == "*":
                break

            row = line.split()
            frequency_list.append(float(row[1]))
            gamma_list.append(float(row[4]))