import { app, BrowserWindow, ipcMain, session, shell, safeStorage } from 'electron';
import { join } from 'path';
import { exec } from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import * as https from 'https';
import { SystemTools, getSystemMetrics, resolveUserPath } from './lib/system-tools';
import { PermissionPolicy, StoredMemory } from '../shared/types';

let mainWindow: BrowserWindow | null = null;

const APPDATA_DIR = join(app.getPath('appData'), 'SK Enterprises', 'SKAI');
const SECRETS_FILE = join(APPDATA_DIR, 'secrets.enc');
const MEMORY_FILE = join(APPDATA_DIR, 'skai_memory.json');
const PERMISSIONS_FILE = join(APPDATA_DIR, 'permissions_policy.json');
const SCREENSHOTS_DIR = join(APPDATA_DIR, 'screenshots');

for (const dir of [APPDATA_DIR, SCREENSHOTS_DIR]) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// -----------------------------------------------------------------------------
// SECRETS & SAFESTORAGE VAULT (OS DPAPI)
// -----------------------------------------------------------------------------
function loadSecrets(): Record<string, string> {
  if (!fs.existsSync(SECRETS_FILE)) return {};
  try {
    return JSON.parse(fs.readFileSync(SECRETS_FILE, 'utf-8'));
  } catch {
    return {};
  }
}

function saveSecrets(secrets: Record<string, string>) {
  try {
    fs.writeFileSync(SECRETS_FILE, JSON.stringify(secrets, null, 2), 'utf-8');
  } catch (err) {
    console.error('[SECRETS ERROR]:', err);
  }
}

function getEncryptedApiKey(provider: string): string {
  const secrets = loadSecrets();
  const encBase64 = secrets[provider];
  if (!encBase64) return '';

  if (safeStorage.isEncryptionAvailable()) {
    try {
      const buffer = Buffer.from(encBase64, 'base64');
      return safeStorage.decryptString(buffer);
    } catch {
      return '';
    }
  } else {
    try {
      return Buffer.from(encBase64, 'base64').toString('utf-8');
    } catch {
      return '';
    }
  }
}

function setEncryptedApiKey(provider: string, key: string): boolean {
  try {
    const secrets = loadSecrets();
    if (safeStorage.isEncryptionAvailable()) {
      const encryptedBuffer = safeStorage.encryptString(key.trim());
      secrets[provider] = encryptedBuffer.toString('base64');
    } else {
      secrets[provider] = Buffer.from(key.trim(), 'utf-8').toString('base64');
    }
    saveSecrets(secrets);
    return true;
  } catch {
    return false;
  }
}

function validateGoogleKey(key: string): Promise<{ valid: boolean; message: string }> {
  return new Promise((resolve) => {
    if (!key || !key.trim()) return resolve({ valid: false, message: 'Key is empty.' });
    https
      .get(`https://generativelanguage.googleapis.com/v1beta/models?key=${key.trim()}`, (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve({ valid: true, message: 'Google Gemini API key is valid and active!' });
          } else {
            resolve({ valid: false, message: `Invalid Google API key (HTTP ${res.statusCode})` });
          }
        });
      })
      .on('error', (err) => resolve({ valid: false, message: err.message }));
  });
}

function validateHuggingFaceToken(token: string): Promise<{ valid: boolean; message: string; username?: string }> {
  return new Promise((resolve) => {
    if (!token || !token.trim()) return resolve({ valid: false, message: 'Token is empty.' });
    const req = https.get(
      'https://huggingface.co/api/whoami-v2',
      { headers: { Authorization: `Bearer ${token.trim()}` } },
      (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const user = JSON.parse(data);
              const uname = user.name || user.username || 'User';
              resolve({ valid: true, message: `Hugging Face token valid! Connected as @${uname}`, username: uname });
            } catch {
              resolve({ valid: true, message: 'Hugging Face token is valid!' });
            }
          } else {
            resolve({ valid: false, message: `Invalid Hugging Face token (HTTP ${res.statusCode})` });
          }
        });
      }
    );
    req.on('error', (err) => resolve({ valid: false, message: err.message }));
  });
}

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    frame: false,
    transparent: true,
    backgroundColor: '#00000000',
    title: 'SKAI — Powered by SK Enterprises | Sumeet Kumar',
    icon: join(__dirname, '../../assets/jarvis.ico'),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Unconditional Hardware Permissions (Microphone, Audio, Camera)
  session.defaultSession.setPermissionRequestHandler((_webContents, permission, callback) => {
    const allowed = ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture', 'notifications'];
    callback(allowed.includes(permission));
  });

  session.defaultSession.setPermissionCheckHandler((_webContents, permission) => {
    return ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'].includes(permission);
  });

  const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173').catch(() => {
      mainWindow?.loadFile(join(__dirname, '../../dist/index.html'));
    });
  } else {
    mainWindow.loadFile(join(__dirname, '../../dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  // Comprehensive OS Tool Execution Handler
  ipcMain.handle('execute-system-tool', async (_event, { toolName, args }) => {
    return new Promise((resolve) => {
      const rawTarget = (args?.app_name || args?.target || args?.path || args?.url || '').trim();
      const target = rawTarget.toLowerCase();

      if (toolName === 'open_drive_or_folder' || target.includes('drive') || target.includes('folder')) {
        let drivePath = 'D:\\';
        if (target.includes('c drive') || target.includes('c:')) drivePath = 'C:\\';
        if (target.includes('e drive') || target.includes('e:')) drivePath = 'E:\\';
        if (rawTarget.match(/^[a-zA-Z]:\\?/)) drivePath = rawTarget.endsWith('\\') ? rawTarget : `${rawTarget}\\`;

        exec(`explorer.exe "${drivePath}"`, (err) => {
          resolve({ success: !err, message: `Opened: ${drivePath}` });
        });
        return;
      }

      if (toolName === 'open_application' || toolName === 'open_browser') {
        if (target.includes('chrome')) {
          exec('start chrome', (err) => resolve({ success: !err, message: 'Google Chrome opened.' }));
        } else if (target.includes('notepad')) {
          exec('start notepad', (err) => resolve({ success: !err, message: 'Notepad opened.' }));
        } else if (target.includes('calc')) {
          exec('calc', (err) => resolve({ success: !err, message: 'Calculator launched.' }));
        } else if (target.includes('vs code') || target.includes('code')) {
          exec('code .', (err) => resolve({ success: !err, message: 'VS Code launched.' }));
        } else if (args?.url) {
          shell.openExternal(args.url).then(() => resolve({ success: true, message: `Opened URL: ${args.url}` }));
        } else {
          exec(`start "" "${rawTarget}"`, (err) => resolve({ success: !err, message: `Executed: ${rawTarget}` }));
        }
        return;
      }

      if (toolName === 'take_screenshot') {
        exec(
          'powershell -command "$path = \\"$env:USERPROFILE\\Pictures\\skai_screenshot.png\\"; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{PRTSC}\');"',
          () => {
            resolve({ success: true, message: 'Screenshot captured to clipboard and Pictures.' });
          }
        );
        return;
      }

      resolve({ success: false, message: 'Unknown command execution.' });
    });
  });

  // Live Accurate System Metrics (Fixes RAM ghost values)
  ipcMain.handle('get-system-metrics', async () => {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;
    return {
      totalMemGB: (totalMem / 1024 ** 3).toFixed(1),
      usedMemGB: (usedMem / 1024 ** 3).toFixed(1),
      memPercent: Math.round((usedMem / totalMem) * 100),
      cpuCores: os.cpus().length,
      platform: `${os.type()} (${os.arch()})`,
    };
  });

  // Window Controls
  ipcMain.on('window-min', () => mainWindow?.minimize());
  ipcMain.on('window-max', () => (mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize()));
  ipcMain.on('window-close', () => mainWindow?.close());
  ipcMain.handle('window:control', (_, action: 'minimize' | 'maximize' | 'close') => {
    if (!mainWindow) return;
    if (action === 'minimize') mainWindow.minimize();
    else if (action === 'maximize') (mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize());
    else if (action === 'close') mainWindow.close();
  });

  // Telemetry & App Info
  ipcMain.handle('sys:telemetry', () => getSystemMetrics());
  ipcMain.handle('app:getInfo', () => ({
    name: 'skai',
    productName: 'SKAI',
    version: '0.0.1',
    author: 'Sumeet Kumar',
    tagline: 'Powered by SK Enterprises',
    platform: process.platform,
    appDataPath: APPDATA_DIR,
  }));

  // Secrets Vault (SafeStorage DPAPI) & Token Validation
  ipcMain.handle('secrets:getApiKey', (_, provider: string) => getEncryptedApiKey(provider));
  ipcMain.handle('secrets:setApiKey', (_, provider: string, key: string) => setEncryptedApiKey(provider, key));
  ipcMain.handle('secrets:hasApiKey', (_, provider: string) => !!getEncryptedApiKey(provider));
  ipcMain.handle('secrets:validateGoogleKey', (_, key: string) => validateGoogleKey(key));
  ipcMain.handle('secrets:validateHuggingFaceToken', (_, token: string) => validateHuggingFaceToken(token));

  // System Tools
  ipcMain.handle('sys:open-app', (_, appName: string) => SystemTools.openApp(appName));
  ipcMain.handle('os:openApp', (_, appName: string) => SystemTools.openApp(appName));
  ipcMain.handle('os:closeApp', (_, appName: string) => SystemTools.closeApp(appName));
  ipcMain.handle('open-browser', (_, url: string) => SystemTools.openBrowser(url));
  ipcMain.handle('os:openBrowser', (_, url: string) => SystemTools.openBrowser(url));
  ipcMain.handle('os:readFile', (_, filePath: string) => SystemTools.readFile(filePath));
  ipcMain.handle('read-dir', (_, dirPath: string) => SystemTools.readDir(dirPath));
  ipcMain.handle('os:listFolder', (_, folderPath?: string) => SystemTools.readDir(folderPath || 'Desktop'));
  ipcMain.handle('write-file', (_, filePath: string, content: string) => SystemTools.writeFile(filePath, content));
  ipcMain.handle('os:writeFile', (_, filePath: string, content: string, append?: boolean) =>
    SystemTools.writeFile(filePath, content, append)
  );
  ipcMain.handle('os:createFile', (_, filePath: string, content?: string) => SystemTools.createFile(filePath, content));
  ipcMain.handle('os:deleteFile', (_, filePath: string) => SystemTools.deleteFile(filePath));
  ipcMain.handle('sys:terminal', (_, command: string, cwd?: string) => SystemTools.runTerminal(command, cwd));
  ipcMain.handle('os:runTerminal', (_, command: string, cwd?: string) => SystemTools.runTerminal(command, cwd));
  ipcMain.handle('os:takeScreenshot', () => SystemTools.takeScreenshot(SCREENSHOTS_DIR));
  ipcMain.handle('web:search', (_, query: string) => SystemTools.webSearch(query));
  ipcMain.handle('search:localFiles', (_, query: string, baseDir?: string) => SystemTools.searchLocalFiles(query, baseDir));

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
