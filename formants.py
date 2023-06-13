""" References: 
https://github.com/drfeinberg/PraatScripts.git

Adapted from: DOI 10.17605/OSF.IO/K2BHS
"""

import parselmouth
import statistics

from parselmouth.praat import call

def detect_formants(sound_data, sample_rate, f0min, f0max):
    sound_data = sound_data.astype('float64')
    sound = parselmouth.Sound(sound_data, sampling_frequency = sample_rate)

    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")
    
    f1_list = []
    f2_list = []
    
    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)

    f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
    f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']

    # # calculate mean and median formants across pulses
    f1_mean = statistics.mean(f1_list)
    f2_mean = statistics.mean(f2_list)

    f1_median = statistics.median(f1_list)
    f2_median = statistics.median(f2_list)

    return f1_mean, f2_mean, f1_median, f2_median