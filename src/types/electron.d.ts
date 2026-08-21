import { SkaiApi } from '../shared/types';

export * from '../shared/types';

declare global {
  interface Window {
    skaiApi: SkaiApi;
    electron?: {
      ipcRenderer: {
        send: (channel: string, ...args: any[]) => void;
        invoke: (channel: string, ...args: any[]) => Promise<any>;
        on: (channel: string, func: (...args: any[]) => void) => () => void;
      };
    };
  }
}
