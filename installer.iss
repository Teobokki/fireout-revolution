#define MyVer "1.0.3"
[Setup]
AppId={{7F1E0A2B-5C3D-4E6F-9A8B-F1REOUTREV01}}
AppName=FIREOUT REVOLUTION™
AppVersion={#MyVer}
AppVerName=FIREOUT REVOLUTION™ {#MyVer}
AppPublisher=EX Inc./HYPERION DIGITAL
AppPublisherURL=https://github.com/Teobokki/fireout-revolution
AppCopyright=©2026 EX Inc./HYPERION DIGITAL ©2026
VersionInfoVersion={#MyVer}.0
VersionInfoCompany=EX Inc./HYPERION DIGITAL
VersionInfoCopyright=©2026 EX Inc./HYPERION DIGITAL ©2026
VersionInfoProductName=FIREOUT REVOLUTION
VersionInfoDescription=FIREOUT REVOLUTION Setup
DefaultDirName={localappdata}\Programs\FIREOUT REVOLUTION
DefaultGroupName=FIREOUT REVOLUTION
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=dist
OutputBaseFilename=FIREOUT.REVOLUTION.Setup.{#MyVer}
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\FIREOUT REVOLUTION.exe
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
Type: filesandordirs; Name: "{app}\_internal"

[Files]
Source: "dist\FIREOUT REVOLUTION\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FIREOUT REVOLUTION™"; Filename: "{app}\FIREOUT REVOLUTION.exe"
Name: "{group}\Uninstall FIREOUT REVOLUTION™"; Filename: "{uninstallexe}"
Name: "{userdesktop}\FIREOUT REVOLUTION™"; Filename: "{app}\FIREOUT REVOLUTION.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FIREOUT REVOLUTION.exe"; Description: "Launch FIREOUT REVOLUTION™ now"; Flags: nowait postinstall skipifsilent
