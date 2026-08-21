"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * SKAI — Autonomous Master Main Process & Hardware Permission Layer
 * Product: SKAI
 * Powered by SK Enterprises | Author: Sumeet Kumar
 * Version: 0.0.1
 */
const electron_1 = require("electron");
const path_1 = require("path");
const child_process_1 = require("child_process");
const fs = __importStar(require("fs"));
const system_tools_1 = require("./lib/system-tools");
let mainWindow = null;
const APPDATA_DIR = (0, path_1.join)(electron_1.app.getPath('appData'), 'SK Enterprises', 'SKAI');
const SECRETS_FILE = (0, path_1.join)(APPDATA_DIR, 'secrets.enc');
const SCREENSHOTS_DIR = (0, path_1.join)(APPDATA_DIR, 'screenshots');
for (const dir of [APPDATA_DIR, SCREENSHOTS_DIR]) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}
function loadSecrets() {
    if (!fs.existsSync(SECRETS_FILE))
        return {};
    try {
        return JSON.parse(fs.readFileSync(SECRETS_FILE, 'utf-8'));
    }
    catch {
        return {};
    }
}
function saveSecrets(secrets) {
    try {
        fs.writeFileSync(SECRETS_FILE, JSON.stringify(secrets, null, 2), 'utf-8');
    }
    catch (err) {
        console.error('[SECRETS ERROR]:', err);
    }
}
function getEncryptedApiKey(provider) {
    const secrets = loadSecrets();
    const encBase64 = secrets[provider];
    if (!encBase64)
        return '';
    if (electron_1.safeStorage.isEncryptionAvailable()) {
        try {
            const buffer = Buffer.from(encBase64, 'base64');
            return electron_1.safeStorage.decryptString(buffer);
        }
        catch {
            return '';
        }
    }
    else {
        try {
            return Buffer.from(encBase64, 'base64').toString('utf-8');
        }
        catch {
            return '';
        }
    }
}
function setEncryptedApiKey(provider, key) {
    try {
        const secrets = loadSecrets();
        if (electron_1.safeStorage.isEncryptionAvailable()) {
            const encryptedBuffer = electron_1.safeStorage.encryptString(key.trim());
            secrets[provider] = encryptedBuffer.toString('base64');
        }
        else {
            secrets[provider] = Buffer.from(key.trim(), 'utf-8').toString('base64');
        }
        saveSecrets(secrets);
        return true;
    }
    catch {
        return false;
    }
}
function createWindow() {
    mainWindow = new electron_1.BrowserWindow({
        width: 1440,
        height: 900,
        minWidth: 1024,
        minHeight: 700,
        frame: false,
        transparent: true,
        backgroundColor: '#00000000',
        title: 'SKAI — Powered by SK Enterprises | Sumeet Kumar',
        icon: (0, path_1.join)(__dirname, '../../assets/jarvis.ico'),
        webPreferences: {
            preload: (0, path_1.join)(__dirname, '../preload/index.js'),
            sandbox: false,
            nodeIntegration: false,
            contextIsolation: true,
        },
    });
    // Explicit Hardware Access Permissions (Microphone, Media, Camera)
    electron_1.session.defaultSession.setPermissionRequestHandler((_webContents, permission, callback) => {
        const allowed = ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture', 'notifications'];
        callback(allowed.includes(permission));
    });
    electron_1.session.defaultSession.setPermissionCheckHandler((_webContents, permission) => {
        const allowed = ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'];
        return allowed.includes(permission);
    });
    const isDev = process.env.NODE_ENV === 'development' || !electron_1.app.isPackaged;
    if (isDev) {
        mainWindow.loadURL('http://localhost:5173').catch(() => {
            mainWindow?.loadFile((0, path_1.join)(__dirname, '../../dist/index.html'));
        });
    }
    else {
        mainWindow.loadFile((0, path_1.join)(__dirname, '../../dist/index.html'));
    }
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}
// Single Instance Lock
const gotTheLock = electron_1.app.requestSingleInstanceLock();
if (!gotTheLock) {
    electron_1.app.quit();
}
else {
    electron_1.app.on('second-instance', () => {
        if (mainWindow) {
            if (mainWindow.isMinimized())
                mainWindow.restore();
            mainWindow.focus();
        }
    });
    electron_1.app.whenReady().then(() => {
        // 1. Native OS Tool Execution Bridge (IPC)
        electron_1.ipcMain.handle('execute-system-tool', async (_event, { toolName, args }) => {
            return new Promise((resolve) => {
                const target = (args?.app_name || args?.url || args?.command || '').toLowerCase().trim();
                if (toolName === 'open_browser' || toolName === 'open_application') {
                    if (target.includes('chrome') || target.includes('google chrome')) {
                        (0, child_process_1.exec)('start chrome', (err) => resolve({ success: !err, message: 'Google Chrome opened successfully.' }));
                    }
                    else if (target.includes('notepad')) {
                        (0, child_process_1.exec)('start notepad', (err) => resolve({ success: !err, message: 'Notepad opened.' }));
                    }
                    else if (target.includes('calc') || target.includes('calculator')) {
                        (0, child_process_1.exec)('calc', (err) => resolve({ success: !err, message: 'Calculator launched.' }));
                    }
                    else if (target.includes('code') || target.includes('vs code')) {
                        (0, child_process_1.exec)('code .', (err) => resolve({ success: !err, message: 'VS Code launched.' }));
                    }
                    else if (args?.url) {
                        electron_1.shell.openExternal(args.url).then(() => resolve({ success: true, message: `Opened URL: ${args.url}` }));
                    }
                    else {
                        (0, child_process_1.exec)(`start "" "${args.app_name || target}"`, (err) => resolve({ success: !err, message: `Executed ${args.app_name || target}` }));
                    }
                }
                else if (toolName === 'system_command') {
                    (0, child_process_1.exec)(args.command, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
                        resolve({ success: !error, output: stdout || stderr });
                    });
                }
                else if (toolName === 'take_screenshot') {
                    system_tools_1.SystemTools.takeScreenshot(SCREENSHOTS_DIR).then((res) => resolve(res));
                }
                else {
                    resolve({ success: false, message: 'Tool not recognized.' });
                }
            });
        });
        // 2. Window Controls
        electron_1.ipcMain.on('window-min', () => mainWindow?.minimize());
        electron_1.ipcMain.on('window-max', () => (mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize()));
        electron_1.ipcMain.on('window-close', () => mainWindow?.close());
        electron_1.ipcMain.handle('window:control', (_, action) => {
            if (!mainWindow)
                return;
            if (action === 'minimize')
                mainWindow.minimize();
            else if (action === 'maximize')
                (mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize());
            else if (action === 'close')
                mainWindow.close();
        });
        // 3. Telemetry & App Info
        electron_1.ipcMain.handle('sys:telemetry', () => (0, system_tools_1.getSystemMetrics)());
        electron_1.ipcMain.handle('get-system-metrics', () => (0, system_tools_1.getSystemMetrics)());
        electron_1.ipcMain.handle('app:getInfo', () => ({
            name: 'skai',
            productName: 'SKAI',
            version: '0.0.1',
            author: 'Sumeet Kumar',
            tagline: 'Powered by SK Enterprises',
            platform: process.platform,
            appDataPath: APPDATA_DIR,
        }));
        // 4. Secrets Vault (SafeStorage DPAPI)
        electron_1.ipcMain.handle('secrets:getApiKey', (_, provider) => getEncryptedApiKey(provider));
        electron_1.ipcMain.handle('secrets:setApiKey', (_, provider, key) => setEncryptedApiKey(provider, key));
        electron_1.ipcMain.handle('secrets:hasApiKey', (_, provider) => !!getEncryptedApiKey(provider));
        // 5. System Tools
        electron_1.ipcMain.handle('sys:open-app', (_, appName) => system_tools_1.SystemTools.openApp(appName));
        electron_1.ipcMain.handle('open-browser', (_, url) => system_tools_1.SystemTools.openBrowser(url));
        electron_1.ipcMain.handle('os:openBrowser', (_, url) => system_tools_1.SystemTools.openBrowser(url));
        electron_1.ipcMain.handle('os:readFile', (_, filePath) => system_tools_1.SystemTools.readFile(filePath));
        electron_1.ipcMain.handle('read-dir', (_, dirPath) => system_tools_1.SystemTools.readDir(dirPath));
        electron_1.ipcMain.handle('write-file', (_, filePath, content) => system_tools_1.SystemTools.writeFile(filePath, content));
        electron_1.ipcMain.handle('os:takeScreenshot', () => system_tools_1.SystemTools.takeScreenshot(SCREENSHOTS_DIR));
        electron_1.ipcMain.handle('web:search', (_, query) => system_tools_1.SystemTools.webSearch(query));
        electron_1.ipcMain.handle('search:localFiles', (_, query, baseDir) => system_tools_1.SystemTools.searchLocalFiles(query, baseDir));
        createWindow();
        electron_1.app.on('activate', () => {
            if (electron_1.BrowserWindow.getAllWindows().length === 0)
                createWindow();
        });
    });
}
electron_1.app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        electron_1.app.quit();
});
