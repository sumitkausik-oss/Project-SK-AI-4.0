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
        backgroundColor: '#030712',
        webPreferences: {
            preload: (0, path_1.join)(__dirname, '../preload/index.js'),
            sandbox: false,
            nodeIntegration: false,
            contextIsolation: true
        }
    });
    electron_1.session.defaultSession.setPermissionRequestHandler((_wc, permission, callback) => {
        callback(['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'].includes(permission));
    });
    electron_1.session.defaultSession.setPermissionCheckHandler((_wc, permission) => {
        return ['media', 'audioCapture', 'microphone', 'camera'].includes(permission);
    });
    if (process.env.ELECTRON_RENDERER_URL) {
        mainWindow.loadURL(process.env.ELECTRON_RENDERER_URL);
    }
    else {
        mainWindow.loadFile((0, path_1.join)(__dirname, '../renderer/index.html'));
    }
}
electron_1.app.whenReady().then(() => {
    // 1. सुरक्षित API Vault
    electron_1.ipcMain.handle('save-api-keys', async (_e, { geminiKey }) => {
        try {
            const encrypted = electron_1.safeStorage.isEncryptionAvailable()
                ? electron_1.safeStorage.encryptString(geminiKey).toString('base64')
                : Buffer.from(geminiKey).toString('base64');
            fs_1.default.writeFileSync(vaultPath, JSON.stringify({ geminiKey: encrypted }), 'utf-8');
            return { success: true };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    });
    electron_1.ipcMain.handle('get-api-keys', async () => {
        try {
            if (!fs_1.default.existsSync(vaultPath))
                return { geminiKey: '' };
            const data = JSON.parse(fs_1.default.readFileSync(vaultPath, 'utf-8'));
            if (!data.geminiKey)
                return { geminiKey: '' };
            const decrypted = electron_1.safeStorage.isEncryptionAvailable()
                ? electron_1.safeStorage.decryptString(Buffer.from(data.geminiKey, 'base64'))
                : Buffer.from(data.geminiKey, 'base64').toString('utf-8');
            return { geminiKey: decrypted };
        }
        catch {
            return { geminiKey: '' };
        }
    });
    // 2. Windows OS टूल्स और ड्राइव कंट्रोल
    electron_1.ipcMain.handle('execute-system-tool', async (_e, { toolName, args }) => {
        return new Promise((resolve) => {
            const target = (args?.target || args?.app_name || args?.query || '').toLowerCase().trim();
            if (toolName === 'open_drive' || target.includes('drive') || target.includes('folder')) {
                let drive = 'D:\\';
                if (target.includes('c'))
                    drive = 'C:\\';
                if (target.includes('e'))
                    drive = 'E:\\';
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
                    (0, child_process_1.exec)(`start "" "${args.app_name || target}"`, (err) => resolve({ success: !err, message: `Launched: ${target}` }));
                }
                return;
            }
            if (toolName === 'take_screenshot') {
                (0, child_process_1.exec)('powershell -command "$p = \\"$env:USERPROFILE\\Pictures\\skai_snap.png\\"; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{PRTSC}\');"', () => {
                    resolve({ success: true, message: 'Screenshot captured.' });
                });
                return;
            }
            resolve({ success: false, message: 'Command executed.' });
        });
    });
    // 3. सिस्टम टेलीमेट्री (RAM Leak Free)
    electron_1.ipcMain.handle('get-system-metrics', async () => {
        const total = os_1.default.totalmem();
        const free = os_1.default.freemem();
        return {
            totalMemGB: (total / 1024 ** 3).toFixed(1),
            usedMemGB: ((total - free) / 1024 ** 3).toFixed(1),
            memPercent: Math.round(((total - free) / total) * 100),
            cpuCores: os_1.default.cpus().length,
            platform: `Windows NT (${os_1.default.arch()})`
        };
    });
    electron_1.ipcMain.on('window-min', () => mainWindow?.minimize());
    electron_1.ipcMain.on('window-max', () => mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize());
    electron_1.ipcMain.on('window-close', () => mainWindow?.close());
    createWindow();
});
electron_1.app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        electron_1.app.quit();
});
