import React, { useState, useEffect } from 'react';
import { TitleBar } from './components/TitleBar';
import { VoiceAssistant } from './components/VoiceAssistant';
import { CodingHelper } from './components/CodingHelper';
import { MemoryInspector } from './components/MemoryInspector';
import { WebSearchTool } from './components/WebSearchTool';
import { AuditTimeline } from './components/AuditTimeline';
import { SettingsModal } from './components/SettingsModal';
import { ActionConfirmModal } from './components/ActionConfirmModal';
import { MessageSquare, Code, Brain, Globe, History, Settings, ShieldAlert } from 'lucide-react';
import { PendingAction } from './types/electron';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'code' | 'memory' | 'search' | 'audit'>('chat');
  const [hasKey, setHasKey] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [assistantState, setAssistantState] = useState<'READY' | 'LISTENING' | 'THINKING' | 'SPEAKING'>('READY');
  const [pendingAction, setPendingAction] = useState<PendingAction | null>(null);

  useEffect(() => {
    checkApiKey();
  }, []);

  const checkApiKey = async () => {
    try {
      if (window.skaiApi?.hasApiKey) {
        const has = await window.skaiApi.hasApiKey('google');
        setHasKey(has);
      }
    } catch (err) {
      console.warn('Key check failed:', err);
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-[#090a10] text-gray-100 overflow-hidden font-sans select-none">
      {/* 1. Custom TitleBar */}
      <TitleBar
        hasKey={hasKey}
        state={assistantState}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* 2. Main Body Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar Navigation */}
        <aside className="w-16 bg-[#0c0e17]/90 border-r border-indigo-950/80 flex flex-col items-center py-3.5 justify-between">
          <div className="flex flex-col items-center gap-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`p-3 rounded-xl transition ${
                activeTab === 'chat'
                  ? 'bg-indigo-600/30 text-indigo-400 border border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
              }`}
              title="Voice & Chat Assistant"
            >
              <MessageSquare className="w-5 h-5" />
            </button>

            <button
              onClick={() => setActiveTab('code')}
              className={`p-3 rounded-xl transition ${
                activeTab === 'code'
                  ? 'bg-indigo-600/30 text-indigo-400 border border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
              }`}
              title="Coding Helper Mode"
            >
              <Code className="w-5 h-5" />
            </button>

            <button
              onClick={() => setActiveTab('memory')}
              className={`p-3 rounded-xl transition ${
                activeTab === 'memory'
                  ? 'bg-indigo-600/30 text-indigo-400 border border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
              }`}
              title="Local Vector Memory Store"
            >
              <Brain className="w-5 h-5" />
            </button>

            <button
              onClick={() => setActiveTab('search')}
              className={`p-3 rounded-xl transition ${
                activeTab === 'search'
                  ? 'bg-indigo-600/30 text-indigo-400 border border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
              }`}
              title="Web Awareness Tool"
            >
              <Globe className="w-5 h-5" />
            </button>

            <button
              onClick={() => setActiveTab('audit')}
              className={`p-3 rounded-xl transition ${
                activeTab === 'audit'
                  ? 'bg-indigo-600/30 text-indigo-400 border border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
              }`}
              title="Audit Action Timeline"
            >
              <History className="w-5 h-5" />
            </button>
          </div>

          <div className="flex flex-col items-center">
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="p-3 rounded-xl text-gray-400 hover:text-indigo-300 hover:bg-white/5 transition"
              title="Settings & Key Vault"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </aside>

        {/* Center Content View */}
        <main className="flex-1 flex flex-col overflow-hidden bg-[#090a10]">
          {activeTab === 'chat' && (
            <VoiceAssistant
              onStateChange={setAssistantState}
              onRequestConfirm={(action) => setPendingAction(action)}
            />
          )}

          {activeTab === 'code' && <CodingHelper />}
          {activeTab === 'memory' && <MemoryInspector />}
          {activeTab === 'search' && <WebSearchTool />}
          {activeTab === 'audit' && <AuditTimeline />}
        </main>
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
