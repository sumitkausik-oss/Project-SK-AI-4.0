/**
 * SKAI — Bulletproof 2-Way Bilingual Voice Engine (Hindi, Hinglish & English)
 * Product: SKAI
 * Powered by SK Enterprises | Founder & Sole Architect: Sumeet Kumar
 * Version: 4.0.1
 */

export interface VoiceEngineCallbacks {
  onStateChange: (state: 'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING') => void;
  onTranscript: (role: 'user' | 'model', text: string) => void;
  onAudioLevel?: (level: number) => void;
  onError: (error: string) => void;
}

export class VoiceEngine {
  private isRunning = false;
  private recognition: any = null;
  private isSpeaking = false;
  private googleApiKey = '';
  private hfToken = '';
  private callbacks: VoiceEngineCallbacks | null = null;
  private audioContext: AudioContext | null = null;
  private analyser: AnalyserNode | null = null;
  private mediaStream: MediaStream | null = null;
  private animFrameId: number | null = null;

  public init(googleKey: string, hfToken: string) {
    this.googleApiKey = googleKey?.trim() || '';
    this.hfToken = hfToken?.trim() || '';
  }

  public setKeys(googleKey: string, hfToken: string) {
    this.googleApiKey = googleKey?.trim() || '';
    this.hfToken = hfToken?.trim() || '';
  }

  public async start(callbacks: VoiceEngineCallbacks): Promise<void> {
    this.callbacks = callbacks;
    this.isRunning = true;
    this.callbacks.onStateChange('LISTENING');

    // 1. Start Audio Visualizer
    await this.startAudioAnalyser();

    // 2. Start Continuous Speech Recognition
    this.initSpeechRecognition();
  }

  private async startAudioAnalyser() {
    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      this.audioContext = new AudioCtx();
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: true, noiseSuppression: true, channelCount: 1 },
      });

      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      source.connect(this.analyser);

      const bufferLength = this.analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const checkLevel = () => {
        if (!this.isRunning) return;
        this.analyser?.getByteFrequencyData(dataArray);
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const avg = sum / bufferLength / 255;
        this.callbacks?.onAudioLevel?.(avg);
        this.animFrameId = requestAnimationFrame(checkLevel);
      };
      checkLevel();
    } catch (err) {
      console.warn('[VOICE ENGINE] Analyser warning:', err);
    }
  }

  private initSpeechRecognition() {
    const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRec) {
      this.callbacks?.onError('इस ब्राउज़र/सिस्टम में Speech Recognition समर्थित नहीं है।');
      return;
    }

    try {
      if (this.recognition) {
        this.recognition.abort();
      }
    } catch {}

    this.recognition = new SpeechRec();
    this.recognition.continuous = true;
    this.recognition.interimResults = false;
    // Set to Hindi / Indian English recognition
    this.recognition.lang = 'hi-IN';

    this.recognition.onstart = () => {
      if (!this.isSpeaking) {
        this.callbacks?.onStateChange('LISTENING');
      }
    };

    this.recognition.onresult = async (event: any) => {
      if (this.isSpeaking) return; // Prevent echo loop

      const lastIndex = event.results.length - 1;
      const transcript = event.results[lastIndex][0].transcript.trim();

      if (transcript) {
        this.callbacks?.onTranscript('user', transcript);
        await this.handleUserQuery(transcript);
      }
    };

    this.recognition.onerror = (event: any) => {
      if (event.error === 'no-speech') return;
      console.warn('[SPEECH RECOGNITION ERROR]:', event.error);
    };

    this.recognition.onend = () => {
      if (this.isRunning && !this.isSpeaking) {
        // Continuous auto-restart
        try {
          this.recognition.start();
        } catch {
          setTimeout(() => {
            if (this.isRunning && !this.isSpeaking) {
              try {
                this.recognition.start();
              } catch {}
            }
          }, 500);
        }
      }
    };

    try {
      this.recognition.start();
    } catch (err) {
      console.warn('[SPEECH RECOGNITION START]:', err);
    }
  }

  public async handleUserQuery(query: string): Promise<void> {
    this.callbacks?.onStateChange('THINKING');
    const qLower = query.toLowerCase().trim();

    // 1. Direct High-Speed OS Tool Execution
    if (qLower.includes('d drive') || qLower.includes('d:') || qLower.includes('d disk') || qLower.includes('d ड्राइव')) {
      const res = await this.executeTool('open_drive_or_folder', { target: 'D:\\' });
      await this.speakResponse(`जी Sumeet Sir, मैंने D Drive खोल दिया है।`);
      return;
    }

    if (qLower.includes('c drive') || qLower.includes('c:') || qLower.includes('c ड्राइव')) {
      const res = await this.executeTool('open_drive_or_folder', { target: 'C:\\' });
      await this.speakResponse(`जी Sir, C Drive खोल दिया गया है।`);
      return;
    }

    if (qLower.includes('e drive') || qLower.includes('e:') || qLower.includes('e ड्राइव')) {
      const res = await this.executeTool('open_drive_or_folder', { target: 'E:\\' });
      await this.speakResponse(`जी Sir, E Drive खोल दिया गया है।`);
      return;
    }

    if (qLower.includes('chrome') || qLower.includes('क्रोम') || qLower.includes('browser') || qLower.includes('ब्राउज़र')) {
      await this.executeTool('open_application', { app_name: 'chrome' });
      await this.speakResponse(`Google Chrome खोल दिया है, Sumeet Sir.`);
      return;
    }

    if (qLower.includes('notepad') || qLower.includes('नोटपैड')) {
      await this.executeTool('open_application', { app_name: 'notepad' });
      await this.speakResponse(`Notepad शुरू कर दिया है।`);
      return;
    }

    if (qLower.includes('calc') || qLower.includes('calculator') || qLower.includes('कैलकुलेटर')) {
      await this.executeTool('open_application', { app_name: 'calc' });
      await this.speakResponse(`Calculator खोल दिया है।`);
      return;
    }

    if (qLower.includes('code') || qLower.includes('vs code') || qLower.includes('कोड')) {
      await this.executeTool('open_application', { app_name: 'code' });
      await this.speakResponse(`VS Code एडिटर लॉन्च कर दिया है।`);
      return;
    }

    if (qLower.includes('screenshot') || qLower.includes('स्क्रीनशॉट')) {
      await this.executeTool('take_screenshot', {});
      await this.speakResponse(`स्क्रीनशॉट कैप्चर करके सेव कर लिया है।`);
      return;
    }

    // 2. Intelligent AI Generative Response (Gemini 2.0 Flash / Hugging Face)
    let aiReply = '';

    if (this.googleApiKey) {
      try {
        aiReply = await this.queryGemini(query);
      } catch (err: any) {
        console.warn('[GEMINI QUERY FAILED]:', err);
      }
    }

    if (!aiReply && this.hfToken) {
      try {
        aiReply = await this.queryHuggingFace(query);
      } catch (err: any) {
        console.warn('[HUGGING FACE QUERY FAILED]:', err);
      }
    }

    if (!aiReply) {
      aiReply = `नमस्ते Sumeet Kumar सर! मैंने आपकी बात सुनी: "${query}". लाइव AI से सीधे बातचीत करने के लिए सेटिंग्स में अपनी Google Gemini या Hugging Face की दर्ज करें।`;
    }

    await this.speakResponse(aiReply);
  }

  private async executeTool(toolName: string, args: any): Promise<any> {
    if (window.electron?.ipcRenderer?.invoke) {
      return window.electron.ipcRenderer.invoke('execute-system-tool', { toolName, args });
    } else if (window.skaiApi?.os?.openApp) {
      if (toolName === 'open_drive_or_folder') {
        return window.skaiApi.os.openApp(`explorer.exe "${args.target || 'D:\\'}"`);
      }
      return window.skaiApi.os.openApp(args.app_name || 'notepad');
    }
    return { success: true };
  }

  private async queryGemini(userPrompt: string): Promise<string> {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${this.googleApiKey}`;

    const systemPrompt = `You are SK AI, an intelligent desktop assistant created exclusively for Sumeet Kumar (Powered by SK Enterprises).
Always reply in natural, friendly, and respectful Hindi (या conversational Hinglish). Keep the response concise, punchy (1-3 sentences), and directly to the point so it is ideal for speech output.`;

    const body = {
      contents: [
        {
          role: 'user',
          parts: [{ text: `${systemPrompt}\n\nUser: ${userPrompt}\nSK AI:` }],
        },
      ],
      generationConfig: {
        maxOutputTokens: 200,
        temperature: 0.7,
      },
    };

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new Error(`Gemini API Error (HTTP ${res.status})`);
    }

    const data = await res.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
  }

  private async queryHuggingFace(userPrompt: string): Promise<string> {
    const url = 'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3';

    const res = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.hfToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        inputs: `<s>[INST] You are SK AI by Sumeet Kumar (SK Enterprises). Reply in pure Hindi or Hinglish concisely: ${userPrompt} [/INST]`,
        parameters: { max_new_tokens: 150, temperature: 0.7 },
      }),
    });

    if (!res.ok) {
      throw new Error(`Hugging Face API Error (HTTP ${res.status})`);
    }

    const data = await res.json();
    if (Array.isArray(data) && data[0]?.generated_text) {
      const full = data[0].generated_text;
      const reply = full.split('[/INST]').pop()?.trim() || full;
      return reply;
    }
    return '';
  }

  public speakResponse(text: string): Promise<void> {
    return new Promise((resolve) => {
      this.callbacks?.onTranscript('model', text);

      if (!window.speechSynthesis) {
        this.callbacks?.onStateChange('LISTENING');
        resolve();
        return;
      }

      window.speechSynthesis.cancel();
      this.isSpeaking = true;
      this.callbacks?.onStateChange('SPEAKING');

      // Clean markdown tags
      const cleanText = text.replace(/[*#`_>\[\]]/g, '').trim();
      const utterance = new SpeechSynthesisUtterance(cleanText);

      // Select Indian Hindi or English voice
      const voices = window.speechSynthesis.getVoices();
      const hindiVoice = voices.find((v) => v.lang.includes('hi') || v.name.includes('Hindi') || v.lang.includes('IN'));
      if (hindiVoice) {
        utterance.voice = hindiVoice;
      }

      utterance.rate = 1.05;
      utterance.pitch = 1.0;

      const finishSpeaking = () => {
        this.isSpeaking = false;
        if (this.isRunning) {
          this.callbacks?.onStateChange('LISTENING');
          // Re-arm recognition
          try {
            this.recognition?.start();
          } catch {}
        } else {
          this.callbacks?.onStateChange('STANDBY');
        }
        resolve();
      };

      utterance.onend = finishSpeaking;
      utterance.onerror = finishSpeaking;

      window.speechSynthesis.speak(utterance);
    });
  }

  public stop(): void {
    this.isRunning = false;
    this.isSpeaking = false;

    if (this.animFrameId) {
      cancelAnimationFrame(this.animFrameId);
      this.animFrameId = null;
    }

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach((t) => t.stop());
      this.mediaStream = null;
    }

    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }

    if (this.recognition) {
      try {
        this.recognition.abort();
      } catch {}
      this.recognition = null;
    }

    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }

    this.callbacks?.onStateChange('STANDBY');
  }
}
