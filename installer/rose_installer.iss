; ROSE OS AI — Inno Setup Installer Script
; Creates a proper Windows installer with Start Menu, Desktop shortcut,
; auto-start option, and clean uninstall.
;
; How to build:
;   1. First build the exe: pyinstaller rose_os_build.spec
;   2. Install Inno Setup from https://jrsoftware.org/isinfo.php
;   3. Open this .iss file in Inno Setup and click Build

[Setup]
AppName=ROSE OS AI
AppVersion=1.0.0
AppPublisher=Kartik Srivastava (Chief)
AppPublisherURL=https://github.com/Cyber-Ashmit5124/Rose-AI
DefaultDirName={autopf}\ROSE OS AI
DefaultGroupName=ROSE OS AI
OutputBaseFilename=ROSE_OS_AI_Setup_v1.0
SetupIconFile=..\assets\rose_icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
OutputDir=..\dist\installer

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &Desktop shortcut"; GroupDescription: "Additional shortcuts:"
Name: "autostart"; Description: "Start ROSE OS AI when Windows starts"; GroupDescription: "Startup options:"

[Files]
Source: "..\dist\ROSE_OS_AI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ROSE OS AI"; Filename: "{app}\ROSE_OS_AI.exe"; Comment: "Launch ROSE OS AI"
Name: "{group}\Uninstall ROSE OS AI"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ROSE OS AI"; Filename: "{app}\ROSE_OS_AI.exe"; Tasks: desktopicon; Comment: "Chief Kartik's AI Companion"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ROSE_OS_AI"; ValueData: """{app}\ROSE_OS_AI.exe"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\ROSE_OS_AI.exe"; Description: "Launch ROSE OS AI now"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
