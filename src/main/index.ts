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
import * as https from 'https';
import { SystemTools, getSystemMetrics, resolveUserPath } from './lib/system-tools';
import { PermissionPolicy, StoredMemory } from '../shared/types';

let mainWindow: BrowserWindow | null = null;

const APPDATA_DIR = join(app.getPath('appData'), 'SK Enterprises', 'SKAI');
const SECRETS_FILE = join(APPDATA_DIR, 'secrets.enc');
const MEMORY_FILE = join(APPDATA_DIR, 'skai_memory.json');
const PERMISSIONS_FILE = join(APPDATA_DIR, 'permissions_policy.json');
const AUDIT_FILE = join(APPDATA_DIR, 'audit_log.json');
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

// -----------------------------------------------------------------------------
// VALIDATORS FOR GOOGLE & HUGGING FACE
// -----------------------------------------------------------------------------
function validateGoogleKey(key: string): Promise<{ valid: boolean; message: string }> {
  return new Promise((resolve) => {
    if (!key || !key.trim()) {
      return resolve({ valid: false, message: 'Google API key is empty.' });
    }
    https
      .get(`https://generativelanguage.googleapis.com/v1beta/models?key=${key.trim()}`, (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve({ valid: true, message: 'Google API key is valid and active!' });
          } else {
            try {
              const err = JSON.parse(data);
              resolve({ valid: false, message: err.error?.message || `Invalid Google Key (HTTP ${res.statusCode})` });
            } catch {
              resolve({ valid: false, message: `Key validation failed (HTTP ${res.statusCode})` });
            }
          }
        });
      })
      .on('error', (err) => {
        resolve({ valid: false, message: `Connection error: ${err.message}` });
      });
  });
}

function validateHuggingFaceToken(token: string): Promise<{ valid: boolean; message: string; username?: string }> {
  return new Promise((resolve) => {
    if (!token || !token.trim()) {
      return resolve({ valid: false, message: 'Hugging Face token is empty.' });
    }
    const req = https.get(
      'https://huggingface.co/api/whoami-v2',
      {
        headers: {
          Authorization: `Bearer ${token.trim()}`,
          'User-Agent': 'SKAI-Desktop-Assistant/0.0.1',
        },
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => (data += chunk));
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const user = JSON.parse(data);
              const uname = user.name || user.username || 'User';
              resolve({
                valid: true,
                message: `Hugging Face token valid! Connected as @${uname}`,
                username: uname,
              });
            } catch {
              resolve({ valid: true, message: 'Hugging Face token is valid and active!' });
            }
          } else {
            resolve({ valid: false, message: `Invalid Hugging Face token (HTTP ${res.statusCode})` });
          }
        });
      }
    );
    req.on('error', (err) => {
      resolve({ valid: false, message: `Connection error: ${err.message}` });
    });
  });
}

// -----------------------------------------------------------------------------
// PERMISSION POLICY & MEMORY STORAGE
// -----------------------------------------------------------------------------
const DEFAULT_POLICY: PermissionPolicy = {
  auto_approve_read_only: true,
  auto_approve_reversible: true,
  require_confirmation_for_destructive: true,
  require_confirmation_for_terminal: false,
  web_tools_enabled: true,
  allowed_directories: [os.homedir()],
};

function loadPermissionPolicy(): PermissionPolicy {
  if (!fs.existsSync(PERMISSIONS_FILE)) return DEFAULT_POLICY;
  try {
    return { ...DEFAULT_POLICY, ...JSON.parse(fs.readFileSync(PERMISSIONS_FILE, 'utf-8')) };
  } catch {
    return DEFAULT_POLICY;
  }
}

function savePermissionPolicy(policy: Partial<PermissionPolicy>): PermissionPolicy {
  const current = loadPermissionPolicy();
  const updated = { ...current, ...policy };
  try {
    fs.writeFileSync(PERMISSIONS_FILE, JSON.stringify(updated, null, 2), 'utf-8');
  } catch {}
  return updated;
}

function loadMemories(): StoredMemory[] {
  if (!fs.existsSync(MEMORY_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(MEMORY_FILE, 'utf-8'));
  } catch {
    return [];
  }
}

function saveMemories(memories: StoredMemory[]) {
  try {
    fs.writeFileSync(MEMORY_FILE, JSON.stringify(memories, null, 2), 'utf-8');
  } catch {}
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

  // Explicit Hardware Access Permissions
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

  // 4. Secrets Vault (SafeStorage DPAPI) & Token Validation
  ipcMain.handle('secrets:getApiKey', (_, provider: string) => getEncryptedApiKey(provider));
  ipcMain.handle('secrets:setApiKey', (_, provider: string, key: string) => setEncryptedApiKey(provider, key));
  ipcMain.handle('secrets:hasApiKey', (_, provider: string) => !!getEncryptedApiKey(provider));
  ipcMain.handle('secrets:validateGoogleKey', (_, key: string) => validateGoogleKey(key));
  ipcMain.handle('secrets:validateHuggingFaceToken', (_, token: string) => validateHuggingFaceToken(token));

  // 5. System Tools
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

  // 6. Permissions & Memory
  ipcMain.handle('permissions:getPolicy', () => loadPermissionPolicy());
  ipcMain.handle('permissions:savePolicy', (_, policy: Partial<PermissionPolicy>) => savePermissionPolicy(policy));
  ipcMain.handle('permissions:confirmAction', async () => ({ success: true }));

  ipcMain.handle('memory:store', (_, key: string, content: string, tags?: string[], category?: string) => {
    const mems = loadMemories();
    const item: StoredMemory = {
      id: `mem_${Date.now()}`,
      key,
      content,
      category: category || 'GENERAL',
      tags: tags || [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    mems.unshift(item);
    saveMemories(mems);
    return item;
  });
  ipcMain.handle('memory:query', (_, query: string, limit?: number) => {
    const mems = loadMemories();
    const q = query.toLowerCase();
    return mems.filter((m) => m.key.toLowerCase().includes(q) || m.content.toLowerCase().includes(q)).slice(0, limit || 20);
  });
  ipcMain.handle('memory:list', (_, limit?: number) => loadMemories().slice(0, limit || 50));
  ipcMain.handle('memory:delete', (_, id: string) => {
    const mems = loadMemories().filter((m) => m.id !== id);
    saveMemories(mems);
    return true;
  });

  // 7. Coding Tools
  ipcMain.handle('code:readProject', async (_, projectPath: string) => {
    const root = resolveUserPath(projectPath);
    return { success: fs.existsSync(root), root };
  });
  ipcMain.handle('code:editFile', async (_, filePath: string, targetContent: string, replacementContent: string) => {
    const fullPath = resolveUserPath(filePath);
    if (!fs.existsSync(fullPath)) return { success: false, error: 'File not found.' };
    const content = fs.readFileSync(fullPath, 'utf-8');
    if (!content.includes(targetContent)) return { success: false, error: 'Target snippet not found in file.' };
    const updated = content.replace(targetContent, replacementContent);
    fs.writeFileSync(fullPath, updated, 'utf-8');
    return { success: true, path: fullPath, message: 'File edited successfully.' };
  });
  ipcMain.handle('code:runTests', async (_, projectPath: string, testCommand: string = 'npm test') => {
    const root = resolveUserPath(projectPath);
    return SystemTools.runTerminal(testCommand, root);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
