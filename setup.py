"""Minimal setup.py for ROSE OS AI."""

from setuptools import find_packages, setup

setup(
    name="rose-os-ai",
    version="1.0.0",
    description="ROSE OS AI — Chief Kartik's Hyper-Intelligent AI Companion",
    author="Kartik Srivastava",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "customtkinter>=5.2.0",
        "groq>=0.4.0",
        "psutil>=5.9.0",
        "pyttsx3>=2.90",
        "SpeechRecognition>=3.10.0",
        "PyAudio>=0.2.13",
    ],
    entry_points={
        "console_scripts": [
            "rose=rose_os.main:main",
        ],
    },
)
