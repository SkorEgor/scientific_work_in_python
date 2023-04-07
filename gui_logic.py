from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox
from gui import Ui_Dialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib

matplotlib.use("Qt5Agg")


def parser_all_data(string_list, frequency_list, gamma_list):
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


def parser(string_list, frequency_list, gamma_list, start_frequency, end_frequency):
    frequency_list.clear()
    gamma_list.clear()

    skipping_first_line = True
    for line in string_list:
        # Пропуск первой строки
        if skipping_first_line:
            skipping_first_line = False
            continue

        # Если звездочки, конец файла
        if line[0] == "*":
            break

        row = line.split()

        # Если частота в диапазоне частот берем
        if start_frequency < float(row[1]) < end_frequency:
            frequency_list.append(float(row[1]))
            gamma_list.append(float(row[4]))


def search_for_peak_on_interval(frequency_list, gamma_list):
    index_max_gamma = 0
    for i in range(1, len(gamma_list)):
        if gamma_list[index_max_gamma] < gamma_list[i]:
            index_max_gamma = i
    return frequency_list[index_max_gamma], gamma_list[index_max_gamma]


def list_ranges_to_list_peaks(frequency_list, gamma_list):
    frequency_peaks = []
    gamma_peaks = []
    for frequency_ranges, gamma_ranges in zip(frequency_list, gamma_list):
        f, g = search_for_peak_on_interval(frequency_ranges, gamma_ranges)
        frequency_peaks.append(f)
        gamma_peaks.append(g)
    return frequency_peaks, gamma_peaks


def frequency_input_check(frequency, field_name):
    try:
        frequency = float(frequency)

    except ValueError:
        QMessageBox.about(None, "Ошибка ввода", "Введите число в поле '" + field_name + "'.")
        return False

    # Проверка положительности
    if frequency < 0:
        QMessageBox.about(None, "Ошибка ввода", "Введите положительное число в поле '" + field_name + "'.")
        return False

    return True


def percentage_check(percentage):
    try:
        percentage = float(percentage)

    except ValueError:
        QMessageBox.about(None, "Ошибка ввода", "Введите число в поле порога.")
        return False

    # Проверка
    if percentage < 0 or percentage > 100:
        QMessageBox.about(None, "Ошибка ввода", "Пороговое значение должно быть от 0 до 100.")
        return False

    return True


class GuiProgram(Ui_Dialog):
    """ A class which takes care of user interaction. """

    def __init__(self, dialog):
        """ This method gets called when the window is created. """
        Ui_Dialog.__init__(self)  # Initialize Window

        # Диапазон частот из файла
        self.frequency_range_start = 0
        self.frequency_range_end = 0

        # Без шума
        self.empty_frequency = []
        self.empty_gamma = []

        # Сигнал
        self.signal_frequency = []
        self.signal_gamma = []

        # Разница сигналов
        self.difference = []

        # Список диапазонов пиков
        self.gamma_range = []
        self.frequency_range = []

        # Список пиков
        self.gamma_peak = []
        self.frequency_peak = []

        # Порог
        self.frequency_indexes_above_threshold = []
        self.threshold_percentage = 30.

        # Параметры 1 графика
        self.ax1 = None
        self.fig1 = None
        self.canvas1 = None
        self.toolbar1 = None

        # Параметры 2 графика
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
        self.pushButton.clicked.connect(self.plotting_without_noise)
        self.pushButton_2.clicked.connect(self.signal_plotting)
        self.pushButton_3.clicked.connect(self.signal_difference)
        self.pushButton_4.clicked.connect(self.threshold)
        self.pushButton_5.clicked.connect(self.saving_data)

        self.lineEdit_threshold.setText(str(self.threshold_percentage))

        self.tableWidget.cellClicked.connect(self.get_clicked_cell)
        self.checkBox.toggled.connect(self.filter_state_changed)

    def filter_state_changed(self):
        state = self.checkBox.checkState()
        self.lineEdit_threshold_2.setEnabled(state)
        self.lineEdit_threshold_3.setEnabled(state)

    def saving_data(self):
        # Проверка, что данные для сохранения есть
        if self.frequency_peak == [] or self.gamma_peak == []:
            return

        # Рек-мое название файла
        recommended_file_name = "F" + str(self.signal_frequency[0]) + "-" + str(
            self.signal_frequency[len(self.signal_frequency) - 1]) + "_threshold-" + self.lineEdit_threshold.text()

        # Окно с выбором места сохранения
        file_name, file_type = QFileDialog.getSaveFileName(
            None,
            'Сохранение',
            recommended_file_name,
            "Spectrometer Data(*.csv);;Text(*.txt);;All Files(*)"
        )

        # Если имя не получено, прервать
        if not file_name:
            return

        # Открываем файл для чтения
        with open(file_name, "w") as file:

            # Заголовок/Название столбцов
            file.write("FREQUENCY:\tGAMMA:\n")

            # Перебираем по парно частоты и гаммы пиков; Записываем по строчно в файл
            for f, g in zip(self.frequency_peak, self.gamma_peak):
                file.write(str('%.3f' % f) + "\t" + str('%.7E' % g) + "\n")

            # Конец файла
            file.write('''***********************************************************\nFinish''')

    def get_clicked_cell(self, row, column):
        window_width = self.lineEdit.text()

        # Проверка на цифры и положительность
        if not window_width.isdigit():
            QMessageBox.about(None, "Ошибка ввода", "Введите положительное число в поле ширины окна.")
            return

        window_width = float(window_width)

        frequency_left_or_right = window_width / 2

        self.ax1.set_xlim([
            self.frequency_peak[row - 1] - frequency_left_or_right,
            self.frequency_peak[row - 1] + frequency_left_or_right
        ])

        self.canvas1.draw()

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

    def plotting_without_noise(self):
        # Вызов окна выбора файла
        # filename, filetype = QFileDialog.getOpenFileName(None,
        #                                                 "Выбрать файл без шума",
        #                                                 ".",
        #                                                "Spectrometer Data(*.csv);;All Files(*)")
        filename = "25empty.csv"

        if filename == '':
            return

        # Чтение данных
        with open(filename) as f:
            list_line = f.readlines()  # Читаем по строчно

        if self.checkBox.checkState():
            # Считываем "Частоту от"
            start_frequency = self.lineEdit_threshold_2.text()
            # Проверка
            if not frequency_input_check(start_frequency, "Частота от"):
                return
            # Приводим к дробному
            start_frequency = float(start_frequency)

            # Считываем "Частоту до"
            end_frequency = self.lineEdit_threshold_3.text()
            # Проверка
            if not frequency_input_check(end_frequency, "Частота до"):
                return
            # Приводим к дробному
            end_frequency = float(end_frequency)

            # Проверка на правильность границ
            if end_frequency < start_frequency:
                QMessageBox.about(None, "Ошибка ввода", "Частота 'от' больше 'до', в фильтре чтения. ")
                return

            # Парс данных
            parser(list_line, self.empty_frequency, self.empty_gamma, start_frequency, end_frequency)
        else:
            parser_all_data(list_line, self.empty_frequency, self.empty_gamma)

        # Clear whatever was in the plot before
        self.ax1.clear()
        # Plot data, add labels, change colors, ...
        self.ax1.set_xlabel('frequency MHz')
        self.ax1.set_ylabel('gamma')
        self.ax1.plot(self.empty_frequency, self.empty_gamma, color='r', label='empty')

        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()
        self.toolbar1.push_current()

    def signal_plotting(self):
        # Вызов окна выбора файла
        # filename, filetype = QFileDialog.getOpenFileName(None,
        #                                                 "Выбрать файл сигнала",
        #                                                 ".",
        #                                                 "Spectrometer Data(*.csv);;All Files(*)")

        filename = "25DMSO.csv"

        if filename == '':
            return

        # Чтение данных
        with open(filename) as f:
            list_line = f.readlines()

        if self.checkBox.checkState():
            # Считываем "Частоту от"
            start_frequency = self.lineEdit_threshold_2.text()
            # Проверка
            if not frequency_input_check(start_frequency, "Частота от"):
                return
            # Приводим к дробному
            start_frequency = float(start_frequency)

            # Считываем "Частоту до"
            end_frequency = self.lineEdit_threshold_3.text()
            # Проверка
            if not frequency_input_check(end_frequency, "Частота до"):
                return
            # Приводим к дробному
            end_frequency = float(end_frequency)

            # Проверка на правильность границ
            if end_frequency < start_frequency:
                QMessageBox.about(None, "Ошибка ввода", "Частота 'от' больше 'до', в фильтре чтения. ")
                return

            # Парс данных
            parser(list_line, self.signal_frequency, self.signal_gamma, start_frequency, end_frequency)
        else:
            parser_all_data(list_line, self.signal_frequency, self.signal_gamma)

        self.ax1.plot(self.signal_frequency, self.signal_gamma, color='g', label='signal')
        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()

    def signal_difference(self):
        # Пустые сигналы - прекращаем
        if self.empty_gamma == [] or self.signal_gamma == []:
            return

        # Вычитаем отсчеты сигнала с ошибкой и без
        self.difference.clear()
        for i in range(0, len(self.empty_gamma)):
            self.difference.append(abs(self.empty_gamma[i] - self.signal_gamma[i]))

        # Отображаем графики
        # Clear whatever was in the plot before
        self.ax2.clear()
        # Plot data, add labels, change colors, ...
        self.ax2.set_xlabel('frequency')
        self.ax2.set_ylabel('error')
        self.ax2.plot(self.empty_frequency, self.difference, color='g', label='empty')
        # Make sure everything fits inside the canvas
        self.fig2.tight_layout()
        # Show the new figure in the interface
        self.canvas2.draw()

        self.threshold()

    def threshold(self):
        if not self.difference:
            return

        # Запрос порогового значения
        threshold = self.lineEdit_threshold.text()

        # Проверка ввода
        if not percentage_check(threshold):
            return
        threshold = float(threshold)

        # Значение порога
        self.threshold_percentage = threshold
        threshold_value = max(self.difference) * self.threshold_percentage / 100.

        # ПЕРЕРИСОВКА 2 ГРАФИКА
        self.ax2.clear()
        # Plot data, add labels, change colors, ...
        self.ax2.set_xlabel('frequency')
        self.ax2.set_ylabel('error')
        self.ax2.plot(self.empty_frequency, self.difference, color='g', label='empty')
        # Make sure everything fits inside the canvas
        self.fig2.tight_layout()
        # Show the new figure in the interface
        self.canvas2.draw()

        # Отрисовка порога
        threshold_signal = [threshold_value] * len(self.difference)
        self.ax2.plot(self.empty_frequency, threshold_signal, color='r', label='empty')
        self.fig2.tight_layout()
        self.canvas2.draw()

        # ПЕРЕРИСОВКА 1 ГРАФИКА
        self.ax1.clear()
        # Plot data, add labels, change colors, ...
        self.ax1.set_xlabel('frequency')
        self.ax1.set_ylabel('gamma')
        self.ax1.plot(self.empty_frequency, self.empty_gamma, color='r', label='empty')
        self.ax1.plot(self.signal_frequency, self.signal_gamma, color='g', label='signal')
        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()

        # Вычисление промежутков и выделение их
        self.frequency_indexes_above_threshold.clear()
        index_interval = []
        last_index = 0
        for i in range(1, len(self.signal_frequency)):
            if self.difference[i] >= threshold_value:
                if last_index + 1 == i:
                    index_interval.append(i)
                else:
                    if index_interval:
                        self.frequency_indexes_above_threshold.append(index_interval)
                    index_interval = [i]
                last_index = i
        self.frequency_indexes_above_threshold.append(index_interval)

        # Выделение промежутков на 1 графике
        self.gamma_range.clear()
        self.frequency_range.clear()
        for interval_i in self.frequency_indexes_above_threshold:
            x = []
            y = []
            for i in interval_i:
                x.append(self.signal_frequency[i])
                y.append(self.signal_gamma[i])

            self.gamma_range.append(y)
            self.frequency_range.append(x)

            self.ax1.plot(x, y, color='b', label='signal')

        # Построение занесенных диапазонов
        self.fig1.tight_layout()
        self.canvas1.draw()

        # Нахождение пиков
        self.frequency_peak, self.gamma_peak = list_ranges_to_list_peaks(self.frequency_range, self.gamma_range)
        print(self.frequency_peak, self.gamma_peak)

        # Вывод данных в таблицу
        self.table()

    def table(self):

        self.tableWidget.setRowCount(len(self.frequency_peak))
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setHorizontalHeaderLabels(["Частота МГц", "Гамма"])

        index = 0
        for f, g in zip(self.frequency_peak, self.gamma_peak):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(f)))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(g)))
            index += 1
