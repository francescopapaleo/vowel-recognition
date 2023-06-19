# Formant detection using Praat's Burg algorithm and Loudness measurement

import numpy as np
from typing import List

import parselmouth
from parselmouth.praat import call

def extract_formants(buffer, sample_rate, frames_per_buffer, f0min, f0max) -> List[float]: 
    sound = parselmouth.Sound(buffer, sampling_frequency=sample_rate)

    time_step = frames_per_buffer
    formants = sound.to_formant_burg(time_step=time_step, max_number_of_formants=4)
    
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    numPoints = call(pointProcess, "Get number of points")

    f1_list, f2_list, f3_list, f4_list = [], [], [], []        
    formants_result = []

    # Measure formants only at glottal pulses
    for point in range(0, numPoints):
        f1_mean, f2_mean, f3_mean, f4_mean = 0.0, 0.0, 0.0, 0.0
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')

        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)

    # Calculate mean of formants
    f1_mean = np.mean(f1_list) if not np.isnan(np.mean(f1_list)) else 0.0
    f2_mean = np.mean(f2_list) if not np.isnan(np.mean(f2_list)) else 0.0
    f3_mean = np.mean(f3_list) if not np.isnan(np.mean(f3_list)) else 0.0
    f4_mean = np.mean(f4_list) if not np.isnan(np.mean(f4_list)) else 0.0
    
    formants_result.append([float(f"{f1_mean:.9f}"), float(f"{f2_mean:.9f}"), float(f"{f3_mean:.9f}"), float(f"{f4_mean:.9f}")])

    return formants_result



""" 
References:
------------
https://github.com/drfeinberg/PraatScripts.git

@article{article,
author = {Jadoul, Yannick and Thompson, Bill and de Boer, Bart},
year = {2018},
month = {11},
pages = {1-15},
title = {Introducing Parselmouth: A Python interface to Praat},
volume = {91},
journal = {Journal of Phonetics},
doi = {10.1016/j.wocn.2018.07.001}
}
"""