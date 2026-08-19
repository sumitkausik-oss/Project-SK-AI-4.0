/**
 * SK Enterprises | Electron Main Process & Lifecycle Supervisor
 * Founder & Sole Architect: Sumeet Kumar
 * Platform: Jarvis Platform V5.0
 */
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const http = require('http');
const { spawn, exec } = require('child_process');

let mainWindow = null;
let backendProcess = null;
let isQuitting = false;
let backendPort = 8000;

const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  console.log('[ELECTRON]: Another instance is already running. Quitting duplicate...');
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

function checkBackendHealth(port = 8000) {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${port}/api/v1/health`, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.status === 'HEALTHY');
        } catch {
          resolve(false);
        }
      });
    });
    req.on('error', () => resolve(false));
    req.setTimeout(1500, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function waitForBackend(port = 8000, maxRetries = 20) {
  for (let i = 0; i < maxRetries; i++) {
    const healthy = await checkBackendHealth(port);
    if (healthy) return true;
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

function spawnBackend() {
  const rootDir = path.resolve(__dirname, '..');
  const backendScript = path.join(rootDir, 'backend', 'main.py');
  const altBackendScript = path.join(rootDir, 'run_sk_ai_4.py');
  const scriptToRun = require('fs').existsSync(backendScript) ? backendScript : altBackendScript;

  console.log(`[ELECTRON PROCESS SUPERVISOR]: Starting Python Backend (${scriptToRun})...`);
  
  // Use python executable from environment
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

  try {
    backendProcess = spawn(pythonCmd, [scriptToRun], {
      cwd: rootDir,
      env: { ...process.env, PYTHONUNBUFFERED: '1' },
      stdio: ['ignore', 'pipe', 'pipe']
    });

    backendProcess.stdout.on('data', (data) => {
      console.log(`[BACKEND STDOUT]: ${data.toString().trim()}`);
    });

    backendProcess.stderr.on('data', (data) => {
      console.error(`[BACKEND STDERR]: ${data.toString().trim()}`);
    });

    backendProcess.on('exit', (code, signal) => {
      console.log(`[BACKEND PROCESS]: Exited with code ${code}, signal ${signal}`);
      backendProcess = null;
    });
  } catch (err) {
    console.error('[ELECTRON]: Failed to spawn Python backend process:', err);
  }
}

function terminateBackend() {
  if (backendProcess) {
    console.log('[ELECTRON SHUTDOWN]: Gracefully terminating backend child process...');
    try {
      if (process.platform === 'win32') {
        exec(`taskkill /F /PID ${backendProcess.pid}`, () => {});
      } else {
        backendProcess.kill('SIGTERM');
      }
    } catch (e) {
      console.error('[ELECTRON SHUTDOWN ERROR]:', e);
    }
    backendProcess = null;
  }
}

async function createWindow() {
  const iconPath = path.join(__dirname, '..', 'assets', 'jarvis.ico');

  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    title: 'SK AI 4.0 | Project JARVIS 4.0 — Sumeet Kumar',
    backgroundColor: '#030712',
    icon: require('fs').existsSync(iconPath) ? iconPath : undefined,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      webSecurity: true
    }
  });

  mainWindow.setMenuBarVisibility(false);

  // Check if backend is already alive, otherwise spawn
  const isAlive = await checkBackendHealth(backendPort);
  if (!isAlive) {
    spawnBackend();
    const ready = await waitForBackend(backendPort, 24);
    if (!ready) {
      console.warn('[ELECTRON]: Backend did not signal healthy within timeout. Loading interface anyway...');
    } else {
      console.log('[ELECTRON]: Backend connection established & verified healthy.');
    }
  } else {
    console.log('[ELECTRON]: Existing backend engine detected and connected.');
  }

  // Load Frontend HUD
  const frontendPath = path.join(__dirname, '..', 'frontend', 'index.html');
  const altFrontendPath = path.join(__dirname, '..', 'src_frontend', 'index.html');
  const fileToLoad = require('fs').existsSync(frontendPath) ? frontendPath : altFrontendPath;

  mainWindow.loadFile(fileToLoad);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// IPC Handlers
ipcMain.handle('get-backend-status', async () => {
  const healthy = await checkBackendHealth(backendPort);
  return { healthy, port: backendPort, pid: backendProcess ? backendProcess.pid : null };
});

ipcMain.handle('restart-backend', async () => {
  terminateBackend();
  await new Promise((r) => setTimeout(r, 1000));
  spawnBackend();
  return await waitForBackend(backendPort, 20);
});

ipcMain.on('app-control', (event, action) => {
  if (action === 'minimize' && mainWindow) mainWindow.minimize();
  if (action === 'maximize' && mainWindow) {
    if (mainWindow.isMaximized()) mainWindow.unmaximize();
    else mainWindow.maximize();
  }
  if (action === 'close' && mainWindow) mainWindow.close();
});

// App Lifecycle
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('before-quit', () => {
  isQuitting = true;
  terminateBackend();
});

app.on('window-all-closed', () => {
  terminateBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
