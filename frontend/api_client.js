/**
 * SK ENTERPRISES | SKAI Centralized Typed API Client
 * Founder & Sole Architect: Sumeet Kumar
 * Platform: SKAI — Powered by SK Enterprises
 */

const API_BASE = "http://127.0.0.1:8000/api/v1";
const API_LEGACY_BASE = "http://127.0.0.1:8000/api";

class SKApiClient {
    constructor(baseUrl = API_BASE) {
        this.baseUrl = baseUrl;
        this.timeoutMs = 15000;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

        const defaultHeaders = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...(options.headers || {})
            },
            signal: controller.signal
        };

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || errorData.message || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === "AbortError") {
                console.error(`[API TIMEOUT]: Request to ${endpoint} timed out after ${this.timeoutMs}ms`);
                throw new Error(`Cognitive server request timed out. Please verify backend service on port 8000.`);
            }
            console.error(`[API ERROR] ${endpoint}:`, error.message);
            throw error;
        }
    }

    // Health & System
    async getHealth() {
        return this.request("/health");
    }

    async getSystemStatus() {
        return this.request("/system/status");
    }

    // Cognitive Assistant / Command Processing
    async sendChatQuery(query, persona = "SKAI", language = "en-US", userEmail = "sumeet.admin@skenterprises.ai") {
        return this.request("/chat", {
            method: "POST",
            body: JSON.stringify({
                query: query,
                persona: persona,
                language: language,
                user_email: userEmail
            })
        });
    }

    // ------------------------------------------------------------------------
    // OS Control & Actuators
    // ------------------------------------------------------------------------
    async openApp(app) {
        return this.request("/os/app/open", {
            method: "POST",
            body: JSON.stringify({ app })
        });
    }

    async closeApp(target) {
        return this.request("/os/app/close", {
            method: "POST",
            body: JSON.stringify({ target })
        });
    }

    async listRunningApps() {
        return this.request("/os/app/running");
    }

    async createFile(filePath, content = "") {
        return this.request("/os/file/create", {
            method: "POST",
            body: JSON.stringify({ file_path: filePath, content })
        });
    }

    async createFolder(folderPath) {
        return this.request("/os/folder/create", {
            method: "POST",
            body: JSON.stringify({ folder_path: folderPath })
        });
    }

    async readFile(filePath) {
        return this.request(`/os/file/read?path=${encodeURIComponent(filePath)}`);
    }

    async writeFile(filePath, content, append = false) {
        return this.request("/os/file/write", {
            method: "POST",
            body: JSON.stringify({ file_path: filePath, content, append })
        });
    }

    async deleteFile(targetPath) {
        return this.request(`/os/file/delete?path=${encodeURIComponent(targetPath)}`, {
            method: "DELETE"
        });
    }

    async listFolder(folderPath = "Desktop") {
        return this.request(`/os/folder/list?path=${encodeURIComponent(folderPath)}`);
    }

    async runTerminal(command, cwd = null, timeoutSec = 30) {
        return this.request("/os/terminal/run", {
            method: "POST",
            body: JSON.stringify({ command, cwd, timeout_sec: timeoutSec })
        });
    }

    async searchLocalFiles(query, baseDir = null, contentSearch = true) {
        const params = new URLSearchParams({ q: query, content: contentSearch });
        if (baseDir) params.append("base_dir", baseDir);
        return this.request(`/os/search?${params.toString()}`);
    }

    async takeScreenshot(filename = null) {
        const query = filename ? `?filename=${encodeURIComponent(filename)}` : "";
        return this.request(`/os/screenshot${query}`, { method: "POST" });
    }

    async getProjectTree(path) {
        return this.request(`/os/code/tree?path=${encodeURIComponent(path)}`);
    }

    // ------------------------------------------------------------------------
    // Safety & Permissions
    // ------------------------------------------------------------------------
    async getPermissions() {
        return this.request("/permissions");
    }

    async updatePermissions(policy) {
        return this.request("/permissions", {
            method: "POST",
            body: JSON.stringify(policy)
        });
    }

    async getPendingActions() {
        return this.request("/permissions/pending");
    }

    async confirmAction(actionId, approved = true) {
        return this.request("/permissions/confirm", {
            method: "POST",
            body: JSON.stringify({ action_id: actionId, approved })
        });
    }

    // ------------------------------------------------------------------------
    // Local Memory Management
    // ------------------------------------------------------------------------
    async listMemories(limit = 100) {
        return this.request(`/memory?limit=${limit}`);
    }

    async storeMemory(key, content, tags = ["preference", "user_context"], category = "GENERAL") {
        return this.request("/memory", {
            method: "POST",
            body: JSON.stringify({ key, content, tags, category })
        });
    }

    async searchMemory(query, limit = 5) {
        return this.request(`/memory/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    }

    async deleteMemory(memoryId) {
        return this.request(`/memory/${encodeURIComponent(memoryId)}`, {
            method: "DELETE"
        });
    }

    // Super Admin & Licensing
    async onboardClient(name, age, location, email, phone) {
        return this.request("/admin/onboard_client", {
            method: "POST",
            body: JSON.stringify({ name, age, location, email, phone })
        });
    }

    async generateLicenseKey(name, email, tier = "USER_ANNUAL_365") {
        const query = new URLSearchParams({ name, email, tier }).toString();
        return this.request(`/admin/generate_license?${query}`, { method: "POST" });
    }

    async validateLicenseKey(token) {
        return this.request("/license/validate", {
            method: "POST",
            body: JSON.stringify({ token })
        });
    }

    async toggleUserStatus(email, active) {
        return this.request("/admin/toggle_user", {
            method: "POST",
            body: JSON.stringify({ email, active })
        });
    }

    // System Diagnostics
    async getDiagnostics() {
        return this.request("/diagnostics/system");
    }
}

window.apiClient = new SKApiClient();
