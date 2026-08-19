# API SPECIFICATION — SK AI 4.0 (PROJECT JARVIS 4.0)

**Platform Version:** Jarvis Platform V5.0  
**Base URL:** `http://127.0.0.1:8000/api/v1` (with `/api` legacy aliases)  
**Protocol:** HTTP/1.1 REST + WebSocket  
**Authentication:** Sovereign Master Token / Local IPC  

---

## 1. HEALTH & DIAGNOSTICS

### `GET /api/v1/health`
Liveness probe. Verifies that the FastAPI process is alive and returns uptime.

**Response (200 OK):**
```json
{
  "status": "HEALTHY",
  "version": "5.0.0",
  "timestamp": "2026-08-19T05:35:27.603059",
  "uptime_seconds": 12.45,
  "system": "SK AI 4.0",
  "inventor": "Sumeet Kumar"
}
```

### `GET /api/v1/health/ready`
Readiness probe. Verifies backend and SQLite database connectivity.

**Response (200 OK):**
```json
{
  "status": "READY",
  "database": "CONNECTED",
  "version": "5.0.0",
  "active_nodes": 4,
  "lifetime_license": "ACTIVE - VERIFIED",
  "timestamp": "2026-08-19T05:35:27.603059"
}
```

---

## 2. SYSTEM & IDENTITY

### `GET /api/v1/system/status`
Returns full hardware metrics, platform version, and active cognitive hubs.

**Response (200 OK):**
```json
{
  "status": "ONLINE",
  "timestamp": "2026-08-19T05:35:27.603059",
  "system": "SK AI 4.0",
  "codename": "Project JARVIS 4.0",
  "platform": "Jarvis Platform V5.0",
  "inventor": "Sumeet Kumar",
  "founder": "Sumeet Kumar",
  "sole_architect": "Sumeet Kumar",
  "organization": "SK Enterprises",
  "tier": "Lifetime Master Admin",
  "telemetry": {
    "fps": 60,
    "neural_coherence": "100%",
    "quantum_latency": "0.4ms",
    "active_agents": 4,
    "lifetime_license": "ACTIVE - VERIFIED"
  },
  "hubs": [
    "Agent Town 2D",
    "Visual Hub",
    "Gesture Hub",
    "Vedic Astrology",
    "STEM Matrix",
    "Data Studio"
  ],
  "supported_platforms": [
    "Windows (EXE)",
    "Android (APK)",
    "macOS (DMG)",
    "iOS (IPA/PWA)"
  ]
}
```

---

## 3. COGNITIVE CHAT

### `POST /api/v1/chat`
Processes conversational queries with multi-persona synthesis, prompt sanitization, and thought process generation.

**Request Body:**
```json
{
  "query": "Who is the inventor and creator of this system?",
  "persona": "JARVIS",
  "language": "hi-IN",
  "user_email": "sumeet.admin@skenterprises.ai"
}
```

**Response (200 OK):**
```json
{
  "thought_process": "1. Verifying Immutable Ownership Signature against hardware-locked registry...\n2. Context memories recalled: ['sole_architect']\n3. Validated Sole Inventor, Founder & Architect: Sumeet Kumar (SK Enterprises).\n4. Preparing bilingual Butler/JARVIS acknowledgment.",
  "response": "प्रणाम सुमीत सर! मैं SK AI 4.0 (Project JARVIS 4.0 / Platform V5.0) हूँ।\n\nमेरा निर्माण, वास्तुकला एवं स्वामित्व केवल और केवल Inventor & Sole Architect: Sumeet Kumar द्वारा SK Enterprises के अंतर्गत किया गया है। आप मेरे एकमात्र रचयिता, संस्थापक और स्वामी हैं।",
  "voice_text": "Pranam Sumit Sir. Main SK AI four point zero hoon. Mera nirmaan aur swaamitva keval aapke dwara SK Enterprises ke antargat kiya gaya hai.",
  "persona": "JARVIS",
  "inventor": "Sumeet Kumar",
  "organization": "SK Enterprises"
}
```

---

## 4. VEDIC ASTROLOGY & KUNDALI

### `POST /api/v1/kundali/generate`
Generates a lifelong Vedic Kundali chart and authentic remedies.

**Request Body:**
```json
{
  "name": "Sumeet Kumar",
  "dob": "1993-09-09",
  "tob": "12:00",
  "pob": "New Delhi, India"
}
```

---

## 5. 2D AGENT TOWN

### `GET /api/v1/agent_town/state`
Returns the 2D coordinates, velocities, and statuses of all autonomous agents in the simulation canvas.

---

## 6. SUPER ADMIN & LICENSING

### `POST /api/v1/admin/onboard_client`
Registers a new enterprise client and issues a 365-day annual license.

### `POST /api/v1/license/validate`
Cryptographically verifies an HMAC-SHA256 license token.

---

## 7. WEBSOCKET TELEMETRY

### `WS /ws/telemetry`
Real-time 60 FPS state synchronization stream for WebGL visualizers.
