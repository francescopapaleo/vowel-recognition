""" References: 
https://github.com/drfeinberg/PraatScripts.git

Adapted from: DOI 10.17605/OSF.IO/K2BHS
"""

import numpy as np
from typing import List

import parselmouth
from parselmouth.praat import call

def detect_formants(buffer, sample_rate, frames_per_buffer, f0min, f0max) -> List:
    
    buffer_float64 = buffer.astype(np.float64)
    sound = parselmouth.Sound(buffer_float64, sampling_frequency=sample_rate)

    intensity = call(sound, "To Intensity", f0min, 0, "yes")
    loudness = call(intensity, "Get mean", 0, 0)
    loudness = loudness if np.isfinite(loudness) else 0.0  # Check if loudness is finite
    
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    
    formants = sound.to_formant_burg(time_step=frames_per_buffer, maximum_formant=3000)    
    num_points = call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []

    # Measure formants only at glottal pulses
    for point in range(0, num_points):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        
        f1_list.append(f1) if f1 else f1_list.append(0.0)
        f2_list.append(f2) if f2 else f2_list.append(0.0)
        f3_list.append(f3) if f3 else f3_list.append(0.0)
        f4_list.append(f4) if f4 else f4_list.append(0.0)

    f1_mean = np.mean(f1_list) if f1_list else 0.0
    f2_mean = np.mean(f2_list) if f2_list else 0.0
    f3_mean = np.mean(f3_list) if f3_list else 0.0
    f4_mean = np.mean(f4_list) if f4_list else 0.0

    formants = [float(f1_mean), float(f2_mean), float(f3_mean), float(f4_mean), float(loudness)]

    return formants