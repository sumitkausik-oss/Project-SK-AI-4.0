/**
 * SK ENTERPRISES | WebSocket Telemetry Stream Manager
 * Founder & Sole Architect: Sumeet Kumar
 * Platform: Jarvis Platform V5.0
 */

class SKTelemetryStream {
    constructor(wsUrl = "ws://127.0.0.1:8000/ws/telemetry") {
        this.wsUrl = wsUrl;
        this.socket = null;
        this.reconnectIntervalMs = 2500;
        this.maxReconnectAttempts = 50;
        this.reconnectAttempts = 0;
        this.listeners = [];
        this.isExplicitlyClosed = false;
        this.pingTimer = null;
    }

    connect() {
        this.isExplicitlyClosed = false;
        try {
            this.socket = new WebSocket(this.wsUrl);

            this.socket.onopen = () => {
                console.log("[WS TELEMETRY]: Connected to sovereign real-time stream.");
                this.reconnectAttempts = 0;
                this.notifyListeners({ type: "connection", status: "CONNECTED" });
                this.startHeartbeat();
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.notifyListeners({ type: "telemetry", data });
                } catch (e) {
                    // Ignore text pongs
                }
            };

            this.socket.onerror = (error) => {
                console.warn("[WS TELEMETRY]: Connection error or backend starting up...");
            };

            this.socket.onclose = () => {
                this.stopHeartbeat();
                this.notifyListeners({ type: "connection", status: "DISCONNECTED" });
                if (!this.isExplicitlyClosed) {
                    this.scheduleReconnect();
                }
            };
        } catch (err) {
            this.scheduleReconnect();
        }
    }

    startHeartbeat() {
        this.stopHeartbeat();
        this.pingTimer = setInterval(() => {
            if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                this.socket.send("ping");
            }
        }, 15000);
    }

    stopHeartbeat() {
        if (this.pingTimer) {
            clearInterval(this.pingTimer);
            this.pingTimer = null;
        }
    }

    scheduleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                console.log(`[WS TELEMETRY]: Reconnecting attempt #${this.reconnectAttempts}...`);
                this.connect();
            }, this.reconnectIntervalMs);
        }
    }

    subscribe(callback) {
        this.listeners.push(callback);
    }

    notifyListeners(event) {
        for (const callback of this.listeners) {
            try {
                callback(event);
            } catch (e) {
                console.error("[WS LISTENER ERROR]:", e);
            }
        }
    }

    disconnect() {
        this.isExplicitlyClosed = true;
        this.stopHeartbeat();
        if (this.socket) {
            this.socket.close();
        }
    }
}

window.telemetryStream = new SKTelemetryStream();
