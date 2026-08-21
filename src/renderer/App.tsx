import React, { useState, useEffect, useRef } from 'react';
import { TopBarHUD } from './components/TopBarHUD';
import { HolographicCore } from './components/HolographicCore';
import { TelemetryHUD } from './components/TelemetryHUD';
import { TranscriptHUD } from './components/TranscriptHUD';
import { SettingsModal } from '../components/SettingsModal';
import { ActionConfirmModal } from '../components/ActionConfirmModal';
import { GeminiLiveService } from './services/gemini-live-service';
import { ClapDetector } from './utils/clapDetector';
import { Mic, Camera, Globe } from 'lucide-react';
import { ChatMessage, PendingAction } from '../types/electron';

export const App: React.FC = () => {
  const [assistantState, setAssistantState] = useState<'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING'>('STANDBY');
  const [audioLevel, setAudioLevel] = useState(0);
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
      response: `✨ **SKAI 4.0 — QUANTUM BILINGUAL CORE ONLINE**
Architect: **Sumeet Kumar** | Powered by **SK Enterprises**

🎙️ **Gemini Live 2-Way Voice Stream Ready (Hindi & English):**
• *"Chrome kholo"* / *"Open Google Chrome"*
• *"Notepad chalu karo"* / *"Launch Calculator"*
• *"Screenshot le lo"* / *"Take display screenshot"*
• 👏 **Double-Clap Wake Detection Active**`,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  useEffect(() => {
    checkApiKey();

    // Initialize Double-Clap Wake Detector
    clapDetectorRef.current = new ClapDetector({
      onWake: () => {
        console.log('👏 Double-clap detected! Waking assistant...');
        if (!liveServiceRef.current.isConnected && apiKey) {
          startLiveVoice();
        } else {
          handleSendMessage('Namaste SKAI! Ready for instructions.');
        }
      },
    });
    clapDetectorRef.current.start();

    return () => {
      liveServiceRef.current.disconnect();
      clapDetectorRef.current?.stop();
    };
  }, [apiKey]);

  const checkApiKey = async () => {
    try {
      if (window.skaiApi?.getApiKey) {
        const key = await window.skaiApi.getApiKey('google');
        if (key && key.trim()) {
          setApiKey(key.trim());
          setHasKey(true);
        } else {
          setHasKey(false);
        }
      }
    } catch (err) {
      console.warn('Key check error:', err);
    }
  };

  const startLiveVoice = async () => {
    if (!apiKey) {
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
      onAudioLevel: (lvl) => setAudioLevel(lvl),
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

    try {
      let responseText = '';
      const qLower = queryText.toLowerCase().trim();

      // Fast Local Tool Execution Dispatch
      if (qLower.includes('chrome') || qLower.includes('browser')) {
        const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
          toolName: 'open_browser',
          args: { app_name: 'chrome' },
        });
        responseText = res?.message || 'Google Chrome opened.';
      } else if (qLower.includes('notepad')) {
        const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
          toolName: 'open_application',
          args: { app_name: 'notepad' },
        });
        responseText = res?.message || 'Notepad opened.';
      } else if (qLower.includes('calc') || qLower.includes('calculator')) {
        const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
          toolName: 'open_application',
          args: { app_name: 'calc' },
        });
        responseText = res?.message || 'Calculator opened.';
      } else if (qLower.includes('screenshot')) {
        const res = await window.electron?.ipcRenderer?.invoke('execute-system-tool', {
          toolName: 'take_screenshot',
          args: {},
        });
        responseText = res?.message || 'Screenshot captured and saved.';
      } else {
        // AI query
        if (apiKey) {
          responseText = `हाँ जी Sumeet Kumar सर, मैंने आपका निर्देश नोट कर लिया है: "${queryText}"`;
        } else {
          responseText = `कमांड निष्पादित: "${queryText}". लाइव AI बातचीत के लिए कृपया सेटिंग्स में जाकर Gemini API Key सेव करें।`;
        }
      }

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

      // Speak feedback
      if (window.speechSynthesis) {
        const u = new SpeechSynthesisUtterance(responseText.replace(/[*#`_]/g, ''));
        u.onend = () => setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');
        window.speechSynthesis.speak(u);
      } else {
        setTimeout(() => setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY'), 1200);
      }
    } catch (err: any) {
      setAssistantState('STANDBY');
      setMessages((prev) => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: 'AI',
          response: `❌ Error: ${err.message}`,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
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
              // HOLOGRAPHIC QUANTUM INTERACTION CORE //
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
              <span>{isVoiceActive ? 'VOICE LIVE (MUTE)' : 'ACTIVATE VOICE'}</span>
            </button>

            <button
              onClick={() => handleSendMessage('take screenshot')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Camera className="w-4 h-4 text-cyan-400" />
              <span>VISION CAPTURE</span>
            </button>

            <button
              onClick={() => handleSendMessage('open chrome')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Globe className="w-4 h-4 text-cyan-400" />
              <span>LAUNCH CHROME</span>
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
        onKeyUpdated={checkApiKey}
      />

      {/* 4. Action Confirmation Modal */}
      <ActionConfirmModal
        action={pendingAction}
        onResolved={() => setPendingAction(null)}
      />
    </div>
  );
};
