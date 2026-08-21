import React from 'react';
import { Minus, Square, X, ShieldCheck, Settings, Radio } from 'lucide-react';

interface TopBarHUDProps {
  state: 'STANDBY' | 'LISTENING' | 'THINKING' | 'SPEAKING';
  hasKey: boolean;
  onOpenSettings: () => void;
}

export const TopBarHUD: React.FC<TopBarHUDProps> = ({ state, hasKey, onOpenSettings }) => {
  const handleControl = (action: 'minimize' | 'maximize' | 'close') => {
    if (window.skaiApi?.windowControl) {
      window.skaiApi.windowControl(action);
    }
  };

  const getStatusBadge = () => {
    switch (state) {
      case 'LISTENING':
        return (
          <div className="flex items-center gap-1.5 bg-rose-950/80 border border-rose-500/60 px-2.5 py-0.5 rounded-full text-[10px] text-rose-300 animate-pulse font-mono font-bold">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
            <span>VOICE CAPTURE ACTIVE</span>
          </div>
        );
      case 'THINKING':
        return (
          <div className="flex items-center gap-1.5 bg-amber-950/80 border border-amber-500/60 px-2.5 py-0.5 rounded-full text-[10px] text-amber-300 font-mono font-bold">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-spin"></span>
            <span>REASONING & ACTUATING</span>
          </div>
        );
      case 'SPEAKING':
        return (
          <div className="flex items-center gap-1.5 bg-cyan-950/80 border border-cyan-500/60 px-2.5 py-0.5 rounded-full text-[10px] text-cyan-300 font-mono font-bold">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
            <span>SYNTHESIZING AUDIO</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center gap-1.5 bg-cyan-950/40 border border-cyan-500/30 px-2.5 py-0.5 rounded-full text-[10px] text-cyan-400 font-mono">
            <Radio className="w-3 h-3 text-cyan-400 animate-pulse" />
            <span>ONLINE // STANDBY</span>
          </div>
        );
    }
  };

  return (
    <header className="h-10 bg-[#030305]/95 border-b border-cyan-950/80 flex items-center justify-between px-3 drag-region select-none z-50">
      {/* Left: Branding */}
      <div className="flex items-center space-x-2.5 no-drag">
        <div className="w-6 h-6 rounded bg-cyan-950/80 border border-cyan-400/50 flex items-center justify-center shadow-[0_0_12px_rgba(0,240,255,0.4)]">
          <span className="text-cyan-300 font-black text-xs">SK</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs font-black tracking-widest text-cyan-300">SKAI</span>
          <span className="text-[10px] text-gray-400 font-medium">| Powered by SK Enterprises</span>
          <span className="text-[9px] bg-cyan-950 border border-cyan-800/60 text-cyan-400 px-1.5 py-0.2 rounded font-mono">
            v0.0.1
          </span>
        </div>
      </div>

      {/* Center: State & Security Pill */}
      <div className="flex items-center space-x-3 no-drag">
        {getStatusBadge()}
        <button
          onClick={onOpenSettings}
          className="flex items-center space-x-1 text-[10px] text-gray-400 hover:text-cyan-300 px-2 py-0.5 rounded bg-black/50 border border-cyan-950 hover:border-cyan-800 transition font-mono"
        >
          <ShieldCheck className={`w-3 h-3 ${hasKey ? 'text-emerald-400' : 'text-amber-400'}`} />
          <span>{hasKey ? 'DPAPI ENCRYPTED' : 'KEY REQUIRED'}</span>
        </button>
      </div>

      {/* Right: Window Controls */}
      <div className="flex items-center space-x-1 no-drag">
        <button
          onClick={onOpenSettings}
          className="w-7 h-7 flex items-center justify-center text-gray-400 hover:text-cyan-300 hover:bg-cyan-950/40 rounded transition"
          title="Settings & Key Vault"
        >
          <Settings className="w-3.5 h-3.5" />
        </button>
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
