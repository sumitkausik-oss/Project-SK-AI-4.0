import { ipcMain, safeStorage, app } from 'electron';
import fs from 'fs';
import path from 'path';

const configPath = path.join(app.getPath('userData'), 'skai_vault.json');

export function registerKeyStoreHandlers() {
  ipcMain.handle('save-api-keys', async (_event, keys: { geminiKey: string; hfToken?: string }) => {
    try {
      let encryptedGemini = '';
      let encryptedHf = '';

      if (safeStorage.isEncryptionAvailable()) {
        if (keys.geminiKey) {
          encryptedGemini = safeStorage.encryptString(keys.geminiKey.trim()).toString('base64');
        }
        if (keys.hfToken) {
          encryptedHf = safeStorage.encryptString(keys.hfToken.trim()).toString('base64');
        }
      } else {
        if (keys.geminiKey) {
          encryptedGemini = Buffer.from(keys.geminiKey.trim()).toString('base64');
        }
        if (keys.hfToken) {
          encryptedHf = Buffer.from(keys.hfToken.trim()).toString('base64');
        }
      }

      fs.writeFileSync(
        configPath,
        JSON.stringify({ geminiKey: encryptedGemini, hfToken: encryptedHf }, null, 2),
        'utf-8'
      );
      return { success: true };
    } catch (e: any) {
      return { success: false, error: e.message };
    }
  });

  ipcMain.handle('get-api-keys', async () => {
    try {
      if (!fs.existsSync(configPath)) return { geminiKey: '', hfToken: '' };
      const data = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

      let geminiKey = '';
      let hfToken = '';

      if (safeStorage.isEncryptionAvailable()) {
        if (data.geminiKey) {
          geminiKey = safeStorage.decryptString(Buffer.from(data.geminiKey, 'base64'));
        }
        if (data.hfToken) {
          hfToken = safeStorage.decryptString(Buffer.from(data.hfToken, 'base64'));
        }
      } else {
        if (data.geminiKey) {
          geminiKey = Buffer.from(data.geminiKey, 'base64').toString('utf-8');
        }
        if (data.hfToken) {
          hfToken = Buffer.from(data.hfToken, 'base64').toString('utf-8');
        }
      }

      return { geminiKey, hfToken };
    } catch {
      return { geminiKey: '', hfToken: '' };
    }
  });
}
