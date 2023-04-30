# coding: utf-8
import functools

from PyQt5.QtGui import QIcon

from data_and_processing import DataAndProcessing
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


# Входной список, парсит по столбцам
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


# Входной список, парсит по столбцам, в заданных частотах
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


# Проверяет ввод частоты (float, x>=0)
def frequency_input_check(frequency, field_name):
    try:
        frequency = float(frequency)

    except ValueError:
        QMessageBox.warning(None, "Ошибка ввода", f"Введите число в поле {field_name!r}.")
        return False

    # Проверка положительности
    if frequency < 0:
        QMessageBox.warning(None, "Ошибка ввода", f"Введите положительное число в поле {field_name!r}.")
        return False

    return True


# Проверяет ввод ширины окна значения частоты (float, x>=0)
def window_width_input_check(window_width):
    try:
        window_width = float(window_width)

    except ValueError:
        QMessageBox.warning(None, "Ошибка ввода", "Введите число в поле 'ширина окна просмотра'.")
        return False

    # Проверка положительности
    if window_width < 0:
        QMessageBox.warning(None, "Ошибка ввода", "Введите положительное число в поле 'ширина окна просмотра'.")
        return False

    return True


# Проверяет ввод процента (float, 0<=x<=100)
def percentage_check(percentage):
    try:
        percentage = float(percentage)

    except ValueError:
        QMessageBox.warning(None, "Ошибка ввода", "Введите число в поле порога.")
        return False

    # Проверка
    if percentage < 0 or percentage > 100:
        QMessageBox.warning(None, "Ошибка ввода", "Пороговое значение должно быть от 0 до 100.")
        return False

    return True


# Класс алгоритма работы приложения
class GuiProgram(Ui_Dialog):

    def __init__(self, dialog):
        # ПОЛЯ КЛАССА
        # Объект данных и обработки их
        self.data_signals = DataAndProcessing()

        # Параметры графика
        self.fig = None
        self.canvas = None
        self.toolbar = None
        # Параметры 1 графика
        self.ax1 = None
        self.horizontal_axis_name1 = "Частота [МГц]"
        self.vertical_axis_name1 = "Гамма"
        self.title1 = "График №1. Данные с исследуемым веществом и без."
        # Параметры 2 графика
        self.ax2 = None
        self.horizontal_axis_name2 = "Частота [МГц]"
        self.vertical_axis_name2 = "Отклонение"
        self.title2 = "График №2. Абсолютная разница между данными."

        # Статистика таблицы
        self.total_rows = 0
        self.selected_rows = 0

        # Для иконок
        self.icon_now = 'selected'
        self.icon_status = {
            'empty': QIcon('./icons/checkBox_empty.png'),
            'mixed': QIcon('./icons/checkBox_mixed.png'),
            'selected': QIcon('./icons/checkBox_selected.png')
        }

        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        # Создаем окно
        Ui_Dialog.__init__(self)
        # Устанавливаем пользовательский интерфейс
        self.setupUi(dialog)

        # Инициализируем фигуру в нашем окне
        figure = Figure()  # Готовим пустую фигуру
        self.ax1 = figure.add_subplot(211)  # Пустой участок
        self.ax2 = figure.add_subplot(212)
        self.initialize_figure(figure)  # Инициализируем!

        # Обработчики нажатий - кнопок порядка работы
        self.pushButton_loading_empty_data.clicked.connect(self.plotting_without_noise)  # Загрузить данные с вакуума
        self.pushButton_loading_signal_data.clicked.connect(self.signal_plotting)  # Загрузить данные с газом
        self.pushButton_signal_difference.clicked.connect(self.signal_difference)  # Найти разницу сигналов
        self.pushButton_update_threshold.clicked.connect(self.threshold)  # Задать порог, найти интервалы, отобразить

        # Диапазон на чтение
        self.checkBox_read_filter.toggled.connect(self.filter_state_changed)  # Вкл/Выкл фильтрации чтения
        self.lineEdit_filter_frequency_start.textChanged.connect(self.filter_changed)  # Изменился текст частоты от
        self.lineEdit_filter_frequency_end.textChanged.connect(self.filter_changed)  # Изменился текст частоты до

        # Таблица
        self.initialize_table()  # Инициализация пустой таблицы с заголовками
        self.pushButton_save_table_to_file.clicked.connect(self.saving_data)  # Сохранить данные из таблицы в файл
        self.tableWidget_frequency_absorption.cellClicked.connect(self.get_clicked_cell)  # Выбрана строка таблицы
        # Выбран заголовок таблицы
        self.tableWidget_frequency_absorption.horizontalHeader().sectionClicked.connect(self.click_handler)

        # Задаем начало сценария, активные и не активные кнопки
        self.state1_initial()

    # Инициализация: Пустая таблица
    def initialize_table(self):
        self.tableWidget_frequency_absorption.clear()
        self.tableWidget_frequency_absorption.setColumnCount(3)
        self.tableWidget_frequency_absorption.setHorizontalHeaderLabels(["Частота МГц", "Гамма", ""])
        self.tableWidget_frequency_absorption.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.tableWidget_frequency_absorption.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

        # Инициализация: Пустой верхний график

    def initialize_figure(self, fig):
        # Инициализирует фигуру matplotlib внутри контейнера GUI.
        # Вызываем только один раз при инициализации

        # Создание фигуры (self.fig и self.ax)
        self.fig = fig
        # Создание холста
        self.canvas = FigureCanvas(self.fig)
        self.plotLayout.addWidget(self.canvas)
        self.canvas.draw()
        # Создание Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.plotWindow_empty_and_signal,
                                         coordinates=True)
        self.plotLayout.addWidget(self.toolbar)

    # Сценарий - (*) Изменился диапазон чтения файлов
    def filter_changed(self):
        self.pushButton_loading_signal_data.setEnabled(False)

    # Сценарий - (**) Изменилось состояние checkbox вкл/выкл фильтра чтения
    def filter_state_changed(self):
        state = self.checkBox_read_filter.checkState()
        self.lineEdit_filter_frequency_start.setEnabled(state)
        self.lineEdit_filter_frequency_end.setEnabled(state)

    # Сценарий - (1) Начальное состояние
    def state1_initial(self):
        self.pushButton_loading_empty_data.setEnabled(True)
        self.pushButton_loading_signal_data.setEnabled(False)
        self.pushButton_signal_difference.setEnabled(False)
        self.pushButton_update_threshold.setEnabled(False)
        self.pushButton_save_table_to_file.setEnabled(False)

    # Сценарий - (2) Загружен сигнал без шума
    def state2_loaded_empty(self):
        self.pushButton_loading_empty_data.setEnabled(True)
        self.pushButton_loading_signal_data.setEnabled(True)
        self.pushButton_signal_difference.setEnabled(False)
        self.pushButton_update_threshold.setEnabled(False)
        self.pushButton_save_table_to_file.setEnabled(False)

        self.ax2.clear()
        self.canvas.draw()

        self.tableWidget_frequency_absorption.setRowCount(0)

        self.tableWidget_frequency_absorption.horizontalHeaderItem(2).setIcon(QIcon())

    # Сценарий - (3) Загружены оба графика
    def state3_data_loaded(self):
        self.pushButton_loading_empty_data.setEnabled(True)
        self.pushButton_loading_signal_data.setEnabled(False)
        self.pushButton_signal_difference.setEnabled(True)
        self.pushButton_update_threshold.setEnabled(False)
        self.pushButton_save_table_to_file.setEnabled(False)

    # Сценарий - (4) Есть разница сигналов
    def state4_difference(self):
        self.pushButton_loading_empty_data.setEnabled(True)
        self.pushButton_loading_signal_data.setEnabled(False)
        self.pushButton_signal_difference.setEnabled(True)
        self.pushButton_update_threshold.setEnabled(True)
        self.pushButton_save_table_to_file.setEnabled(True)

    # Основная программа - (1) Чтение и построение сигнала без шума
    def plotting_without_noise(self):
        # Вызов окна выбора файла
        # filename, filetype = QFileDialog.getOpenFileName(None,
        #                                                  "Выбрать файл без шума",
        #                                                  ".",
        #                                                  "Spectrometer Data(*.csv);;All Files(*)")
        filename = "25empty.csv"

        # Если имя файла не получено, сброс
        if not filename:
            return

        # Чтение данных
        with open(filename) as f:
            list_line = f.readlines()  # Читаем по строчно, в список

        if self.checkBox_read_filter.checkState():
            # Считываем "Частоту от"
            start_frequency = self.lineEdit_filter_frequency_start.text()
            # Проверка
            if not frequency_input_check(start_frequency, "Частота от"):
                return
            # Приводим к дробному
            start_frequency = float(start_frequency)

            # Считываем "Частоту до"
            end_frequency = self.lineEdit_filter_frequency_end.text()
            # Проверка
            if not frequency_input_check(end_frequency, "Частота до"):
                return
            # Приводим к дробному
            end_frequency = float(end_frequency)

            # Проверка на правильность границ
            if end_frequency < start_frequency:
                QMessageBox.warning(None, "Ошибка ввода", "Частота 'от' больше 'до', в фильтре чтения. ")
                return

            # Парс данных в заданных частотах
            parser(list_line,
                   self.data_signals.empty_frequency, self.data_signals.empty_gamma,
                   start_frequency, end_frequency)
        else:
            # Парс данных
            parser_all_data(list_line,
                            self.data_signals.empty_frequency, self.data_signals.empty_gamma)

        # Очищаем график
        self.ax1.clear()
        # Строим данные, добавляем название осей, устанавливаем цвета
        self.ax1.set_xlabel(self.horizontal_axis_name1)
        self.ax1.set_ylabel(self.vertical_axis_name1)
        self.ax1.set_title(self.title1)
        self.ax1.plot(self.data_signals.empty_frequency, self.data_signals.empty_gamma, color='r', label='empty')
        self.ax1.grid()
        # Убеждаемся, что все помещается внутри холста
        self.fig.tight_layout()
        # Показываем новую фигуру в интерфейсе
        self.canvas.draw()

        # Запускаем сценарий: Загружен сигнал без шума
        self.state2_loaded_empty()

    # Основная программа - (2) Чтение и построение полезного сигнала
    def signal_plotting(self):
        # Вызов окна выбора файла
        # filename, filetype = QFileDialog.getOpenFileName(None,
        #                                                  "Выбрать файл сигнала",
        #                                                  ".",
        #                                                  "Spectrometer Data(*.csv);;All Files(*)")

        filename = "25DMSO.csv"

        # Если имя файла не получено, сброс
        if not filename:
            return

        # Чтение данных
        with open(filename) as f:
            list_line = f.readlines()  # Читаем по строчно, в список

        if self.checkBox_read_filter.checkState():
            # Считываем "Частоту от"
            start_frequency = self.lineEdit_filter_frequency_start.text()
            # Проверка
            if not frequency_input_check(start_frequency, "Частота от"):
                return
            # Приводим к дробному
            start_frequency = float(start_frequency)

            # Считываем "Частоту до"
            end_frequency = self.lineEdit_filter_frequency_end.text()
            # Проверка
            if not frequency_input_check(end_frequency, "Частота до"):
                return
            # Приводим к дробному
            end_frequency = float(end_frequency)

            # Проверка на правильность границ
            if end_frequency < start_frequency:
                QMessageBox.warning(None, "Ошибка ввода", "Частота 'от' больше 'до', в фильтре чтения. ")
                return

            # Парс данных в заданных частотах
            parser(list_line,
                   self.data_signals.signal_frequency, self.data_signals.signal_gamma,
                   start_frequency, end_frequency)
        else:
            # Парс данных
            parser_all_data(list_line,
                            self.data_signals.signal_frequency, self.data_signals.signal_gamma)

        self.toolbar.home()  # Возвращаем зум
        self.toolbar.update()  # Очищаем стек осей (от старых x, y lim)
        # Строим данные
        self.ax1.plot(self.data_signals.signal_frequency, self.data_signals.signal_gamma, color='g', label='signal')
        # Убеждаемся, что все помещается внутри холста
        self.fig.tight_layout()
        # Показываем новую фигуру в интерфейсе
        self.canvas.draw()
        self.toolbar.push_current()  # Сохранить текущий статус zoom как домашний

        # Запускаем сценарий: Все данные загружены
        self.state3_data_loaded()

    # Основная программа - (3) Разница пустого и полезного сигнала
    def signal_difference(self):
        # Сигналов нет - прекращаем
        if not self.data_signals.empty_gamma or not self.data_signals.signal_gamma:
            return

        # Вычитаем отсчеты сигнала с ошибкой и без
        self.data_signals.difference_empty_and_signal()

        # Отображаем графики
        self.toolbar.home()  # Возвращаем зум
        self.toolbar.update()  # Очищаем стек осей (от старых x, y lim)
        # очищаем график
        self.ax2.clear()
        # Строим данные, добавляем название осей, устанавливаем цвета
        self.ax2.set_xlabel(self.horizontal_axis_name2)
        self.ax2.set_ylabel(self.vertical_axis_name2)
        self.ax2.set_title(self.title2)
        self.ax2.plot(self.data_signals.empty_frequency, self.data_signals.difference, color='g', label='empty')
        self.ax2.grid()
        # Убеждаемся, что все помещается внутри холста
        self.fig.tight_layout()
        # Показываем новую фигуру в интерфейсе
        self.canvas.draw()
        self.toolbar.push_current()  # Сохранить текущий статус zoom как домашний

        # Запускаем расчет порогового значения, интервалов, отрисовку таблицы
        self.threshold()

        # Запускаем сценарий: Есть разница сигналов
        self.state4_difference()

    # Основная программа - (4) Расчет порога, интервалов больше порога, частот поглощения, отображение на графиках
    def threshold(self):
        # Нет разницы сигналов - сброс
        if not self.data_signals.difference:
            return

        # Запрос порогового значения
        threshold = self.lineEdit_threshold.text()

        # Проверка ввода
        if not percentage_check(threshold):
            return
        threshold = float(threshold)

        # Значение порога от макс. значения графика ошибки
        self.data_signals.threshold_percentage = threshold
        threshold_value = max(self.data_signals.difference) * self.data_signals.threshold_percentage / 100.

        # ПЕРЕРИСОВКА 2 ГРАФИКА
        self.toolbar.home()  # Возвращаем зум
        self.toolbar.update()  # Очищаем стек осей (от старых x, y lim)
        self.ax2.clear()
        # Строим данные, добавляем название осей, устанавливаем цвета
        self.ax2.set_xlabel(self.horizontal_axis_name2)
        self.ax2.set_ylabel(self.vertical_axis_name2)
        self.ax2.set_title(self.title2)
        self.ax2.plot(self.data_signals.empty_frequency, self.data_signals.difference, color='g', label='empty')

        # Отрисовка порога
        threshold_signal = [threshold_value] * len(self.data_signals.difference)
        self.ax2.plot(self.data_signals.empty_frequency, threshold_signal, color='r', label='empty')
        self.ax2.grid()
        self.fig.tight_layout()
        self.canvas.draw()

        # ПЕРЕРИСОВКА 1 ГРАФИКА
        self.ax1.clear()
        # Строим данные, добавляем название осей, устанавливаем цвета
        self.ax1.set_xlabel(self.horizontal_axis_name1)
        self.ax1.set_ylabel(self.vertical_axis_name1)
        self.ax1.set_title(self.title1)
        self.ax1.plot(self.data_signals.empty_frequency, self.data_signals.empty_gamma, color='r', label='empty')
        self.ax1.plot(self.data_signals.signal_frequency, self.data_signals.signal_gamma, color='g', label='signal')
        self.ax1.grid()
        # Убеждаемся, что все помещается внутри холста
        self.fig.tight_layout()
        # Показываем новую фигуру в интерфейсе
        self.canvas.draw()

        # Вычисление промежутков больше порога
        self.data_signals.range_above_threshold(threshold_value)

        # Выделение промежутков на 1 графике
        for x, y in zip(self.data_signals.frequency_range, self.data_signals.gamma_range):
            self.ax1.plot(x, y, color='b', label='signal')

        # Построение занесенных диапазонов
        self.fig.tight_layout()
        self.canvas.draw()

        # Нахождение пиков
        self.data_signals.search_peaks()

        # Вывод данных в таблицу
        self.table()

    # РАБОТА С ТАБЛИЦЕЙ
    # Основная программа - (4.1) Заполение таблицы
    def table(self):
        # Задаем кол-во столбцов и строк
        self.tableWidget_frequency_absorption.setRowCount(len(self.data_signals.frequency_peak))
        self.tableWidget_frequency_absorption.setColumnCount(3)

        # Задаем название столбцов
        self.tableWidget_frequency_absorption.setHorizontalHeaderLabels(["Частота МГц", "Гамма"])

        # Устанавливаем начальное состояние иконки таблицы
        self.icon_now = 'selected'
        self.tableWidget_frequency_absorption.horizontalHeaderItem(2).setIcon(
            QIcon('./icons/checkBox_selected.png')
        )

        # Заполняем таблицу
        index = 0
        for f, g in zip(self.data_signals.frequency_peak, self.data_signals.gamma_peak):
            # значения частоты и гаммы для 0 и 1 столбца
            self.tableWidget_frequency_absorption.setItem(index, 0, QTableWidgetItem(str('%.3f' % f)))
            self.tableWidget_frequency_absorption.setItem(index, 1, QTableWidgetItem(str('%.7E' % g)))

            # Элемент 2 столбца - checkbox, сохранения данных
            check_box = QtWidgets.QCheckBox()  # Создаем объект чекбокс
            check_box.setCheckState(Qt.Checked)  # Задаем состояние - нажат
            # Обработчик нажатия, с передачей отправителя
            check_box.toggled.connect(
                functools.partial(
                    self.frequency_selection, check_box
                )
            )
            self.tableWidget_frequency_absorption.setCellWidget(index, 2, check_box)  # Вводим в таблицу

            index += 1

        # Размеры строк выровнять под содержимое
        self.tableWidget_frequency_absorption.resizeColumnsToContents()
        # Начальные данные для статистики
        self.total_rows = len(self.data_signals.frequency_peak)
        self.selected_rows = self.total_rows
        self.frequency_selection()

    # Меняет состояние иконки таблицы при клике
    def click_handler(self):
        if self.icon_now == 'selected':
            self.state_check_box_all_rows(False)
            self.update_table_icon('empty')
        else:
            self.state_check_box_all_rows(True)
            self.update_table_icon('selected')

    # Установить значение во все checkBox таблицы
    def state_check_box_all_rows(self, state):
        if state:
            state_check_box = Qt.Checked
        else:
            state_check_box = Qt.Unchecked

        # Перебираем строки
        for i in range(self.tableWidget_frequency_absorption.rowCount()):
            self.tableWidget_frequency_absorption.cellWidget(i, 2).setCheckState(state_check_box)

    # Обновляет иконку в соответствии со статусом
    def update_table_icon(self, status):
        # Запоминаем статус для следующего раза
        self.icon_now = status
        update_icon = self.icon_status[self.icon_now]  # Получаем новую иконку

        self.tableWidget_frequency_absorption.horizontalHeaderItem(2).setIcon(
            update_icon  # Вставляем новую иконку
        )

    # Сбор и вывод статистики под таблицей
    def frequency_selection(self, sender=None):
        # Если передали отправителя, проверяем состояние
        if sender is not None:
            # Если новое состояние - нажатое, то прибавляем к числу выбранных
            if sender.checkState() == Qt.CheckState.Checked:
                self.selected_rows += 1
            else:
                self.selected_rows -= 1

        # Создаем строки статистики
        text_statistics \
            = f'Выбрано {self.selected_rows} из {self.total_rows} ( {self.selected_rows / self.total_rows:.2%} ) '

        # Вывод в label под таблицей
        self.label_statistics_on_selected_frequencies.setText(text_statistics)

        # Обновляем статус у checkbox в заголовке
        if self.selected_rows == self.total_rows:
            self.update_table_icon('selected')
        else:
            self.update_table_icon('mixed')

        # Возвращает текст статистики
        return text_statistics

    # Кнопка сохранения таблицы
    def saving_data(self):
        # Проверка, что данные для сохранения есть
        if not self.data_signals.frequency_peak or not self.data_signals.gamma_peak:
            QMessageBox.warning(None, "Ошибка данных", "Нет данных для сохранения.")
            return

        # Рек-мое название файла
        recommended_file_name = f'F{self.data_signals.signal_frequency[0]}-{self.data_signals.signal_frequency[-1]}' \
                                f'_threshold-{self.lineEdit_threshold.text()}'

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
            for i in range(self.tableWidget_frequency_absorption.rowCount()):
                if self.tableWidget_frequency_absorption.cellWidget(i, 2).checkState() == Qt.CheckState.Checked:
                    f = self.tableWidget_frequency_absorption.item(i, 0).text()
                    g = self.tableWidget_frequency_absorption.item(i, 1).text()
                    file.write(f'{f}\t{g}\n')

            # Конец файла
            file.write('''***********************************************************\n''')
            file.write(self.frequency_selection())

    # Выбрана строка таблицы
    def get_clicked_cell(self, row):
        # Запрашиваем из окна, значение порога
        window_width = self.lineEdit_window_width.text()

        # Проверка на цифры и положительность
        if not window_width_input_check(window_width):
            return

        window_width = float(window_width)

        frequency_left_or_right = window_width / 2
        # Приближаем область с выделенной частотой
        self.ax1.set_xlim([
            self.data_signals.frequency_peak[row] - frequency_left_or_right,
            self.data_signals.frequency_peak[row] + frequency_left_or_right
        ])

        # Перерисовываем
        self.canvas.draw()
