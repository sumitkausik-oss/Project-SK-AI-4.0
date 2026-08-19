/**
 * SK Enterprises | Electron Main Process & Lifecycle Supervisor
 * Founder & Sole Architect: Sumeet Kumar
 * Platform: Jarvis Platform V5.0
 */
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const http = require('http');
const fs = require('fs');
const { spawn, exec } = require('child_process');

let mainWindow = null;
let backendProcess = null;
let isQuitting = false;
let backendPort = 8000;

// Single Instance Lock
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

function findPythonExecutable(rootDir) {
  if (process.platform !== 'win32') {
    return 'python3';
  }

  const candidates = [
    path.join(rootDir, '.venv', 'Scripts', 'python.exe'),
    path.join(rootDir, 'venv', 'Scripts', 'python.exe'),
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Python', 'Python311', 'python.exe'),
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Python', 'Python312', 'python.exe'),
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Python', 'Python310', 'python.exe'),
    path.join(process.env.ProgramFiles || '', 'Python311', 'python.exe'),
    'C:\\Python311\\python.exe',
    'C:\\Python312\\python.exe',
    'python.exe',
    'python'
  ];

  for (const candidate of candidates) {
    if (candidate.includes('\\') && fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return 'python';
}

function findBackendExecutable(rootDir) {
  const possiblePaths = [
    path.join(process.resourcesPath || '', 'dist', 'SK_AI_4.0', 'SK_AI_4.0.exe'),
    path.join(process.resourcesPath || '', 'SK_AI_4.0', 'SK_AI_4.0.exe'),
    path.join(process.resourcesPath || '', 'SK_AI_4.0.exe'),
    path.join(rootDir, 'dist', 'SK_AI_4.0', 'SK_AI_4.0.exe'),
    path.join(rootDir, 'SK_AI_4.0.exe')
  ];

  for (const p of possiblePaths) {
    if (p && fs.existsSync(p)) {
      return p;
    }
  }
  return null;
}

function spawnBackend() {
  const rootDir = app.isPackaged ? path.dirname(app.getPath('exe')) : path.resolve(__dirname, '..');
  
  // 1. Check for standalone compiled backend executable first
  const standaloneExe = findBackendExecutable(rootDir);
  if (standaloneExe) {
    console.log(`[ELECTRON PROCESS SUPERVISOR]: Spawning Standalone Backend Engine:\n  ${standaloneExe}`);
    try {
      backendProcess = spawn(standaloneExe, [], {
        cwd: path.dirname(standaloneExe),
        env: { ...process.env, PYTHONUNBUFFERED: '1' },
        stdio: ['ignore', 'pipe', 'pipe']
      });

      backendProcess.stdout.on('data', (data) => {
        console.log(`[BACKEND STDOUT]: ${data.toString().trim()}`);
      });

      backendProcess.stderr.on('data', (data) => {
        console.error(`[BACKEND STDERR]: ${data.toString().trim()}`);
      });

      backendProcess.on('error', (err) => {
        console.error('[ELECTRON]: Standalone backend spawn error:', err);
        backendProcess = null;
      });

      backendProcess.on('exit', (code, signal) => {
        console.log(`[BACKEND PROCESS]: Exited with code ${code}, signal ${signal}`);
        backendProcess = null;
      });
      return;
    } catch (err) {
      console.error('[ELECTRON]: Failed to spawn standalone backend:', err);
    }
  }

  // 2. Fallback to Python script execution
  const backendScript = path.join(rootDir, 'backend', 'main.py');
  const altBackendScript = path.join(rootDir, 'run_sk_ai_4.py');
  const scriptToRun = fs.existsSync(backendScript) ? backendScript : altBackendScript;

  const pythonCmd = findPythonExecutable(rootDir);
  console.log(`[ELECTRON PROCESS SUPERVISOR]: Starting Python Backend (${pythonCmd} -> ${scriptToRun})...`);

  try {
    backendProcess = spawn(pythonCmd, [scriptToRun], {
      cwd: rootDir,
      env: { ...process.env, PYTHONUNBUFFERED: '1' },
      shell: process.platform === 'win32',
      stdio: ['ignore', 'pipe', 'pipe']
    });

    backendProcess.stdout.on('data', (data) => {
      console.log(`[BACKEND STDOUT]: ${data.toString().trim()}`);
    });

    backendProcess.stderr.on('data', (data) => {
      console.error(`[BACKEND STDERR]: ${data.toString().trim()}`);
    });

    backendProcess.on('error', (err) => {
      console.error('[ELECTRON]: Python backend spawn error:', err);
      backendProcess = null;
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
    icon: fs.existsSync(iconPath) ? iconPath : undefined,
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
  const fileToLoad = fs.existsSync(frontendPath) ? frontendPath : altFrontendPath;

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
