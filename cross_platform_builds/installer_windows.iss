[Setup]
AppName=SK AI 4.0
AppVersion=5.0.0
AppPublisher=SK Enterprises (Sumeet Kumar)
DefaultDirName={autopf}\SK Enterprises\SK AI 4.0
DefaultGroupName=SK AI 4.0
OutputDir=..\cross_platform_builds\windows_installer
OutputBaseFilename=SK_AI_4.0_Setup_x64
SetupIconFile=..\assets\jarvis.ico
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "..\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "cross_platform_builds\*,*.git\*"

[Icons]
Name: "{group}\SK AI 4.0"; Filename: "{app}\run_sk_ai.py"; WorkingDir: "{app}"
Name: "{autodesktop}\SK AI 4.0"; Filename: "{app}\run_sk_ai.py"; WorkingDir: "{app}"
