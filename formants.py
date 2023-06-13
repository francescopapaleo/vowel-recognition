""" References: 
https://github.com/drfeinberg/PraatScripts.git

Adapted from: DOI 10.17605/OSF.IO/K2BHS
"""
import numpy as np
import parselmouth
import numpy as np
from typing import List

from parselmouth.praat import call

def detect_formants(buffer, sample_rate, frames_per_buffer, f0min, f0max) -> List:
    
    buffer_float64 = buffer.astype(np.float64)
    sound = parselmouth.Sound(buffer_float64, sampling_frequency=sample_rate)

    # pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    # f0 = pitch.selected_array['frequency']

    formants = sound.to_formant_burg(time_step=frames_per_buffer, maximum_formant=3000)    
    num_points = call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f1 = 0.0
    f2 = 0.0

    # Measure formants only at glottal pulses
    for point in range(0, num_points):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        
    f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
    f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
    
    # # calculate mean formants across pulses
    f1_mean = np.mean(f1_list) if f1_list else 0.0
    f2_mean = np.mean(f2_list) if f2_list else 0.0
    
    # Calculate mean of f0
    # f0_mean = np.mean(f0) if f0.size != 0 else 0.0

    formants = [ float(f1), float(f2), float(f1_mean), float(f2_mean)]

    return formants