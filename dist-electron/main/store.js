"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerKeyStoreHandlers = registerKeyStoreHandlers;
const electron_1 = require("electron");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const configPath = path_1.default.join(electron_1.app.getPath('userData'), 'skai_vault.json');
function registerKeyStoreHandlers() {
    electron_1.ipcMain.handle('save-api-keys', async (_event, keys) => {
        try {
            let encryptedGemini = '';
            let encryptedHf = '';
            if (electron_1.safeStorage.isEncryptionAvailable()) {
                if (keys.geminiKey) {
                    encryptedGemini = electron_1.safeStorage.encryptString(keys.geminiKey.trim()).toString('base64');
                }
                if (keys.hfToken) {
                    encryptedHf = electron_1.safeStorage.encryptString(keys.hfToken.trim()).toString('base64');
                }
            }
            else {
                if (keys.geminiKey) {
                    encryptedGemini = Buffer.from(keys.geminiKey.trim()).toString('base64');
                }
                if (keys.hfToken) {
                    encryptedHf = Buffer.from(keys.hfToken.trim()).toString('base64');
                }
            }
            fs_1.default.writeFileSync(configPath, JSON.stringify({ geminiKey: encryptedGemini, hfToken: encryptedHf }, null, 2), 'utf-8');
            return { success: true };
        }
        catch (e) {
            return { success: false, error: e.message };
        }
    });
    electron_1.ipcMain.handle('get-api-keys', async () => {
        try {
            if (!fs_1.default.existsSync(configPath))
                return { geminiKey: '', hfToken: '' };
            const data = JSON.parse(fs_1.default.readFileSync(configPath, 'utf-8'));
            let geminiKey = '';
            let hfToken = '';
            if (electron_1.safeStorage.isEncryptionAvailable()) {
                if (data.geminiKey) {
                    geminiKey = electron_1.safeStorage.decryptString(Buffer.from(data.geminiKey, 'base64'));
                }
                if (data.hfToken) {
                    hfToken = electron_1.safeStorage.decryptString(Buffer.from(data.hfToken, 'base64'));
                }
            }
            else {
                if (data.geminiKey) {
                    geminiKey = Buffer.from(data.geminiKey, 'base64').toString('utf-8');
                }
                if (data.hfToken) {
                    hfToken = Buffer.from(data.hfToken, 'base64').toString('utf-8');
                }
            }
            return { geminiKey, hfToken };
        }
        catch {
            return { geminiKey: '', hfToken: '' };
        }
    });
}
