"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * SKAI — Typed Preload ContextBridge
 * Tagline: Powered by SK Enterprises
 * Founder & Sole Architect: Sumeet Kumar
 */
const electron_1 = require("electron");
const skaiApi = {
    // App & System
    getAppInfo: () => electron_1.ipcRenderer.invoke('app:getInfo'),
    windowControl: (action) => electron_1.ipcRenderer.invoke('window:control', action),
    // Secrets & Encrypted API Keys
    getApiKey: (provider) => electron_1.ipcRenderer.invoke('secrets:getApiKey', provider),
    setApiKey: (provider, key) => electron_1.ipcRenderer.invoke('secrets:setApiKey', provider, key),
    hasApiKey: (provider) => electron_1.ipcRenderer.invoke('secrets:hasApiKey', provider),
    validateGoogleKey: (key) => electron_1.ipcRenderer.invoke('secrets:validateGoogleKey', key),
    // AI & Conversational Logic
    sendMessage: (query, history) => electron_1.ipcRenderer.invoke('ai:sendMessage', query, history),
    // OS Control
    os: {
        readFile: (filePath) => electron_1.ipcRenderer.invoke('os:readFile', filePath),
        writeFile: (filePath, content, append) => electron_1.ipcRenderer.invoke('os:writeFile', filePath, content, append),
        createFile: (filePath, content) => electron_1.ipcRenderer.invoke('os:createFile', filePath, content),
        createFolder: (folderPath) => electron_1.ipcRenderer.invoke('os:createFolder', folderPath),
        listFolder: (folderPath) => electron_1.ipcRenderer.invoke('os:listFolder', folderPath),
        deleteFile: (filePath) => electron_1.ipcRenderer.invoke('os:deleteFile', filePath),
        openApp: (appName) => electron_1.ipcRenderer.invoke('os:openApp', appName),
        closeApp: (appName) => electron_1.ipcRenderer.invoke('os:closeApp', appName),
        listRunningApps: () => electron_1.ipcRenderer.invoke('os:listRunningApps'),
        runTerminal: (command, cwd) => electron_1.ipcRenderer.invoke('os:runTerminal', command, cwd),
        takeScreenshot: () => electron_1.ipcRenderer.invoke('os:takeScreenshot'),
    },
    // Coding Helper Tools
    code: {
        readProject: (projectPath) => electron_1.ipcRenderer.invoke('code:readProject', projectPath),
        editFile: (filePath, targetContent, replacementContent) => electron_1.ipcRenderer.invoke('code:editFile', filePath, targetContent, replacementContent),
        runTests: (projectPath, testCommand) => electron_1.ipcRenderer.invoke('code:runTests', projectPath, testCommand),
    },
    // Search
    search: {
        localFiles: (query, baseDir) => electron_1.ipcRenderer.invoke('search:localFiles', query, baseDir),
        web: (query) => electron_1.ipcRenderer.invoke('search:web', query),
    },
    // Local Vector Memory
    memory: {
        store: (key, content, tags, category) => electron_1.ipcRenderer.invoke('memory:store', key, content, tags, category),
        query: (query, limit) => electron_1.ipcRenderer.invoke('memory:query', query, limit),
        list: (limit) => electron_1.ipcRenderer.invoke('memory:list', limit),
        delete: (id) => electron_1.ipcRenderer.invoke('memory:delete', id),
    },
    // Safety & Permission Policies
    permissions: {
        getPolicy: () => electron_1.ipcRenderer.invoke('permissions:getPolicy'),
        savePolicy: (policy) => electron_1.ipcRenderer.invoke('permissions:savePolicy', policy),
        confirmAction: (actionId, approved) => electron_1.ipcRenderer.invoke('permissions:confirmAction', actionId, approved),
        onConfirmRequested: (callback) => {
            const handler = (_, data) => callback(data);
            electron_1.ipcRenderer.on('permissions:confirmRequest', handler);
            return () => electron_1.ipcRenderer.removeListener('permissions:confirmRequest', handler);
        },
    },
    // Audit Logs
    audit: {
        getLogs: (limit) => electron_1.ipcRenderer.invoke('audit:getLogs', limit),
    },
};
electron_1.contextBridge.exposeInMainWorld('skaiApi', skaiApi);
