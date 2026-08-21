/**
 * SKAI — Gemini Live Core 2-Way Duplex Engine
 * Product: SKAI Platform | Powered by SK Enterprises
 * Lead Architect: Sumeet Kumar | Version: 4.1.0
 */

export interface LiveEngineCallbacks {
  onStateChange: (state: 'IDLE' | 'LISTENING' | 'THINKING' | 'SPEAKING') => void;
  onTranscript: (role: 'user' | 'model', text: string) => void;
  onError: (error: string) => void;
  onAudioLevel?: (level: number) => void;
}

export class GeminiLiveCore {
  private ws: WebSocket | null = null;
  private audioContext: AudioContext | null = null;
  private mediaStream: MediaStream | null = null;
  private processor: ScriptProcessorNode | null = null;
  private playbackContext: AudioContext | null = null;
  private nextPlayTime = 0;
  public isConnected = false;

  async connect(apiKey: string, callbacks: LiveEngineCallbacks) {
    if (!apiKey || apiKey.trim() === '') {
      callbacks.onError('Settings me jakar valid Google Gemini API Key enter karein.');
      return;
    }

    try {
      callbacks.onStateChange('LISTENING');
      const cleanKey = apiKey.trim();
      const URI = `wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=${cleanKey}`;
      this.ws = new WebSocket(URI);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.sendSetupEnvelope();
        this.startResampledAudioInput(callbacks);
      };

      this.ws.onmessage = async (event) => {
        let payload: any;
        if (event.data instanceof Blob) {
          payload = JSON.parse(await event.data.text());
        } else {
          payload = JSON.parse(event.data);
        }

        // 1. Process Spoken Audio Stream
        const parts = payload.serverContent?.modelTurn?.parts;
        if (parts) {
          for (const part of parts) {
            if (part.inlineData?.data) {
              callbacks.onStateChange('SPEAKING');
              this.enqueuePlayback(part.inlineData.data);
            }
            if (part.text) {
              callbacks.onTranscript('model', part.text);
            }
          }
        }

        if (payload.serverContent?.turnComplete) {
          callbacks.onStateChange('LISTENING');
        }

        // 2. Process Dynamic Tools (Causal Master / Actuators)
        const toolCalls = payload.toolCall?.functionCalls;
        if (toolCalls && toolCalls.length > 0) {
          callbacks.onStateChange('THINKING');
          for (const call of toolCalls) {
            const result = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
              toolName: call.name,
              args: call.args,
            });

            callbacks.onTranscript('model', `[System Actuation]: ${result?.message || 'Done'}`);

            this.ws?.send(
              JSON.stringify({
                toolResponse: {
                  functionResponses: [
                    {
                      response: { output: result },
                      id: call.id,
                    },
                  ],
                },
              })
            );
          }
        }
      };

      this.ws.onerror = (err) => {
        console.error('[SKAI Live Socket Error]', err);
        callbacks.onError('AI Connection Error. Check Network/API Key.');
      };

      this.ws.onclose = (e) => {
        console.warn(`[SKAI Socket Terminated] Code: ${e.code}, Reason: ${e.reason || 'None'}`);
        this.disconnect(callbacks);
      };
    } catch (e: any) {
      callbacks.onError(e.message || 'Microphone activation failed.');
      this.disconnect(callbacks);
    }
  }

  sendTextMessage(text: string, callbacks: LiveEngineCallbacks) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      callbacks.onError('Please connect Live AI first.');
      return;
    }
    callbacks.onTranscript('user', text);
    callbacks.onStateChange('THINKING');

    this.ws.send(
      JSON.stringify({
        clientContent: {
          turns: [{ role: 'user', parts: [{ text }] }],
          turnComplete: true,
        },
      })
    );
  }

  private sendSetupEnvelope() {
    const envelope = {
      setup: {
        model: 'models/gemini-2.0-flash-exp',
        generationConfig: {
          responseModalities: ['AUDIO'],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: { voiceName: 'Puck' },
            },
          },
        },
        systemInstruction: {
          parts: [
            {
              text: 'You are SK AI, an autonomous intelligence built by Sumeet Kumar (Powered by SK Enterprises). You converse fluently, respectfully, and crisply in Hindi / Hinglish. When the user asks to open D drive, applications, take screenshots, or inspect files, ALWAYS invoke the corresponding tool function immediately and confirm verbally in Hindi.',
            },
          ],
        },
        tools: [
          {
            functionDeclarations: [
              {
                name: 'open_drive_or_folder',
                description: 'Opens local drives (D: drive, C: drive) or directories in Windows Explorer',
                parameters: {
                  type: 'OBJECT',
                  properties: {
                    target: { type: 'STRING', description: 'Drive or path e.g. D:, C:, Downloads' },
                  },
                  required: ['target'],
                },
              },
              {
                name: 'open_application',
                description: 'Launches Windows applications like Chrome, Notepad, Calculator, VS Code',
                parameters: {
                  type: 'OBJECT',
                  properties: {
                    app_name: { type: 'STRING', description: 'App name to launch' },
                  },
                  required: ['app_name'],
                },
              },
              {
                name: 'take_screenshot',
                description: 'Takes a full desktop screenshot and saves it',
                parameters: { type: 'OBJECT', properties: {} },
              },
            ],
          },
        ],
      },
    };
    this.ws?.send(JSON.stringify(envelope));
  }

  private async startResampledAudioInput(callbacks: LiveEngineCallbacks) {
    this.mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: { echoCancellation: true, noiseSuppression: true, channelCount: 1 },
    });

    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    this.audioContext = new AudioCtx({ sampleRate: 16000 });
    const source = this.audioContext.createMediaStreamSource(this.mediaStream);
    this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);

    source.connect(this.processor);
    this.processor.connect(this.audioContext.destination);

    this.processor.onaudioprocess = (e) => {
      if (!this.isConnected || this.ws?.readyState !== WebSocket.OPEN) return;

      const input = e.inputBuffer.getChannelData(0);
      const pcm16 = new Int16Array(input.length);
      let sum = 0;

      for (let i = 0; i < input.length; i++) {
        const s = Math.max(-1, Math.min(1, input[i]));
        pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
        sum += input[i] * input[i];
      }

      if (callbacks.onAudioLevel) {
        callbacks.onAudioLevel(Math.sqrt(sum / input.length));
      }

      let binary = '';
      const bytes = new Uint8Array(pcm16.buffer);
      for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
      }

      this.ws.send(
        JSON.stringify({
          realtimeInput: {
            mediaChunks: [
              {
                mimeType: 'audio/pcm;rate=16000',
                data: btoa(binary),
              },
            ],
          },
        })
      );
    };
  }

  private enqueuePlayback(base64Pcm: string) {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!this.playbackContext) {
      this.playbackContext = new AudioCtx({ sampleRate: 24000 });
      this.nextPlayTime = this.playbackContext.currentTime;
    }

    const binary = atob(base64Pcm);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);

    const int16 = new Int16Array(bytes.buffer);
    const float32 = new Float32Array(int16.length);
    for (let i = 0; i < int16.length; i++) float32[i] = int16[i] / 32768;

    const buffer = this.playbackContext.createBuffer(1, float32.length, 24000);
    buffer.getChannelData(0).set(float32);

    const source = this.playbackContext.createBufferSource();
    source.buffer = buffer;
    source.connect(this.playbackContext.destination);

    const start = Math.max(this.playbackContext.currentTime, this.nextPlayTime);
    source.start(start);
    this.nextPlayTime = start + buffer.duration;
  }

  disconnect(callbacks?: LiveEngineCallbacks) {
    this.isConnected = false;
    this.processor?.disconnect();
    this.processor = null;
    this.mediaStream?.getTracks().forEach((t) => t.stop());
    this.mediaStream = null;
    this.audioContext?.close();
    this.audioContext = null;
    this.playbackContext?.close();
    this.playbackContext = null;

    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.close();
    }
    this.ws = null;
    callbacks?.onStateChange('IDLE');
  }
}

export { GeminiLiveCore as GeminiLiveService };
