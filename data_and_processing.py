# Поиск значений поглощения на интервале
def search_for_peak_on_interval(frequency_list, gamma_list):
    index_max_gamma = 0
    # Перебираем индексы в интервале и находим с макс значением
    for i in range(1, len(gamma_list)):
        if gamma_list[index_max_gamma] < gamma_list[i]:
            index_max_gamma = i
    # Возвращаем частоту и гамму поглощения
    return frequency_list[index_max_gamma], gamma_list[index_max_gamma]


# Класс хранения данных сигналов с шумом и без, разницы, списки частот поглощения
# Методов обработки и получения данных
class DataAndProcessing:
    def __init__(self):
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
        self.threshold_percentage = 30

    # Считаем разницу пустого и полезного сигнала
    def difference_empty_and_signal(self):
        # Вычитаем отсчеты сигнала с ошибкой и без
        self.difference.clear()
        for i in range(0, len(self.empty_gamma)):
            self.difference.append(
                # Находим абсолютную разницу сигналов
                abs(self.empty_gamma[i] - self.signal_gamma[i]))

        return self.difference

    # Находит интервалы индексов, значения которых выше порога
    def calculation_frequency_indexes_above_threshold(self, threshold_value):
        self.frequency_indexes_above_threshold.clear()
        index_interval = []
        last_index = 0
        for i in range(1, len(self.signal_frequency)):
            # Если i-тый отсчет оказался больше порога
            if self.difference[i] >= threshold_value:
                # Если индекс идут друг за другом, записываем их в общий промежуток
                if last_index + 1 == i:
                    index_interval.append(i)
                # Иначе сохраняем интервал в общий список и начинаем новый
                else:
                    if index_interval:
                        self.frequency_indexes_above_threshold.append(index_interval)
                    index_interval = [i]
                # Сохраняем индекс последнего индекса
                last_index = i

        # Сохраняем результат в класс
        self.frequency_indexes_above_threshold.append(index_interval)

    # Интервалы значений выше порога, по интервалам индексов
    def index_to_val_range(self):
        # Очищаем от старых данных
        self.gamma_range.clear()
        self.frequency_range.clear()

        # Перебираем интервалы индексов
        for interval_i in self.frequency_indexes_above_threshold:
            x = []
            y = []
            # Строим интервал значений
            for i in interval_i:
                x.append(self.signal_frequency[i])
                y.append(self.signal_gamma[i])

            # Интервал значений добавляем к общему списку
            self.gamma_range.append(y)
            self.frequency_range.append(x)

    # Находим интервалы значений выше порога
    def range_above_threshold(self, threshold_value):
        # Находим интервалы индексов выше порога
        self.calculation_frequency_indexes_above_threshold(threshold_value)
        # Находим интервалы значений
        self.index_to_val_range()

    # Перебирает интервалы значений и находит частоту поглощения
    def search_peaks(self):
        # Списки частот и гамм поглощения
        frequency_peaks = []
        gamma_peaks = []

        # Перебираем интервалы выше порога
        for frequency_ranges, gamma_ranges in zip(self.frequency_range, self.gamma_range):
            # Находим значение поглощения
            f, g = search_for_peak_on_interval(frequency_ranges, gamma_ranges)

            # Записываем в общий список
            frequency_peaks.append(f)
            gamma_peaks.append(g)

        # Сохраняем в классе
        self.frequency_peak = frequency_peaks
        self.gamma_peak = gamma_peaks

        # Возвращаем списки частот и гамм поглощения
        return frequency_peaks, gamma_peaks
