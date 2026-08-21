import React, { useState, useEffect, useRef } from 'react';
import { Send, Mic, Terminal, Globe, Brain, Sparkles, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { ChatMessage } from '../../types/electron';

interface TranscriptHUDProps {
  messages: ChatMessage[];
  isListening: boolean;
  onSendMessage: (query: string) => void;
  onToggleMic: () => void;
}

export const TranscriptHUD: React.FC<TranscriptHUDProps> = ({
  messages,
  isListening,
  onSendMessage,
  onToggleMic,
}) => {
  const [input, setInput] = useState('');
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="w-96 h-full flex flex-col gap-3 p-3 text-xs select-none overflow-hidden">
      {/* Header */}
      <div className="glass-panel p-2.5 rounded-xl border border-cyan-500/25 flex items-center justify-between font-mono">
        <div className="flex items-center gap-1.5 text-cyan-400 font-bold text-[11px]">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <span>BILINGUAL TRANSCRIPT & LOG</span>
        </div>
        <span className="text-[9px] bg-cyan-950/80 border border-cyan-500/40 px-1.5 py-0.5 rounded text-cyan-300">
          EN / HI
        </span>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-1 font-sans">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.sender === 'USER' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`max-w-[90%] rounded-xl p-3 space-y-1.5 border text-xs leading-relaxed ${
                msg.sender === 'USER'
                  ? 'bg-cyan-950/60 border-cyan-500/50 text-cyan-100 rounded-br-none shadow-[0_0_15px_rgba(0,240,255,0.15)]'
                  : 'glass-panel text-gray-200 rounded-bl-none border-cyan-500/25'
              }`}
            >
              <div className="flex items-center justify-between gap-3 text-[10px] font-mono border-b border-white/10 pb-1">
                <span className={`font-bold ${msg.sender === 'USER' ? 'text-cyan-400' : 'text-emerald-400'}`}>
                  {msg.sender === 'USER' ? 'OPERATOR' : 'SKAI CORE'}
                </span>
                <span className="text-gray-500">{msg.timestamp}</span>
              </div>

              <div className="whitespace-pre-wrap font-sans text-xs">{msg.response}</div>

              {msg.tool_result?.thumbnail_data_uri && (
                <div className="mt-2 border border-cyan-500/40 rounded-lg overflow-hidden max-w-xs">
                  <img
                    src={msg.tool_result.thumbnail_data_uri}
                    alt="Screenshot"
                    className="w-full object-cover rounded"
                  />
                </div>
              )}

              {msg.thought_process && (
                <details className="mt-1.5 text-[10px] bg-black/50 p-1.5 rounded border border-cyan-950 text-gray-400 font-mono">
                  <summary className="cursor-pointer font-bold text-cyan-400">Execution Trace</summary>
                  <pre className="mt-1 whitespace-pre-wrap text-[10px] text-gray-300 font-mono">
                    {msg.thought_process}
                  </pre>
                </details>
              )}
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      {/* Input Bar */}
      <div className="glass-panel p-2 rounded-xl flex items-center gap-1.5 border border-cyan-500/30">
        <button
          onClick={onToggleMic}
          className={`p-2 rounded-lg border transition ${
            isListening
              ? 'bg-rose-600 border-rose-400 text-white animate-pulse shadow-[0_0_15px_rgba(244,63,94,0.6)]'
              : 'bg-cyan-950/60 border-cyan-500/40 text-cyan-400 hover:bg-cyan-900/60'
          }`}
          title="Toggle Voice Mic (Hindi & English)"
        >
          <Mic className="w-4 h-4" />
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Command in English or Hindi (e.g. open calc, screenshot lo)..."
          className="flex-1 bg-transparent px-2 py-1 text-xs text-white placeholder-gray-500 focus:outline-none font-sans"
        />

        <button
          onClick={handleSend}
          disabled={!input.trim()}
          className="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-30 text-black font-bold text-xs rounded-lg flex items-center gap-1 shadow-[0_0_10px_rgba(0,240,255,0.4)] transition"
        >
          <span>SEND</span>
          <Send className="w-3 h-3" />
        </button>
      </div>
    </div>
  );
};
