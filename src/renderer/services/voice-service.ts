/**
 * SKAI — Voice Engine & Audio Capture Service
 * Product: SKAI
 * Tagline: Powered by SK Enterprises
 * Author / Owner: Sumeet Kumar
 * Version: 0.0.1
 */

export type VoiceState = 'DISCONNECTED' | 'CONNECTING' | 'LISTENING' | 'THINKING' | 'SPEAKING' | 'RECONNECTING';

export interface VoiceServiceOptions {
  sampleRate?: number;
  bufferSize?: number;
  vadThreshold?: number;
  silenceTimeoutMs?: number;
  onStateChange: (state: VoiceState) => void;
  onAudioLevel: (level: number) => void;
  onTranscript: (transcript: string) => void;
  onError: (error: string) => void;
}

export class VoiceService {
  private options: VoiceServiceOptions;
  private audioContext: AudioContext | null = null;
  private mediaStream: MediaStream | null = null;
  private sourceNode: MediaStreamAudioSourceNode | null = null;
  private processorNode: ScriptProcessorNode | null = null;
  private analyserNode: AnalyserNode | null = null;
  private recognition: any = null;

  private state: VoiceState = 'DISCONNECTED';
  private shouldAutoReconnect = true;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeoutId: any = null;

  // Echo protection & VAD settings
  private isSpeakingLocally = false;
  private consecutiveSilenceCount = 0;

  constructor(options: VoiceServiceOptions) {
    this.options = {
      sampleRate: 16000,
      bufferSize: 4096,
      vadThreshold: 0.018,
      silenceTimeoutMs: 2500,
      ...options,
    };
  }

  public getState(): VoiceState {
    return this.state;
  }

  public setSpeakingLocally(isSpeaking: boolean) {
    this.isSpeakingLocally = isSpeaking;
    if (isSpeaking) {
      this.setState('SPEAKING');
    } else if (this.state === 'SPEAKING') {
      this.setState('LISTENING');
    }
  }

  private setState(newState: VoiceState) {
    if (this.state === newState) return;
    this.state = newState;
    this.options.onStateChange(newState);
  }

  public async start(): Promise<void> {
    this.shouldAutoReconnect = true;
    this.reconnectAttempts = 0;
    this.setState('CONNECTING');

    try {
      // 1. AudioContext setup with 16kHz or default
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      this.audioContext = new AudioCtx({ sampleRate: this.options.sampleRate });

      // 2. Microphone capture
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: this.options.sampleRate,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      // 3. Audio Node Pipeline (4096 frames mono)
      this.sourceNode = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.analyserNode = this.audioContext.createAnalyser();
      this.analyserNode.fftSize = 512;

      const bufferSize = this.options.bufferSize || 4096;
      this.processorNode = this.audioContext.createScriptProcessor(bufferSize, 1, 1);

      this.processorNode.onaudioprocess = (e) => {
        if (this.state === 'DISCONNECTED' || this.isSpeakingLocally) return;

        const inputData = e.inputBuffer.getChannelData(0);
        // Calculate Root Mean Square (RMS) for VAD
        let sum = 0;
        for (let i = 0; i < inputData.length; i++) {
          sum += inputData[i] * inputData[i];
        }
        const rms = Math.sqrt(sum / inputData.length);
        this.options.onAudioLevel(rms);

        // VAD Trigger check
        if (rms > (this.options.vadThreshold || 0.018)) {
          this.consecutiveSilenceCount = 0;
        } else {
          this.consecutiveSilenceCount++;
        }
      };

      this.sourceNode.connect(this.analyserNode);
      this.analyserNode.connect(this.processorNode);
      this.processorNode.connect(this.audioContext.destination);

      // 4. Web Speech Recognition for bilingual input
      this.initSpeechRecognition();

      this.setState('LISTENING');
    } catch (err: any) {
      console.error('[VOICE SERVICE ERROR]:', err);
      this.options.onError(err.message || 'Microphone access denied.');
      this.handleReconnect();
    }
  }

  private initSpeechRecognition() {
    const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRec) return;

    if (this.recognition) {
      try {
        this.recognition.abort();
      } catch {}
    }

    this.recognition = new SpeechRec();
    this.recognition.continuous = true;
    this.recognition.interimResults = false;
    this.recognition.lang = 'en-US';

    this.recognition.onstart = () => {
      if (!this.isSpeakingLocally) {
        this.setState('LISTENING');
      }
    };

    this.recognition.onresult = (event: any) => {
      if (this.isSpeakingLocally) return; // Prevent software echo feedback
      const lastIndex = event.results.length - 1;
      const transcript = event.results[lastIndex][0].transcript.trim();
      if (transcript) {
        this.options.onTranscript(transcript);
      }
    };

    this.recognition.onerror = (event: any) => {
      if (event.error === 'no-speech') return;
      console.warn('[VOICE SERVICE] Recognition error:', event.error);
      if (this.shouldAutoReconnect) {
        this.handleReconnect();
      }
    };

    this.recognition.onend = () => {
      if (this.shouldAutoReconnect && this.state !== 'DISCONNECTED') {
        // Auto-re-arm continuous recognition loop
        try {
          this.recognition.start();
        } catch {
          this.handleReconnect();
        }
      }
    };

    try {
      this.recognition.start();
    } catch (err) {
      console.warn('[VOICE SERVICE] Failed to start recognition:', err);
    }
  }

  private handleReconnect() {
    if (!this.shouldAutoReconnect || this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.setState('DISCONNECTED');
      return;
    }

    this.setState('RECONNECTING');
    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(1.5, this.reconnectAttempts), 5000);

    if (this.reconnectTimeoutId) clearTimeout(this.reconnectTimeoutId);
    this.reconnectTimeoutId = setTimeout(() => {
      this.start();
    }, delay);
  }

  public stop(): void {
    this.shouldAutoReconnect = false;
    if (this.reconnectTimeoutId) clearTimeout(this.reconnectTimeoutId);

    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch {}
      this.recognition = null;
    }

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach((track) => track.stop());
      this.mediaStream = null;
    }

    if (this.processorNode) {
      this.processorNode.disconnect();
      this.processorNode = null;
    }

    if (this.analyserNode) {
      this.analyserNode.disconnect();
      this.analyserNode = null;
    }

    if (this.sourceNode) {
      this.sourceNode.disconnect();
      this.sourceNode = null;
    }

    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }

    this.setState('DISCONNECTED');
  }
}
