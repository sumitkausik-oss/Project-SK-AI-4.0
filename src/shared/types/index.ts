/**
 * SKAI — Shared Types Definition
 * Product: SKAI
 * Tagline: Powered by SK Enterprises
 * Author / Owner: Sumeet Kumar
 * Version: 0.0.1
 */

export interface SystemTelemetry {
  cpuPercent: number;
  cpuCores: number;
  cpuModel: string;
  ramTotalGB: string;
  ramUsedGB: string;
  ramFreeGB: string;
  ramPercent: number;
  uptimeHours: string;
  platform: string;
  hostname: string;
  timestamp: string;
}

export interface AppInfo {
  name: string;
  productName: string;
  version: string;
  author: string;
  tagline: string;
  platform: string;
  appDataPath: string;
}

export interface StoredMemory {
  id: string;
  key: string;
  content: string;
  category: string;
  tags: string[];
  embedding?: number[];
  created_at: string;
  updated_at: string;
}

export interface PermissionPolicy {
  auto_approve_read_only: boolean;
  auto_approve_reversible: boolean;
  require_confirmation_for_destructive: boolean;
  require_confirmation_for_terminal: boolean;
  web_tools_enabled: boolean;
  allowed_directories: string[];
}

export interface PendingAction {
  action_id: string;
  action_type: string;
  category: string;
  params: Record<string, any>;
  description: string;
  status: string;
  created_at: string;
}

export interface ToolResult {
  success: boolean;
  action?: string;
  result?: any;
  error?: string;
  stdout?: string;
  stderr?: string;
  path?: string;
  thumbnail_data_uri?: string;
  [key: string]: any;
}

export interface SearchMatch {
  filename: string;
  path: string;
  extension: string;
  score: number;
  snippet: string;
}

export interface WebSearchResult {
  title: string;
  link: string;
  snippet: string;
}

export interface ChatMessage {
  id: string;
  sender: 'USER' | 'AI';
  query?: string;
  response: string;
  thought_process?: string;
  voice_text?: string;
  action?: string;
  action_id?: string;
  requires_confirmation?: boolean;
  tool_result?: ToolResult;
  timestamp: string;
}

export interface SkaiApi {
  getAppInfo: () => Promise<AppInfo>;
  getTelemetry: () => Promise<SystemTelemetry>;
  windowControl: (action: 'minimize' | 'maximize' | 'close') => Promise<void>;
  
  // Secrets & Encrypted Keys (SafeStorage)
  getApiKey: (provider: string) => Promise<string>;
  setApiKey: (provider: string, key: string) => Promise<boolean>;
  hasApiKey: (provider: string) => Promise<boolean>;
  validateGoogleKey: (key: string) => Promise<{ valid: boolean; message: string }>;
  validateHuggingFaceToken: (token: string) => Promise<{ valid: boolean; message: string; username?: string }>;

  // AI & Bilingual Voice/Chat Engine
  sendMessage: (query: string, history: Array<{ role: string; content: string }>) => Promise<{
    status: string;
    response: string;
    thought_process?: string;
    voice_text?: string;
    action?: string;
    action_id?: string;
    result?: any;
  }>;

  // OS Control & Tools
  os: {
    openApp: (appName: string) => Promise<ToolResult>;
    closeApp: (appName: string) => Promise<ToolResult>;
    openBrowser: (urlOrQuery: string) => Promise<ToolResult>;
    readFile: (filePath: string) => Promise<ToolResult>;
    writeFile: (filePath: string, content: string, append?: boolean) => Promise<ToolResult>;
    createFile: (filePath: string, content?: string) => Promise<ToolResult>;
    listFolder: (folderPath?: string) => Promise<ToolResult>;
    deleteFile: (filePath: string) => Promise<ToolResult>;
    runTerminal: (command: string, cwd?: string) => Promise<ToolResult>;
    takeScreenshot: () => Promise<ToolResult>;
  };

  // Coding Tools
  code: {
    readProject: (projectPath: string) => Promise<ToolResult>;
    editFile: (filePath: string, targetContent: string, replacementContent: string) => Promise<ToolResult>;
    runTests: (projectPath: string, testCommand?: string) => Promise<ToolResult>;
  };

  // Search
  search: {
    localFiles: (query: string, baseDir?: string) => Promise<{ success: boolean; results: SearchMatch[] }>;
    web: (query: string) => Promise<{ success: boolean; results: WebSearchResult[]; summary: string }>;
  };

  // Local Memory
  memory: {
    store: (key: string, content: string, tags?: string[], category?: string) => Promise<StoredMemory>;
    query: (query: string, limit?: number) => Promise<StoredMemory[]>;
    list: (limit?: number) => Promise<StoredMemory[]>;
    delete: (id: string) => Promise<boolean>;
  };

  // Safety & Permissions
  permissions: {
    getPolicy: () => Promise<PermissionPolicy>;
    savePolicy: (policy: Partial<PermissionPolicy>) => Promise<PermissionPolicy>;
    confirmAction: (actionId: string, approved: boolean) => Promise<ToolResult>;
  };

  // Audit Logs
  audit: {
    getLogs: (limit?: number) => Promise<Array<{ id: string; event_type: string; description: string; severity: string; timestamp: string }>>;
  };
}
