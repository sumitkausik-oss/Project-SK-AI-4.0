import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    send: (channel: string, data?: any) => ipcRenderer.send(channel, data),
    invoke: (channel: string, data?: any) => ipcRenderer.invoke(channel, data),
    on: (channel: string, func: (...args: any[]) => void) => {
      const sub = (_e: any, ...args: any[]) => func(...args)
      ipcRenderer.on(channel, sub)
      return () => ipcRenderer.removeListener(channel, sub)
    }
  }
})
