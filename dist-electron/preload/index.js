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
    validateGoogleKey: (key) => electron_1.ipcRenderer.invoke('secrets:validateGoogleKey', key),
    validateHuggingFaceToken: (token) => electron_1.ipcRenderer.invoke('secrets:validateHuggingFaceToken', token),
    // OS Control & Tools
    os: {
        openApp: (appName) => electron_1.ipcRenderer.invoke('sys:open-app', appName),
        closeApp: (appName) => electron_1.ipcRenderer.invoke('os:closeApp', appName),
        openBrowser: (urlOrQuery) => electron_1.ipcRenderer.invoke('open-browser', urlOrQuery),
        readFile: (filePath) => electron_1.ipcRenderer.invoke('os:readFile', filePath),
        writeFile: (filePath, content, append) => electron_1.ipcRenderer.invoke('os:writeFile', filePath, content, append),
        createFile: (filePath, content) => electron_1.ipcRenderer.invoke('os:createFile', filePath, content),
        listFolder: (folderPath) => electron_1.ipcRenderer.invoke('read-dir', folderPath),
        deleteFile: (filePath) => electron_1.ipcRenderer.invoke('os:deleteFile', filePath),
        runTerminal: (command, cwd) => electron_1.ipcRenderer.invoke('sys:terminal', command, cwd),
        takeScreenshot: () => electron_1.ipcRenderer.invoke('os:takeScreenshot'),
        executeSystemTool: (toolName, args) => electron_1.ipcRenderer.invoke('execute-system-tool', { toolName, args }),
    },
    // Search
    search: {
        localFiles: (query, baseDir) => electron_1.ipcRenderer.invoke('search:localFiles', query, baseDir),
        web: (query) => electron_1.ipcRenderer.invoke('web:search', query),
    },
    // Memory
    memory: {
        store: (key, content, tags, category) => electron_1.ipcRenderer.invoke('memory:store', key, content, tags, category),
        query: (query, limit) => electron_1.ipcRenderer.invoke('memory:query', query, limit),
        list: (limit) => electron_1.ipcRenderer.invoke('memory:list', limit),
        delete: (id) => electron_1.ipcRenderer.invoke('memory:delete', id),
    },
    // Permissions & Safety
    permissions: {
        getPolicy: () => electron_1.ipcRenderer.invoke('permissions:getPolicy'),
        savePolicy: (policy) => electron_1.ipcRenderer.invoke('permissions:savePolicy', policy),
        confirmAction: (actionId, approved) => electron_1.ipcRenderer.invoke('permissions:confirmAction', actionId, approved),
    },
    // Coding Tools
    code: {
        readProject: (projectPath) => electron_1.ipcRenderer.invoke('code:readProject', projectPath),
        editFile: (filePath, targetContent, replacementContent) => electron_1.ipcRenderer.invoke('code:editFile', filePath, targetContent, replacementContent),
        runTests: (projectPath, testCommand) => electron_1.ipcRenderer.invoke('code:runTests', projectPath, testCommand),
    },
});
