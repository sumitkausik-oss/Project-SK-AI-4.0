[Setup]
AppName=SK AI 4.0
AppVersion=4.0.0
AppPublisher=SK Enterprises (Sumit Kumar)
AppPublisherURL=https://github.com/sumitkausik-oss/Project-SK-AI-4.0
DefaultDirName={autopf}\SK Enterprises\SK AI 4.0
DefaultGroupName=SK AI 4.0
OutputDir=Output_Installer
OutputBaseFilename=SK_AI_4.0_Setup_x64
SetupIconFile=assets\jarvis.ico
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Dist & Native App Resources
Source: "src_frontend\*"; DestDir: "{app}\src_frontend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "src_backend\*"; DestDir: "{app}\src_backend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "plugins\*"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "run_sk_ai_4.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "Main_SK_AI_4.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SK AI 4.0 (Project JARVIS 4.0)"; Filename: "python.exe"; Parameters: """{app}\run_sk_ai_4.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\jarvis.ico"
Name: "{autodesktop}\SK AI 4.0 (Project JARVIS 4.0)"; Filename: "python.exe"; Parameters: """{app}\run_sk_ai_4.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\jarvis.ico"; Tasks: desktopicon

[Run]
Filename: "python.exe"; Parameters: """{app}\run_sk_ai_4.py"""; Description: "{cm:LaunchProgram,SK AI 4.0}"; Flags: nowait postinstall skipifsilent
