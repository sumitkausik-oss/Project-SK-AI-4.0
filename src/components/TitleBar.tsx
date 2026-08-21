import React from 'react';
import { Minus, Square, X, Cpu, ShieldCheck } from 'lucide-react';

interface TitleBarProps {
  hasKey: boolean;
  state: 'READY' | 'LISTENING' | 'THINKING' | 'SPEAKING';
  onOpenSettings: () => void;
}

export const TitleBar: React.FC<TitleBarProps> = ({ hasKey, state, onOpenSettings }) => {
  const handleControl = (action: 'minimize' | 'maximize' | 'close') => {
    if (window.skaiApi?.windowControl) {
      window.skaiApi.windowControl(action);
    }
  };

  const getStatePill = () => {
    switch (state) {
      case 'LISTENING':
        return (
          <div className="flex items-center space-x-1.5 bg-rose-950/80 border border-rose-500/60 px-2.5 py-0.5 rounded-full text-[11px] text-rose-300 animate-pulse">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
            <span className="font-mono font-semibold tracking-wider">LISTENING...</span>
          </div>
        );
      case 'THINKING':
        return (
          <div className="flex items-center space-x-1.5 bg-amber-950/80 border border-amber-500/60 px-2.5 py-0.5 rounded-full text-[11px] text-amber-300">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-spin"></span>
            <span className="font-mono font-semibold tracking-wider">REASONING & ACTING...</span>
          </div>
        );
      case 'SPEAKING':
        return (
          <div className="flex items-center space-x-1.5 bg-indigo-950/80 border border-indigo-500/60 px-2.5 py-0.5 rounded-full text-[11px] text-indigo-300">
            <div className="flex items-center space-x-0.5">
              <span className="wave-bar !h-3 !bg-indigo-400"></span>
              <span className="wave-bar !h-4 !bg-indigo-400"></span>
              <span className="wave-bar !h-2 !bg-indigo-400"></span>
            </div>
            <span className="font-mono font-semibold tracking-wider">SPEAKING</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center space-x-1.5 bg-indigo-950/40 border border-indigo-500/30 px-2.5 py-0.5 rounded-full text-[11px] text-indigo-300">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
            <span className="font-mono font-medium">LOCAL CONTROL ACTIVE</span>
          </div>
        );
    }
  };

  return (
    <header className="h-10 bg-[#090a10]/95 border-b border-indigo-950/80 flex items-center justify-between px-3 drag-region select-none z-50">
      {/* Left: Branding */}
      <div className="flex items-center space-x-2.5 no-drag">
        <div className="w-6 h-6 rounded-lg bg-indigo-900/60 border border-indigo-400/50 flex items-center justify-center shadow-[0_0_10px_rgba(99,102,241,0.4)]">
          <span className="text-indigo-300 font-black text-xs">SK</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs font-black tracking-widest text-indigo-300">SKAI</span>
          <span className="text-[10px] text-gray-400 font-medium">| Powered by SK Enterprises</span>
          <span className="text-[9px] bg-indigo-950 border border-indigo-800/60 text-indigo-400 px-1.5 py-0.2 rounded font-mono">v0.0.1</span>
        </div>
      </div>

      {/* Center: State & Security Pill */}
      <div className="flex items-center space-x-3 no-drag">
        {getStatePill()}
        <button
          onClick={onOpenSettings}
          className="flex items-center space-x-1 text-[11px] text-gray-400 hover:text-indigo-300 px-2 py-0.5 rounded bg-black/40 border border-gray-800/60 transition"
        >
          <ShieldCheck className={`w-3.5 h-3.5 ${hasKey ? 'text-emerald-400' : 'text-amber-400'}`} />
          <span className="font-mono">{hasKey ? 'DPAPI ENCRYPTED' : 'KEY REQUIRED'}</span>
        </button>
      </div>

      {/* Right: Window Controls */}
      <div className="flex items-center space-x-1 no-drag">
        <button
          onClick={() => handleControl('minimize')}
          className="w-7 h-7 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 rounded transition"
          title="Minimize"
        >
          <Minus className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => handleControl('maximize')}
          className="w-7 h-7 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 rounded transition"
          title="Maximize"
        >
          <Square className="w-3 h-3" />
        </button>
        <button
          onClick={() => handleControl('close')}
          className="w-7 h-7 flex items-center justify-center text-gray-400 hover:text-white hover:bg-rose-600 rounded transition"
          title="Close"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </header>
  );
};
