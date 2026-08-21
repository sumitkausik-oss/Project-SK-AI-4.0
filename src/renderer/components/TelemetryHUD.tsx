import React, { useState, useEffect } from 'react';
import { Activity, Cpu, HardDrive, Terminal, Camera, Calculator, FileText, Monitor, ShieldCheck } from 'lucide-react';
import { SystemTelemetry } from '../../types/electron';

interface TelemetryHUDProps {
  onQuickAction: (cmd: string) => void;
}

export const TelemetryHUD: React.FC<TelemetryHUDProps> = ({ onQuickAction }) => {
  const [telemetry, setTelemetry] = useState<SystemTelemetry>({
    cpuPercent: 12,
    cpuCores: 8,
    cpuModel: 'Intel Core i7 / AMD Ryzen',
    ramTotalGB: '16.0',
    ramUsedGB: '6.4',
    ramFreeGB: '9.6',
    ramPercent: 40,
    uptimeHours: '4.2',
    platform: 'Windows NT (x64)',
    hostname: 'DESKTOP-NODE',
    timestamp: new Date().toISOString(),
  });

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        if (window.skaiApi?.getTelemetry) {
          const data = await window.skaiApi.getTelemetry();
          setTelemetry(data);
        }
      } catch (err) {
        console.warn('Telemetry poll error:', err);
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-80 h-full flex flex-col gap-3 p-3 text-xs font-mono select-none overflow-y-auto">
      {/* 1. Header Card */}
      <div className="glass-panel p-3 rounded-xl border border-cyan-500/25 space-y-1">
        <div className="flex items-center justify-between text-[11px] font-bold text-cyan-400">
          <div className="flex items-center gap-1.5">
            <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
            <span>SYSTEM TELEMETRY</span>
          </div>
          <span className="text-[9px] bg-cyan-950/80 border border-cyan-500/40 px-1.5 py-0.5 rounded text-cyan-300">
            LIVE
          </span>
        </div>
        <p className="text-[10px] text-gray-400 truncate">{telemetry.cpuModel}</p>
      </div>

      {/* 2. CPU Metric Panel */}
      <div className="glass-panel p-3 rounded-xl border border-cyan-500/25 space-y-2">
        <div className="flex items-center justify-between text-gray-300">
          <div className="flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>CPU UTILIZATION</span>
          </div>
          <span className="font-bold text-cyan-300">{telemetry.cpuPercent}%</span>
        </div>
        <div className="w-full h-1.5 bg-black/60 rounded-full overflow-hidden border border-cyan-950">
          <div
            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-500"
            style={{ width: `${telemetry.cpuPercent}%` }}
          />
        </div>
        <div className="flex justify-between text-[10px] text-gray-400">
          <span>CORES: {telemetry.cpuCores} THREADS</span>
          <span>UPTIME: {telemetry.uptimeHours}h</span>
        </div>
      </div>

      {/* 3. RAM Memory Panel */}
      <div className="glass-panel p-3 rounded-xl border border-cyan-500/25 space-y-2">
        <div className="flex items-center justify-between text-gray-300">
          <div className="flex items-center gap-1.5">
            <HardDrive className="w-4 h-4 text-cyan-400" />
            <span>MEMORY (RAM)</span>
          </div>
          <span className="font-bold text-cyan-300">{telemetry.ramPercent}%</span>
        </div>
        <div className="w-full h-1.5 bg-black/60 rounded-full overflow-hidden border border-cyan-950">
          <div
            className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400 transition-all duration-500"
            style={{ width: `${telemetry.ramPercent}%` }}
          />
        </div>
        <div className="flex justify-between text-[10px] text-gray-400">
          <span>USED: {telemetry.ramUsedGB} GB</span>
          <span>TOTAL: {telemetry.ramTotalGB} GB</span>
        </div>
      </div>

      {/* 4. Host Info */}
      <div className="glass-panel p-3 rounded-xl border border-cyan-500/25 space-y-1.5 text-[10px]">
        <div className="flex justify-between text-gray-400">
          <span>HOST NODE:</span>
          <span className="text-gray-200">{telemetry.hostname}</span>
        </div>
        <div className="flex justify-between text-gray-400">
          <span>PLATFORM:</span>
          <span className="text-cyan-300">{telemetry.platform}</span>
        </div>
        <div className="flex justify-between text-gray-400">
          <span>SECURITY:</span>
          <span className="text-emerald-400 flex items-center gap-1">
            <ShieldCheck className="w-3 h-3" />
            <span>DPAPI VAULT</span>
          </span>
        </div>
      </div>

      {/* 5. Fast Actuator Launcher */}
      <div className="glass-panel p-3 rounded-xl border border-cyan-500/25 space-y-2 flex-1">
        <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block border-b border-cyan-950 pb-1">
          ACTUATOR CONTROLS
        </span>
        <div className="grid grid-cols-2 gap-1.5">
          <button
            onClick={() => onQuickAction('open notepad')}
            className="p-2 rounded bg-black/40 hover:bg-cyan-950/60 border border-cyan-900/40 text-gray-300 hover:text-cyan-300 flex items-center gap-1.5 transition text-[10px]"
          >
            <FileText className="w-3.5 h-3.5 text-cyan-400" />
            <span>Notepad</span>
          </button>
          <button
            onClick={() => onQuickAction('open calc')}
            className="p-2 rounded bg-black/40 hover:bg-cyan-950/60 border border-cyan-900/40 text-gray-300 hover:text-cyan-300 flex items-center gap-1.5 transition text-[10px]"
          >
            <Calculator className="w-3.5 h-3.5 text-cyan-400" />
            <span>Calculator</span>
          </button>
          <button
            onClick={() => onQuickAction('take a screenshot')}
            className="p-2 rounded bg-black/40 hover:bg-cyan-950/60 border border-cyan-900/40 text-gray-300 hover:text-cyan-300 flex items-center gap-1.5 transition text-[10px]"
          >
            <Camera className="w-3.5 h-3.5 text-cyan-400" />
            <span>Screenshot</span>
          </button>
          <button
            onClick={() => onQuickAction('open cmd')}
            className="p-2 rounded bg-black/40 hover:bg-cyan-950/60 border border-cyan-900/40 text-gray-300 hover:text-cyan-300 flex items-center gap-1.5 transition text-[10px]"
          >
            <Terminal className="w-3.5 h-3.5 text-cyan-400" />
            <span>Terminal</span>
          </button>
        </div>
      </div>
    </div>
  );
};
