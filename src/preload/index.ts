/**
 * SKAI — Preload Script Context Bridge
 * Product: SKAI
 * Powered by SK Enterprises | Author: Sumeet Kumar
 * Version: 0.0.1
 */
import { contextBridge, ipcRenderer } from 'electron';
import { PermissionPolicy } from '../shared/types';

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
  validateGoogleKey: (key: string) => ipcRenderer.invoke('secrets:validateGoogleKey', key),
  validateHuggingFaceToken: (token: string) => ipcRenderer.invoke('secrets:validateHuggingFaceToken', token),

  // OS Control & Tools
  os: {
    openApp: (appName: string) => ipcRenderer.invoke('sys:open-app', appName),
    closeApp: (appName: string) => ipcRenderer.invoke('os:closeApp', appName),
    openBrowser: (urlOrQuery: string) => ipcRenderer.invoke('open-browser', urlOrQuery),
    readFile: (filePath: string) => ipcRenderer.invoke('os:readFile', filePath),
    writeFile: (filePath: string, content: string, append?: boolean) =>
      ipcRenderer.invoke('os:writeFile', filePath, content, append),
    createFile: (filePath: string, content?: string) => ipcRenderer.invoke('os:createFile', filePath, content),
    listFolder: (folderPath?: string) => ipcRenderer.invoke('read-dir', folderPath),
    deleteFile: (filePath: string) => ipcRenderer.invoke('os:deleteFile', filePath),
    runTerminal: (command: string, cwd?: string) => ipcRenderer.invoke('sys:terminal', command, cwd),
    takeScreenshot: () => ipcRenderer.invoke('os:takeScreenshot'),
    executeSystemTool: (toolName: string, args: any) =>
      ipcRenderer.invoke('execute-system-tool', { toolName, args }),
  },

  // Search
  search: {
    localFiles: (query: string, baseDir?: string) => ipcRenderer.invoke('search:localFiles', query, baseDir),
    web: (query: string) => ipcRenderer.invoke('web:search', query),
  },

  // Memory
  memory: {
    store: (key: string, content: string, tags?: string[], category?: string) =>
      ipcRenderer.invoke('memory:store', key, content, tags, category),
    query: (query: string, limit?: number) => ipcRenderer.invoke('memory:query', query, limit),
    list: (limit?: number) => ipcRenderer.invoke('memory:list', limit),
    delete: (id: string) => ipcRenderer.invoke('memory:delete', id),
  },

  // Permissions & Safety
  permissions: {
    getPolicy: () => ipcRenderer.invoke('permissions:getPolicy'),
    savePolicy: (policy: Partial<PermissionPolicy>) => ipcRenderer.invoke('permissions:savePolicy', policy),
    confirmAction: (actionId: string, approved: boolean) =>
      ipcRenderer.invoke('permissions:confirmAction', actionId, approved),
  },

  // Coding Tools
  code: {
    readProject: (projectPath: string) => ipcRenderer.invoke('code:readProject', projectPath),
    editFile: (filePath: string, targetContent: string, replacementContent: string) =>
      ipcRenderer.invoke('code:editFile', filePath, targetContent, replacementContent),
    runTests: (projectPath: string, testCommand?: string) =>
      ipcRenderer.invoke('code:runTests', projectPath, testCommand),
  },
});
