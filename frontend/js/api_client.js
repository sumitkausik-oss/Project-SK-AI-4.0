/**
 * SK ENTERPRISES | Centralized Typed API Client
 * Founder & Sole Architect: Sumeet Kumar
 * Platform: Jarvis Platform V5.0
 */

const API_BASE = "http://127.0.0.1:8000/api/v1";
const API_LEGACY_BASE = "http://127.0.0.1:8000/api";

class SKApiClient {
    constructor(baseUrl = API_BASE) {
        this.baseUrl = baseUrl;
        this.timeoutMs = 10000;
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

    // Cognitive Chat
    async sendChatQuery(query, persona = "JARVIS", language = "hi-IN", userEmail = "sumeet.admin@skenterprises.ai") {
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

    // 2D Agent Town
    async getAgentTownState() {
        return this.request("/agent_town/state");
    }

    // Vedic Astrology & Kundali
    async generateKundali(name, dob, tob, pob) {
        return this.request("/kundali/generate", {
            method: "POST",
            body: JSON.stringify({ name, dob, tob, pob })
        });
    }

    // Universal STEM & Education
    async generateEducationTest(subject, standard, difficulty, topic) {
        return this.request("/education/test", {
            method: "POST",
            body: JSON.stringify({ subject, standard, difficulty, topic })
        });
    }

    // Autonomous Data Analyst
    async analyzeData(datasetName, columns) {
        return this.request("/data/analyze", {
            method: "POST",
            body: JSON.stringify({ dataset_name: datasetName, columns })
        });
    }

    // Cloud DevOps & Zero-Trust
    async executeCloudTask(action, targetUser) {
        return this.request("/cloud/execute", {
            method: "POST",
            body: JSON.stringify({ action, target_user: targetUser })
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

    // Core Intelligence Graph (5-Layer Architecture)
    async getIntelligenceGraph() {
        return this.request("/intelligence/graph");
    }

    async executeNexusTask(task) {
        return this.request("/intelligence/nexus/execute", {
            method: "POST",
            body: JSON.stringify({ task })
        });
    }

    // Structured Agent Hub & Lifecycle
    async listAgents() {
        return this.request("/agents");
    }

    async getAgent(agentKey) {
        return this.request(`/agents/${agentKey}`);
    }

    async dispatchAgentTask(agentKey, task) {
        return this.request(`/agents/${agentKey}/task`, {
            method: "POST",
            body: JSON.stringify({ task })
        });
    }

    // AI Provider Management
    async listProviders() {
        return this.request("/providers");
    }

    async testProvider(providerId) {
        return this.request(`/providers/${providerId}/test`, { method: "POST" });
    }

    // System Diagnostics
    async getDiagnostics() {
        return this.request("/diagnostics/system");
    }
}

window.apiClient = new SKApiClient();
