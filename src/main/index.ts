/**
 * SKAI — Autonomous Master Main Process & Hardware Permission Layer
 * Product: SKAI
 * Powered by SK Enterprises | Author: Sumeet Kumar
 * Version: 0.0.1
 */
import { app, BrowserWindow, ipcMain, session, shell, safeStorage } from 'electron';
import { join } from 'path';
import { exec } from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import { SystemTools, getSystemMetrics } from './lib/system-tools';

let mainWindow: BrowserWindow | null = null;

const APPDATA_DIR = join(app.getPath('appData'), 'SK Enterprises', 'SKAI');
const SECRETS_FILE = join(APPDATA_DIR, 'secrets.enc');
const SCREENSHOTS_DIR = join(APPDATA_DIR, 'screenshots');

for (const dir of [APPDATA_DIR, SCREENSHOTS_DIR]) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

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

  // Explicit Hardware Access Permissions (Microphone, Media, Camera)
  session.defaultSession.setPermissionRequestHandler((_webContents, permission, callback) => {
    const allowed = ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture', 'notifications'];
    callback(allowed.includes(permission));
  });

  session.defaultSession.setPermissionCheckHandler((_webContents, permission) => {
    const allowed = ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'];
    return allowed.includes(permission);
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

// Single Instance Lock
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  app.whenReady().then(() => {
    // 1. Native OS Tool Execution Bridge (IPC)
    ipcMain.handle('execute-system-tool', async (_event, { toolName, args }) => {
      return new Promise((resolve) => {
        const target = (args?.app_name || args?.url || args?.command || '').toLowerCase().trim();

        if (toolName === 'open_browser' || toolName === 'open_application') {
          if (target.includes('chrome') || target.includes('google chrome')) {
            exec('start chrome', (err) => resolve({ success: !err, message: 'Google Chrome opened successfully.' }));
          } else if (target.includes('notepad')) {
            exec('start notepad', (err) => resolve({ success: !err, message: 'Notepad opened.' }));
          } else if (target.includes('calc') || target.includes('calculator')) {
            exec('calc', (err) => resolve({ success: !err, message: 'Calculator launched.' }));
          } else if (target.includes('code') || target.includes('vs code')) {
            exec('code .', (err) => resolve({ success: !err, message: 'VS Code launched.' }));
          } else if (args?.url) {
            shell.openExternal(args.url).then(() => resolve({ success: true, message: `Opened URL: ${args.url}` }));
          } else {
            exec(`start "" "${args.app_name || target}"`, (err) =>
              resolve({ success: !err, message: `Executed ${args.app_name || target}` })
            );
          }
        } else if (toolName === 'system_command') {
          exec(args.command, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
            resolve({ success: !error, output: stdout || stderr });
          });
        } else if (toolName === 'take_screenshot') {
          SystemTools.takeScreenshot(SCREENSHOTS_DIR).then((res) => resolve(res));
        } else {
          resolve({ success: false, message: 'Tool not recognized.' });
        }
      });
    });

    // 2. Window Controls
    ipcMain.on('window-min', () => mainWindow?.minimize());
    ipcMain.on('window-max', () => (mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize()));
    ipcMain.on('window-close', () => mainWindow?.close());
    ipcMain.handle('window:control', (_, action: 'minimize' | 'maximize' | 'close') => {
      if (!mainWindow) return;
      if (action === 'minimize') mainWindow.minimize();
      else if (action === 'maximize') (mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize());
      else if (action === 'close') mainWindow.close();
    });

    // 3. Telemetry & App Info
    ipcMain.handle('sys:telemetry', () => getSystemMetrics());
    ipcMain.handle('get-system-metrics', () => getSystemMetrics());
    ipcMain.handle('app:getInfo', () => ({
      name: 'skai',
      productName: 'SKAI',
      version: '0.0.1',
      author: 'Sumeet Kumar',
      tagline: 'Powered by SK Enterprises',
      platform: process.platform,
      appDataPath: APPDATA_DIR,
    }));

    // 4. Secrets Vault (SafeStorage DPAPI)
    ipcMain.handle('secrets:getApiKey', (_, provider: string) => getEncryptedApiKey(provider));
    ipcMain.handle('secrets:setApiKey', (_, provider: string, key: string) => setEncryptedApiKey(provider, key));
    ipcMain.handle('secrets:hasApiKey', (_, provider: string) => !!getEncryptedApiKey(provider));

    // 5. System Tools
    ipcMain.handle('sys:open-app', (_, appName: string) => SystemTools.openApp(appName));
    ipcMain.handle('open-browser', (_, url: string) => SystemTools.openBrowser(url));
    ipcMain.handle('os:openBrowser', (_, url: string) => SystemTools.openBrowser(url));
    ipcMain.handle('os:readFile', (_, filePath: string) => SystemTools.readFile(filePath));
    ipcMain.handle('read-dir', (_, dirPath: string) => SystemTools.readDir(dirPath));
    ipcMain.handle('write-file', (_, filePath: string, content: string) => SystemTools.writeFile(filePath, content));
    ipcMain.handle('os:takeScreenshot', () => SystemTools.takeScreenshot(SCREENSHOTS_DIR));
    ipcMain.handle('web:search', (_, query: string) => SystemTools.webSearch(query));
    ipcMain.handle('search:localFiles', (_, query: string, baseDir?: string) => SystemTools.searchLocalFiles(query, baseDir));

    createWindow();

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
