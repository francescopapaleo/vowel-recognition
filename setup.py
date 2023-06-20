from setuptools import setup, find_packages

setup(
    name="vowel-recognition",
    version="0.1.0",
    description="Real-time vowel recognition system with GUI",
    author="Francesco Papaleo, Chis Morse, Tommaso Settimi",
    author_email="francesco.papaleo01@estudiant.upf.edu",
    url="https://github.com/francescopapaleo/vowel-recognition",
    packages=find_packages(),
    python_requires=">=3.9.0",
    install_requires=[
        "numpy==1.24.3",
        "praat-parselmouth==0.4.3",
        "PyAudio==0.2.13",
        "python-osc==1.8.1",
        "scipy==1.10.1",
    ],
    entry_points={
        'console_scripts': [
            'vowel-recognition=src.audio_video_server:main',
        ],
    },
)
