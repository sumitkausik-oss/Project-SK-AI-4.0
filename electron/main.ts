/**
 * SKAI — Master Electron Main Process
 * Tagline: Powered by SK Enterprises
 * Founder & Sole Architect: Sumeet Kumar
 * Version: 0.0.1
 */
import { app, BrowserWindow, ipcMain, safeStorage, desktopCapturer } from 'electron';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';
import * as https from 'https';
import { spawn, exec } from 'child_process';

let mainWindow: BrowserWindow | null = null;

// App Data & Storage Directories
const APPDATA_DIR = path.join(app.getPath('appData'), 'SK Enterprises', 'SKAI');
const SECRETS_FILE = path.join(APPDATA_DIR, 'secrets.enc');
const MEMORY_FILE = path.join(APPDATA_DIR, 'skai_memory.json');
const AUDIT_FILE = path.join(APPDATA_DIR, 'audit_log.json');
const SCREENSHOTS_DIR = path.join(APPDATA_DIR, 'screenshots');
const PERMISSIONS_FILE = path.join(APPDATA_DIR, 'permissions_policy.json');

// Ensure directories exist
for (const dir of [APPDATA_DIR, SCREENSHOTS_DIR]) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// -----------------------------------------------------------------------------
// 1. SECRETS & SAFESTORAGE ENCRYPTION
// -----------------------------------------------------------------------------
interface SecretsStore {
  [provider: string]: string; // Base64 encrypted buffer strings
}

function loadSecrets(): SecretsStore {
  if (!fs.existsSync(SECRETS_FILE)) return {};
  try {
    const raw = fs.readFileSync(SECRETS_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error('[SECRETS]: Failed to read secrets file:', err);
    return {};
  }
}

function saveSecrets(secrets: SecretsStore) {
  try {
    fs.writeFileSync(SECRETS_FILE, JSON.stringify(secrets, null, 2), 'utf-8');
  } catch (err) {
    console.error('[SECRETS]: Failed to write secrets file:', err);
  }
}

function getEncryptedApiKey(provider: string): string {
  const secrets = loadSecrets();
  const encBase64 = secrets[provider];
  if (!encBase64) return '';

  if (safeStorage.isEncryptionAvailable()) {
    try {
      const buffer = Buffer.from(encBase64, 'base64');
      return safeStorage.decryptString(buffer);
    } catch (err) {
      console.error('[SECRETS]: Decryption failed:', err);
      return '';
    }
  } else {
    // Plaintext fallback in dev environments where safeStorage is unavailable
    try {
      return Buffer.from(encBase64, 'base64').toString('utf-8');
    } catch {
      return '';
    }
  }
}

function setEncryptedApiKey(provider: string, key: string): boolean {
  try {
    const secrets = loadSecrets();
    if (safeStorage.isEncryptionAvailable()) {
      const encryptedBuffer = safeStorage.encryptString(key.trim());
      secrets[provider] = encryptedBuffer.toString('base64');
    } else {
      secrets[provider] = Buffer.from(key.trim(), 'utf-8').toString('base64');
    }
    saveSecrets(secrets);
    return true;
  } catch (err) {
    console.error('[SECRETS]: Encryption failed:', err);
    return false;
  }
}

// -----------------------------------------------------------------------------
// 2. AUDIT TRAIL REPOSITORY
// -----------------------------------------------------------------------------
interface AuditLog {
  id: string;
  event_type: string;
  description: string;
  severity: 'INFO' | 'WARNING' | 'ERROR';
  timestamp: string;
}

function logAuditEvent(eventType: string, description: string, severity: 'INFO' | 'WARNING' | 'ERROR' = 'INFO') {
  let logs: AuditLog[] = [];
  if (fs.existsSync(AUDIT_FILE)) {
    try {
      logs = JSON.parse(fs.readFileSync(AUDIT_FILE, 'utf-8'));
    } catch {}
  }

  const newLog: AuditLog = {
    id: `log_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
    event_type: eventType,
    description,
    severity,
    timestamp: new Date().toISOString(),
  };

  logs.unshift(newLog);
  if (logs.length > 500) logs = logs.slice(0, 500);

  try {
    fs.writeFileSync(AUDIT_FILE, JSON.stringify(logs, null, 2), 'utf-8');
  } catch {}
}

function getAuditLogs(limit: number = 50): AuditLog[] {
  if (!fs.existsSync(AUDIT_FILE)) return [];
  try {
    const logs: AuditLog[] = JSON.parse(fs.readFileSync(AUDIT_FILE, 'utf-8'));
    return logs.slice(0, limit);
  } catch {
    return [];
  }
}

// -----------------------------------------------------------------------------
// 3. LOCAL VECTOR & MEMORY STORE
// -----------------------------------------------------------------------------
interface MemoryFact {
  id: string;
  key: string;
  content: string;
  category: string;
  tags: string[];
  embedding: number[];
  created_at: string;
  updated_at: string;
}

function generateSimpleEmbedding(text: string): number[] {
  // 64-dimensional semantic character & word hash vector
  const vec = new Array(64).fill(0);
  const words = text.toLowerCase().split(/\s+/);
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    for (let j = 0; j < w.length; j++) {
      const idx = (w.charCodeAt(j) * (j + 1) + i) % 64;
      vec[idx] += 1.0 / (1.0 + j);
    }
  }
  // Normalize vector
  const mag = Math.sqrt(vec.reduce((sum, v) => sum + v * v, 0)) || 1.0;
  return vec.map((v) => v / mag);
}

function cosineSimilarity(vecA: number[], vecB: number[]): number {
  if (vecA.length !== vecB.length) return 0;
  let dot = 0;
  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
  }
  return dot;
}

function loadMemories(): MemoryFact[] {
  if (!fs.existsSync(MEMORY_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(MEMORY_FILE, 'utf-8'));
  } catch {
    return [];
  }
}

function saveMemories(mems: MemoryFact[]) {
  try {
    fs.writeFileSync(MEMORY_FILE, JSON.stringify(mems, null, 2), 'utf-8');
  } catch (err) {
    console.error('[MEMORY]: Failed to save memory store:', err);
  }
}

function storeMemoryFact(key: string, content: string, tags: string[] = [], category: string = 'PREFERENCE'): MemoryFact {
  const mems = loadMemories();
  const existingIdx = mems.findIndex((m) => m.key.toLowerCase() === key.toLowerCase());

  const fact: MemoryFact = {
    id: existingIdx >= 0 ? mems[existingIdx].id : `mem_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
    key: key.trim(),
    content: content.trim(),
    category,
    tags: tags.length ? tags : ['context'],
    embedding: generateSimpleEmbedding(`${key} ${content} ${tags.join(' ')}`),
    created_at: existingIdx >= 0 ? mems[existingIdx].created_at : new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  if (existingIdx >= 0) {
    mems[existingIdx] = fact;
  } else {
    mems.unshift(fact);
  }

  saveMemories(mems);
  logAuditEvent('STORE_MEMORY', `Stored memory fact: '${key}'`);
  return fact;
}

function queryMemories(queryStr: string, limit: number = 5): MemoryFact[] {
  const mems = loadMemories();
  if (!mems.length) return [];

  const queryEmb = generateSimpleEmbedding(queryStr);
  const qWords = new Set(queryStr.toLowerCase().split(/\s+/));

  const scored = mems.map((m) => {
    const sim = cosineSimilarity(queryEmb, m.embedding || generateSimpleEmbedding(m.content));
    let keywordMatches = 0;
    const combined = `${m.key} ${m.content} ${m.tags.join(' ')}`.toLowerCase();
    for (const w of qWords) {
      if (w.length > 2 && combined.includes(w)) keywordMatches++;
    }
    const score = sim * 0.6 + (keywordMatches > 0 ? 0.4 : 0);
    return { fact: m, score };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.filter((s) => s.score > 0.1).slice(0, limit).map((s) => s.fact);
}

function deleteMemoryFact(id: string): boolean {
  let mems = loadMemories();
  const initialLen = mems.length;
  mems = mems.filter((m) => m.id !== id);
  if (mems.length !== initialLen) {
    saveMemories(mems);
    logAuditEvent('DELETE_MEMORY', `Deleted memory ID: ${id}`);
    return true;
  }
  return false;
}

// -----------------------------------------------------------------------------
// 4. SAFETY & PERMISSIONS GATEKEEPER
// -----------------------------------------------------------------------------
interface PermissionPolicy {
  auto_approve_read_only: boolean;
  auto_approve_reversible: boolean;
  require_confirmation_for_destructive: boolean;
  require_confirmation_for_terminal: boolean;
  web_tools_enabled: boolean;
  allowed_directories: string[];
}

function loadPermissionPolicy(): PermissionPolicy {
  const defaults: PermissionPolicy = {
    auto_approve_read_only: true,
    auto_approve_reversible: true,
    require_confirmation_for_destructive: true,
    require_confirmation_for_terminal: true,
    web_tools_enabled: false,
    allowed_directories: [
      path.join(os.homedir(), 'Desktop'),
      path.join(os.homedir(), 'Documents'),
      path.join(os.homedir(), 'Downloads'),
      process.cwd(),
    ],
  };

  if (fs.existsSync(PERMISSIONS_FILE)) {
    try {
      const data = JSON.parse(fs.readFileSync(PERMISSIONS_FILE, 'utf-8'));
      return { ...defaults, ...data };
    } catch {}
  }
  return defaults;
}

function savePermissionPolicy(policy: Partial<PermissionPolicy>): PermissionPolicy {
  const current = loadPermissionPolicy();
  const updated = { ...current, ...policy };
  try {
    fs.writeFileSync(PERMISSIONS_FILE, JSON.stringify(updated, null, 2), 'utf-8');
  } catch {}
  return updated;
}

interface PendingAction {
  action_id: string;
  action_type: string;
  category: 'READ_ONLY' | 'REVERSIBLE_WRITE' | 'DESTRUCTIVE_HIGH_IMPACT';
  params: Record<string, any>;
  description: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  created_at: string;
}

const pendingActions = new Map<string, PendingAction>();

function evaluatePermission(
  actionType: string,
  params: Record<string, any>,
  description: string
): { allowed: boolean; action_id?: string; category: string } {
  const policy = loadPermissionPolicy();
  let category: 'READ_ONLY' | 'REVERSIBLE_WRITE' | 'DESTRUCTIVE_HIGH_IMPACT' = 'READ_ONLY';

  if (['READ_FILE', 'LIST_FOLDER', 'SEARCH_LOCAL_FILES', 'TAKE_SCREENSHOT', 'GET_MEMORY'].includes(actionType)) {
    category = 'READ_ONLY';
  } else if (['CREATE_FILE', 'CREATE_FOLDER', 'OPEN_APP', 'STORE_MEMORY'].includes(actionType)) {
    category = 'REVERSIBLE_WRITE';
  } else {
    category = 'DESTRUCTIVE_HIGH_IMPACT';
  }

  if (category === 'READ_ONLY') return { allowed: true, category };
  if (category === 'REVERSIBLE_WRITE' && policy.auto_approve_reversible) return { allowed: true, category };

  let requiresConfirm = false;
  if (actionType === 'TERMINAL_COMMAND') {
    requiresConfirm = policy.require_confirmation_for_terminal;
  } else {
    requiresConfirm = policy.require_confirmation_for_destructive;
  }

  if (requiresConfirm) {
    const action_id = `act_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    const pending: PendingAction = {
      action_id,
      action_type: actionType,
      category,
      params,
      description,
      status: 'PENDING',
      created_at: new Date().toISOString(),
    };
    pendingActions.set(action_id, pending);
    return { allowed: false, action_id, category };
  }

  return { allowed: true, category };
}

// -----------------------------------------------------------------------------
// 5. OS CONTROL ACTUATOR
// -----------------------------------------------------------------------------
function resolveUserPath(rawPath: string): string {
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

const OSControl = {
  openApp: async (appName: string): Promise<any> => {
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
          logAuditEvent('OPEN_APP', `Launched application: ${appName}`);
          resolve({ success: true, action: 'OPEN_APP', app: appName, message: `Application '${appName}' launched.` });
        }
      });
    });
  },

  closeApp: async (appName: string): Promise<any> => {
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
          logAuditEvent('CLOSE_APP', `Closed application: ${appName}`);
          resolve({ success: true, action: 'CLOSE_APP', app: appName, message: `Application '${appName}' closed.` });
        }
      });
    });
  },

  listRunningApps: async () => {
    return new Promise((resolve) => {
      if (process.platform === 'win32') {
        exec('tasklist /NH /FO CSV', (err, stdout) => {
          if (err) return resolve({ success: false, error: err.message });
          const lines = stdout.split('\n');
          const apps = new Set<string>();
          for (const line of lines) {
            const parts = line.split(',');
            if (parts.length && parts[0]) {
              const name = parts[0].replace(/"/g, '').trim();
              if (name && !name.startsWith('svchost') && !name.startsWith('System')) {
                apps.add(name);
              }
            }
          }
          resolve({ success: true, count: apps.size, apps: Array.from(apps).slice(0, 30) });
        });
      } else {
        exec('ps -ax -o comm=', (err, stdout) => {
          if (err) return resolve({ success: false, error: err.message });
          const list = Array.from(new Set(stdout.split('\n').filter(Boolean))).slice(0, 30);
          resolve({ success: true, count: list.length, apps: list });
        });
      }
    });
  },

  createFile: async (filePath: string, content: string = '') => {
    try {
      const target = resolveUserPath(filePath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, content, 'utf-8');
      logAuditEvent('CREATE_FILE', `Created file at ${target}`);
      return { success: true, action: 'CREATE_FILE', path: target, message: `File created at ${target}` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  readFile: async (filePath: string) => {
    try {
      const target = resolveUserPath(filePath);
      if (!fs.existsSync(target)) return { success: false, error: `File not found: ${target}` };
      const content = fs.readFileSync(target, 'utf-8');
      logAuditEvent('READ_FILE', `Read file at ${target}`);
      return { success: true, action: 'READ_FILE', path: target, content, size: content.length };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  writeFile: async (filePath: string, content: string, append: boolean = false) => {
    try {
      const target = resolveUserPath(filePath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      if (append) {
        fs.appendFileSync(target, content, 'utf-8');
      } else {
        fs.writeFileSync(target, content, 'utf-8');
      }
      logAuditEvent('WRITE_FILE', `Wrote to file ${target} (${append ? 'append' : 'overwrite'})`);
      return { success: true, action: 'WRITE_FILE', path: target, message: `File written successfully.` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  deleteFile: async (filePath: string) => {
    try {
      const target = resolveUserPath(filePath);
      if (!fs.existsSync(target)) return { success: false, error: `Target not found: ${target}` };
      const stat = fs.statSync(target);
      if (stat.isDirectory()) {
        fs.rmSync(target, { recursive: true, force: true });
      } else {
        fs.unlinkSync(target);
      }
      logAuditEvent('DELETE_FILE', `Deleted target at ${target}`, 'WARNING');
      return { success: true, action: 'DELETE_FILE', path: target, message: `Deleted '${target}' successfully.` };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  listFolder: async (folderPath: string = 'Desktop') => {
    try {
      const target = resolveUserPath(folderPath);
      if (!fs.existsSync(target)) return { success: false, error: `Folder not found: ${target}` };
      const entries = fs.readdirSync(target, { withFileTypes: true });
      const items = entries.map((e) => ({
        name: e.name,
        isDirectory: e.isDirectory(),
        path: path.join(target, e.name),
      }));
      logAuditEvent('LIST_FOLDER', `Listed folder at ${target}`);
      return { success: true, path: target, count: items.length, items };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  },

  runTerminalCommand: async (command: string, cwd?: string) => {
    return new Promise((resolve) => {
      const workDir = cwd ? resolveUserPath(cwd) : os.homedir();
      logAuditEvent('RUN_TERMINAL', `Executed command: ${command}`, 'INFO');
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

  takeScreenshot: async () => {
    try {
      const sources = await desktopCapturer.getSources({ types: ['screen'], thumbnailSize: { width: 1920, height: 1080 } });
      if (!sources.length) return { success: false, error: 'No display screen detected.' };

      const thumb = sources[0].thumbnail;
      const fileName = `skai_screenshot_${Date.now()}.png`;
      const filePath = path.join(SCREENSHOTS_DIR, fileName);
      fs.writeFileSync(filePath, thumb.toPNG());

      logAuditEvent('TAKE_SCREENSHOT', `Captured screenshot at ${filePath}`);
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

  searchLocalFiles: async (queryStr: string, baseDir?: string) => {
    const q = queryStr.trim().toLowerCase();
    const searchRoot = baseDir ? resolveUserPath(baseDir) : os.homedir();
    const targetDirs = baseDir
      ? [searchRoot]
      : [path.join(os.homedir(), 'Desktop'), path.join(os.homedir(), 'Documents'), path.join(os.homedir(), 'Downloads')];

    const results: any[] = [];
    const supportedExts = new Set(['.txt', '.py', '.js', '.ts', '.json', '.md', '.html', '.css', '.csv', '.yaml']);
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
              let match_type = 'NONE';
              let snippet = '';

              if (ent.name.toLowerCase().includes(q)) {
                score += 50;
                match_type = 'FILENAME';
              }

              const ext = path.extname(ent.name).toLowerCase();
              if (supportedExts.has(ext)) {
                try {
                  const stat = fs.statSync(fullPath);
                  if (stat.size < 2 * 1024 * 1024) {
                    const text = fs.readFileSync(fullPath, 'utf-8');
                    const lines = text.split('\n');
                    for (let lIdx = 0; lIdx < lines.length; lIdx++) {
                      if (lines[lIdx].toLowerCase().includes(q)) {
                        score += 10;
                        match_type = match_type === 'NONE' ? 'CONTENT' : 'FILENAME_AND_CONTENT';
                        snippet = lines[lIdx].trim().substring(0, 140);
                        break;
                      }
                    }
                  }
                } catch {}
              }

              if (score > 0) {
                results.push({
                  filename: ent.name,
                  path: fullPath,
                  extension: ext,
                  match_type,
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
    logAuditEvent('LOCAL_SEARCH', `Searched files for: '${queryStr}' (${results.length} results)`);
    return { success: true, query: queryStr, count: results.length, results };
  },

  webSearch: async (queryStr: string): Promise<{ success: boolean; results: any[]; summary: string }> => {
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
              const results: any[] = [];
              if (json.AbstractText) {
                results.push({
                  title: json.Heading || queryStr,
                  link: json.AbstractURL || '',
                  snippet: json.AbstractText,
                });
              }
              if (Array.isArray(json.RelatedTopics)) {
                for (const topic of json.RelatedTopics.slice(0, 4)) {
                  if (topic.Text && topic.FirstURL) {
                    results.push({
                      title: topic.Text.split(' - ')[0] || queryStr,
                      link: topic.FirstURL,
                      snippet: topic.Text,
                    });
                  }
                }
              }
              const summary =
                json.AbstractText ||
                (results.length ? results.map((r) => r.snippet).join('\n') : `Search completed for '${queryStr}'.`);
              logAuditEvent('WEB_SEARCH', `Executed web search for '${queryStr}'`);
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

// -----------------------------------------------------------------------------
// 6. GOOGLE GEMINI AI CLIENT & TOOL EXECUTION
// -----------------------------------------------------------------------------
async function callGeminiApi(
  apiKey: string,
  userMessage: string,
  history: Array<{ role: string; content: string }>
): Promise<{ text: string; thought?: string; action?: string; result?: any; requires_confirmation?: boolean; action_id?: string }> {
  const memories = queryMemories(userMessage, 4);
  const memoryContext = memories.map((m) => `[Remembered Fact] ${m.key}: ${m.content}`).join('\n');

  const systemInstruction = `You are SKAI, a sovereign local-first desktop AI assistant powered by SK Enterprises and invented & architected exclusively by Sumeet Kumar.
You live directly on the user's computer with deep OS control powers (reading/writing files, launching/closing apps, executing terminal commands, taking screenshots, searching local files, and storing persistent memory).

Owner / Founder: Sumeet Kumar
Company: SK Enterprises
Platform: SKAI (v0.0.1)

${memoryContext ? `DURABLE LOCAL MEMORY CONTEXT:\n${memoryContext}\n` : ''}

CRITICAL RULES:
1. Always be honest, concise, and helpful.
2. If the user asks to open/close an app, create/read/write/delete a file, run a terminal command, search files, or take a screenshot, state clearly what action you are taking.
3. For destructive operations, state that safety confirmation is required.`;

  // Check for direct local tool intent before calling cloud API
  const qLower = userMessage.toLowerCase().trim();

  // 1. Screenshot
  if (['take screenshot', 'take a screenshot', 'capture screen', 'screenshot'].some((k) => qLower.includes(k))) {
    const res = await OSControl.takeScreenshot();
    return {
      text: res.success ? `📸 **Screenshot Captured:** Saved high-resolution display screenshot.` : `❌ **Screenshot Failed:** ${res.error}`,
      thought: 'Captured display screen via native DesktopCapturer.',
      action: 'TAKE_SCREENSHOT',
      result: res,
    };
  }

  // 2. Open App
  if (qLower.startsWith('open ') && !qLower.includes('file') && !qLower.includes('folder')) {
    const appName = userMessage.replace(/^(open|launch|start)\s+/i, '').trim();
    const res = await OSControl.openApp(appName);
    return {
      text: res.success ? `🚀 **Application Launched:** Successfully opened **${appName}**.` : `❌ **Launch Failed:** ${res.error}`,
      thought: `Executed OS app launch for '${appName}'.`,
      action: 'OPEN_APP',
      result: res,
    };
  }

  // 3. Create File
  if (['create file', 'create a file', 'make file', 'new file'].some((k) => qLower.includes(k))) {
    const match = userMessage.match(/(?:called|named|file)\s+([a-zA-Z0-9_\-\.]+(?:\.[a-zA-Z0-9]+)?)/i);
    const fname = match ? match[1] : 'test.txt';
    const dest = qLower.includes('documents') ? 'Documents' : 'Desktop';
    const filePath = `${dest}/${fname}`;

    const contentMatch = userMessage.match(/(?:with content|saying|containing)\s+["']?([^"']+)["']?/i);
    const content = contentMatch ? contentMatch[1] : '';

    const evalRes = evaluatePermission('CREATE_FILE', { filePath, content }, `Create file '${filePath}'`);
    if (!evalRes.allowed) {
      return {
        text: `🛡️ **Safety Confirmation Required** for creating file \`${filePath}\`.`,
        thought: 'Action requires user permission approval.',
        action: 'CREATE_FILE',
        requires_confirmation: true,
        action_id: evalRes.action_id,
      };
    }

    const res = await OSControl.createFile(filePath, content);
    return {
      text: res.success ? `📄 **File Created:** Successfully created \`${res.path}\`.` : `❌ **Creation Failed:** ${res.error}`,
      thought: `Created file at ${filePath}`,
      action: 'CREATE_FILE',
      result: res,
    };
  }

  // 4. Delete File
  if (['delete file', 'remove file', 'delete folder', 'erase file'].some((k) => qLower.includes(k))) {
    const match = userMessage.match(/(?:delete file|remove file|delete folder|erase file)\s+["']?([^"']+)["']?/i);
    const target = match ? match[1] : 'test.txt';

    const evalRes = evaluatePermission('DELETE_FILE', { targetPath: target }, `Permanently delete '${target}'`);
    if (!evalRes.allowed) {
      return {
        text: `⚠️ **Safety Gate Confirmation Required**\n\nSKAI requires your explicit authorization before permanently deleting:\n• **Target:** \`${target}\`\n• **Action ID:** \`${evalRes.action_id}\``,
        thought: 'Destructive action intercepted by safety gatekeeper.',
        action: 'DELETE_FILE',
        requires_confirmation: true,
        action_id: evalRes.action_id,
      };
    }

    const res = await OSControl.deleteFile(target);
    return {
      text: res.success ? `🗑️ **File Deleted:** Successfully deleted \`${target}\`.` : `❌ **Deletion Failed:** ${res.error}`,
      thought: `Executed file deletion for '${target}'.`,
      action: 'DELETE_FILE',
      result: res,
    };
  }

  // 5. Remember Fact
  if (['remember that', 'remember my', 'store fact', 'remember '].some((k) => qLower.startsWith(k))) {
    const fact = userMessage.replace(/^(remember that|remember my|store fact|remember)\s+/i, '').trim();
    const key = fact.split(' ').slice(0, 4).join(' ');
    const stored = storeMemoryFact(key, fact, ['user_preference'], 'PREFERENCE');
    return {
      text: `🧠 **Fact Remembered:** I have securely recorded this to local memory:\n\n> *"${fact}"*`,
      thought: `Stored durable fact under key '${key}'.`,
      action: 'STORE_MEMORY',
      result: stored,
    };
  }

  // 6. Memory Recall
  if (['what do you remember', 'recall memory', 'my preferences', 'show memories'].some((k) => qLower.includes(k))) {
    const list = loadMemories();
    if (!list.length) {
      return {
        text: `🧠 **Local Memory:** No durable facts saved yet. You can say *"remember that [fact]"* anytime!`,
        thought: 'Retrieved memory list (empty).',
        action: 'GET_MEMORY',
      };
    }
    const memList = list.map((m) => `• **${m.key}**: ${m.content}`).join('\n');
    return {
      text: `🧠 **SKAI Local Memory (${list.length} facts):**\n\n${memList}`,
      thought: `Retrieved ${list.length} stored facts from vector memory.`,
      action: 'GET_MEMORY',
    };
  }

  // 7. Local File Search
  if (['search my documents', 'search files for', 'search my computer', 'search for file', 'find file'].some((k) => qLower.includes(k))) {
    const term = userMessage.replace(/^(search my documents for|search files for|search my computer for|search for file|find file|search for)\s+/i, '').trim();
    const res = await OSControl.searchLocalFiles(term);
    return {
      text: res.success && res.results.length
        ? `🔍 **Search Results for '${term}' (${res.results.length} matches):**\n\n` +
          res.results.slice(0, 5).map((r: any) => `• **${r.filename}** (\`${r.path}\`)${r.snippet ? `\n  > "${r.snippet}"` : ''}`).join('\n\n')
        : `🔍 No local files matched query '${term}'.`,
      thought: `Scanned local directory tree for '${term}'.`,
      action: 'SEARCH_LOCAL_FILES',
      result: res,
    };
  }

  // 8. Terminal Command
  if (['run command', 'run terminal', 'execute command'].some((k) => qLower.startsWith(k))) {
    const cmd = userMessage.replace(/^(run command|run terminal|execute command)\s+/i, '').trim();
    const evalRes = evaluatePermission('TERMINAL_COMMAND', { command: cmd }, `Execute shell command: \`${cmd}\``);
    if (!evalRes.allowed) {
      return {
        text: `🛡️ **Safety Confirmation Required** before executing terminal command:\n\`\`\`powershell\n${cmd}\n\`\`\``,
        thought: 'Terminal command requires user confirmation.',
        action: 'TERMINAL_COMMAND',
        requires_confirmation: true,
        action_id: evalRes.action_id,
      };
    }

    const res: any = await OSControl.runTerminalCommand(cmd);
    return {
      text: res.success
        ? `⚡ **Terminal Output:**\n\`\`\`text\n${res.stdout || '[Command completed with zero output]'}\n\`\`\``
        : `❌ **Command Error:**\n\`\`\`text\n${res.stderr || res.error}\n\`\`\``,
      thought: `Executed command in subprocess: ${cmd}`,
      action: 'TERMINAL_COMMAND',
      result: res,
    };
  }

  // 9. Web Search
  if (['search web for', 'search the web for', 'google ', 'search online for'].some((k) => qLower.startsWith(k))) {
    const query = userMessage.replace(/^(search web for|search the web for|google|search online for)\s+/i, '').trim();
    const res = await OSControl.webSearch(query);
    return {
      text: res.success ? `🌐 **Web Search Results for '${query}':**\n\n${res.summary}` : `❌ **Web Search Error:** ${res.summary}`,
      thought: `Queried DuckDuckGo web search API for '${query}'.`,
      action: 'WEB_SEARCH',
      result: res,
    };
  }

  // 10. Fallback to Google Gemini API if key is present
  if (apiKey) {
    try {
      const contents = history.map((h) => ({
        role: h.role === 'AI' || h.role === 'model' ? 'model' : 'user',
        parts: [{ text: h.content }],
      }));
      contents.push({ role: 'user', parts: [{ text: userMessage }] });

      const requestBody = JSON.stringify({
        system_instruction: { parts: [{ text: systemInstruction }] },
        contents,
      });

      const responseText = await new Promise<string>((resolve, reject) => {
        const req = https.request(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Content-Length': Buffer.byteLength(requestBody),
            },
          },
          (res) => {
            let data = '';
            res.on('data', (chunk) => (data += chunk));
            res.on('end', () => {
              try {
                const parsed = JSON.parse(data);
                if (parsed.error) {
                  reject(new Error(parsed.error.message || 'Gemini API Error'));
                } else if (parsed.candidates && parsed.candidates[0]?.content?.parts?.[0]?.text) {
                  resolve(parsed.candidates[0].content.parts[0].text);
                } else {
                  resolve("I've processed your request.");
                }
              } catch (e: any) {
                reject(e);
              }
            });
          }
        );
        req.on('error', reject);
        req.write(requestBody);
        req.end();
      });

      return {
        text: responseText,
        thought: 'Processed reasoning via Google Gemini 2.0 Flash engine.',
      };
    } catch (err: any) {
      console.warn('[GEMINI API WARNING]:', err.message);
      // Fallback gracefully
    }
  }

  // Standard Offline Assistant Response
  return {
    text: `Hello! I am **SKAI**, your local desktop AI assistant powered by **SK Enterprises** (Sumeet Kumar).\n\nYou can ask me to **open applications**, **create or view files**, **take a screenshot**, **remember preferences**, or **search your computer**. To enable generative AI answers, enter your Google API key in the **Settings** panel.`,
    thought: 'Provided local-first response; Google API key not configured or offline mode active.',
  };
}

// -----------------------------------------------------------------------------
// 7. WINDOW INITIALIZATION & IPC HANDLERS
// -----------------------------------------------------------------------------
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1360,
    height: 860,
    minWidth: 1024,
    minHeight: 680,
    frame: false, // Frameless for custom titlebar
    backgroundColor: '#090a10',
    title: 'SKAI — Powered by SK Enterprises | Sumeet Kumar',
    icon: path.join(__dirname, '..', 'assets', 'jarvis.ico'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false,
    },
  });

  const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173').catch(() => {
      mainWindow?.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
    });
  } else {
    mainWindow.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Single Instance Lock
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  app.whenReady().then(() => {
    registerIpcHandlers();
    createWindow();

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// -----------------------------------------------------------------------------
// 8. IPC HANDLERS REGISTRATION
// -----------------------------------------------------------------------------
function registerIpcHandlers() {
  // App Info & System
  ipcMain.handle('app:getInfo', () => ({
    name: 'skai',
    productName: 'SKAI',
    version: '0.0.1',
    author: 'Sumeet Kumar',
    tagline: 'Powered by SK Enterprises',
    platform: process.platform,
    appDataPath: APPDATA_DIR,
  }));

  // Window Controls
  ipcMain.handle('window:control', (_, action: 'minimize' | 'maximize' | 'close') => {
    if (!mainWindow) return;
    if (action === 'minimize') mainWindow.minimize();
    else if (action === 'maximize') mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize();
    else if (action === 'close') mainWindow.close();
  });

  // Secrets & API Keys (SafeStorage Encrypted)
  ipcMain.handle('secrets:getApiKey', (_, provider: string) => {
    return getEncryptedApiKey(provider);
  });

  ipcMain.handle('secrets:setApiKey', (_, provider: string, key: string) => {
    return setEncryptedApiKey(provider, key);
  });

  ipcMain.handle('secrets:hasApiKey', (_, provider: string) => {
    return !!getEncryptedApiKey(provider);
  });

  ipcMain.handle('secrets:validateGoogleKey', async (_, key: string) => {
    return new Promise((resolve) => {
      https
        .get(`https://generativelanguage.googleapis.com/v1beta/models?key=${key.trim()}`, (res) => {
          if (res.statusCode === 200) {
            resolve({ valid: true, message: 'Google API key validated successfully!' });
          } else {
            resolve({ valid: false, message: `Key validation failed with status HTTP ${res.statusCode}` });
          }
        })
        .on('error', (err) => {
          resolve({ valid: false, message: `Validation error: ${err.message}` });
        });
    });
  });

  // Master AI Chat
  ipcMain.handle('ai:sendMessage', async (_, query: string, history: Array<{ role: string; content: string }>) => {
    const key = getEncryptedApiKey('google');
    return callGeminiApi(key, query, history);
  });

  // OS Control Operations
  ipcMain.handle('os:readFile', (_, filePath: string) => OSControl.readFile(filePath));
  ipcMain.handle('os:writeFile', (_, filePath: string, content: string, append?: boolean) => OSControl.writeFile(filePath, content, append));
  ipcMain.handle('os:createFile', (_, filePath: string, content?: string) => OSControl.createFile(filePath, content));
  ipcMain.handle('os:createFolder', (_, folderPath: string) => {
    const target = resolveUserPath(folderPath);
    try {
      fs.mkdirSync(target, { recursive: true });
      logAuditEvent('CREATE_FOLDER', `Created folder at ${target}`);
      return { success: true, path: target };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  });
  ipcMain.handle('os:listFolder', (_, folderPath?: string) => OSControl.listFolder(folderPath));
  ipcMain.handle('os:deleteFile', (_, filePath: string) => OSControl.deleteFile(filePath));
  ipcMain.handle('os:openApp', (_, appName: string) => OSControl.openApp(appName));
  ipcMain.handle('os:closeApp', (_, appName: string) => OSControl.closeApp(appName));
  ipcMain.handle('os:listRunningApps', () => OSControl.listRunningApps());
  ipcMain.handle('os:runTerminal', (_, command: string, cwd?: string) => OSControl.runTerminalCommand(command, cwd));
  ipcMain.handle('os:takeScreenshot', () => OSControl.takeScreenshot());

  // Search
  ipcMain.handle('search:localFiles', (_, query: string, baseDir?: string) => OSControl.searchLocalFiles(query, baseDir));
  ipcMain.handle('search:web', (_, query: string) => OSControl.webSearch(query));

  // Memory
  ipcMain.handle('memory:store', (_, key: string, content: string, tags?: string[], category?: string) =>
    storeMemoryFact(key, content, tags, category)
  );
  ipcMain.handle('memory:query', (_, query: string, limit?: number) => queryMemories(query, limit));
  ipcMain.handle('memory:list', (_, limit?: number) => loadMemories().slice(0, limit || 50));
  ipcMain.handle('memory:delete', (_, id: string) => deleteMemoryFact(id));

  // Coding Tools
  ipcMain.handle('code:readProject', async (_, projectPath: string) => {
    const root = resolveUserPath(projectPath);
    if (!fs.existsSync(root)) return { success: false, error: 'Project path not found.' };

    const tree: any[] = [];
    const readDirRecursive = (dir: string, depth = 0) => {
      if (depth > 4) return;
      try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const ent of entries) {
          if (['.git', 'node_modules', '.venv', 'dist', 'build'].includes(ent.name)) continue;
          const full = path.join(dir, ent.name);
          tree.push({
            name: ent.name,
            path: full,
            relPath: path.relative(root, full),
            isDirectory: ent.isDirectory(),
          });
          if (ent.isDirectory()) readDirRecursive(full, depth + 1);
        }
      } catch {}
    };
    readDirRecursive(root);
    return { success: true, root, count: tree.length, files: tree };
  });

  ipcMain.handle('code:editFile', async (_, filePath: string, targetContent: string, replacementContent: string) => {
    const fullPath = resolveUserPath(filePath);
    if (!fs.existsSync(fullPath)) return { success: false, error: 'File not found.' };
    const content = fs.readFileSync(fullPath, 'utf-8');
    if (!content.includes(targetContent)) return { success: false, error: 'Target snippet not found in file.' };
    const updated = content.replace(targetContent, replacementContent);
    fs.writeFileSync(fullPath, updated, 'utf-8');
    logAuditEvent('CODE_EDIT', `Surgically edited file at ${fullPath}`);
    return { success: true, path: fullPath, message: 'File edited successfully.' };
  });

  ipcMain.handle('code:runTests', async (_, projectPath: string, testCommand: string = 'npm test') => {
    const root = resolveUserPath(projectPath);
    return OSControl.runTerminalCommand(testCommand, root);
  });

  // Safety Policies & Confirmations
  ipcMain.handle('permissions:getPolicy', () => loadPermissionPolicy());
  ipcMain.handle('permissions:savePolicy', (_, policy: Partial<PermissionPolicy>) => savePermissionPolicy(policy));
  ipcMain.handle('permissions:confirmAction', async (_, actionId: string, approved: boolean) => {
    const pending = pendingActions.get(actionId);
    if (!pending) return { success: false, error: 'Pending action not found or expired.' };
    pendingActions.delete(actionId);

    if (!approved) {
      logAuditEvent('REJECT_ACTION', `User rejected action: ${pending.action_type}`, 'WARNING');
      return { success: false, action: pending.action_type, message: 'Action was cancelled by user.' };
    }

    logAuditEvent('APPROVE_ACTION', `User approved action: ${pending.action_type}`, 'INFO');
    // Execute approved action
    if (pending.action_type === 'DELETE_FILE') {
      return OSControl.deleteFile(pending.params.targetPath || pending.params.filePath);
    } else if (pending.action_type === 'TERMINAL_COMMAND') {
      return OSControl.runTerminalCommand(pending.params.command, pending.params.cwd);
    } else if (pending.action_type === 'CLOSE_APP') {
      return OSControl.closeApp(pending.params.appName);
    }
    return { success: true, message: 'Action executed.' };
  });

  // Audit Logs
  ipcMain.handle('audit:getLogs', (_, limit?: number) => getAuditLogs(limit));
}
