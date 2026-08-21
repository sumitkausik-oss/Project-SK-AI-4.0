"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * SKAI — Senior Architect Preload Context Bridge
 * Product: SKAI Platform | Powered by SK Enterprises
 * Lead Architect: Sumeet Kumar | Version: 4.1.0
 */
const electron_1 = require("electron");
// 1. Expose window.electron per user directive
electron_1.contextBridge.exposeInMainWorld('electron', {
    ipcRenderer: {
        send: (channel, data) => electron_1.ipcRenderer.send(channel, data),
        invoke: (channel, data) => electron_1.ipcRenderer.invoke(channel, data),
        on: (channel, func) => {
            const sub = (_e, ...args) => func(...args);
            electron_1.ipcRenderer.on(channel, sub);
            return () => electron_1.ipcRenderer.removeListener(channel, sub);
        },
    },
});
// 2. Expose window.skaiApi for comprehensive HUD controls
electron_1.contextBridge.exposeInMainWorld('skaiApi', {
    getAppInfo: () => ({
        name: 'skai',
        productName: 'SKAI',
        version: '4.1.0',
        author: 'Sumeet Kumar',
        tagline: 'Powered by SK Enterprises',
    }),
    getTelemetry: () => electron_1.ipcRenderer.invoke('sys:telemetry'),
    windowControl: (action) => electron_1.ipcRenderer.invoke('window:control', action),
    // Secrets & Encrypted Keys (SafeStorage)
    getApiKey: (provider) => electron_1.ipcRenderer.invoke('secrets:getApiKey', provider),
    setApiKey: (provider, key) => electron_1.ipcRenderer.invoke('secrets:setApiKey', provider, key),
    hasApiKey: (provider) => electron_1.ipcRenderer.invoke('secrets:hasApiKey', provider),
    validateGoogleKey: (key) => electron_1.ipcRenderer.invoke('secrets:validateGoogleKey', key),
    validateHuggingFaceToken: (token) => electron_1.ipcRenderer.invoke('secrets:validateHuggingFaceToken', token),
    // OS Control & Tools
    os: {
        openApp: (appName) => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName: 'open_application', args: { app_name: appName } }),
        openBrowser: (urlOrQuery) => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName: 'open_browser', args: { url: urlOrQuery } }),
        openDrive: (target) => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName: 'open_drive_or_folder', args: { target } }),
        takeScreenshot: () => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName: 'take_screenshot', args: {} }),
        executeSystemTool: (toolName, args) => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName, args }),
    },
    // Permissions & Safety
    permissions: {
        getPolicy: () => electron_1.ipcRenderer.invoke('permissions:getPolicy'),
        savePolicy: (policy) => electron_1.ipcRenderer.invoke('permissions:savePolicy', policy),
    },
});
