import React, { useState, useEffect, useRef } from 'react';
import { TopBarHUD } from './components/TopBarHUD';
import { HolographicCore } from './components/HolographicCore';
import { TelemetryHUD } from './components/TelemetryHUD';
import { TranscriptHUD } from './components/TranscriptHUD';
import { SettingsModal } from '../components/SettingsModal';
import { ActionConfirmModal } from '../components/ActionConfirmModal';
import { VoiceEngine } from './services/voice-engine';
import { ClapDetector } from './utils/clapDetector';
import { Mic, Camera, Globe, Folder } from 'lucide-react';
import { ChatMessage, PendingAction } from '../types/electron';

export const App: React.FC = () => {
  const [assistantState, setAssistantState] = useState<'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING'>('STANDBY');
  const [audioLevel, setAudioLevel] = useState(0);
  const [hasKey, setHasKey] = useState(false);
  const [googleKey, setGoogleKey] = useState('');
  const [hfToken, setHfToken] = useState('');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [pendingAction, setPendingAction] = useState<PendingAction | null>(null);
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const voiceEngineRef = useRef<VoiceEngine>(new VoiceEngine());
  const clapDetectorRef = useRef<ClapDetector | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'AI',
      response: `✨ **SKAI 4.0 — 2-WAY HINDI VOICE ASSISTANT ONLINE**
Architect: **Sumeet Kumar** | Powered by **SK Enterprises**

🎙️ **2-Way Voice Communication Active (Pure Hindi & Hinglish):**
• *"D drive kholo"* / *"Open D Drive"*
• *"Chrome kholo"* / *"Notepad chalu karo"*
• *"Calculator kholo"* / *"Screenshot le lo"*
• 👏 **Double-Clap Wake Detection Ready**`,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  useEffect(() => {
    loadApiKeys();

    // Initialize Double-Clap Wake Detector
    clapDetectorRef.current = new ClapDetector({
      onWake: () => {
        console.log('👏 Double-clap detected! Waking assistant...');
        if (!isVoiceActive) {
          startVoice();
        } else {
          voiceEngineRef.current.speakResponse('हाँ जी Sumeet Sir, मैं सुन रहा हूँ। क्या करना है?');
        }
      },
    });
    clapDetectorRef.current.start();

    return () => {
      voiceEngineRef.current.stop();
      clapDetectorRef.current?.stop();
    };
  }, []);

  const loadApiKeys = async () => {
    try {
      let gKey = '';
      let hf = '';
      if (window.skaiApi?.getApiKey) {
        gKey = (await window.skaiApi.getApiKey('google')) || '';
        hf = (await window.skaiApi.getApiKey('huggingface')) || '';
      }
      if (!gKey) gKey = localStorage.getItem('skai_key_google') || '';
      if (!hf) hf = localStorage.getItem('skai_key_huggingface') || '';

      setGoogleKey(gKey);
      setHfToken(hf);
      setHasKey(Boolean(gKey || hf));
      voiceEngineRef.current.setKeys(gKey, hf);
    } catch (err) {
      console.warn('Key check error:', err);
    }
  };

  const startVoice = async () => {
    setIsVoiceActive(true);
    voiceEngineRef.current.init(googleKey, hfToken);

    await voiceEngineRef.current.start({
      onStateChange: (st) => setAssistantState(st),
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
      onAudioLevel: (lvl) => setAudioLevel(lvl),
      onError: (err) => {
        setIsVoiceActive(false);
        setAssistantState('STANDBY');
        setMessages((prev) => [
          ...prev,
          {
            id: `err_${Date.now()}`,
            sender: 'AI',
            response: `⚠️ **Voice Info:** ${err}`,
            timestamp: new Date().toLocaleTimeString(),
          },
        ]);
      },
    });
  };

  const toggleVoice = () => {
    if (isVoiceActive) {
      voiceEngineRef.current.stop();
      setIsVoiceActive(false);
      setAssistantState('STANDBY');
    } else {
      startVoice();
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
    await voiceEngineRef.current.handleUserQuery(queryText);
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
              // 2-WAY HINDI VOICE & HOLOGRAPHIC CORE //
            </span>
            <h1 className="text-lg font-black tracking-widest text-cyan-300 drop-shadow-[0_0_15px_rgba(0,240,255,0.6)]">
              SKAI PLATFORM
            </h1>
          </div>

          <div className="w-full h-80 flex items-center justify-center">
            <HolographicCore state={assistantState} audioLevel={audioLevel} />
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
              <span>{isVoiceActive ? 'VOICE LIVE (बोलिए)' : 'START 2-WAY VOICE'}</span>
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
        onKeyUpdated={loadApiKeys}
      />

      {/* 4. Action Confirmation Modal */}
      <ActionConfirmModal
        action={pendingAction}
        onResolved={() => setPendingAction(null)}
      />
    </div>
  );
};
