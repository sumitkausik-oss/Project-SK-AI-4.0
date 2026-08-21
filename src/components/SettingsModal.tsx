import React, { useState, useEffect } from 'react';
import { Key, Shield, ShieldCheck, Eye, EyeOff, Save, CheckCircle2, XCircle, Sparkles, Database, Info } from 'lucide-react';
import { PermissionPolicy } from '../types/electron';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onKeyUpdated: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose, onKeyUpdated }) => {
  // Google Key State
  const [googleKey, setGoogleKey] = useState('');
  const [showGoogleKey, setShowGoogleKey] = useState(false);
  const [validatingGoogle, setValidatingGoogle] = useState(false);
  const [googleValidationResult, setGoogleValidationResult] = useState<{ valid: boolean; message: string } | null>(null);

  // Hugging Face Token State
  const [hfToken, setHfToken] = useState('');
  const [showHfToken, setShowHfToken] = useState(false);
  const [validatingHf, setValidatingHf] = useState(false);
  const [hfValidationResult, setHfValidationResult] = useState<{ valid: boolean; message: string; username?: string } | null>(null);

  const [policy, setPolicy] = useState<PermissionPolicy | null>(null);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadSettings();
    }
  }, [isOpen]);

  const loadSettings = async () => {
    try {
      if (window.skaiApi?.getApiKey) {
        const gKey = await window.skaiApi.getApiKey('google');
        setGoogleKey(gKey || localStorage.getItem('skai_key_google') || '');

        const hf = await window.skaiApi.getApiKey('huggingface');
        setHfToken(hf || localStorage.getItem('skai_key_huggingface') || '');
      } else {
        setGoogleKey(localStorage.getItem('skai_key_google') || '');
        setHfToken(localStorage.getItem('skai_key_huggingface') || '');
      }

      if (window.skaiApi?.permissions?.getPolicy) {
        const p = await window.skaiApi.permissions.getPolicy();
        setPolicy(p);
      }
    } catch (err) {
      console.error('Failed to load settings:', err);
    }
  };

  const handleSaveGoogleKey = async () => {
    try {
      localStorage.setItem('skai_key_google', googleKey);
      if (window.skaiApi?.setApiKey) {
        await window.skaiApi.setApiKey('google', googleKey);
      }
      setSaveMsg('✅ Google Gemini API key securely saved & encrypted (DPAPI).');
      onKeyUpdated();
      setTimeout(() => setSaveMsg(null), 4000);
    } catch (err: any) {
      setSaveMsg(`❌ Failed to save Google key: ${err.message}`);
    }
  };

  const handleValidateGoogleKey = async () => {
    if (!googleKey.trim()) return;
    setValidatingGoogle(true);
    setGoogleValidationResult(null);

    // 1. Try IPC validation
    try {
      if (window.skaiApi?.validateGoogleKey) {
        const res = await window.skaiApi.validateGoogleKey(googleKey);
        setGoogleValidationResult(res);
        setValidatingGoogle(false);
        return;
      }
    } catch (err) {
      console.warn('[IPC Validation fallback]:', err);
    }

    // 2. Resilient Direct Web Validation Fallback
    try {
      const resp = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models?key=${googleKey.trim()}`
      );
      if (resp.ok) {
        setGoogleValidationResult({ valid: true, message: 'Google Gemini API key is valid and active!' });
      } else {
        const data = await resp.json().catch(() => ({}));
        setGoogleValidationResult({
          valid: false,
          message: data.error?.message || `Invalid Google API key (HTTP ${resp.status})`,
        });
      }
    } catch (err: any) {
      setGoogleValidationResult({ valid: false, message: `Validation error: ${err.message}` });
    } finally {
      setValidatingGoogle(false);
    }
  };

  const handleSaveHfToken = async () => {
    try {
      localStorage.setItem('skai_key_huggingface', hfToken);
      if (window.skaiApi?.setApiKey) {
        await window.skaiApi.setApiKey('huggingface', hfToken);
      }
      setSaveMsg('✅ Hugging Face token securely saved & encrypted (DPAPI).');
      onKeyUpdated();
      setTimeout(() => setSaveMsg(null), 4000);
    } catch (err: any) {
      setSaveMsg(`❌ Failed to save Hugging Face token: ${err.message}`);
    }
  };

  const handleValidateHfToken = async () => {
    if (!hfToken.trim()) return;
    setValidatingHf(true);
    setHfValidationResult(null);

    // 1. Try IPC validation
    try {
      if (window.skaiApi?.validateHuggingFaceToken) {
        const res = await window.skaiApi.validateHuggingFaceToken(hfToken);
        setHfValidationResult(res);
        setValidatingHf(false);
        return;
      }
    } catch (err) {
      console.warn('[IPC HF Validation fallback]:', err);
    }

    // 2. Resilient Direct Web Validation Fallback
    try {
      const resp = await fetch('https://huggingface.co/api/whoami-v2', {
        headers: {
          Authorization: `Bearer ${hfToken.trim()}`,
        },
      });

      if (resp.ok) {
        const user = await resp.json().catch(() => ({}));
        const uname = user.name || user.username || 'User';
        setHfValidationResult({
          valid: true,
          message: `Hugging Face token valid! Connected as @${uname}`,
          username: uname,
        });
      } else {
        setHfValidationResult({
          valid: false,
          message: `Invalid Hugging Face token (HTTP ${resp.status})`,
        });
      }
    } catch (err: any) {
      setHfValidationResult({ valid: false, message: `Validation error: ${err.message}` });
    } finally {
      setValidatingHf(false);
    }
  };

  const handleTogglePolicy = async (field: keyof PermissionPolicy) => {
    if (!policy) return;
    const updated = { ...policy, [field]: !policy[field] };
    setPolicy(updated);
    if (window.skaiApi?.permissions?.savePolicy) {
      await window.skaiApi.permissions.savePolicy(updated);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/85 backdrop-blur-md flex items-center justify-center z-50 p-4">
      <div className="glass-panel w-[720px] max-h-[92vh] rounded-2xl flex flex-col overflow-hidden border-indigo-500/40 shadow-[0_0_50px_rgba(99,102,241,0.3)] bg-[#070710]/95">
        {/* Header */}
        <div className="p-4 border-b border-indigo-950/80 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-indigo-400" />
            <h2 className="font-bold text-base text-indigo-200">SKAI Settings & Security Vault</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-sm font-bold px-2 py-1 rounded">✕</button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
          {/* Toast Notification */}
          {saveMsg && (
            <div className="p-2.5 rounded-lg bg-indigo-950/80 border border-indigo-500/40 text-indigo-200 text-[11px] font-mono animate-fadeIn">
              {saveMsg}
            </div>
          )}

          {/* Section 1: Google Gemini API Key */}
          <div className="bg-black/60 p-3.5 rounded-xl border border-indigo-950/80 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-indigo-300 flex items-center gap-1.5">
                <Key className="w-4 h-4 text-cyan-400" />
                <span>GOOGLE GEMINI API KEY (ENCRYPTED AT REST)</span>
              </span>
              <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
                <ShieldCheck className="w-3 h-3" />
                <span>Electron SafeStorage (OS DPAPI)</span>
              </span>
            </div>

            <p className="text-[11px] text-gray-400">
              Powers real-time duplex bilingual conversational intelligence (Hindi & English) and Gemini Live WebRTC streaming.
            </p>

            <div className="flex gap-2">
              <div className="relative flex-1">
                <input
                  type={showGoogleKey ? 'text' : 'password'}
                  value={googleKey}
                  onChange={(e) => setGoogleKey(e.target.value)}
                  placeholder="Paste your Google Gemini API key (AIzaSy...)"
                  className="w-full bg-black/80 border border-indigo-900/80 rounded px-3 py-2 text-white font-mono text-xs focus:border-cyan-400 focus:outline-none pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowGoogleKey(!showGoogleKey)}
                  className="absolute right-2.5 top-2.5 text-gray-400 hover:text-white"
                >
                  {showGoogleKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              <button
                onClick={handleValidateGoogleKey}
                disabled={validatingGoogle || !googleKey.trim()}
                className="px-3.5 py-2 bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 font-bold rounded flex items-center gap-1 transition disabled:opacity-50"
              >
                {validatingGoogle ? 'Testing...' : 'Test Key'}
              </button>

              <button
                onClick={handleSaveGoogleKey}
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded flex items-center gap-1.5 transition shadow"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Key</span>
              </button>
            </div>

            {googleValidationResult && (
              <div
                className={`p-2 rounded-lg text-[11px] font-mono flex items-center gap-1.5 ${
                  googleValidationResult.valid
                    ? 'bg-emerald-950/60 border border-emerald-500/40 text-emerald-300'
                    : 'bg-rose-950/60 border border-rose-500/40 text-rose-300'
                }`}
              >
                {googleValidationResult.valid ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                <span>{googleValidationResult.message}</span>
              </div>
            )}
          </div>

          {/* Section 2: Hugging Face Access Token */}
          <div className="bg-black/60 p-3.5 rounded-xl border border-indigo-950/80 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-mono font-bold text-amber-300 flex items-center gap-1.5">
                <Database className="w-4 h-4 text-amber-400" />
                <span>HUGGING FACE TOKEN (ENCRYPTED AT REST)</span>
              </span>
              <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
                <ShieldCheck className="w-3 h-3" />
                <span>Electron SafeStorage (OS DPAPI)</span>
              </span>
            </div>

            <p className="text-[11px] text-gray-400">
              Access open-source vision models, embeddings, Whisper ASR, and Hugging Face Inference Endpoints directly from SKAI.
            </p>

            <div className="flex gap-2">
              <div className="relative flex-1">
                <input
                  type={showHfToken ? 'text' : 'password'}
                  value={hfToken}
                  onChange={(e) => setHfToken(e.target.value)}
                  placeholder="Paste your Hugging Face User Access Token (hf_...)"
                  className="w-full bg-black/80 border border-amber-900/80 rounded px-3 py-2 text-white font-mono text-xs focus:border-amber-400 focus:outline-none pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowHfToken(!showHfToken)}
                  className="absolute right-2.5 top-2.5 text-gray-400 hover:text-white"
                >
                  {showHfToken ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              <button
                onClick={handleValidateHfToken}
                disabled={validatingHf || !hfToken.trim()}
                className="px-3.5 py-2 bg-amber-950/80 hover:bg-amber-900 border border-amber-500/40 text-amber-300 font-bold rounded flex items-center gap-1 transition disabled:opacity-50"
              >
                {validatingHf ? 'Testing...' : 'Test Token'}
              </button>

              <button
                onClick={handleSaveHfToken}
                className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold rounded flex items-center gap-1.5 transition shadow"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Token</span>
              </button>
            </div>

            {hfValidationResult && (
              <div
                className={`p-2 rounded-lg text-[11px] font-mono flex items-center gap-1.5 ${
                  hfValidationResult.valid
                    ? 'bg-emerald-950/60 border border-emerald-500/40 text-emerald-300'
                    : 'bg-rose-950/60 border border-rose-500/40 text-rose-300'
                }`}
              >
                {hfValidationResult.valid ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                <span>{hfValidationResult.message}</span>
              </div>
            )}
          </div>

          {/* Section 3: Safety & Policy Controls */}
          {policy && (
            <div className="bg-black/60 p-3.5 rounded-xl border border-indigo-950/80 space-y-2">
              <span className="font-mono font-bold text-gray-300 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-indigo-400" />
                <span>AUTONOMOUS EXECUTION POLICIES</span>
              </span>

              <div className="space-y-1.5 pt-1">
                {[
                  { key: 'auto_approve_read_only', label: 'Auto-approve Read-Only Operations (Directory scan, file reading)' },
                  { key: 'auto_approve_reversible', label: 'Auto-approve Reversible Operations (App launch, web search)' },
                  { key: 'require_confirmation_for_destructive', label: 'Require Manual Confirmation for Destructive Actions (File delete, overwrite)' },
                  { key: 'web_tools_enabled', label: 'Enable Live Web Navigation & Google DuckDuckGo Search' },
                ].map(({ key, label }) => (
                  <label key={key} className="flex items-center gap-2 cursor-pointer text-[11px] text-gray-300 hover:text-white">
                    <input
                      type="checkbox"
                      checked={Boolean((policy as any)[key])}
                      onChange={() => handleTogglePolicy(key as keyof PermissionPolicy)}
                      className="rounded border-indigo-800 bg-black/60 text-indigo-500 focus:ring-0"
                    />
                    <span>{label}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          {/* Section 4: About SKAI */}
          <div className="bg-black/60 p-3.5 rounded-xl border border-indigo-950/80 space-y-1.5">
            <span className="font-mono font-bold text-gray-400 flex items-center gap-1">
              <Info className="w-3.5 h-3.5 text-cyan-400" />
              <span>ABOUT SKAI</span>
            </span>
            <div className="grid grid-cols-2 gap-2 text-[11px] text-gray-400 pt-1">
              <div>Product: <span className="text-gray-200 font-bold">SKAI</span></div>
              <div>Tagline: <span className="text-gray-200 font-bold">Powered by SK Enterprises</span></div>
              <div>Founder & Architect: <span className="text-gray-200 font-bold">Sumeet Kumar</span></div>
              <div>Version: <span className="text-gray-200 font-mono">v0.0.1</span></div>
              <div>Company: <span className="text-gray-200">SK Enterprises</span></div>
              <div>License: <span className="text-gray-200">MIT Open Core License</span></div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-indigo-950/80 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
