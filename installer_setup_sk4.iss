; ==============================================================================
; SK ENTERPRISES | INNO SETUP INSTALLER SCRIPT
; PROJECT SK AI 4.0 (PROJECT JARVIS 4.0)
; INVENTOR & SOLE ARCHITECT: Sumeet Kumar
; PLATFORM: JARVIS PLATFORM V5.0
; ==============================================================================

#define MyAppName "SK AI 4.0"
#define MyAppVersion "5.0.0"
#define MyAppPublisher "SK Enterprises (Sumeet Kumar)"
#define MyAppURL "https://github.com/sumitkausik-oss/Project-SK-AI-4.0"
#define MyAppExeName "SK_AI_4.0.exe"

[Setup]
AppId={{C8E19011-8F32-4C10-9114-8A5E12F5A9A0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion} (Platform V5.0)
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\SK Enterprises\SK AI 4.0
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=release
OutputBaseFilename=SK_AI_4.0_Setup_x64_v5.0.0
SetupIconFile=assets\jarvis.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
VersionInfoVersion=5.0.0.0
VersionInfoCompany=SK Enterprises
VersionInfoDescription=SK AI 4.0 Sovereign Cognitive Operating System
VersionInfoCopyright=(C) 2026 SK Enterprises. All Rights Reserved.
VersionInfoProductName=SK AI 4.0 (Project JARVIS 4.0)
VersionInfoProductVersion=5.0.0.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Standalone compiled application distribution (Zero Python dependency on target machine)
Source: "dist\SK_AI_4.0\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\jarvis.ico"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\jarvis.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
