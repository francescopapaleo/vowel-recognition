import librosa
import numpy as np

from scipy.signal import butter, filtfilt


class Filter:
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
        
        return self.calculate_average()

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

def extract_formants(audio, sample_rate):
        """Extract the first three formants from the audio signal with librosa and LPC."""
        formants = librosa.lpc(audio, order=16)             
        roots = np.roots(formants)               # Only take roots in the upper half-plane
        roots = roots[np.imag(roots) >= 0]       
        
        frequencies = np.sort(np.angle(roots) * (sample_rate / (2 * np.pi))) # Convert LPC > frequency
        frequencies = frequencies[frequencies > 0]  # Filter out zero frequencies
        
        selected_formants = frequencies[:3]
        return selected_formants[0], selected_formants[1], selected_formants[2]

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
