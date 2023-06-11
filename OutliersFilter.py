import numpy as np

class RealTimeAverageCalculator:
    def __init__(self, window_size, threshold=3):
        self.window_size = window_size
        self.threshold = threshold
        self.data = []
        self.filtered_data = []

    def add_data_point(self, value):
        self.data.append(value)

        if len(self.data) > self.window_size:
            removed_value = self.data.pop(0)
            if removed_value in self.filtered_data:
                self.filtered_data.remove(removed_value)
        if not self.is_outlier(value):
            self.filtered_data.append(value)

    def is_outlier(self, value):
        sorted_data = np.sort(self.data)
        median = np.median(sorted_data)
        abs_deviations = np.abs(sorted_data - median)
        mad = np.median(abs_deviations)
        outlier_threshold = self.threshold * mad
        return np.abs(value - median) > outlier_threshold

    def calculate_average(self):
        if len(self.filtered_data) > 0:
            return np.mean(self.filtered_data)
        else:
            return np.nan