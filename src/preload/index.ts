/**
 * SKAI — Preload Script Context Bridge
 * Product: SKAI
 * Powered by SK Enterprises | Author: Sumeet Kumar
 * Version: 0.0.1
 */
import { contextBridge, ipcRenderer } from 'electron';

// 1. Expose window.electron per user directive
contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    send: (channel: string, data?: any) => ipcRenderer.send(channel, data),
    invoke: (channel: string, data?: any) => ipcRenderer.invoke(channel, data),
    on: (channel: string, func: (...args: any[]) => void) => {
      const subscription = (_event: any, ...args: any[]) => func(...args);
      ipcRenderer.on(channel, subscription);
      return () => ipcRenderer.removeListener(channel, subscription);
    },
  },
});

// 2. Expose window.skaiApi for comprehensive HUD controls
contextBridge.exposeInMainWorld('skaiApi', {
  getAppInfo: () => ipcRenderer.invoke('app:getInfo'),
  getTelemetry: () => ipcRenderer.invoke('sys:telemetry'),
  windowControl: (action: 'minimize' | 'maximize' | 'close') => ipcRenderer.invoke('window:control', action),

  // Secrets & Encrypted Keys (SafeStorage)
  getApiKey: (provider: string) => ipcRenderer.invoke('secrets:getApiKey', provider),
  setApiKey: (provider: string, key: string) => ipcRenderer.invoke('secrets:setApiKey', provider, key),
  hasApiKey: (provider: string) => ipcRenderer.invoke('secrets:hasApiKey', provider),

  // OS Control & Tools
  os: {
    openApp: (appName: string) => ipcRenderer.invoke('sys:open-app', appName),
    openBrowser: (urlOrQuery: string) => ipcRenderer.invoke('open-browser', urlOrQuery),
    readFile: (filePath: string) => ipcRenderer.invoke('os:readFile', filePath),
    writeFile: (filePath: string, content: string) => ipcRenderer.invoke('write-file', filePath, content),
    listFolder: (folderPath?: string) => ipcRenderer.invoke('read-dir', folderPath),
    takeScreenshot: () => ipcRenderer.invoke('os:takeScreenshot'),
    executeSystemTool: (toolName: string, args: any) =>
      ipcRenderer.invoke('execute-system-tool', { toolName, args }),
  },

  // Search
  search: {
    localFiles: (query: string, baseDir?: string) => ipcRenderer.invoke('search:localFiles', query, baseDir),
    web: (query: string) => ipcRenderer.invoke('web:search', query),
  },
});
