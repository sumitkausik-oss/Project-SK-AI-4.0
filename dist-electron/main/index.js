"use strict";
/**
 * SKAI — Electron Main Process
 * Product: SKAI | Powered by SK Enterprises
 * Author: Sumeet Kumar
 * Version: 0.0.1
 *
 * Architecture:
 *  - All privileged OS operations live here.
 *  - Renderer never touches fs/shell/child_process directly.
 *  - IPC bridge via preload/index.ts (contextBridge).
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
const path_1 = require("path");
const child_process_1 = require("child_process");
const os_1 = __importDefault(require("os"));
const store_1 = require("./store");
let mainWindow = null;
// ─────────────────────────────────────────────────────────────────────────────
// Window Creation
// ─────────────────────────────────────────────────────────────────────────────
function createWindow() {
    mainWindow = new electron_1.BrowserWindow({
        width: 1440,
        height: 900,
        minWidth: 1024,
        minHeight: 700,
        frame: false,
        transparent: false,
        backgroundColor: '#030712',
        webPreferences: {
            preload: (0, path_1.join)(__dirname, '../preload/index.js'),
            sandbox: false,
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false
        }
    });
    // ── Media / Microphone Permissions ──────────────────────────────────────────
    electron_1.session.defaultSession.setPermissionRequestHandler((_wc, permission, callback) => {
        callback(['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'].includes(permission));
    });
    electron_1.session.defaultSession.setPermissionCheckHandler((_wc, permission) => {
        return ['media', 'audioCapture', 'microphone', 'camera'].includes(permission);
    });
    // ── DevTools shortcut (F12 / Ctrl+Shift+I) ──────────────────────────────────
    mainWindow.webContents.on('before-input-event', (event, input) => {
        if (input.key === 'F12' || (input.control && input.shift && input.key.toLowerCase() === 'i')) {
            mainWindow?.webContents.toggleDevTools();
            event.preventDefault();
        }
    });
    // ── Load renderer ────────────────────────────────────────────────────────────
    // In dev mode, concurrently sets ELECTRON_RENDERER_URL → load Vite dev server.
    // In production, load the built dist/index.html via file:// protocol.
    if (process.env.ELECTRON_RENDERER_URL) {
        mainWindow.loadURL(process.env.ELECTRON_RENDERER_URL);
    }
    else {
        mainWindow.loadFile((0, path_1.join)(__dirname, '../../dist/index.html'));
    }
}
// ─────────────────────────────────────────────────────────────────────────────
// App Ready
// ─────────────────────────────────────────────────────────────────────────────
electron_1.app.whenReady().then(() => {
    // ── Secure Key Vault (DPAPI / safeStorage) ───────────────────────────────────
    // Registers 'save-api-keys' and 'get-api-keys' IPC handlers.
    (0, store_1.registerKeyStoreHandlers)();
    // ── OS Tool Actuator ─────────────────────────────────────────────────────────
    // Handles: open_drive_or_folder, open_application, take_screenshot
    electron_1.ipcMain.handle('execute-system-tool', async (_e, { toolName, args }) => {
        return new Promise((resolve) => {
            const target = (args?.target || args?.app_name || args?.query || '').toLowerCase().trim();
            // Drive / Folder navigation
            if (toolName === 'open_drive_or_folder' || toolName === 'open_drive' ||
                target.includes('drive') || target.includes('folder')) {
                let drive = 'D:\\';
                if (args?.target) {
                    drive = args.target;
                }
                else if (target.includes('c:') || (target.includes('c') && target.includes('drive'))) {
                    drive = 'C:\\';
                }
                else if (target.includes('e:') || (target.includes('e') && target.includes('drive'))) {
                    drive = 'E:\\';
                }
                (0, child_process_1.exec)(`explorer.exe "${drive}"`, (err) => {
                    resolve({ success: !err, message: `${drive} opened in Explorer.` });
                });
                return;
            }
            // Application launch
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
                    (0, child_process_1.exec)(`start "" "${args?.app_name || target}"`, (err) => resolve({ success: !err, message: `Launched: ${target}` }));
                }
                return;
            }
            // Screenshot via PowerShell clipboard capture
            if (toolName === 'take_screenshot') {
                const ps = `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | Out-Null; Add-Type -AssemblyName System.Drawing; $bmp = [System.Drawing.Bitmap]::new([System.Windows.Forms.SystemInformation]::PrimaryMonitorSize.Width,[System.Windows.Forms.SystemInformation]::PrimaryMonitorSize.Height); $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen(0,0,0,0,$bmp.Size); $p = "$env:USERPROFILE\\Pictures\\skai_snap_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"; $bmp.Save($p); Write-Output $p`;
                (0, child_process_1.exec)(`powershell -NonInteractive -Command "${ps}"`, (err, stdout) => {
                    if (err) {
                        resolve({ success: false, message: `Screenshot failed: ${err.message}` });
                    }
                    else {
                        resolve({ success: true, message: `Screenshot saved: ${stdout.trim()}` });
                    }
                });
                return;
            }
            resolve({ success: false, message: `Unknown tool: ${toolName}` });
        });
    });
    // ── System Metrics ────────────────────────────────────────────────────────────
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
    // ── Window Controls ───────────────────────────────────────────────────────────
    electron_1.ipcMain.on('window-min', () => mainWindow?.minimize());
    electron_1.ipcMain.on('window-max', () => mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize());
    electron_1.ipcMain.on('window-close', () => mainWindow?.close());
    createWindow();
});
electron_1.app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        electron_1.app.quit();
});
