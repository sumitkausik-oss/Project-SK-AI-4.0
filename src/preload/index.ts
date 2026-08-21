/**
 * SKAI — Holographic Preload ContextBridge
 * Product: SKAI
 * Tagline: Powered by SK Enterprises
 * Founder & Sole Architect: Sumeet Kumar
 */
import { contextBridge, ipcRenderer } from 'electron';

const skaiApi = {
  // App & System Telemetry
  getAppInfo: () => ipcRenderer.invoke('app:getInfo'),
  getTelemetry: () => ipcRenderer.invoke('sys:telemetry'),
  windowControl: (action: 'minimize' | 'maximize' | 'close') => ipcRenderer.invoke('window:control', action),

  // Secrets & Encrypted API Keys (SafeStorage)
  getApiKey: (provider: string) => ipcRenderer.invoke('secrets:getApiKey', provider),
  setApiKey: (provider: string, key: string) => ipcRenderer.invoke('secrets:setApiKey', provider, key),
  hasApiKey: (provider: string) => ipcRenderer.invoke('secrets:hasApiKey', provider),
  validateGoogleKey: (key: string) => ipcRenderer.invoke('secrets:validateGoogleKey', key),

  // AI & Bilingual Voice/Chat Engine
  sendMessage: (query: string, history: Array<{ role: string; content: string }>) =>
    ipcRenderer.invoke('ai:sendMessage', query, history),

  // OS Control & Tools
  os: {
    openApp: (appName: string) => ipcRenderer.invoke('sys:open-app', appName),
    closeApp: (appName: string) => ipcRenderer.invoke('os:closeApp', appName),
    readFile: (filePath: string) => ipcRenderer.invoke('os:readFile', filePath),
    writeFile: (filePath: string, content: string, append?: boolean) =>
      ipcRenderer.invoke('os:writeFile', filePath, content, append),
    createFile: (filePath: string, content?: string) => ipcRenderer.invoke('os:createFile', filePath, content),
    listFolder: (folderPath?: string) => ipcRenderer.invoke('os:listFolder', folderPath),
    deleteFile: (filePath: string) => ipcRenderer.invoke('os:deleteFile', filePath),
    runTerminal: (command: string, cwd?: string) => ipcRenderer.invoke('sys:terminal', command, cwd),
    takeScreenshot: () => ipcRenderer.invoke('os:takeScreenshot'),
  },

  // Coding Tools
  code: {
    readProject: (projectPath: string) => ipcRenderer.invoke('code:readProject', projectPath),
    editFile: (filePath: string, targetContent: string, replacementContent: string) =>
      ipcRenderer.invoke('code:editFile', filePath, targetContent, replacementContent),
    runTests: (projectPath: string, testCommand?: string) =>
      ipcRenderer.invoke('code:runTests', projectPath, testCommand),
  },

  // Search
  search: {
    localFiles: (query: string, baseDir?: string) => ipcRenderer.invoke('search:localFiles', query, baseDir),
    web: (query: string) => ipcRenderer.invoke('web:search', query),
  },

  // Local Vector Memory
  memory: {
    store: (key: string, content: string, tags?: string[], category?: string) =>
      ipcRenderer.invoke('memory:store', key, content, tags, category),
    query: (query: string, limit?: number) => ipcRenderer.invoke('memory:query', query, limit),
    list: (limit?: number) => ipcRenderer.invoke('memory:list', limit),
    delete: (id: string) => ipcRenderer.invoke('memory:delete', id),
  },

  // Safety & Permission Policies
  permissions: {
    getPolicy: () => ipcRenderer.invoke('permissions:getPolicy'),
    savePolicy: (policy: any) => ipcRenderer.invoke('permissions:savePolicy', policy),
    confirmAction: (actionId: string, approved: boolean) =>
      ipcRenderer.invoke('permissions:confirmAction', actionId, approved),
  },

  // Audit Logs
  audit: {
    getLogs: (limit?: number) => ipcRenderer.invoke('audit:getLogs', limit),
  },
};

contextBridge.exposeInMainWorld('skaiApi', skaiApi);
