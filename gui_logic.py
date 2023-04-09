from Data_and_processing import DataAndProcessing
from gui import Ui_Dialog

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt

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

        self.data_signals = DataAndProcessing()

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

        self.tableWidget.cellClicked.connect(self.get_clicked_cell)
        self.checkBox_read_filter.toggled.connect(self.filter_state_changed)

        self.lineEdit_threshold_2.textChanged.connect(self.filter_changed)
        self.lineEdit_threshold_3.textChanged.connect(self.filter_changed)

        self.initialize_table()

        # Задаем начало сценария, активные и не активные кнопки
        self.state1_initial()

    # Сценарий: Изменился фильтр чтения файлов
    def filter_changed(self):
        self.pushButton_2.setEnabled(False)

    # Сценарий: Начальное состояние
    def state1_initial(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        # Загружен пустой график

    # Сценарий: Загружен сигнал без шума
    def state2_loaded_empty(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

        self.ax2.clear()
        self.canvas2.draw()

        self.tableWidget.setRowCount(0)

    # Сценарий: Загружены оба графика
    def state3_data_loaded(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(False)

    # Сценарий: Есть разница сигналов
    def state4_difference(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    # Сценарий: Изменился checkbox вкл/выкл фильтра чтения
    def filter_state_changed(self):
        state = self.checkBox_read_filter.checkState()
        self.lineEdit_threshold_2.setEnabled(state)
        self.lineEdit_threshold_3.setEnabled(state)

    # Кнопка сохранения таблицы
    def saving_data(self):
        # Проверка, что данные для сохранения есть
        if self.data_signals.frequency_peak == [] or self.data_signals.gamma_peak == []:
            return

        # Рек-мое название файла
        recommended_file_name = "F" + str(self.data_signals.signal_frequency[0]) + "-" + str(
            self.data_signals.signal_frequency[
                len(self.data_signals.signal_frequency) - 1]) + "_threshold-" + self.lineEdit_threshold.text()

        # Окно с выбором места сохранения
        file_name, file_type = QFileDialog.getSaveFileName(
            None,
            'Сохранение',
            recommended_file_name,
            "Text(*.txt);;Spectrometer Data(*.csv);;All Files(*)"
        )

        # Если имя не получено, прервать
        if not file_name:
            return

        # Открываем файл для чтения
        with open(file_name, "w") as file:

            # Заголовок/Название столбцов
            file.write("FREQUENCY:\tGAMMA:\n")

            # Перебираем по парно частоты и гаммы пиков; Записываем по строчно в файл
            for i in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(i, 2).checkState() == Qt.CheckState.Checked:
                    f = self.tableWidget.item(i, 0).text()
                    g = self.tableWidget.item(i, 1).text()
                    file.write(f + "\t" + g + "\n")

            # Конец файла
            file.write('''***********************************************************\n''')
            file.write(self.frequency_selection())

    # Выбрана строка таблицы
    def get_clicked_cell(self, row, column):
        window_width = self.lineEdit.text()

        # Проверка на цифры и положительность
        if not window_width.isdigit():
            QMessageBox.about(None, "Ошибка ввода", "Введите положительное число в поле ширины окна.")
            return

        window_width = float(window_width)

        frequency_left_or_right = window_width / 2

        self.ax1.set_xlim([
            self.data_signals.frequency_peak[row - 1] - frequency_left_or_right,
            self.data_signals.frequency_peak[row - 1] + frequency_left_or_right
        ])

        self.canvas1.draw()

    # Инициализация пустой таблицы
    def initialize_table(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Частота МГц", "Гамма", ""])
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

    # Инициализация пустого верхнего графика
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

    # Инициализация пустого нижнего графика
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

    # Чтение и построение сигнала без шума
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

        if self.checkBox_read_filter.checkState():
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
            parser(list_line,
                   self.data_signals.empty_frequency, self.data_signals.empty_gamma,
                   start_frequency, end_frequency)
        else:
            parser_all_data(list_line,
                            self.data_signals.empty_frequency, self.data_signals.empty_gamma)

        # Clear whatever was in the plot before
        self.ax1.clear()
        # Plot data, add labels, change colors, ...
        self.ax1.set_xlabel('frequency MHz')
        self.ax1.set_ylabel('gamma')
        self.ax1.plot(self.data_signals.empty_frequency, self.data_signals.empty_gamma, color='r', label='empty')

        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()
        self.toolbar1.push_current()

        self.state2_loaded_empty()

    # Чтение и построение полезного сигнала
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

        if self.checkBox_read_filter.checkState():
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
            parser(list_line,
                   self.data_signals.signal_frequency, self.data_signals.signal_gamma,
                   start_frequency, end_frequency)
        else:
            parser_all_data(list_line,
                            self.data_signals.signal_frequency, self.data_signals.signal_gamma)

        self.ax1.plot(self.data_signals.signal_frequency, self.data_signals.signal_gamma, color='g', label='signal')
        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()

        self.state3_data_loaded()

    # Разница пустого и полезного сигнала
    def signal_difference(self):
        # Сигналов нет - прекращаем
        if self.data_signals.empty_gamma == [] or self.data_signals.signal_gamma == []:
            return

        # Вычитаем отсчеты сигнала с ошибкой и без
        self.data_signals.difference_empty_and_signal()

        # Отображаем графики
        # Clear whatever was in the plot before
        self.ax2.clear()
        # Plot data, add labels, change colors, ...
        self.ax2.set_xlabel('frequency MHz')
        self.ax2.set_ylabel('error')
        self.ax2.plot(self.data_signals.empty_frequency, self.data_signals.difference, color='g', label='empty')
        # Make sure everything fits inside the canvas
        self.fig2.tight_layout()
        # Show the new figure in the interface
        self.canvas2.draw()

        self.threshold()

        self.state4_difference()

    def threshold(self):
        if not self.data_signals.difference:
            return

        # Запрос порогового значения
        threshold = self.lineEdit_threshold.text()

        # Проверка ввода
        if not percentage_check(threshold):
            return
        threshold = float(threshold)

        # Значение порога
        self.data_signals.threshold_percentage = threshold
        threshold_value = max(self.data_signals.difference) * self.data_signals.threshold_percentage / 100.

        # ПЕРЕРИСОВКА 2 ГРАФИКА
        self.ax2.clear()
        # Plot data, add labels, change colors, ...
        self.ax2.set_xlabel('frequency MHz')
        self.ax2.set_ylabel('error')
        self.ax2.plot(self.data_signals.empty_frequency, self.data_signals.difference, color='g', label='empty')
        # Make sure everything fits inside the canvas
        self.fig2.tight_layout()
        # Show the new figure in the interface
        self.canvas2.draw()

        # Отрисовка порога
        threshold_signal = [threshold_value] * len(self.data_signals.difference)
        self.ax2.plot(self.data_signals.empty_frequency, threshold_signal, color='r', label='empty')
        self.fig2.tight_layout()
        self.canvas2.draw()

        # ПЕРЕРИСОВКА 1 ГРАФИКА
        self.ax1.clear()
        # Plot data, add labels, change colors, ...
        self.ax1.set_xlabel('frequency MHz')
        self.ax1.set_ylabel('gamma')
        self.ax1.plot(self.data_signals.empty_frequency, self.data_signals.empty_gamma, color='r', label='empty')
        self.ax1.plot(self.data_signals.signal_frequency, self.data_signals.signal_gamma, color='g', label='signal')
        # Make sure everything fits inside the canvas
        self.fig1.tight_layout()
        # Show the new figure in the interface
        self.canvas1.draw()

        # Вычисление промежутков больше порога
        self.data_signals.range_above_threshold(threshold_value)

        # Выделение промежутков на 1 графике
        for x, y in zip(self.data_signals.frequency_range, self.data_signals.gamma_range):
            self.ax1.plot(x, y, color='b', label='signal')

        # Построение занесенных диапазонов
        self.fig1.tight_layout()
        self.canvas1.draw()

        # Нахождение пиков
        self.data_signals.search_peaks()

        # Вывод данных в таблицу
        self.table()

    def table(self):

        self.tableWidget.setRowCount(len(self.data_signals.frequency_peak))
        self.tableWidget.setColumnCount(3)

        self.tableWidget.setHorizontalHeaderLabels(["Частота МГц", "Гамма"])

        index = 0
        for f, g in zip(self.data_signals.frequency_peak, self.data_signals.gamma_peak):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str('%.3f' % f)))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str('%.7E' % g)))

            check_box = QtWidgets.QCheckBox()  # Создаем объект чекбокс
            check_box.setCheckState(Qt.Checked)
            check_box.toggled.connect(self.frequency_selection)
            self.tableWidget.setCellWidget(index, 2, check_box)

            index += 1

        self.tableWidget.resizeColumnsToContents()
        self.frequency_selection()

    def frequency_selection(self):
        number_of_selected = 0
        number_of_missed = 0
        total = 0
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(i, 2).checkState() == Qt.CheckState.Checked:
                number_of_selected += 1
            else:
                number_of_missed += 1
            total += 1

        text_all_number = "Всего: " + str(total)
        percentage_of_selected = number_of_selected / total * 100
        text_selected = "Выбрано: " + str(number_of_selected) + " ( " + str('%.2f' % percentage_of_selected) + "% ) "
        text_statistics = text_all_number + ' ' + text_selected

        self.label_statistics_on_selected_frequencies.setText(text_statistics)

        return text_statistics
