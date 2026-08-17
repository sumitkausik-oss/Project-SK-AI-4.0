[Setup]
AppName=SK AI 4.0
AppVersion=4.0
AppPublisher=SK Enterprises (Sumeet Kumar)
AppPublisherURL=https://github.com/sumitkausik-oss/Project-SK-AI-4.0
DefaultDirName={autopf}\SK Enterprises\SK AI 4.0
DefaultGroupName=SK AI 4.0
OutputDir=Output_Installer
OutputBaseFilename=SK_AI_4.0_Setup_x64
SetupIconFile=assets\jarvis.ico
UninstallIconFile=assets\jarvis.ico
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "_extracted_staging_temp\*,Output_Installer\*,*.git\*,*.exe"

[Icons]
Name: "{group}\SK AI 4.0"; Filename: "{app}\Main_SK_AI_4.py"; IconFilename: "{app}\assets\jarvis.ico"
Name: "{autodesktop}\SK AI 4.0"; Filename: "{app}\Main_SK_AI_4.py"; IconFilename: "{app}\assets\jarvis.ico"; Tasks: desktopicon
