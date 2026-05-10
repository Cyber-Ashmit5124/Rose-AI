# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ROSE OS AI.
Build a portable .exe with:
    pyinstaller rose_os_build.spec
"""

a = Analysis(
    ["rose_os/main.py"],
    pathex=[],
    binaries=[],
    datas=[("assets", "assets")],
    hiddenimports=[
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "pyttsx3.drivers.nsss",
        "pyttsx3.drivers.espeak",
        "customtkinter",
        "speech_recognition",
        "groq",
        "psutil",
        "pystray",
        "PIL",
        "keyboard",
        "edge_tts",
        "pygame",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ROSE_OS_AI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/rose_icon.ico",
)
