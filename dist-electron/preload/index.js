"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
electron_1.contextBridge.exposeInMainWorld('electron', {
    ipcRenderer: {
        send: (channel, data) => electron_1.ipcRenderer.send(channel, data),
        invoke: (channel, data) => electron_1.ipcRenderer.invoke(channel, data),
        on: (channel, func) => {
            const sub = (_e, ...args) => func(...args);
            electron_1.ipcRenderer.on(channel, sub);
            return () => electron_1.ipcRenderer.removeListener(channel, sub);
        }
    }
});
