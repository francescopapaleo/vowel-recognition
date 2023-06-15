# Real-Time Audio/Video Vowel Recognition System

***Authors: Francesco Papaleo, Tommaso Settimi, Chris Morse***

Sound Communication - Master in Sound and Music Computing

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

1. install FaceOSC (optional)

1. install SuperCollider

1. run from terminal:

    ```bash
    pip3 install -r requirements.txt

    cd src

    python3 audio_video_server.py
    ```

1. open Wekinator > File > Open > [project file](./DemoClassifier/)

1. run the pre-trained model

## FaceOSC Keyboard controls

```bash
r - reset the face tracker
m - toggle face mesh drawing
g - toggle gui's visibility
p - pause/unpause (only works with movie source)
up/down - increase/decrease movie playback speed (only works with movie source)
```

## Folder Structure

```tree
    .
    ├── assets
    ├── AVclassifier
    │   ├── current
    │   │   └── models
    │   └── saved
    └── src
        ├── audio_osc.py
        ├── audio_features.py
        ├── audio_video_server.py
        ├── FeatureExtractor.scd
        ├── training_GUI.amxd
        └── video_osc.py
```
