import React, { useState, useEffect, useRef } from 'react';
import { TopBarHUD } from './components/TopBarHUD';
import { HolographicCore } from './components/HolographicCore';
import { TelemetryHUD } from './components/TelemetryHUD';
import { TranscriptHUD } from './components/TranscriptHUD';
import { SettingsModal } from '../components/SettingsModal';
import { ActionConfirmModal } from '../components/ActionConfirmModal';
import { GeminiLiveService } from './services/gemini-live-service';
import { ClapDetector } from './utils/clapDetector';
import { Mic, Camera, Globe, Folder } from 'lucide-react';
import { ChatMessage, PendingAction } from '../types/electron';

export const App: React.FC = () => {
  const [assistantState, setAssistantState] = useState<'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING'>('STANDBY');
  const [hasKey, setHasKey] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [pendingAction, setPendingAction] = useState<PendingAction | null>(null);
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const liveServiceRef = useRef<GeminiLiveService>(new GeminiLiveService());
  const clapDetectorRef = useRef<ClapDetector | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'AI',
      response: `✨ **SKAI 4.0 — LIVE GEMINI VOICE & NATIVE TOOLS ACTIVE**
Architect: **Sumeet Kumar** | Powered by **SK Enterprises**

🎙️ **Live Bidirectional 2-Way Voice Stream (Hindi & Hinglish):**
• *"D drive kholo"* / *"Open D Drive"*
• *"Chrome kholo"* / *"Notepad chalu karo"*
• *"Calculator kholo"* / *"Screenshot le lo"*
• 👏 **Double-Clap Wake Detection Online**`,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  // Load persistent API keys on initial boot
  useEffect(() => {
    loadPersistentKeys();

    clapDetectorRef.current = new ClapDetector({
      onWake: () => {
        console.log('👏 Double-clap detected! Waking assistant...');
        if (!liveServiceRef.current.isConnected) {
          startLiveVoice();
        }
      },
    });
    clapDetectorRef.current.start();

    return () => {
      liveServiceRef.current.disconnect();
      clapDetectorRef.current?.stop();
    };
  }, []);

  const loadPersistentKeys = async () => {
    try {
      let key = '';

      if (window.electron?.ipcRenderer?.invoke) {
        const keys = await window.electron.ipcRenderer.invoke('get-api-keys');
        if (keys?.geminiKey) {
          key = keys.geminiKey;
        }
      }

      if (!key && window.skaiApi?.getApiKey) {
        key = (await window.skaiApi.getApiKey('google')) || '';
      }

      if (!key) {
        key = localStorage.getItem('skai_key_google') || '';
      }

      if (key && key.trim()) {
        setApiKey(key.trim());
        setHasKey(true);
      } else {
        setHasKey(false);
      }
    } catch (err) {
      console.warn('[KEY LOAD ERROR]:', err);
    }
  };

  const startLiveVoice = async () => {
    if (!apiKey || !apiKey.trim()) {
      setIsSettingsOpen(true);
      return;
    }

    setIsVoiceActive(true);
    await liveServiceRef.current.connect(apiKey, {
      onStateChange: (st) => {
        if (st === 'IDLE') {
          setAssistantState('STANDBY');
          setIsVoiceActive(false);
        } else {
          setAssistantState(st);
        }
      },
      onTranscript: (role, text) => {
        setMessages((prev) => [
          ...prev,
          {
            id: `${role}_${Date.now()}`,
            sender: role === 'user' ? 'USER' : 'AI',
            response: text,
            timestamp: new Date().toLocaleTimeString(),
          },
        ]);
      },
      onError: (err) => {
        setIsVoiceActive(false);
        setAssistantState('STANDBY');
        setMessages((prev) => [
          ...prev,
          {
            id: `err_${Date.now()}`,
            sender: 'AI',
            response: `⚠️ **Voice Error:** ${err}`,
            timestamp: new Date().toLocaleTimeString(),
          },
        ]);
      },
    });
  };

  const toggleVoice = () => {
    if (isVoiceActive) {
      liveServiceRef.current.disconnect();
      setIsVoiceActive(false);
      setAssistantState('STANDBY');
    } else {
      startLiveVoice();
    }
  };

  const handleSendMessage = async (queryText: string) => {
    if (!queryText.trim()) return;

    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      sender: 'USER',
      response: queryText,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setAssistantState('THINKING');

    const qLower = queryText.toLowerCase().trim();

    // 1. Direct High-Speed OS Tool Execution
    if (qLower.includes('d drive') || qLower.includes('d:') || qLower.includes('d ड्राइव')) {
      const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
        toolName: 'open_drive_or_folder',
        args: { target: 'D:\\' },
      });
      speakAndRecordResponse(res?.message || 'D Drive opened.');
      return;
    }

    if (qLower.includes('c drive') || qLower.includes('c:') || qLower.includes('c ड्राइव')) {
      const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
        toolName: 'open_drive_or_folder',
        args: { target: 'C:\\' },
      });
      speakAndRecordResponse(res?.message || 'C Drive opened.');
      return;
    }

    if (qLower.includes('chrome') || qLower.includes('browser') || qLower.includes('क्रोम')) {
      const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
        toolName: 'open_application',
        args: { app_name: 'chrome' },
      });
      speakAndRecordResponse(res?.message || 'Google Chrome opened.');
      return;
    }

    if (qLower.includes('notepad') || qLower.includes('नोटपैड')) {
      const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
        toolName: 'open_application',
        args: { app_name: 'notepad' },
      });
      speakAndRecordResponse(res?.message || 'Notepad opened.');
      return;
    }

    if (qLower.includes('calc') || qLower.includes('calculator') || qLower.includes('कैलकुलेटर')) {
      const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
        toolName: 'open_application',
        args: { app_name: 'calc' },
      });
      speakAndRecordResponse(res?.message || 'Calculator opened.');
      return;
    }

    if (qLower.includes('screenshot') || qLower.includes('स्क्रीनशॉट')) {
      const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
        toolName: 'take_screenshot',
        args: {},
      });
      speakAndRecordResponse(res?.message || 'Screenshot captured.');
      return;
    }

    // 2. Direct Gemini Live / REST Query
    if (apiKey) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey.trim()}`;
        const resp = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [
              {
                role: 'user',
                parts: [
                  {
                    text: `You are SK AI created by Sumeet Kumar (Powered by SK Enterprises). Answer in concise, polite Hindi/Hinglish: ${queryText}`,
                  },
                ],
              },
            ],
            generationConfig: { maxOutputTokens: 180 },
          }),
        });

        if (resp.ok) {
          const data = await resp.json();
          const reply = data.candidates?.[0]?.content?.parts?.[0]?.text;
          if (reply) {
            speakAndRecordResponse(reply);
            return;
          }
        }
      } catch (err) {
        console.warn('[GEMINI FETCH ERROR]:', err);
      }
    }

    speakAndRecordResponse('कृपया सेटिंग्स (⚙) में अपनी Google Gemini API Key दर्ज करें।');
  };

  const speakAndRecordResponse = (responseText: string) => {
    setAssistantState('SPEAKING');
    setMessages((prev) => [
      ...prev,
      {
        id: `ai_${Date.now()}`,
        sender: 'AI',
        response: responseText,
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);

    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(responseText.replace(/[*#`_]/g, ''));
      const voices = window.speechSynthesis.getVoices();
      const hindiVoice = voices.find((v) => v.lang.includes('hi') || v.name.includes('Hindi') || v.lang.includes('IN'));
      if (hindiVoice) u.voice = hindiVoice;
      u.rate = 1.05;
      u.onend = () => setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');
      u.onerror = () => setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');
      window.speechSynthesis.speak(u);
    } else {
      setTimeout(() => setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY'), 1000);
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-[#030305] text-gray-100 overflow-hidden font-sans select-none relative">
      {/* 1. Top Bar */}
      <TopBarHUD
        state={assistantState}
        hasKey={hasKey}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* 2. Master Sci-Fi Dashboard Layout */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Left Telemetry HUD */}
        <TelemetryHUD onQuickAction={handleSendMessage} />

        {/* Center: 3D Holographic Core */}
        <div className="flex-1 flex flex-col items-center justify-between relative overflow-hidden p-4">
          <div className="text-center space-y-1 z-10">
            <span className="text-[10px] font-mono tracking-[0.3em] text-cyan-400/80 uppercase">
              // GEMINI LIVE 2-WAY QUANTUM AUDIO CORE //
            </span>
            <h1 className="text-lg font-black tracking-widest text-cyan-300 drop-shadow-[0_0_15px_rgba(0,240,255,0.6)]">
              SKAI PLATFORM
            </h1>
          </div>

          <div className="w-full h-80 flex items-center justify-center">
            <HolographicCore state={assistantState} />
          </div>

          {/* Quick Action Control Bar */}
          <div className="glass-panel p-2 rounded-2xl flex items-center gap-3 border border-cyan-500/30 shadow-[0_0_30px_rgba(0,240,255,0.15)] z-10">
            <button
              onClick={toggleVoice}
              className={`p-3 rounded-xl transition flex items-center gap-2 font-mono text-xs font-bold ${
                isVoiceActive
                  ? 'bg-rose-600 border border-rose-400 text-white animate-pulse shadow-[0_0_20px_rgba(244,63,94,0.8)]'
                  : 'bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/50 text-cyan-300'
              }`}
            >
              <Mic className="w-4 h-4" />
              <span>{isVoiceActive ? 'VOICE LIVE (MUTE)' : 'START LIVE GEMINI VOICE'}</span>
            </button>

            <button
              onClick={() => handleSendMessage('D drive kholo')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Folder className="w-4 h-4 text-cyan-400" />
              <span>OPEN D DRIVE</span>
            </button>

            <button
              onClick={() => handleSendMessage('screenshot le lo')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Camera className="w-4 h-4 text-cyan-400" />
              <span>SCREENSHOT</span>
            </button>

            <button
              onClick={() => handleSendMessage('chrome kholo')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Globe className="w-4 h-4 text-cyan-400" />
              <span>CHROME</span>
            </button>
          </div>
        </div>

        {/* Right Transcript HUD */}
        <TranscriptHUD
          messages={messages}
          isListening={isVoiceActive}
          onSendMessage={handleSendMessage}
          onToggleMic={toggleVoice}
        />
      </div>

      {/* 3. Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onKeyUpdated={loadPersistentKeys}
      />

      {/* 4. Action Confirmation Modal */}
      <ActionConfirmModal
        action={pendingAction}
        onResolved={() => setPendingAction(null)}
      />
    </div>
  );
};
