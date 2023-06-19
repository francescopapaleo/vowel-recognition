# Real-Time Audio/Video Vowel Recognition System

***Authors: Francesco Papaleo, Tommaso Settimi, Chris Morse***

Final Project for the Sound Communication course - Master in Sound and Music Computing

Universitat Pompeu Fabra, Barcelona

## Description

This project is a *proof-of-concept* for a vowel recognition system based on mouth gesture and sound.
The system is based on the following steps:

```tree
  audio-in                                                        FaceOSC (Face tracking)
    |                                                                       |
audio feature extraction                                        mouth gesture extraction 
(Super Collider)                                                        (FaceOSC)
    |                                                                       |
   OSC                                                                     OSC
    |                                                                       |                                           
    ---------------------------> Python OSC Server  <------------------------
                                        |
                                       OSC
                                        |
                                Wekinator Input Helper
                                        |
                                        |
                                Wekinator Classifier
                                (Vowels recognition)
                                        |
                                        |
                                       OSC
                                        |
                                    Max / MSP
                        (visual feedback and audio examples)
```

## Goals (work in progress)

The purpose of this project is to create a working infra-structure that could support language teaching applications.

For demonstration purposes, 5 possible vowels sounds are considered: /a/, /e/, /i/, /o/, /u/.

## Run this code

1. install Wekinator and the Wekinator Input Helper

1. install [FaceOSC](https://github.com/kylemcdonald/ofxFaceTracker) (optional)

1. install [SuperCollider](https://supercollider.github.io/)

1. install [Max / MSP](https://cycling74.com)

1. run from terminal:

    ```bash
    pip3 install -r requirements.txt

    cd src

    python3 audio_video_server.py
    ```

1. open SuperCollider > File > Open > [script](./src/FeatureExtractor.scd)

1. launch FaceOSC (optional)

1. open Max / MSP > File > Open > [patch](./src/training_GUI.amxd)

1. open Wekinator > File > Open > [project file](./DemoClassifier/DemoSession.wekproj)

1. run the pre-trained model

## FaceOSC Keyboard controls

```bash
r - reset the face tracker
m - toggle face mesh drawing
g - toggle gui's visibility
p - pause/unpause (only works with movie source)
up/down - increase/decrease movie playback speed (only works with movie source)
```

## Other scripts in python

For demonstration purposes we provide some scripts that can be used to extract audio and video features from audio files and live audio/video input.
These script are optional and are not required to run the main project.

- [audio_osc.py](./src/audio_osc.py): sends audio features to Wekinator
- [formants_extractor.py](./src/formants_extractor.py): extract formants from audio files with Praat-Parselmouth
- [video_osc.py](./src/video_osc.py): sends mouth gesture features to Wekinator

## Folder Structure

```tree
    .
    ├── assets                              # screenshots and slides of the project's presentation
    ├── Democlassifier                      # pre-trained model for Wekinator
    │   ├── current
    │   │   └── models
    │   └── saved
    └── src                                 # source code
        ├── audio_osc.py                    # calls formants_extractor and sends audio features to Wekinator
        ├── audio_video_server.py           # sends audio and video features to Wekinator via OSC  
        ├── FeatureExtractor.scd            # SuperCollider script for audio feature extraction
        ├── formants_extractor.py           # extract formants from audio files with Praat-Parselmouth
        ├── MonitorOSC.maxpat               # Max patch for monitoring OSC messages and testing the project
        ├── training_GUI.amxd               # Max patch for the training of vowel sounds
        └── video_osc.py                    # sends mouth gesture features to Wekinator
```
