import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, Camera, Terminal, Search, Brain, ShieldAlert, CheckCircle2, ChevronDown, ChevronRight } from 'lucide-react';
import { ChatMessage } from '../types/electron';

interface VoiceAssistantProps {
  onStateChange: (state: 'READY' | 'LISTENING' | 'THINKING' | 'SPEAKING') => void;
  onRequestConfirm: (action: any) => void;
}

export const VoiceAssistant: React.FC<VoiceAssistantProps> = ({ onStateChange, onRequestConfirm }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'AI',
      response: `Greetings! I am **SKAI**, your local-first voice-driven desktop assistant engineered by **Sumeet Kumar** under **SK Enterprises**.\n\nI can execute real OS commands on your computer:
• **Launch/Close Apps** *(e.g., "open notepad", "launch calculator")*
• **File Management** *(e.g., "create a file called test.txt on desktop")*
• **Local Search** *(e.g., "search my documents for python")*
• **Screenshot Capture** *(e.g., "take a screenshot")*
• **Durable Memory** *(e.g., "remember that I prefer dark mode")*

Speak or type a command to begin!`,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [isListening, setIsListening] = useState(false);
  const [speechRec, setSpeechRec] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat feed
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize Web Speech API for voice recognition
  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
        onStateChange('LISTENING');
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        handleSend(transcript);
      };

      recognition.onerror = (event: any) => {
        console.warn('[VOICE ERROR]:', event.error);
        setIsListening(false);
        onStateChange('READY');
      };

      recognition.onend = () => {
        setIsListening(false);
        onStateChange('READY');
      };

      setSpeechRec(recognition);
    }
  }, []);

  const toggleMic = () => {
    if (!speechRec) {
      alert('Speech recognition is not supported in this browser environment. You can type commands directly.');
      return;
    }
    if (isListening) {
      speechRec.stop();
      setIsListening(false);
      onStateChange('READY');
    } else {
      speechRec.start();
    }
  };

  const speakText = (text: string) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const clean = text.replace(/[*#`_>\[\]]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(clean);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onstart = () => onStateChange('SPEAKING');
    utterance.onend = () => onStateChange('READY');
    utterance.onerror = () => onStateChange('READY');
    window.speechSynthesis.speak(utterance);
  };

  const handleSend = async (customQuery?: string) => {
    const queryText = (customQuery || input).trim();
    if (!queryText) return;

    setInput('');
    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      sender: 'USER',
      response: queryText,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    onStateChange('THINKING');

    try {
      const history = messages.map((m) => ({
        role: m.sender === 'USER' ? 'user' : 'model',
        content: m.response,
      }));

      const res = await window.skaiApi.sendMessage(queryText, history);

      if (res.action_id && (res as any).requires_confirmation) {
        onRequestConfirm({
          action_id: res.action_id,
          action_type: res.action || 'DESTRUCTIVE_ACTION',
          description: res.response,
        });
      }

      const aiMsg: ChatMessage = {
        id: `ai_${Date.now()}`,
        sender: 'AI',
        response: res.response || (res as any).text || 'Command processed.',
        thought_process: res.thought_process || (res as any).thought,
        action: res.action,
        action_id: res.action_id,
        tool_result: res.result,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, aiMsg]);
      onStateChange('READY');

      // Spoken voice feedback
      const voiceFeedback = res.voice_text || aiMsg.response.split('\n')[0];
      speakText(voiceFeedback);
    } catch (err: any) {
      onStateChange('READY');
      setMessages((prev) => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: 'AI',
          response: `❌ **Error executing command:** ${err.message || 'Unknown internal error'}`,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden p-3 gap-3">
      {/* Top Quick Actions Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        <span className="text-[10px] text-gray-500 font-mono font-bold uppercase tracking-wider">Quick Actions:</span>
        <button
          onClick={() => handleSend('take a screenshot')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-950/50 hover:bg-indigo-900/60 border border-indigo-500/30 text-indigo-200 transition"
        >
          <Camera className="w-3.5 h-3.5 text-indigo-400" />
          <span>Take Screenshot</span>
        </button>
        <button
          onClick={() => handleSend('open notepad')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-950/50 hover:bg-indigo-900/60 border border-indigo-500/30 text-indigo-200 transition"
        >
          <Terminal className="w-3.5 h-3.5 text-indigo-400" />
          <span>Open Notepad</span>
        </button>
        <button
          onClick={() => handleSend('search my documents for python')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-950/50 hover:bg-indigo-900/60 border border-indigo-500/30 text-indigo-200 transition"
        >
          <Search className="w-3.5 h-3.5 text-indigo-400" />
          <span>Search Files</span>
        </button>
        <button
          onClick={() => handleSend('what do you remember about my preferences?')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-950/50 hover:bg-indigo-900/60 border border-indigo-500/30 text-indigo-200 transition"
        >
          <Brain className="w-3.5 h-3.5 text-indigo-400" />
          <span>Recall Memory</span>
        </button>
      </div>

      {/* Main Conversation Stream */}
      <div className="flex-1 overflow-y-auto pr-2 space-y-3.5 font-sans text-sm">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.sender === 'USER' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`max-w-[82%] rounded-xl p-3.5 space-y-2 border ${
                msg.sender === 'USER'
                  ? 'bg-indigo-600/30 border-indigo-500/50 text-white rounded-br-none shadow-[0_0_15px_rgba(99,102,241,0.2)]'
                  : 'glass-panel text-gray-200 rounded-bl-none border-indigo-500/20'
              }`}
            >
              {/* Sender Label & Timestamp */}
              <div className="flex items-center justify-between gap-4 text-[10px] font-mono border-b border-white/10 pb-1">
                <span className={`font-bold ${msg.sender === 'USER' ? 'text-indigo-300' : 'text-indigo-400'}`}>
                  {msg.sender === 'USER' ? 'YOU' : 'SKAI ASSISTANT'}
                </span>
                <span className="text-gray-400">{msg.timestamp}</span>
              </div>

              {/* Message Content with Markdown Parsing */}
              <div className="text-xs leading-relaxed whitespace-pre-wrap">
                {msg.response}
              </div>

              {/* Screenshot Preview Image if returned */}
              {msg.tool_result?.thumbnail_data_uri && (
                <div className="mt-2 border border-indigo-500/40 rounded-lg overflow-hidden max-w-sm">
                  <img
                    src={msg.tool_result.thumbnail_data_uri}
                    alt="Screenshot"
                    className="w-full object-cover rounded"
                  />
                </div>
              )}

              {/* Thought Process Accordion */}
              {msg.thought_process && (
                <details className="mt-2 text-[10px] bg-black/40 p-2 rounded border border-indigo-950 text-gray-400">
                  <summary className="cursor-pointer font-mono font-bold text-indigo-400 hover:text-indigo-300">
                    Reasoning & Execution Trace
                  </summary>
                  <pre className="mt-1.5 whitespace-pre-wrap font-mono text-[10px] text-gray-300">
                    {msg.thought_process}
                  </pre>
                </details>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Interactive Command Input Bar */}
      <div className="glass-panel p-2 rounded-xl flex items-center gap-2 border-indigo-500/30">
        <button
          onClick={toggleMic}
          className={`p-2.5 rounded-lg border transition ${
            isListening
              ? 'mic-active text-white'
              : 'bg-indigo-950/60 border-indigo-500/40 text-indigo-300 hover:bg-indigo-900/80'
          }`}
          title={isListening ? 'Stop Listening' : 'Speak Command (Mic)'}
        >
          <Mic className="w-4 h-4" />
        </button>

        <button
          onClick={() => handleSend('take a screenshot')}
          className="p-2.5 rounded-lg bg-indigo-950/60 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-900/80 transition"
          title="Capture Screen"
        >
          <Camera className="w-4 h-4" />
        </button>

        {isListening && (
          <div className="flex items-center gap-1 px-2">
            <span className="wave-bar"></span>
            <span className="wave-bar"></span>
            <span className="wave-bar"></span>
            <span className="wave-bar"></span>
            <span className="wave-bar"></span>
          </div>
        )}

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Speak or type a command (e.g. open notepad, take a screenshot, search documents)..."
          className="flex-1 bg-transparent px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none font-sans"
        />

        <button
          onClick={() => handleSend()}
          disabled={!input.trim()}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:hover:bg-indigo-600 text-white font-bold text-xs rounded-lg flex items-center gap-1.5 shadow-[0_0_15px_rgba(99,102,241,0.4)] transition"
        >
          <span>EXECUTE</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
