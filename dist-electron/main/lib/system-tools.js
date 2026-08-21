"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.SystemTools = void 0;
exports.resolveUserPath = resolveUserPath;
exports.getCpuUsage = getCpuUsage;
exports.getSystemMetrics = getSystemMetrics;
/**
 * SKAI — Native System Execution Tools & Telemetry
 * Product: SKAI
 * Tagline: Powered by SK Enterprises
 * Author / Owner: Sumeet Kumar
 * Version: 0.0.1
 */
const os = __importStar(require("os"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const https = __importStar(require("https"));
const child_process_1 = require("child_process");
const electron_1 = require("electron");
let lastCpuTimes = [];
function resolveUserPath(rawPath) {
    let p = rawPath.trim().replace(/^["']|["']$/g, '');
    const lower = p.toLowerCase();
    if (lower.startsWith('desktop/') || lower.startsWith('desktop\\') || lower === 'desktop') {
        return path.join(os.homedir(), 'Desktop', p.substring(7));
    }
    else if (lower.startsWith('documents/') || lower.startsWith('documents\\') || lower === 'documents') {
        return path.join(os.homedir(), 'Documents', p.substring(9));
    }
    else if (lower.startsWith('downloads/') || lower.startsWith('downloads\\') || lower === 'downloads') {
        return path.join(os.homedir(), 'Downloads', p.substring(9));
    }
    else if (p.startsWith('~')) {
        return path.join(os.homedir(), p.substring(1));
    }
    if (!path.isAbsolute(p)) {
        return path.join(os.homedir(), 'Desktop', p);
    }
    return p;
}
function getCpuUsage() {
    const cpus = os.cpus();
    let totalIdle = 0;
    let totalTick = 0;
    for (let i = 0; i < cpus.length; i++) {
        const cpu = cpus[i];
        const times = cpu.times;
        const idle = times.idle;
        const total = times.user + times.nice + times.sys + times.irq + times.idle;
        if (lastCpuTimes[i]) {
            const idleDiff = idle - lastCpuTimes[i].idle;
            const totalDiff = total - lastCpuTimes[i].total;
            totalIdle += idleDiff;
            totalTick += totalDiff;
        }
        lastCpuTimes[i] = { idle, total };
    }
    if (totalTick === 0)
        return 15;
    const usage = 100 - (totalIdle / totalTick) * 100;
    return Math.max(0, Math.min(100, Math.round(usage)));
}
function getSystemMetrics() {
    const totalMemBytes = os.totalmem();
    const freeMemBytes = os.freemem();
    const usedMemBytes = totalMemBytes - freeMemBytes;
    const totalMemGB = (totalMemBytes / (1024 * 1024 * 1024)).toFixed(1);
    const usedMemGB = (usedMemBytes / (1024 * 1024 * 1024)).toFixed(1);
    const freeMemGB = (freeMemBytes / (1024 * 1024 * 1024)).toFixed(1);
    const ramPercent = Math.round((usedMemBytes / totalMemBytes) * 100);
    return {
        cpuPercent: getCpuUsage(),
        cpuCores: os.cpus().length,
        cpuModel: os.cpus()[0]?.model || 'Generic Processor',
        ramTotalGB: totalMemGB,
        ramUsedGB: usedMemGB,
        ramFreeGB: freeMemGB,
        ramPercent,
        uptimeHours: (os.uptime() / 3600).toFixed(1),
        platform: process.platform === 'win32' ? 'Windows NT (x64)' : process.platform,
        hostname: os.hostname(),
        timestamp: new Date().toISOString(),
    };
}
exports.SystemTools = {
    openBrowser: async (urlOrQuery) => {
        try {
            let target = urlOrQuery.trim();
            if (!target.startsWith('http://') && !target.startsWith('https://')) {
                target = `https://www.google.com/search?q=${encodeURIComponent(target)}`;
            }
            await electron_1.shell.openExternal(target);
            return { success: true, action: 'OPEN_BROWSER', url: target, message: `Opened browser at ${target}` };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    openApp: async (appName) => {
        return new Promise((resolve) => {
            let cmd = '';
            if (process.platform === 'win32') {
                cmd = `start "" "${appName}"`;
            }
            else if (process.platform === 'darwin') {
                cmd = `open -a "${appName}"`;
            }
            else {
                cmd = `${appName} &`;
            }
            (0, child_process_1.exec)(cmd, (err) => {
                if (err) {
                    resolve({ success: false, error: err.message });
                }
                else {
                    resolve({ success: true, action: 'OPEN_APP', app: appName, message: `Application '${appName}' launched.` });
                }
            });
        });
    },
    closeApp: async (appName) => {
        return new Promise((resolve) => {
            let cmd = '';
            if (process.platform === 'win32') {
                const target = appName.endsWith('.exe') ? appName : `${appName}.exe`;
                cmd = `taskkill /F /IM "${target}"`;
            }
            else {
                cmd = `pkill -f "${appName}"`;
            }
            (0, child_process_1.exec)(cmd, (err) => {
                if (err) {
                    resolve({ success: false, error: err.message });
                }
                else {
                    resolve({ success: true, action: 'CLOSE_APP', app: appName, message: `Application '${appName}' closed.` });
                }
            });
        });
    },
    createFile: async (filePath, content = '') => {
        try {
            const target = resolveUserPath(filePath);
            fs.mkdirSync(path.dirname(target), { recursive: true });
            fs.writeFileSync(target, content, 'utf-8');
            return { success: true, action: 'CREATE_FILE', path: target, message: `File created at ${target}` };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    readFile: async (filePath) => {
        try {
            const target = resolveUserPath(filePath);
            if (!fs.existsSync(target))
                return { success: false, error: `File not found: ${target}` };
            const content = fs.readFileSync(target, 'utf-8');
            return { success: true, action: 'READ_FILE', path: target, content, size: content.length };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    writeFile: async (filePath, content, append = false) => {
        try {
            const target = resolveUserPath(filePath);
            fs.mkdirSync(path.dirname(target), { recursive: true });
            if (append) {
                fs.appendFileSync(target, content, 'utf-8');
            }
            else {
                fs.writeFileSync(target, content, 'utf-8');
            }
            return { success: true, action: 'WRITE_FILE', path: target, message: `File written successfully.` };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    deleteFile: async (filePath) => {
        try {
            const target = resolveUserPath(filePath);
            if (!fs.existsSync(target))
                return { success: false, error: `Target not found: ${target}` };
            const stat = fs.statSync(target);
            if (stat.isDirectory()) {
                fs.rmSync(target, { recursive: true, force: true });
            }
            else {
                fs.unlinkSync(target);
            }
            return { success: true, action: 'DELETE_FILE', path: target, message: `Deleted '${target}' successfully.` };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    readDir: async (dirPath = 'Desktop') => {
        try {
            const target = resolveUserPath(dirPath);
            if (!fs.existsSync(target))
                return { success: false, error: `Directory not found: ${target}` };
            const entries = fs.readdirSync(target, { withFileTypes: true });
            const items = entries.map((e) => ({
                name: e.name,
                isDirectory: e.isDirectory(),
                path: path.join(target, e.name),
            }));
            return { success: true, path: target, count: items.length, items };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    runTerminal: async (command, cwd) => {
        return new Promise((resolve) => {
            const workDir = cwd ? resolveUserPath(cwd) : os.homedir();
            (0, child_process_1.exec)(command, { cwd: workDir, timeout: 30000 }, (err, stdout, stderr) => {
                resolve({
                    success: !err,
                    action: 'TERMINAL_COMMAND',
                    command,
                    cwd: workDir,
                    stdout: stdout.trim(),
                    stderr: stderr.trim(),
                    error: err ? err.message : undefined,
                });
            });
        });
    },
    takeScreenshot: async (outputDir) => {
        try {
            const sources = await electron_1.desktopCapturer.getSources({ types: ['screen'], thumbnailSize: { width: 1920, height: 1080 } });
            if (!sources.length)
                return { success: false, error: 'No display screen detected.' };
            const thumb = sources[0].thumbnail;
            const fileName = `skai_screenshot_${Date.now()}.png`;
            const filePath = path.join(outputDir, fileName);
            fs.writeFileSync(filePath, thumb.toPNG());
            return {
                success: true,
                action: 'TAKE_SCREENSHOT',
                path: filePath,
                thumbnail_data_uri: thumb.toDataURL(),
                message: `Screenshot saved to ${filePath}`,
            };
        }
        catch (err) {
            return { success: false, error: err.message };
        }
    },
    searchLocalFiles: async (queryStr, baseDir) => {
        const q = queryStr.trim().toLowerCase();
        const searchRoot = baseDir ? resolveUserPath(baseDir) : os.homedir();
        const targetDirs = baseDir
            ? [searchRoot]
            : [path.join(os.homedir(), 'Desktop'), path.join(os.homedir(), 'Documents'), path.join(os.homedir(), 'Downloads')];
        const results = [];
        let scanned = 0;
        for (const root of targetDirs) {
            if (!fs.existsSync(root))
                continue;
            const stack = [root];
            while (stack.length > 0 && results.length < 25 && scanned < 1000) {
                const cur = stack.pop();
                try {
                    const entries = fs.readdirSync(cur, { withFileTypes: true });
                    for (const ent of entries) {
                        scanned++;
                        if (ent.name.startsWith('.') || ent.name === 'node_modules' || ent.name === 'AppData')
                            continue;
                        const fullPath = path.join(cur, ent.name);
                        if (ent.isDirectory()) {
                            stack.push(fullPath);
                        }
                        else if (ent.isFile()) {
                            let score = 0;
                            let snippet = '';
                            if (ent.name.toLowerCase().includes(q)) {
                                score += 50;
                            }
                            if (score > 0) {
                                results.push({
                                    filename: ent.name,
                                    path: fullPath,
                                    extension: path.extname(ent.name).toLowerCase(),
                                    score,
                                    snippet,
                                });
                            }
                        }
                    }
                }
                catch { }
            }
        }
        results.sort((a, b) => b.score - a.score);
        return { success: true, results };
    },
    webSearch: async (queryStr) => {
        return new Promise((resolve) => {
            const q = encodeURIComponent(queryStr);
            const url = `https://api.duckduckgo.com/?q=${q}&format=json&no_html=1&skip_disambig=1`;
            https
                .get(url, { headers: { 'User-Agent': 'SKAI-Desktop-Assistant/0.0.1' } }, (res) => {
                let data = '';
                res.on('data', (chunk) => (data += chunk));
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        const results = [];
                        if (json.AbstractText) {
                            results.push({
                                title: json.Heading || queryStr,
                                link: json.AbstractURL || '',
                                snippet: json.AbstractText,
                            });
                        }
                        const summary = json.AbstractText || `Web search completed for '${queryStr}'.`;
                        resolve({ success: true, results, summary });
                    }
                    catch (err) {
                        resolve({ success: false, results: [], summary: `Web search error: ${err.message}` });
                    }
                });
            })
                .on('error', (err) => {
                resolve({ success: false, results: [], summary: `Connection error: ${err.message}` });
            });
        });
    },
};
