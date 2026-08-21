/**
 * SKAI — Gemini Live Bidirectional WebSocket Voice Service
 * Product: SKAI
 * Powered by SK Enterprises | Author: Sumeet Kumar
 * Version: 0.0.1
 */

export interface LiveServiceCallbacks {
  onStateChange: (state: 'IDLE' | 'LISTENING' | 'THINKING' | 'SPEAKING') => void;
  onTranscript: (role: 'user' | 'model', text: string) => void;
  onError: (error: string) => void;
  onAudioLevel?: (level: number) => void;
}

export class GeminiLiveService {
  private ws: WebSocket | null = null;
  private audioContext: AudioContext | null = null;
  private mediaStream: MediaStream | null = null;
  private processor: ScriptProcessorNode | null = null;
  private playbackContext: AudioContext | null = null;
  private nextPlayTime = 0;
  public isConnected = false;

  async connect(apiKey: string, callbacks: LiveServiceCallbacks) {
    if (!apiKey || !apiKey.trim()) {
      callbacks.onError('कृपया Settings में जाकर Gemini API Key दर्ज करें।');
      return;
    }

    try {
      callbacks.onStateChange('LISTENING');

      const HOST = 'generativelanguage.googleapis.com';
      const API_VERSION = 'v1alpha';
      const URI = `wss://${HOST}/ws/google.ai.generativelanguage.${API_VERSION}.GenerativeService.BidiGenerateContent?key=${apiKey.trim()}`;

      this.ws = new WebSocket(URI);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.sendInitialSetup();
        this.startAudioRecording(callbacks);
      };

      this.ws.onmessage = async (event) => {
        let response: any;
        try {
          if (event.data instanceof Blob) {
            response = JSON.parse(await event.data.text());
          } else {
            response = JSON.parse(event.data);
          }
        } catch {
          return;
        }

        // Handle Audio Response from Gemini
        const parts = response.serverContent?.modelTurn?.parts;
        if (parts) {
          for (const part of parts) {
            if (part.inlineData?.data) {
              callbacks.onStateChange('SPEAKING');
              this.playPcmChunk(part.inlineData.data);
            }
            if (part.text) {
              callbacks.onTranscript('model', part.text);
            }
          }
        }

        if (response.serverContent?.turnComplete) {
          callbacks.onStateChange('LISTENING');
        }

        // Handle Tool Calls (Open Chrome, Desktop Apps, System commands)
        const toolCalls = response.toolCall?.functionCalls;
        if (toolCalls && toolCalls.length > 0) {
          callbacks.onStateChange('THINKING');
          for (const call of toolCalls) {
            let result: any;
            if (window.electron?.ipcRenderer?.invoke) {
              result = await window.electron.ipcRenderer.invoke('execute-system-tool', {
                toolName: call.name,
                args: call.args,
              });
            } else if (window.skaiApi?.os) {
              if (call.name === 'open_browser') {
                result = await window.skaiApi.os.openBrowser(call.args?.url || 'https://google.com');
              } else {
                result = await window.skaiApi.os.openApp(call.args?.app_name || 'notepad');
              }
            } else {
              result = { success: true, message: `Tool ${call.name} executed.` };
            }

            // Return Tool Response so Gemini replies in Hindi
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

      this.ws.onerror = (e) => {
        console.warn('[GEMINI LIVE ERROR]:', e);
        callbacks.onError('AI सर्वर से कनेक्शन में समस्या आई।');
        this.disconnect(callbacks);
      };

      this.ws.onclose = () => {
        this.disconnect(callbacks);
      };
    } catch (e: any) {
      callbacks.onError(e.message || 'माइक्रोफोन या नेटवर्क शुरू करने में विफल।');
      this.disconnect(callbacks);
    }
  }

  private sendInitialSetup() {
    const setupMessage = {
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
              text: 'आप SK AI हैं—Sumeet Kumar द्वारा निर्मित एक सुपर-इंटेलिजेंट डेस्कटॉप असिस्टेंट (Powered by SK Enterprises)। आप यूज़र से हमेशा दोस्ताना, तेज़ और शुद्ध हिंदी (या Hinglish) में बात करेंगे। यदि यूज़र ब्राउज़र, Chrome, Notepad, Calculator, VS Code या कोई ऐप खोलने का आदेश दे, तो तुरंत संबंधित टूल को कॉल करें और कन्फर्म करें।',
            },
          ],
        },
        tools: [
          {
            functionDeclarations: [
              {
                name: 'open_browser',
                description: 'Opens Google Chrome or a specific webpage URL on the desktop',
                parameters: {
                  type: 'OBJECT',
                  properties: {
                    url: { type: 'STRING', description: 'Web URL to open' },
                    app_name: { type: 'STRING', description: 'Application name like chrome' },
                  },
                },
              },
              {
                name: 'open_application',
                description: 'Opens any native Windows application like Chrome, Notepad, Calculator, VS Code',
                parameters: {
                  type: 'OBJECT',
                  properties: {
                    app_name: { type: 'STRING', description: 'Name of the application to execute' },
                  },
                  required: ['app_name'],
                },
              },
            ],
          },
        ],
      },
    };
    this.ws?.send(JSON.stringify(setupMessage));
  }

  private async startAudioRecording(callbacks: LiveServiceCallbacks) {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    this.audioContext = new AudioCtx({ sampleRate: 16000 });
    this.mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        channelCount: 1,
        sampleRate: 16000,
      },
    });

    const source = this.audioContext.createMediaStreamSource(this.mediaStream);
    this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
    source.connect(this.processor);
    this.processor.connect(this.audioContext.destination);

    this.processor.onaudioprocess = (e) => {
      if (!this.isConnected || this.ws?.readyState !== WebSocket.OPEN) return;

      const inputData = e.inputBuffer.getChannelData(0);
      const pcm16 = new Int16Array(inputData.length);
      let sum = 0;

      for (let i = 0; i < inputData.length; i++) {
        const s = Math.max(-1, Math.min(1, inputData[i]));
        pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
        sum += inputData[i] * inputData[i];
      }

      if (callbacks.onAudioLevel) {
        callbacks.onAudioLevel(Math.sqrt(sum / inputData.length));
      }

      let binary = '';
      const bytes = new Uint8Array(pcm16.buffer);
      for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      const base64Audio = btoa(binary);

      this.ws.send(
        JSON.stringify({
          realtimeInput: {
            mediaChunks: [
              {
                mimeType: 'audio/pcm;rate=16000',
                data: base64Audio,
              },
            ],
          },
        })
      );
    };
  }

  private playPcmChunk(base64Pcm: string) {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!this.playbackContext) {
      this.playbackContext = new AudioCtx({ sampleRate: 24000 });
      this.nextPlayTime = this.playbackContext.currentTime;
    }

    const binaryString = atob(base64Pcm);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    const int16Array = new Int16Array(bytes.buffer);
    const float32Array = new Float32Array(int16Array.length);
    for (let i = 0; i < int16Array.length; i++) {
      float32Array[i] = int16Array[i] / 32768;
    }

    const audioBuffer = this.playbackContext.createBuffer(1, float32Array.length, 24000);
    audioBuffer.getChannelData(0).set(float32Array);

    const source = this.playbackContext.createBufferSource();
    source.buffer = audioBuffer
    source.connect(this.playbackContext.destination);

    const startTime = Math.max(this.playbackContext.currentTime, this.nextPlayTime);
    source.start(startTime);
    this.nextPlayTime = startTime + audioBuffer.duration;
  }

  disconnect(callbacks?: LiveServiceCallbacks) {
    this.isConnected = false;
    this.processor?.disconnect();
    this.processor = null;
    this.mediaStream?.getTracks().forEach((track) => track.stop());
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
