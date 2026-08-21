export interface LiveServiceCallbacks {
  onStateChange: (state: 'IDLE' | 'LISTENING' | 'THINKING' | 'SPEAKING') => void;
  onTranscript: (role: 'user' | 'model', text: string) => void;
  onError: (error: string) => void;
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
    if (!apiKey || apiKey.trim() === '') {
      callbacks.onError('Settings में जाकर अपनी Google Gemini API Key दर्ज करें।');
      return;
    }

    try {
      callbacks.onStateChange('LISTENING');
      const cleanKey = apiKey.trim();
      const HOST = 'generativelanguage.googleapis.com';
      const API_VERSION = 'v1alpha';
      const URI = `wss://${HOST}/ws/google.ai.generativelanguage.${API_VERSION}.GenerativeService.BidiGenerateContent?key=${cleanKey}`;

      this.ws = new WebSocket(URI);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.sendSetupPayload();
        this.startMicrophone(callbacks);
      };

      this.ws.onmessage = async (event) => {
        let response: any;
        if (event.data instanceof Blob) {
          response = JSON.parse(await event.data.text());
        } else {
          response = JSON.parse(event.data);
        }

        // 1. Process Voice Chunks from Gemini
        const parts = response.serverContent?.modelTurn?.parts;
        if (parts) {
          for (const part of parts) {
            if (part.inlineData?.data) {
              callbacks.onStateChange('SPEAKING');
              this.playAudioChunk(part.inlineData.data);
            }
            if (part.text) {
              callbacks.onTranscript('model', part.text);
            }
          }
        }

        if (response.serverContent?.turnComplete) {
          callbacks.onStateChange('LISTENING');
        }

        // 2. Process Real-Time Tools
        const toolCalls = response.toolCall?.functionCalls;
        if (toolCalls && toolCalls.length > 0) {
          callbacks.onStateChange('THINKING');
          for (const call of toolCalls) {
            const result = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
              toolName: call.name,
              args: call.args,
            });

            callbacks.onTranscript('model', `[System]: ${result?.message || 'Action executed.'}`);

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
        console.error('WS Error:', err);
        callbacks.onError('AI कनेक्शन में त्रुटि हुई। API Key और इंटरनेट की जांच करें।');
      };

      this.ws.onclose = (e) => {
        console.warn(`WS Closed [Code: ${e.code}, Reason: ${e.reason || 'None'}]`);
        this.disconnect(callbacks);
      };
    } catch (e: any) {
      callbacks.onError(e.message || 'माइक्रोफ़ोन शुरू करने में विफल।');
      this.disconnect(callbacks);
    }
  }

  // Text message sender for the bottom input bar
  sendTextMessage(text: string, callbacks: LiveServiceCallbacks) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      callbacks.onError('कृपया पहले "START LIVE GEMINI VOICE" पर क्लिक करके AI को कनेक्ट करें।');
      return;
    }
    callbacks.onTranscript('user', text);
    callbacks.onStateChange('THINKING');

    this.ws.send(
      JSON.stringify({
        clientContent: {
          turns: [
            {
              role: 'user',
              parts: [{ text }],
            },
          ],
          turnComplete: true,
        },
      })
    );
  }

  private sendSetupPayload() {
    const payload = {
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
              text: 'You are SK AI, an ultra-fast desktop assistant built for Sumeet Kumar (Powered by SK Enterprises). Always respond in clear, polite Hindi or Hinglish. When the user asks to open D drive, Chrome, Calculator, Notepad, or any app, ALWAYS trigger the tool immediately and confirm in Hindi.',
            },
          ],
        },
        tools: [
          {
            functionDeclarations: [
              {
                name: 'open_drive',
                description: 'Opens a local drive or folder like D Drive or C Drive in Explorer',
                parameters: {
                  type: 'OBJECT',
                  properties: {
                    target: { type: 'STRING', description: 'Drive letter (D:, C:) or folder name' },
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
                    app_name: { type: 'STRING', description: 'Name of the application' },
                  },
                  required: ['app_name'],
                },
              },
              {
                name: 'take_screenshot',
                description: 'Captures full screen screenshot',
                parameters: { type: 'OBJECT', properties: {} },
              },
            ],
          },
        ],
      },
    };
    this.ws?.send(JSON.stringify(payload));
  }

  private async startMicrophone(callbacks: LiveServiceCallbacks) {
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

      const inputData = e.inputBuffer.getChannelData(0);
      const pcm16 = new Int16Array(inputData.length);
      for (let i = 0; i < inputData.length; i++) {
        const s = Math.max(-1, Math.min(1, inputData[i]));
        pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
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

  private playAudioChunk(base64Pcm: string) {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
    if (!this.playbackContext) {
      this.playbackContext = new AudioCtx({ sampleRate: 24000 });
      this.nextPlayTime = this.playbackContext.currentTime;
    }

    const binaryString = atob(base64Pcm);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
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
    source.buffer = audioBuffer;
    source.connect(this.playbackContext.destination);

    const startTime = Math.max(this.playbackContext.currentTime, this.nextPlayTime);
    source.start(startTime);
    this.nextPlayTime = startTime + audioBuffer.duration;
  }

  disconnect(callbacks?: LiveServiceCallbacks) {
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
