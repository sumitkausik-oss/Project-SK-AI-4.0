import React, { useState, useEffect } from 'react';
import { Key, Shield, ShieldCheck, Eye, EyeOff, Save, CheckCircle2, XCircle, Info, Sparkles } from 'lucide-react';
import { PermissionPolicy } from '../types/electron';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onKeyUpdated: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose, onKeyUpdated }) => {
  const [googleKey, setGoogleKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [validating, setValidating] = useState(false);
  const [validationResult, setValidationResult] = useState<{ valid: boolean; message: string } | null>(null);
  const [policy, setPolicy] = useState<PermissionPolicy | null>(null);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadSettings();
    }
  }, [isOpen]);

  const loadSettings = async () => {
    try {
      const key = await window.skaiApi.getApiKey('google');
      setGoogleKey(key);
      const p = await window.skaiApi.permissions.getPolicy();
      setPolicy(p);
    } catch (err) {
      console.error('Failed to load settings:', err);
    }
  };

  const handleSaveKey = async () => {
    try {
      await window.skaiApi.setApiKey('google', googleKey);
      setSaveMsg('✅ Google API key securely encrypted & saved (DPAPI).');
      onKeyUpdated();
      setTimeout(() => setSaveMsg(null), 4000);
    } catch (err: any) {
      setSaveMsg(`❌ Failed to save key: ${err.message}`);
    }
  };

  const handleValidateKey = async () => {
    if (!googleKey.trim()) return;
    setValidating(true);
    setValidationResult(null);
    try {
      const res = await window.skaiApi.validateGoogleKey(googleKey);
      setValidationResult(res);
    } catch (err: any) {
      setValidationResult({ valid: false, message: err.message });
    } finally {
      setValidating(false);
    }
  };

  const handleTogglePolicy = async (field: keyof PermissionPolicy) => {
    if (!policy) return;
    const updated = { ...policy, [field]: !policy[field] };
    setPolicy(updated);
    await window.skaiApi.permissions.savePolicy(updated);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 p-4">
      <div className="glass-panel w-[680px] max-h-[90vh] rounded-2xl flex flex-col overflow-hidden border-indigo-500/40 shadow-[0_0_40px_rgba(99,102,241,0.25)]">
        {/* Header */}
        <div className="p-4 border-b border-indigo-950/80 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-indigo-400" />
            <h2 className="font-bold text-base text-indigo-200">SKAI Settings & Security Vault</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-sm font-bold">✕</button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
          {/* Section 1: Secrets & SafeStorage Key Management */}
          <div className="bg-black/50 p-3.5 rounded-xl border border-indigo-950/80 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-indigo-300 flex items-center gap-1.5">
                <Key className="w-4 h-4 text-indigo-400" />
                <span>GOOGLE API KEY (ENCRYPTED AT REST)</span>
              </span>
              <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
                <ShieldCheck className="w-3 h-3" />
                <span>Electron SafeStorage (OS DPAPI)</span>
              </span>
            </div>

            <p className="text-[11px] text-gray-400">
              Your API key is never saved in plaintext. It is encrypted directly using your operating system's cryptographic master key.
            </p>

            <div className="flex gap-2">
              <div className="relative flex-1">
                <input
                  type={showKey ? 'text' : 'password'}
                  value={googleKey}
                  onChange={(e) => setGoogleKey(e.target.value)}
                  placeholder="Paste your Google API key (AIzaSy...)"
                  className="w-full bg-black/80 border border-indigo-900/80 rounded px-3 py-2 text-white font-mono text-xs focus:border-indigo-400 focus:outline-none pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowKey(!showKey)}
                  className="absolute right-2.5 top-2.5 text-gray-400 hover:text-white"
                >
                  {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              <button
                onClick={handleValidateKey}
                disabled={validating || !googleKey.trim()}
                className="px-3.5 py-2 bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-500/40 text-indigo-300 font-bold rounded flex items-center gap-1 transition"
              >
                {validating ? 'Testing...' : 'Test Key'}
              </button>

              <button
                onClick={handleSaveKey}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded flex items-center gap-1.5 transition shadow"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Key</span>
              </button>
            </div>

            {validationResult && (
              <div
                className={`p-2 rounded-lg text-[11px] font-mono flex items-center gap-1.5 ${
                  validationResult.valid
                    ? 'bg-emerald-950/60 border border-emerald-500/40 text-emerald-300'
                    : 'bg-rose-950/60 border border-rose-500/40 text-rose-300'
                }`}
              >
                {validationResult.valid ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                <span>{validationResult.message}</span>
              </div>
            )}

            {saveMsg && (
              <div className="p-2 rounded-lg bg-indigo-950/60 border border-indigo-500/40 text-indigo-200 text-[11px] font-mono">
                {saveMsg}
              </div>
            )}
          </div>

          {/* Section 2: Safety & Permission Gatekeeper */}
          {policy && (
            <div className="bg-black/50 p-3.5 rounded-xl border border-indigo-950/80 space-y-3">
              <span className="font-mono font-bold text-indigo-300 flex items-center gap-1.5">
                <Shield className="w-4 h-4 text-indigo-400" />
                <span>SAFETY CONFIRMATION GATES</span>
              </span>

              <div className="space-y-2 text-xs">
                <label className="flex items-center justify-between p-2 rounded bg-black/40 border border-indigo-950 hover:border-indigo-900 cursor-pointer">
                  <div>
                    <span className="text-white font-bold block">Require Confirmation for Destructive Actions</span>
                    <span className="text-[10px] text-gray-400">Prompts user before deleting files, folders, or closing apps.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.require_confirmation_for_destructive}
                    onChange={() => handleTogglePolicy('require_confirmation_for_destructive')}
                    className="w-4 h-4 accent-indigo-500 cursor-pointer"
                  />
                </label>

                <label className="flex items-center justify-between p-2 rounded bg-black/40 border border-indigo-950 hover:border-indigo-900 cursor-pointer">
                  <div>
                    <span className="text-white font-bold block">Require Confirmation for Terminal Commands</span>
                    <span className="text-[10px] text-gray-400">Prompts user before executing PowerShell/CMD commands.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.require_confirmation_for_terminal}
                    onChange={() => handleTogglePolicy('require_confirmation_for_terminal')}
                    className="w-4 h-4 accent-indigo-500 cursor-pointer"
                  />
                </label>

                <label className="flex items-center justify-between p-2 rounded bg-black/40 border border-indigo-950 hover:border-indigo-900 cursor-pointer">
                  <div>
                    <span className="text-white font-bold block">Web Search & Awareness Add-on</span>
                    <span className="text-[10px] text-gray-400">Allows assistant to query online search engines when explicitly requested.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.web_tools_enabled}
                    onChange={() => handleTogglePolicy('web_tools_enabled')}
                    className="w-4 h-4 accent-indigo-500 cursor-pointer"
                  />
                </label>
              </div>
            </div>
          )}

          {/* Section 3: About SKAI Card */}
          <div className="bg-black/50 p-3.5 rounded-xl border border-indigo-950/80 space-y-2">
            <div className="flex items-center gap-1.5 text-indigo-300 font-mono font-bold">
              <Info className="w-4 h-4 text-indigo-400" />
              <span>ABOUT SKAI</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px] font-sans text-gray-300">
              <p><span className="text-gray-500 font-mono">Product:</span> <strong className="text-white">SKAI</strong></p>
              <p><span className="text-gray-500 font-mono">Tagline:</span> <span className="text-indigo-300">Powered by SK Enterprises</span></p>
              <p><span className="text-gray-500 font-mono">Founder & Architect:</span> <strong className="text-white">Sumeet Kumar</strong></p>
              <p><span className="text-gray-500 font-mono">Version:</span> <span className="text-emerald-400 font-mono">v0.0.1</span></p>
              <p><span className="text-gray-500 font-mono">Company:</span> <span className="text-white">SK Enterprises</span></p>
              <p><span className="text-gray-500 font-mono">License:</span> <span className="text-gray-300">MIT Open Core License</span></p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-indigo-950/80 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-lg transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
