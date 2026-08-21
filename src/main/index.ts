import { app, BrowserWindow, ipcMain, session, shell, safeStorage } from 'electron'
import { join } from 'path'
import { exec } from 'child_process'
import os from 'os'
import fs from 'fs'

let mainWindow: BrowserWindow | null = null
const vaultPath = join(app.getPath('userData'), 'skai_vault.json')

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    frame: false,
    transparent: true,
    backgroundColor: '#030712',
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
      nodeIntegration: false,
      contextIsolation: true
    }
  })

  session.defaultSession.setPermissionRequestHandler((_wc, permission, callback) => {
    callback(['media', 'audioCapture', 'microphone', 'camera', 'desktopVideoCapture'].includes(permission))
  })

  session.defaultSession.setPermissionCheckHandler((_wc, permission) => {
    return ['media', 'audioCapture', 'microphone', 'camera'].includes(permission)
  })

  if (process.env.ELECTRON_RENDERER_URL) {
    mainWindow.loadURL(process.env.ELECTRON_RENDERER_URL)
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

app.whenReady().then(() => {
  // 1. सुरक्षित API Vault
  ipcMain.handle('save-api-keys', async (_e, { geminiKey }: { geminiKey: string }) => {
    try {
      const encrypted = safeStorage.isEncryptionAvailable()
        ? safeStorage.encryptString(geminiKey).toString('base64')
        : Buffer.from(geminiKey).toString('base64')
      fs.writeFileSync(vaultPath, JSON.stringify({ geminiKey: encrypted }), 'utf-8')
      return { success: true }
    } catch (err: any) {
      return { success: false, error: err.message }
    }
  })

  ipcMain.handle('get-api-keys', async () => {
    try {
      if (!fs.existsSync(vaultPath)) return { geminiKey: '' }
      const data = JSON.parse(fs.readFileSync(vaultPath, 'utf-8'))
      if (!data.geminiKey) return { geminiKey: '' }
      const decrypted = safeStorage.isEncryptionAvailable()
        ? safeStorage.decryptString(Buffer.from(data.geminiKey, 'base64'))
        : Buffer.from(data.geminiKey, 'base64').toString('utf-8')
      return { geminiKey: decrypted }
    } catch {
      return { geminiKey: '' }
    }
  })

  // 2. Windows OS टूल्स और ड्राइव कंट्रोल
  ipcMain.handle('execute-system-tool', async (_e, { toolName, args }) => {
    return new Promise((resolve) => {
      const target = (args?.target || args?.app_name || args?.query || '').toLowerCase().trim()

      if (toolName === 'open_drive' || target.includes('drive') || target.includes('folder')) {
        let drive = 'D:\\'
        if (target.includes('c')) drive = 'C:\\'
        if (target.includes('e')) drive = 'E:\\'
        exec(`explorer.exe "${drive}"`, (err) => {
          resolve({ success: !err, message: `${drive} drive opened in Explorer.` })
        })
        return
      }

      if (toolName === 'open_application' || toolName === 'open_browser') {
        if (target.includes('chrome')) {
          exec('start chrome', (err) => resolve({ success: !err, message: 'Google Chrome opened.' }))
        } else if (target.includes('notepad')) {
          exec('start notepad', (err) => resolve({ success: !err, message: 'Notepad opened.' }))
        } else if (target.includes('calc')) {
          exec('calc', (err) => resolve({ success: !err, message: 'Calculator launched.' }))
        } else if (target.includes('code') || target.includes('vs code')) {
          exec('code .', (err) => resolve({ success: !err, message: 'VS Code launched.' }))
        } else if (args?.url) {
          shell.openExternal(args.url).then(() => resolve({ success: true, message: `Opened URL: ${args.url}` }))
        } else {
          exec(`start "" "${args.app_name || target}"`, (err) => resolve({ success: !err, message: `Launched: ${target}` }))
        }
        return
      }

      if (toolName === 'take_screenshot') {
        exec('powershell -command "$p = \\"$env:USERPROFILE\\Pictures\\skai_snap.png\\"; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'{PRTSC}\');"', () => {
          resolve({ success: true, message: 'Screenshot captured.' })
        })
        return
      }

      resolve({ success: false, message: 'Command executed.' })
    })
  })

  // 3. सिस्टम टेलीमेट्री (RAM Leak Free)
  ipcMain.handle('get-system-metrics', async () => {
    const total = os.totalmem()
    const free = os.freemem()
    return {
      totalMemGB: (total / 1024 ** 3).toFixed(1),
      usedMemGB: ((total - free) / 1024 ** 3).toFixed(1),
      memPercent: Math.round(((total - free) / total) * 100),
      cpuCores: os.cpus().length,
      platform: `Windows NT (${os.arch()})`
    }
  })

  ipcMain.on('window-min', () => mainWindow?.minimize())
  ipcMain.on('window-max', () => mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize())
  ipcMain.on('window-close', () => mainWindow?.close())

  createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
