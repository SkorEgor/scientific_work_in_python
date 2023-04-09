def search_for_peak_on_interval(frequency_list, gamma_list):
    index_max_gamma = 0
    for i in range(1, len(gamma_list)):
        if gamma_list[index_max_gamma] < gamma_list[i]:
            index_max_gamma = i
    return frequency_list[index_max_gamma], gamma_list[index_max_gamma]


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

    def difference_empty_and_signal(self):
        # Вычитаем отсчеты сигнала с ошибкой и без
        self.difference.clear()
        for i in range(0, len(self.empty_gamma)):
            self.difference.append(
                abs(self.empty_gamma[i] - self.signal_gamma[i]))

        return self.difference

    def calculation_frequency_indexes_above_threshold(self, threshold_value):
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

    def index_to_val_range(self):
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

    def range_above_threshold(self, threshold_value):
        self.calculation_frequency_indexes_above_threshold(threshold_value)
        self.index_to_val_range()

    def search_peaks(self):
        frequency_peaks = []
        gamma_peaks = []
        for frequency_ranges, gamma_ranges in zip(self.frequency_range, self.gamma_range):
            f, g = search_for_peak_on_interval(frequency_ranges, gamma_ranges)
            frequency_peaks.append(f)
            gamma_peaks.append(g)

        self.frequency_peak = frequency_peaks
        self.gamma_peak = gamma_peaks
        return frequency_peaks, gamma_peaks
