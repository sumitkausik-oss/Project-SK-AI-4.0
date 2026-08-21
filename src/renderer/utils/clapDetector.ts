/**
 * SKAI — Double-Clap Wake Detection Engine
 * Product: SKAI
 * Tagline: Powered by SK Enterprises
 * Author / Owner: Sumeet Kumar
 * Version: 0.0.1
 */

export interface ClapDetectorOptions {
  threshold?: number; // Energy spike threshold (e.g. 0.25 - 0.45)
  minWindowMs?: number; // 150ms minimum gap
  maxWindowMs?: number; // 450ms maximum gap
  onWake: () => void;
}

export class ClapDetector {
  private options: ClapDetectorOptions;
  private audioContext: AudioContext | null = null;
  private mediaStream: MediaStream | null = null;
  private analyser: AnalyserNode | null = null;
  private processor: ScriptProcessorNode | null = null;
  private isListening = false;

  private lastSpikeTime = 0;
  private spikeCount = 0;
  private isCoolingDown = false;

  constructor(options: ClapDetectorOptions) {
    this.options = {
      threshold: 0.32,
      minWindowMs: 150,
      maxWindowMs: 450,
      ...options,
    };
  }

  public async start(): Promise<void> {
    if (this.isListening) return;

    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      this.audioContext = new AudioCtx();

      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false,
        },
      });

      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 512;

      // High-pass filter to isolate sharp clap/snap frequencies (> 1.5kHz)
      const highpass = this.audioContext.createBiquadFilter();
      highpass.type = 'highpass';
      highpass.frequency.value = 1500;

      this.processor = this.audioContext.createScriptProcessor(2048, 1, 1);

      this.processor.onaudioprocess = (e) => {
        if (!this.isListening || this.isCoolingDown) return;

        const input = e.inputBuffer.getChannelData(0);
        let maxEnergy = 0;
        for (let i = 0; i < input.length; i++) {
          const abs = Math.abs(input[i]);
          if (abs > maxEnergy) maxEnergy = abs;
        }

        const now = performance.now();
        const threshold = this.options.threshold || 0.32;

        if (maxEnergy > threshold) {
          const timeSinceLastSpike = now - this.lastSpikeTime;

          if (this.spikeCount === 0) {
            // First clap spike registered
            this.spikeCount = 1;
            this.lastSpikeTime = now;
          } else if (this.spikeCount === 1) {
            // Check if second clap falls within the 150ms - 450ms window
            const minWin = this.options.minWindowMs || 150;
            const maxWin = this.options.maxWindowMs || 450;

            if (timeSinceLastSpike >= minWin && timeSinceLastSpike <= maxWin) {
              // Valid Double Clap detected!
              this.spikeCount = 0;
              this.isCoolingDown = true;

              // Fire wake callbacks
              this.options.onWake();
              if ((window as any).electron?.ipcRenderer?.send) {
                (window as any).electron.ipcRenderer.send('wake-assistant');
              }

              // Cooldown 1.2s to prevent repeated triggers
              setTimeout(() => {
                this.isCoolingDown = false;
              }, 1200);
            } else if (timeSinceLastSpike > maxWin) {
              // Too slow, reset to 1st clap
              this.spikeCount = 1;
              this.lastSpikeTime = now;
            }
          }
        } else {
          // Decay check: if waiting too long, reset
          if (this.spikeCount === 1 && now - this.lastSpikeTime > (this.options.maxWindowMs || 450)) {
            this.spikeCount = 0;
          }
        }
      };

      source.connect(highpass);
      highpass.connect(this.analyser);
      this.analyser.connect(this.processor);
      this.processor.connect(this.audioContext.destination);

      this.isListening = true;
    } catch (err) {
      console.warn('[CLAP DETECTOR] Init failed:', err);
    }
  }

  public stop(): void {
    this.isListening = false;
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach((t) => t.stop());
      this.mediaStream = null;
    }
    if (this.processor) {
      this.processor.disconnect();
      this.processor = null;
    }
    if (this.analyser) {
      this.analyser.disconnect();
      this.analyser = null;
    }
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }
  }
}
