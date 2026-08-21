/**
 * SK Enterprises | SKAI Electron Secure Preload Bridge
 * Founder & Sole Architect: Sumeet Kumar
 * Platform: SKAI — Powered by SK Enterprises
 */
const { contextBridge, ipcRenderer, shell } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
  version: '5.0.0',
  productName: 'SKAI',
  isElectron: true,
  openExternal: (url) => {
    if (typeof url === 'string' && (url.startsWith('http://') || url.startsWith('https://'))) {
      shell.openExternal(url);
    }
  },
  getBackendStatus: () => ipcRenderer.invoke('get-backend-status'),
  restartBackend: () => ipcRenderer.invoke('restart-backend'),
  sendAppControl: (action) => ipcRenderer.send('app-control', action)
});
