/**
 * SKAI — Senior Architect Preload Context Bridge
 * Product: SKAI Platform | Powered by SK Enterprises
 * Lead Architect: Sumeet Kumar | Version: 4.1.0
 */
import { contextBridge, ipcRenderer } from 'electron';
import { PermissionPolicy } from '../shared/types';

// 1. Expose window.electron per user directive
contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    send: (channel: string, data?: any) => ipcRenderer.send(channel, data),
    invoke: (channel: string, data?: any) => ipcRenderer.invoke(channel, data),
    on: (channel: string, func: (...args: any[]) => void) => {
      const sub = (_e: any, ...args: any[]) => func(...args);
      ipcRenderer.on(channel, sub);
      return () => ipcRenderer.removeListener(channel, sub);
    },
  },
});

// 2. Expose window.skaiApi for comprehensive HUD controls
contextBridge.exposeInMainWorld('skaiApi', {
  getAppInfo: () => ({
    name: 'skai',
    productName: 'SKAI',
    version: '4.1.0',
    author: 'Sumeet Kumar',
    tagline: 'Powered by SK Enterprises',
  }),
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
    openApp: (appName: string) =>
      ipcRenderer.invoke('execute-system-tool', { toolName: 'open_application', args: { app_name: appName } }),
    openBrowser: (urlOrQuery: string) =>
      ipcRenderer.invoke('execute-system-tool', { toolName: 'open_browser', args: { url: urlOrQuery } }),
    openDrive: (target: string) =>
      ipcRenderer.invoke('execute-system-tool', { toolName: 'open_drive_or_folder', args: { target } }),
    takeScreenshot: () =>
      ipcRenderer.invoke('execute-system-tool', { toolName: 'take_screenshot', args: {} }),
    executeSystemTool: (toolName: string, args: any) =>
      ipcRenderer.invoke('execute-system-tool', { toolName, args }),
  },

  // Permissions & Safety
  permissions: {
    getPolicy: () => ipcRenderer.invoke('permissions:getPolicy'),
    savePolicy: (policy: Partial<PermissionPolicy>) => ipcRenderer.invoke('permissions:savePolicy', policy),
  },
});
