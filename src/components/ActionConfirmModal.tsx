import React from 'react';
import { AlertTriangle, Check, X, ShieldAlert } from 'lucide-react';
import { PendingAction } from '../types/electron';

interface ActionConfirmModalProps {
  action: PendingAction | null;
  onResolved: () => void;
}

export const ActionConfirmModal: React.FC<ActionConfirmModalProps> = ({ action, onResolved }) => {
  if (!action) return null;

  const handleDecision = async (approved: boolean) => {
    try {
      await window.skaiApi.permissions.confirmAction(action.action_id, approved);
      onResolved();
    } catch (err) {
      alert('Error confirming action: ' + err);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/85 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-in fade-in">
      <div className="glass-panel w-[520px] rounded-2xl p-5 border-amber-500/60 shadow-[0_0_40px_rgba(245,158,11,0.3)] space-y-4">
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-amber-900/60 pb-3">
          <div className="p-2 rounded-xl bg-amber-950/80 border border-amber-500/50 text-amber-400">
            <ShieldAlert className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h3 className="font-bold text-sm text-amber-300">Safety Gate Confirmation Required</h3>
            <p className="text-[11px] text-gray-400">High-impact / destructive operating system action</p>
          </div>
        </div>

        {/* Action Details Box */}
        <div className="bg-black/80 rounded-xl p-3.5 border border-amber-900/40 space-y-2 text-xs font-mono">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Action:</span>
            <span className="text-amber-300 font-bold">{action.action_type}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Action ID:</span>
            <span className="text-indigo-400">{action.action_id}</span>
          </div>
          <div>
            <span className="text-gray-400 block mb-1">Details:</span>
            <div className="p-2 rounded bg-black/90 text-gray-200 border border-gray-800 text-[11px] whitespace-pre-wrap">
              {action.description}
            </div>
          </div>
        </div>

        <p className="text-xs text-gray-300">
          Are you sure you want SKAI to execute this action on your computer?
        </p>

        {/* Footer Actions */}
        <div className="flex items-center justify-end gap-2 pt-2 border-t border-gray-800">
          <button
            onClick={() => handleDecision(false)}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white font-bold text-xs rounded-lg flex items-center gap-1.5 transition"
          >
            <X className="w-4 h-4" />
            <span>Reject (Cancel)</span>
          </button>
          <button
            onClick={() => handleDecision(true)}
            className="px-5 py-2 bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs rounded-lg flex items-center gap-1.5 shadow-[0_0_20px_rgba(245,158,11,0.4)] transition"
          >
            <Check className="w-4 h-4" />
            <span>Approve & Execute</span>
          </button>
        </div>
      </div>
    </div>
  );
};
