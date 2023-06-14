# Formant detection using Praat's Burg algorithm and Loudness measurement

import numpy as np
from typing import List

import parselmouth
from parselmouth.praat import call

def extract_audio_features(buffer, sample_rate, frames_per_buffer, f0min, f0max) -> List[float]: 
    sound = parselmouth.Sound(buffer, sampling_frequency=sample_rate)
    formants = sound.to_formant_burg(time_step=frames_per_buffer, max_number_of_formants=4)
    
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    numPoints = call(pointProcess, "Get number of points")
        
    intensity = sound.to_intensity()
    loudness = intensity.get_average(intensity.end_time,intensity.start_time,'DB')

    pre_emphasis = 0.97
    sound = sound.pre_emphasize(from_frequency=pre_emphasis)

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []

    # Measure formants only at glottal pulses
    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        
        f1_list.append(f1) if not np.isnan(f1) else f1_list.append(0.0)
        f2_list.append(f2) if not np.isnan(f2) else f2_list.append(0.0)
        f3_list.append(f3) if not np.isnan(f3) else f3_list.append(0.0)
        f4_list.append(f4) if not np.isnan(f4) else f4_list.append(0.0)
        
    f1_mean = np.mean(f1_list) if f1_list else 0.0 
    f2_mean = np.mean(f2_list) if f2_list else 0.0
    f3_mean = np.mean(f3_list) if f3_list else 0.0
    f4_mean = np.mean(f4_list) if f4_list else 0.0

    audio_feautures = [float(f1_mean), float(f2_mean), float(f3_mean), float(f4_mean), float(loudness)]
    # audio_feautures = np.nan_to_num(audio_feautures)
    return audio_feautures


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