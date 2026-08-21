"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
const path_1 = require("path");
const child_process_1 = require("child_process");
const os_1 = __importDefault(require("os"));
const fs_1 = __importDefault(require("fs"));
let mainWindow = null;
const vaultPath = (0, path_1.join)(electron_1.app.getPath('userData'), 'skai_vault.json');
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
    // Grant all hardware audio/video permissions unconditionally
    electron_1.session.defaultSession.setPermissionRequestHandler((_wc, permission, callback) => {
        callback(['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture', 'notifications'].includes(permission));
    });
    electron_1.session.defaultSession.setPermissionCheckHandler((_wc, permission) => {
        return ['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'].includes(permission);
    });
    const distPath = (0, path_1.join)(__dirname, '../../dist/index.html');
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev && !process.env.LOAD_LOCAL) {
        mainWindow.loadURL('http://localhost:5173').catch(() => {
            if (fs_1.default.existsSync(distPath)) {
                mainWindow?.loadFile(distPath);
            }
        });
    }
    else if (fs_1.default.existsSync(distPath)) {
        mainWindow.loadFile(distPath);
    }
    else {
        mainWindow.loadURL('http://localhost:5173').catch(() => { });
    }
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}
electron_1.app.whenReady().then(() => {
    // 1. API Key Vault (SafeStorage DPAPI)
    electron_1.ipcMain.handle('save-api-keys', async (_e, { geminiKey, hfToken }) => {
        try {
            let encryptedGemini = '';
            let encryptedHf = '';
            if (electron_1.safeStorage.isEncryptionAvailable()) {
                if (geminiKey)
                    encryptedGemini = electron_1.safeStorage.encryptString(geminiKey.trim()).toString('base64');
                if (hfToken)
                    encryptedHf = electron_1.safeStorage.encryptString(hfToken.trim()).toString('base64');
            }
            else {
                if (geminiKey)
                    encryptedGemini = Buffer.from(geminiKey.trim()).toString('base64');
                if (hfToken)
                    encryptedHf = Buffer.from(hfToken.trim()).toString('base64');
            }
            fs_1.default.writeFileSync(vaultPath, JSON.stringify({ geminiKey: encryptedGemini, hfToken: encryptedHf }, null, 2), 'utf-8');
            return { success: true };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    });
    electron_1.ipcMain.handle('get-api-keys', async () => {
        try {
            if (!fs_1.default.existsSync(vaultPath))
                return { geminiKey: '', hfToken: '' };
            const data = JSON.parse(fs_1.default.readFileSync(vaultPath, 'utf-8'));
            let geminiKey = '';
            let hfToken = '';
            if (electron_1.safeStorage.isEncryptionAvailable()) {
                if (data.geminiKey)
                    geminiKey = electron_1.safeStorage.decryptString(Buffer.from(data.geminiKey, 'base64'));
                if (data.hfToken)
                    hfToken = electron_1.safeStorage.decryptString(Buffer.from(data.hfToken, 'base64'));
            }
            else {
                if (data.geminiKey)
                    geminiKey = Buffer.from(data.geminiKey, 'base64').toString('utf-8');
                if (data.hfToken)
                    hfToken = Buffer.from(data.hfToken, 'base64').toString('utf-8');
            }
            return { geminiKey, hfToken };
        }
        catch {
            return { geminiKey: '', hfToken: '' };
        }
    });
    electron_1.ipcMain.handle('secrets:getApiKey', async (_, provider) => {
        try {
            if (!fs_1.default.existsSync(vaultPath))
                return '';
            const data = JSON.parse(fs_1.default.readFileSync(vaultPath, 'utf-8'));
            const raw = provider === 'huggingface' ? data.hfToken : data.geminiKey;
            if (!raw)
                return '';
            return electron_1.safeStorage.isEncryptionAvailable()
                ? electron_1.safeStorage.decryptString(Buffer.from(raw, 'base64'))
                : Buffer.from(raw, 'base64').toString('utf-8');
        }
        catch {
            return '';
        }
    });
    electron_1.ipcMain.handle('secrets:setApiKey', async (_, provider, key) => {
        try {
            let current = {};
            if (fs_1.default.existsSync(vaultPath)) {
                try {
                    current = JSON.parse(fs_1.default.readFileSync(vaultPath, 'utf-8'));
                }
                catch { }
            }
            const enc = electron_1.safeStorage.isEncryptionAvailable()
                ? electron_1.safeStorage.encryptString(key.trim()).toString('base64')
                : Buffer.from(key.trim()).toString('base64');
            if (provider === 'huggingface') {
                current.hfToken = enc;
            }
            else {
                current.geminiKey = enc;
            }
            fs_1.default.writeFileSync(vaultPath, JSON.stringify(current, null, 2), 'utf-8');
            return true;
        }
        catch {
            return false;
        }
    });
    electron_1.ipcMain.handle('secrets:hasApiKey', async (_, provider) => {
        try {
            if (!fs_1.default.existsSync(vaultPath))
                return false;
            const data = JSON.parse(fs_1.default.readFileSync(vaultPath, 'utf-8'));
            return provider === 'huggingface' ? Boolean(data.hfToken) : Boolean(data.geminiKey);
        }
        catch {
            return false;
        }
    });
    // 2. Native Windows Tool Execution
    electron_1.ipcMain.handle('execute-system-tool', async (_e, { toolName, args }) => {
        return new Promise((resolve) => {
            const rawTarget = (args?.target || args?.app_name || args?.query || '').trim();
            const target = rawTarget.toLowerCase();
            if (toolName === 'open_drive' || target.includes('drive') || target.includes('folder')) {
                let drive = 'D:\\';
                if (target.includes('c'))
                    drive = 'C:\\';
                if (target.includes('e'))
                    drive = 'E:\\';
                if (rawTarget.match(/^[a-zA-Z]:\\?/))
                    drive = rawTarget.endsWith('\\') ? rawTarget : `${rawTarget}\\`;
                (0, child_process_1.exec)(`explorer.exe "${drive}"`, (err) => {
                    resolve({ success: !err, message: `${drive} drive opened in Explorer.` });
                });
                return;
            }
            if (toolName === 'open_application' || toolName === 'open_browser') {
                if (target.includes('chrome')) {
                    (0, child_process_1.exec)('start chrome', (err) => resolve({ success: !err, message: 'Google Chrome opened.' }));
                }
                else if (target.includes('notepad')) {
                    (0, child_process_1.exec)('start notepad', (err) => resolve({ success: !err, message: 'Notepad opened.' }));
                }
                else if (target.includes('calc')) {
                    (0, child_process_1.exec)('calc', (err) => resolve({ success: !err, message: 'Calculator launched.' }));
                }
                else if (target.includes('code') || target.includes('vs code')) {
                    (0, child_process_1.exec)('code .', (err) => resolve({ success: !err, message: 'VS Code launched.' }));
                }
                else if (args?.url) {
                    electron_1.shell.openExternal(args.url).then(() => resolve({ success: true, message: `Opened URL: ${args.url}` }));
                }
                else {
                    (0, child_process_1.exec)(`start "" "${rawTarget}"`, (err) => resolve({ success: !err, message: `Launched ${rawTarget}` }));
                }
                return;
            }
            if (toolName === 'take_screenshot') {
                (0, child_process_1.exec)('powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{PRTSC}\');"', () => {
                    resolve({ success: true, message: 'Screenshot captured.' });
                });
                return;
            }
            resolve({ success: false, message: `Tool ${toolName} not found.` });
        });
    });
    // 3. System Metrics
    electron_1.ipcMain.handle('get-system-metrics', async () => {
        const total = os_1.default.totalmem();
        const free = os_1.default.freemem();
        return {
            totalMemGB: (total / 1024 ** 3).toFixed(1),
            usedMemGB: ((total - free) / 1024 ** 3).toFixed(1),
            memPercent: Math.round(((total - free) / total) * 100),
            cpuCores: os_1.default.cpus().length,
            platform: `${os_1.default.type()} (${os_1.default.arch()})`,
        };
    });
    electron_1.ipcMain.handle('sys:telemetry', async () => {
        const total = os_1.default.totalmem();
        const free = os_1.default.freemem();
        return {
            totalMemGB: (total / 1024 ** 3).toFixed(1),
            usedMemGB: ((total - free) / 1024 ** 3).toFixed(1),
            ramPercent: Math.round(((total - free) / total) * 100),
            cpuCores: os_1.default.cpus().length,
            cpuPercent: 15,
            uptimeHours: (os_1.default.uptime() / 3600).toFixed(1),
            platform: `${os_1.default.type()} (${os_1.default.arch()})`,
            hostname: os_1.default.hostname(),
        };
    });
    // 4. Permissions & Policy Mock/Storage
    electron_1.ipcMain.handle('permissions:getPolicy', async () => ({
        auto_approve_read_only: true,
        auto_approve_reversible: true,
        require_confirmation_for_destructive: true,
        web_tools_enabled: true,
    }));
    electron_1.ipcMain.handle('permissions:savePolicy', async () => ({ success: true }));
    // 5. Window Controls
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
    createWindow();
    electron_1.app.on('activate', () => {
        if (electron_1.BrowserWindow.getAllWindows().length === 0)
            createWindow();
    });
});
electron_1.app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        electron_1.app.quit();
});
