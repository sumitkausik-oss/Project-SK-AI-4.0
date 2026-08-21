import React, { useState, useEffect, useRef } from 'react';
import { TopBarHUD } from './components/TopBarHUD';
import { HolographicCore } from './components/HolographicCore';
import { TelemetryHUD } from './components/TelemetryHUD';
import { TranscriptHUD } from './components/TranscriptHUD';
import { SettingsModal } from '../components/SettingsModal';
import { ActionConfirmModal } from '../components/ActionConfirmModal';
import { VoiceService, VoiceState } from './services/voice-service';
import { ClapDetector } from './utils/clapDetector';
import { Mic, Camera, Globe, Sparkles } from 'lucide-react';
import { ChatMessage, PendingAction } from '../types/electron';

export const App: React.FC = () => {
  const [assistantState, setAssistantState] = useState<'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING'>('STANDBY');
  const [audioLevel, setAudioLevel] = useState(0);
  const [hasKey, setHasKey] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [pendingAction, setPendingAction] = useState<PendingAction | null>(null);
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const voiceServiceRef = useRef<VoiceService | null>(null);
  const clapDetectorRef = useRef<ClapDetector | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'AI',
      response: `SYSTEM READY // **SKAI HOLOGRAPHIC QUANTUM CORE**
Architect: **Sumeet Kumar** | Powered by **SK Enterprises**

Bilingual duplex intelligence active (English, Hindi & Hinglish).
• "Open notepad" / "Notepad chalu karo"
• "Take a screenshot" / "Screenshot le lo"
• "Search web for AI news"
• 👏 **Double-Clap Wake Detection Active**`,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  useEffect(() => {
    checkApiKey();
    initVoiceAndClapEngine();

    return () => {
      voiceServiceRef.current?.stop();
      clapDetectorRef.current?.stop();
    };
  }, []);

  const checkApiKey = async () => {
    try {
      if (window.skaiApi?.hasApiKey) {
        const has = await window.skaiApi.hasApiKey('google');
        setHasKey(has);
      }
    } catch (err) {
      console.warn('Key check error:', err);
    }
  };

  const initVoiceAndClapEngine = () => {
    // 1. Initialize Voice Service with 4096-frame chunking and auto-reconnect
    voiceServiceRef.current = new VoiceService({
      onStateChange: (vState: VoiceState) => {
        if (vState === 'LISTENING') setAssistantState('LISTENING');
        else if (vState === 'SPEAKING') setAssistantState('SPEAKING');
        else if (vState === 'DISCONNECTED') setAssistantState('STANDBY');
      },
      onAudioLevel: (lvl: number) => {
        setAudioLevel(lvl);
      },
      onTranscript: (transcript: string) => {
        handleSendMessage(transcript);
      },
      onError: (err: string) => {
        console.warn('[VOICE SERVICE] Error:', err);
      },
    });

    // 2. Initialize Double-Clap Wake Detector
    clapDetectorRef.current = new ClapDetector({
      onWake: () => {
        console.log('👏 Double-clap detected! Waking assistant...');
        handleSendMessage('System wake: Greetings SKAI');
      },
    });
    clapDetectorRef.current.start();
  };

  const toggleVoice = () => {
    if (!voiceServiceRef.current) return;

    if (isVoiceActive) {
      voiceServiceRef.current.stop();
      setIsVoiceActive(false);
      setAssistantState('STANDBY');
    } else {
      voiceServiceRef.current.start();
      setIsVoiceActive(true);
      setAssistantState('LISTENING');
    }
  };

  const speakText = (text: string) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    voiceServiceRef.current?.setSpeakingLocally(true);

    const clean = text.replace(/[*#`_>\[\]]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(clean);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    utterance.onstart = () => setAssistantState('SPEAKING');
    utterance.onend = () => {
      setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');
      voiceServiceRef.current?.setSpeakingLocally(false);
    };
    utterance.onerror = () => {
      setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');
      voiceServiceRef.current?.setSpeakingLocally(false);
    };
    window.speechSynthesis.speak(utterance);
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
      const history = messages.map((m) => ({
        role: m.sender === 'USER' ? 'user' : 'model',
        content: m.response,
      }));

      const res = await window.skaiApi.sendMessage(queryText, history);

      if (res.action_id && (res as any).requires_confirmation) {
        setPendingAction({
          action_id: res.action_id,
          action_type: res.action || 'DESTRUCTIVE_ACTION',
          description: res.response,
          category: 'DESTRUCTIVE_HIGH_IMPACT',
          params: {},
          status: 'PENDING',
          created_at: new Date().toISOString(),
        });
      }

      const aiMsg: ChatMessage = {
        id: `ai_${Date.now()}`,
        sender: 'AI',
        response: res.response || (res as any).text || 'Command executed.',
        thought_process: res.thought_process || (res as any).thought,
        action: res.action,
        action_id: res.action_id,
        tool_result: res.result,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, aiMsg]);
      setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');

      const voiceFeedback = res.voice_text || aiMsg.response.split('\n')[0];
      speakText(voiceFeedback);
    } catch (err: any) {
      setAssistantState(isVoiceActive ? 'LISTENING' : 'STANDBY');
      setMessages((prev) => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: 'AI',
          response: `❌ **Execution Error:** ${err.message || 'Fault encountered.'}`,
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
              onClick={() => handleSendMessage('take a screenshot')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Camera className="w-4 h-4 text-cyan-400" />
              <span>VISION CAPTURE</span>
            </button>

            <button
              onClick={() => handleSendMessage('search web for latest AI breakthroughs')}
              className="p-3 rounded-xl bg-black/60 hover:bg-cyan-950/60 border border-cyan-900/60 text-gray-300 hover:text-cyan-300 transition flex items-center gap-1.5 text-xs font-mono"
            >
              <Globe className="w-4 h-4 text-cyan-400" />
              <span>WEB RADAR</span>
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
