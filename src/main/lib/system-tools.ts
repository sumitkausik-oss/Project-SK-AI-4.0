/**
 * SKAI — Native System Execution Tools & Telemetry
 * Product: SKAI
 * Tagline: Powered by SK Enterprises
 * Author / Owner: Sumeet Kumar
 * Version: 0.0.1
 */
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as https from 'https';
import { exec } from 'child_process';
import { desktopCapturer, shell } from 'electron';
import { SystemTelemetry, ToolResult, SearchMatch, WebSearchResult } from '../../shared/types';

let lastCpuTimes: { idle: number; total: number }[] = [];

export function resolveUserPath(rawPath: string): string {
  let p = rawPath.trim().replace(/^["']|["']$/g, '');
  const lower = p.toLowerCase();
  if (lower.startsWith('desktop/') || lower.startsWith('desktop\\') || lower === 'desktop') {
    return path.join(os.homedir(), 'Desktop', p.substring(7));
  } else if (lower.startsWith('documents/') || lower.startsWith('documents\\') || lower === 'documents') {
    return path.join(os.homedir(), 'Documents', p.substring(9));
  } else if (lower.startsWith('downloads/') || lower.startsWith('downloads\\') || lower === 'downloads') {
    return path.join(os.homedir(), 'Downloads', p.substring(9));
  } else if (p.startsWith('~')) {
    return path.join(os.homedir(), p.substring(1));
  }
  if (!path.isAbsolute(p)) {
    return path.join(os.homedir(), 'Desktop', p);
  }
  return p;
}

export function getCpuUsage(): number {
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

  if (totalTick === 0) return 15;
  const usage = 100 - (totalIdle / totalTick) * 100;
  return Math.max(0, Math.min(100, Math.round(usage)));
}

export function getSystemMetrics(): SystemTelemetry {
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

export const SystemTools = {
  openBrowser: async (urlOrQuery: string): Promise<ToolResult> => {
    try {
      let target = urlOrQuery.trim();
      if (!target.startsWith('http://') && !target.startsWith('https://')) {
        target = `https://www.google.com/search?q=${encodeURIComponent(target)}`;
      }
      await shell.openExternal(target);
      return { success: true, action: 'OPEN_BROWSER', url: target, message: `Opened browser at ${target}` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  openApp: async (appName: string): Promise<ToolResult> => {
    return new Promise((resolve) => {
      let cmd = '';
      if (process.platform === 'win32') {
        cmd = `start "" "${appName}"`;
      } else if (process.platform === 'darwin') {
        cmd = `open -a "${appName}"`;
      } else {
        cmd = `${appName} &`;
      }

      exec(cmd, (err) => {
        if (err) {
          resolve({ success: false, error: err.message });
        } else {
          resolve({ success: true, action: 'OPEN_APP', app: appName, message: `Application '${appName}' launched.` });
        }
      });
    });
  },

  closeApp: async (appName: string): Promise<ToolResult> => {
    return new Promise((resolve) => {
      let cmd = '';
      if (process.platform === 'win32') {
        const target = appName.endsWith('.exe') ? appName : `${appName}.exe`;
        cmd = `taskkill /F /IM "${target}"`;
      } else {
        cmd = `pkill -f "${appName}"`;
      }

      exec(cmd, (err) => {
        if (err) {
          resolve({ success: false, error: err.message });
        } else {
          resolve({ success: true, action: 'CLOSE_APP', app: appName, message: `Application '${appName}' closed.` });
        }
      });
    });
  },

  createFile: async (filePath: string, content: string = ''): Promise<ToolResult> => {
    try {
      const target = resolveUserPath(filePath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, content, 'utf-8');
      return { success: true, action: 'CREATE_FILE', path: target, message: `File created at ${target}` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  readFile: async (filePath: string): Promise<ToolResult> => {
    try {
      const target = resolveUserPath(filePath);
      if (!fs.existsSync(target)) return { success: false, error: `File not found: ${target}` };
      const content = fs.readFileSync(target, 'utf-8');
      return { success: true, action: 'READ_FILE', path: target, content, size: content.length };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  writeFile: async (filePath: string, content: string, append: boolean = false): Promise<ToolResult> => {
    try {
      const target = resolveUserPath(filePath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      if (append) {
        fs.appendFileSync(target, content, 'utf-8');
      } else {
        fs.writeFileSync(target, content, 'utf-8');
      }
      return { success: true, action: 'WRITE_FILE', path: target, message: `File written successfully.` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  deleteFile: async (filePath: string): Promise<ToolResult> => {
    try {
      const target = resolveUserPath(filePath);
      if (!fs.existsSync(target)) return { success: false, error: `Target not found: ${target}` };
      const stat = fs.statSync(target);
      if (stat.isDirectory()) {
        fs.rmSync(target, { recursive: true, force: true });
      } else {
        fs.unlinkSync(target);
      }
      return { success: true, action: 'DELETE_FILE', path: target, message: `Deleted '${target}' successfully.` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  readDir: async (dirPath: string = 'Desktop'): Promise<ToolResult> => {
    try {
      const target = resolveUserPath(dirPath);
      if (!fs.existsSync(target)) return { success: false, error: `Directory not found: ${target}` };
      const entries = fs.readdirSync(target, { withFileTypes: true });
      const items = entries.map((e) => ({
        name: e.name,
        isDirectory: e.isDirectory(),
        path: path.join(target, e.name),
      }));
      return { success: true, path: target, count: items.length, items };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  runTerminal: async (command: string, cwd?: string): Promise<ToolResult> => {
    return new Promise((resolve) => {
      const workDir = cwd ? resolveUserPath(cwd) : os.homedir();
      exec(command, { cwd: workDir, timeout: 30000 }, (err, stdout, stderr) => {
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

  takeScreenshot: async (outputDir: string): Promise<ToolResult> => {
    try {
      const sources = await desktopCapturer.getSources({ types: ['screen'], thumbnailSize: { width: 1920, height: 1080 } });
      if (!sources.length) return { success: false, error: 'No display screen detected.' };

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
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  searchLocalFiles: async (queryStr: string, baseDir?: string): Promise<{ success: boolean; results: SearchMatch[] }> => {
    const q = queryStr.trim().toLowerCase();
    const searchRoot = baseDir ? resolveUserPath(baseDir) : os.homedir();
    const targetDirs = baseDir
      ? [searchRoot]
      : [path.join(os.homedir(), 'Desktop'), path.join(os.homedir(), 'Documents'), path.join(os.homedir(), 'Downloads')];

    const results: SearchMatch[] = [];
    let scanned = 0;

    for (const root of targetDirs) {
      if (!fs.existsSync(root)) continue;
      const stack = [root];

      while (stack.length > 0 && results.length < 25 && scanned < 1000) {
        const cur = stack.pop()!;
        try {
          const entries = fs.readdirSync(cur, { withFileTypes: true });
          for (const ent of entries) {
            scanned++;
            if (ent.name.startsWith('.') || ent.name === 'node_modules' || ent.name === 'AppData') continue;
            const fullPath = path.join(cur, ent.name);

            if (ent.isDirectory()) {
              stack.push(fullPath);
            } else if (ent.isFile()) {
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
        } catch {}
      }
    }

    results.sort((a, b) => b.score - a.score);
    return { success: true, results };
  },

  webSearch: async (queryStr: string): Promise<{ success: boolean; results: WebSearchResult[]; summary: string }> => {
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
              const results: WebSearchResult[] = [];
              if (json.AbstractText) {
                results.push({
                  title: json.Heading || queryStr,
                  link: json.AbstractURL || '',
                  snippet: json.AbstractText,
                });
              }
              const summary = json.AbstractText || `Web search completed for '${queryStr}'.`;
              resolve({ success: true, results, summary });
            } catch (err: any) {
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
