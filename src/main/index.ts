import { app, BrowserWindow, ipcMain, session, shell, safeStorage } from 'electron';
import { join } from 'path';
import { exec } from 'child_process';
import os from 'os';
import fs from 'fs';
import https from 'https';

let mainWindow: BrowserWindow | null = null;
const vaultPath = join(app.getPath('userData'), 'skai_vault.json');

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

  // Grant all hardware audio/video permissions unconditionally
  session.defaultSession.setPermissionRequestHandler((_wc, permission, callback) => {
    callback(['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture', 'notifications'].includes(permission));
  });

  session.defaultSession.setPermissionCheckHandler((_wc, permission) => {
    return ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'].includes(permission);
  });

  const distPath = join(__dirname, '../../dist/index.html');
  const isDev = process.env.NODE_ENV === 'development';

  if (isDev && !process.env.LOAD_LOCAL) {
    mainWindow.loadURL('http://localhost:5173').catch(() => {
      if (fs.existsSync(distPath)) {
        mainWindow?.loadFile(distPath);
      }
    });
  } else if (fs.existsSync(distPath)) {
    mainWindow.loadFile(distPath);
  } else {
    mainWindow.loadURL('http://localhost:5173').catch(() => {});
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  // 1. API Key Vault (SafeStorage DPAPI)
  ipcMain.handle('save-api-keys', async (_e, { geminiKey, hfToken }: { geminiKey: string; hfToken?: string }) => {
    try {
      let encryptedGemini = '';
      let encryptedHf = '';
      if (safeStorage.isEncryptionAvailable()) {
        if (geminiKey) encryptedGemini = safeStorage.encryptString(geminiKey.trim()).toString('base64');
        if (hfToken) encryptedHf = safeStorage.encryptString(hfToken.trim()).toString('base64');
      } else {
        if (geminiKey) encryptedGemini = Buffer.from(geminiKey.trim()).toString('base64');
        if (hfToken) encryptedHf = Buffer.from(hfToken.trim()).toString('base64');
      }
      fs.writeFileSync(vaultPath, JSON.stringify({ geminiKey: encryptedGemini, hfToken: encryptedHf }, null, 2), 'utf-8');
      return { success: true };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  });

  ipcMain.handle('get-api-keys', async () => {
    try {
      if (!fs.existsSync(vaultPath)) return { geminiKey: '', hfToken: '' };
      const data = JSON.parse(fs.readFileSync(vaultPath, 'utf-8'));
      let geminiKey = '';
      let hfToken = '';
      if (safeStorage.isEncryptionAvailable()) {
        if (data.geminiKey) geminiKey = safeStorage.decryptString(Buffer.from(data.geminiKey, 'base64'));
        if (data.hfToken) hfToken = safeStorage.decryptString(Buffer.from(data.hfToken, 'base64'));
      } else {
        if (data.geminiKey) geminiKey = Buffer.from(data.geminiKey, 'base64').toString('utf-8');
        if (data.hfToken) hfToken = Buffer.from(data.hfToken, 'base64').toString('utf-8');
      }
      return { geminiKey, hfToken };
    } catch {
      return { geminiKey: '', hfToken: '' };
    }
  });

  ipcMain.handle('secrets:getApiKey', async (_, provider: string) => {
    try {
      if (!fs.existsSync(vaultPath)) return '';
      const data = JSON.parse(fs.readFileSync(vaultPath, 'utf-8'));
      const raw = provider === 'huggingface' ? data.hfToken : data.geminiKey;
      if (!raw) return '';
      return safeStorage.isEncryptionAvailable()
        ? safeStorage.decryptString(Buffer.from(raw, 'base64'))
        : Buffer.from(raw, 'base64').toString('utf-8');
    } catch {
      return '';
    }
  });

  ipcMain.handle('secrets:setApiKey', async (_, provider: string, key: string) => {
    try {
      let current: any = {};
      if (fs.existsSync(vaultPath)) {
        try {
          current = JSON.parse(fs.readFileSync(vaultPath, 'utf-8'));
        } catch {}
      }
      const enc = safeStorage.isEncryptionAvailable()
        ? safeStorage.encryptString(key.trim()).toString('base64')
        : Buffer.from(key.trim()).toString('base64');
      if (provider === 'huggingface') {
        current.hfToken = enc;
      } else {
        current.geminiKey = enc;
      }
      fs.writeFileSync(vaultPath, JSON.stringify(current, null, 2), 'utf-8');
      return true;
    } catch {
      return false;
    }
  });

  ipcMain.handle('secrets:hasApiKey', async (_, provider: string) => {
    try {
      if (!fs.existsSync(vaultPath)) return false;
      const data = JSON.parse(fs.readFileSync(vaultPath, 'utf-8'));
      return provider === 'huggingface' ? Boolean(data.hfToken) : Boolean(data.geminiKey);
    } catch {
      return false;
    }
  });

  // 2. Native Windows Tool Execution
  ipcMain.handle('execute-system-tool', async (_e, { toolName, args }) => {
    return new Promise((resolve) => {
      const rawTarget = (args?.target || args?.app_name || args?.query || '').trim();
      const target = rawTarget.toLowerCase();

      if (toolName === 'open_drive' || target.includes('drive') || target.includes('folder')) {
        let drive = 'D:\\';
        if (target.includes('c')) drive = 'C:\\';
        if (target.includes('e')) drive = 'E:\\';
        if (rawTarget.match(/^[a-zA-Z]:\\?/)) drive = rawTarget.endsWith('\\') ? rawTarget : `${rawTarget}\\`;

        exec(`explorer.exe "${drive}"`, (err) => {
          resolve({ success: !err, message: `${drive} drive opened in Explorer.` });
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
        } else if (target.includes('code') || target.includes('vs code')) {
          exec('code .', (err) => resolve({ success: !err, message: 'VS Code launched.' }));
        } else if (args?.url) {
          shell.openExternal(args.url).then(() => resolve({ success: true, message: `Opened URL: ${args.url}` }));
        } else {
          exec(`start "" "${rawTarget}"`, (err) => resolve({ success: !err, message: `Launched ${rawTarget}` }));
        }
        return;
      }

      if (toolName === 'take_screenshot') {
        exec('powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{PRTSC}\');"', () => {
          resolve({ success: true, message: 'Screenshot captured.' });
        });
        return;
      }

      resolve({ success: false, message: `Tool ${toolName} not found.` });
    });
  });

  // 3. System Metrics
  ipcMain.handle('get-system-metrics', async () => {
    const total = os.totalmem();
    const free = os.freemem();
    return {
      totalMemGB: (total / 1024 ** 3).toFixed(1),
      usedMemGB: ((total - free) / 1024 ** 3).toFixed(1),
      memPercent: Math.round(((total - free) / total) * 100),
      cpuCores: os.cpus().length,
      platform: `${os.type()} (${os.arch()})`,
    };
  });

  ipcMain.handle('sys:telemetry', async () => {
    const total = os.totalmem();
    const free = os.freemem();
    return {
      totalMemGB: (total / 1024 ** 3).toFixed(1),
      usedMemGB: ((total - free) / 1024 ** 3).toFixed(1),
      ramPercent: Math.round(((total - free) / total) * 100),
      cpuCores: os.cpus().length,
      cpuPercent: 15,
      uptimeHours: (os.uptime() / 3600).toFixed(1),
      platform: `${os.type()} (${os.arch()})`,
      hostname: os.hostname(),
    };
  });

  // 4. Permissions & Policy Mock/Storage
  ipcMain.handle('permissions:getPolicy', async () => ({
    auto_approve_read_only: true,
    auto_approve_reversible: true,
    require_confirmation_for_destructive: true,
    web_tools_enabled: true,
  }));
  ipcMain.handle('permissions:savePolicy', async () => ({ success: true }));

  // 5. Window Controls
  ipcMain.on('window-min', () => mainWindow?.minimize());
  ipcMain.on('window-max', () => (mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize()));
  ipcMain.on('window-close', () => mainWindow?.close());
  ipcMain.handle('window:control', (_, action: 'minimize' | 'maximize' | 'close') => {
    if (!mainWindow) return;
    if (action === 'minimize') mainWindow.minimize();
    else if (action === 'maximize') (mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize());
    else if (action === 'close') mainWindow.close();
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
