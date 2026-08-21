"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * SKAI — Preload Script Context Bridge
 * Product: SKAI
 * Powered by SK Enterprises | Author: Sumeet Kumar
 * Version: 0.0.1
 */
const electron_1 = require("electron");
// 1. Expose window.electron per user directive
electron_1.contextBridge.exposeInMainWorld('electron', {
    ipcRenderer: {
        send: (channel, data) => electron_1.ipcRenderer.send(channel, data),
        invoke: (channel, data) => electron_1.ipcRenderer.invoke(channel, data),
        on: (channel, func) => {
            const subscription = (_event, ...args) => func(...args);
            electron_1.ipcRenderer.on(channel, subscription);
            return () => electron_1.ipcRenderer.removeListener(channel, subscription);
        },
    },
});
// 2. Expose window.skaiApi for comprehensive HUD controls
electron_1.contextBridge.exposeInMainWorld('skaiApi', {
    getAppInfo: () => electron_1.ipcRenderer.invoke('app:getInfo'),
    getTelemetry: () => electron_1.ipcRenderer.invoke('sys:telemetry'),
    windowControl: (action) => electron_1.ipcRenderer.invoke('window:control', action),
    // Secrets & Encrypted Keys (SafeStorage)
    getApiKey: (provider) => electron_1.ipcRenderer.invoke('secrets:getApiKey', provider),
    setApiKey: (provider, key) => electron_1.ipcRenderer.invoke('secrets:setApiKey', provider, key),
    hasApiKey: (provider) => electron_1.ipcRenderer.invoke('secrets:hasApiKey', provider),
    // OS Control & Tools
    os: {
        openApp: (appName) => electron_1.ipcRenderer.invoke('sys:open-app', appName),
        openBrowser: (urlOrQuery) => electron_1.ipcRenderer.invoke('open-browser', urlOrQuery),
        readFile: (filePath) => electron_1.ipcRenderer.invoke('os:readFile', filePath),
        writeFile: (filePath, content) => electron_1.ipcRenderer.invoke('write-file', filePath, content),
        listFolder: (folderPath) => electron_1.ipcRenderer.invoke('read-dir', folderPath),
        takeScreenshot: () => electron_1.ipcRenderer.invoke('os:takeScreenshot'),
        executeSystemTool: (toolName, args) => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName, args }),
    },
    // Search
    search: {
        localFiles: (query, baseDir) => electron_1.ipcRenderer.invoke('search:localFiles', query, baseDir),
        web: (query) => electron_1.ipcRenderer.invoke('web:search', query),
    },
});
