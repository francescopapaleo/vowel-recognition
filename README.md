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

For demonstration purposes, 5 possible vowels sounds are considered: /a/, /e/, /i/, /o/, /u/

## Run this code

1. install Wekinator

1. install FaceOSC (optional)

1. run from terminal:

    ```bash
    pip3 install -r requirements.txt

    cd src

    python3 main.py
    ```

1. open Wekinator > File > Open > [project file](./AudioVideoClassifier/Classifier13in5out.wekproj)

1. run the pre-trained model

## Folder Structure

```tree
    .
    ├── AudioVideoClassifier
    │   ├── current
    │   │   └── models
    │   └── saved
    ├── SuperCollider
    │   └── Classifier4in5out
    │       ├── current
    │       │   └── models
    │       └── saved
    ├── __pycache__
    ├── assets
    └── src
        └── __pycache__
```
