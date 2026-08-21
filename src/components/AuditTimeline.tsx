import React, { useState, useEffect } from 'react';
import { History, Shield, AlertTriangle, Info, RefreshCw } from 'lucide-react';

export const AuditTimeline: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await window.skaiApi.audit.getLogs(60);
      setLogs(res);
    } catch (err) {
      console.error('Failed to load audit logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden p-3 gap-3">
      {/* Top Header */}
      <div className="glass-panel p-2.5 rounded-xl flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-indigo-400" />
          <span className="font-mono font-bold text-indigo-300">SYSTEM AUDIT TRAIL & ACTION TIMELINE</span>
        </div>
        <button
          onClick={fetchLogs}
          disabled={loading}
          className="px-3 py-1 bg-indigo-950/60 hover:bg-indigo-900 border border-indigo-500/30 text-indigo-300 rounded flex items-center gap-1.5 transition text-xs font-mono"
        >
          <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Logs Stream */}
      <div className="flex-1 overflow-y-auto pr-1 space-y-2 font-mono text-xs">
        {logs.length === 0 ? (
          <div className="glass-panel p-8 rounded-xl text-center text-gray-500 font-mono text-xs">
            <Shield className="w-8 h-8 text-indigo-400/40 mx-auto mb-2" />
            <p>No actions logged yet. Executed OS commands will appear here in real-time.</p>
          </div>
        ) : (
          logs.map((log) => {
            const isWarning = log.severity === 'WARNING';
            const isError = log.severity === 'ERROR';

            return (
              <div
                key={log.id}
                className={`glass-panel p-2.5 rounded-lg flex items-center justify-between gap-3 border ${
                  isError
                    ? 'border-rose-500/40 bg-rose-950/20'
                    : isWarning
                    ? 'border-amber-500/40 bg-amber-950/20'
                    : 'border-indigo-950/80 bg-black/40'
                }`}
              >
                <div className="flex items-center gap-2.5 truncate">
                  <span
                    className={`text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider border ${
                      isError
                        ? 'bg-rose-950 border-rose-500 text-rose-300'
                        : isWarning
                        ? 'bg-amber-950 border-amber-500 text-amber-300'
                        : 'bg-indigo-950 border-indigo-500/40 text-indigo-300'
                    }`}
                  >
                    {log.event_type}
                  </span>
                  <span className="text-gray-200 text-xs truncate">{log.description}</span>
                </div>
                <span className="text-[10px] text-gray-500 whitespace-nowrap">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
