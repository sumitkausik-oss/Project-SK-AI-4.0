/**
 * SKAI — Typed Preload ContextBridge
 * Tagline: Powered by SK Enterprises
 * Founder & Sole Architect: Sumeet Kumar
 */
import { contextBridge, ipcRenderer } from 'electron';

const skaiApi = {
  // App & System
  getAppInfo: () => ipcRenderer.invoke('app:getInfo'),
  windowControl: (action: 'minimize' | 'maximize' | 'close') => ipcRenderer.invoke('window:control', action),

  // Secrets & Encrypted API Keys
  getApiKey: (provider: string) => ipcRenderer.invoke('secrets:getApiKey', provider),
  setApiKey: (provider: string, key: string) => ipcRenderer.invoke('secrets:setApiKey', provider, key),
  hasApiKey: (provider: string) => ipcRenderer.invoke('secrets:hasApiKey', provider),
  validateGoogleKey: (key: string) => ipcRenderer.invoke('secrets:validateGoogleKey', key),

  // AI & Conversational Logic
  sendMessage: (query: string, history: Array<{ role: string; content: string }>) =>
    ipcRenderer.invoke('ai:sendMessage', query, history),

  // OS Control
  os: {
    readFile: (filePath: string) => ipcRenderer.invoke('os:readFile', filePath),
    writeFile: (filePath: string, content: string, append?: boolean) =>
      ipcRenderer.invoke('os:writeFile', filePath, content, append),
    createFile: (filePath: string, content?: string) => ipcRenderer.invoke('os:createFile', filePath, content),
    createFolder: (folderPath: string) => ipcRenderer.invoke('os:createFolder', folderPath),
    listFolder: (folderPath?: string) => ipcRenderer.invoke('os:listFolder', folderPath),
    deleteFile: (filePath: string) => ipcRenderer.invoke('os:deleteFile', filePath),
    openApp: (appName: string) => ipcRenderer.invoke('os:openApp', appName),
    closeApp: (appName: string) => ipcRenderer.invoke('os:closeApp', appName),
    listRunningApps: () => ipcRenderer.invoke('os:listRunningApps'),
    runTerminal: (command: string, cwd?: string) => ipcRenderer.invoke('os:runTerminal', command, cwd),
    takeScreenshot: () => ipcRenderer.invoke('os:takeScreenshot'),
  },

  // Coding Helper Tools
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
    web: (query: string) => ipcRenderer.invoke('search:web', query),
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
    onConfirmRequested: (callback: (action: any) => void) => {
      const handler = (_: any, data: any) => callback(data);
      ipcRenderer.on('permissions:confirmRequest', handler);
      return () => ipcRenderer.removeListener('permissions:confirmRequest', handler);
    },
  },

  // Audit Logs
  audit: {
    getLogs: (limit?: number) => ipcRenderer.invoke('audit:getLogs', limit),
  },
};

contextBridge.exposeInMainWorld('skaiApi', skaiApi);
