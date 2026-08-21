import React, { useState } from 'react';
import { FolderCode, FileText, Play, Edit3, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';

export const CodingHelper: React.FC = () => {
  const [projectPath, setProjectPath] = useState('.');
  const [files, setFiles] = useState<any[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [targetSnippet, setTargetSnippet] = useState<string>('');
  const [replacementSnippet, setReplacementSnippet] = useState<string>('');
  const [testOutput, setTestOutput] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const loadProject = async () => {
    setLoading(true);
    setStatusMsg(null);
    try {
      const res = await window.skaiApi.code.readProject(projectPath);
      if (res.success && res.files) {
        setFiles(res.files);
        setStatusMsg(`Loaded ${res.count} project items.`);
      } else {
        setStatusMsg(`Failed: ${res.error}`);
      }
    } catch (err: any) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const loadFile = async (filePath: string) => {
    setSelectedFile(filePath);
    try {
      const res = await window.skaiApi.os.readFile(filePath);
      if (res.success && res.content !== undefined) {
        setFileContent(res.content);
      } else {
        setFileContent(`[Error reading file: ${res.error}]`);
      }
    } catch (err: any) {
      setFileContent(`[Error: ${err.message}]`);
    }
  };

  const applySurgicalEdit = async () => {
    if (!selectedFile || !targetSnippet) return;
    try {
      const res = await window.skaiApi.code.editFile(selectedFile, targetSnippet, replacementSnippet);
      if (res.success) {
        setStatusMsg('✅ Code edit applied successfully.');
        loadFile(selectedFile);
        setTargetSnippet('');
        setReplacementSnippet('');
      } else {
        setStatusMsg(`❌ Edit failed: ${res.error}`);
      }
    } catch (err: any) {
      setStatusMsg(`❌ Edit error: ${err.message}`);
    }
  };

  const runTests = async () => {
    setLoading(true);
    setTestOutput('Running tests...\n');
    try {
      const res = await window.skaiApi.code.runTests(projectPath, 'npm test');
      setTestOutput(res.stdout || res.stderr || res.error || 'Test run complete.');
    } catch (err: any) {
      setTestOutput(`Error running tests: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden p-3 gap-3">
      {/* Top Project Selector & Actions */}
      <div className="glass-panel p-2.5 rounded-xl flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-1">
          <FolderCode className="w-4 h-4 text-indigo-400" />
          <input
            type="text"
            value={projectPath}
            onChange={(e) => setProjectPath(e.target.value)}
            placeholder="Project Directory Path (e.g. . or D:\Project)"
            className="flex-1 bg-black/50 border border-indigo-900/60 rounded px-2.5 py-1.5 text-white font-mono text-xs focus:border-indigo-400 focus:outline-none"
          />
          <button
            onClick={loadProject}
            disabled={loading}
            className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded flex items-center gap-1.5 transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Scan Project</span>
          </button>
        </div>

        <button
          onClick={runTests}
          disabled={loading}
          className="px-3.5 py-1.5 bg-emerald-600/80 hover:bg-emerald-500 text-white font-bold rounded flex items-center gap-1.5 transition"
        >
          <Play className="w-3.5 h-3.5" />
          <span>Run Tests</span>
        </button>
      </div>

      {statusMsg && (
        <div className="text-xs px-3 py-1.5 rounded-lg bg-indigo-950/60 border border-indigo-500/40 text-indigo-300 font-mono">
          {statusMsg}
        </div>
      )}

      {/* Main Grid: File Tree + Code Editor/Viewer + Surgical Edit */}
      <div className="flex-1 grid grid-cols-12 gap-3 overflow-hidden">
        {/* Left: File Tree */}
        <div className="col-span-4 glass-panel rounded-xl p-2.5 flex flex-col overflow-hidden">
          <span className="text-[11px] font-mono font-bold text-indigo-300 mb-2 border-b border-indigo-900/60 pb-1 flex items-center gap-1">
            <FileText className="w-3.5 h-3.5 text-indigo-400" />
            <span>PROJECT FILES ({files.length})</span>
          </span>
          <div className="flex-1 overflow-y-auto space-y-1 font-mono text-xs pr-1">
            {files.length === 0 ? (
              <p className="text-gray-500 text-center py-6">Scan project to list files.</p>
            ) : (
              files.map((f, idx) => (
                <button
                  key={idx}
                  onClick={() => !f.isDirectory && loadFile(f.path)}
                  className={`w-full text-left px-2 py-1 rounded truncate flex items-center gap-1.5 transition ${
                    selectedFile === f.path
                      ? 'bg-indigo-600/40 text-indigo-200 border border-indigo-500/50'
                      : f.isDirectory
                      ? 'text-gray-400 hover:bg-white/5'
                      : 'text-gray-300 hover:bg-indigo-950/40'
                  }`}
                >
                  <span className="text-[10px] text-gray-500">{f.isDirectory ? '📁' : '📄'}</span>
                  <span className="truncate">{f.relPath || f.name}</span>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Right: Code Viewer & Surgical Editor */}
        <div className="col-span-8 flex flex-col gap-3 overflow-hidden">
          {/* File Content Preview */}
          <div className="flex-1 glass-panel rounded-xl p-2.5 flex flex-col overflow-hidden">
            <div className="flex items-center justify-between border-b border-indigo-900/60 pb-1 mb-1.5 text-xs font-mono">
              <span className="text-indigo-300 font-bold truncate">
                {selectedFile ? selectedFile : 'No file selected'}
              </span>
              <span className="text-[10px] text-gray-500">
                {fileContent ? `${fileContent.length} chars` : ''}
              </span>
            </div>
            <pre className="flex-1 overflow-y-auto bg-black/60 p-2.5 rounded-lg text-indigo-200 font-mono text-xs whitespace-pre-wrap">
              {fileContent || 'Select a file from the left to view its contents.'}
            </pre>
          </div>

          {/* Surgical Edit Panel */}
          <div className="h-44 glass-panel rounded-xl p-2.5 flex flex-col justify-between text-xs">
            <div className="flex items-center justify-between border-b border-indigo-900/60 pb-1">
              <span className="font-mono font-bold text-indigo-300 flex items-center gap-1">
                <Edit3 className="w-3.5 h-3.5 text-indigo-400" />
                <span>SURGICAL CODE EDIT</span>
              </span>
              <button
                onClick={applySurgicalEdit}
                disabled={!selectedFile || !targetSnippet}
                className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-bold rounded text-[11px] transition shadow"
              >
                Apply Edit
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2 mt-1.5 flex-1">
              <div className="flex flex-col">
                <span className="text-[10px] text-gray-400 font-mono mb-0.5">Target Exact Code to Replace:</span>
                <textarea
                  value={targetSnippet}
                  onChange={(e) => setTargetSnippet(e.target.value)}
                  placeholder="Paste existing code snippet..."
                  className="flex-1 bg-black/60 border border-indigo-900/60 rounded p-1.5 text-rose-300 font-mono text-[11px] resize-none focus:outline-none focus:border-indigo-400"
                />
              </div>

              <div className="flex flex-col">
                <span className="text-[10px] text-gray-400 font-mono mb-0.5">Replacement Code:</span>
                <textarea
                  value={replacementSnippet}
                  onChange={(e) => setReplacementSnippet(e.target.value)}
                  placeholder="Paste new replacement code..."
                  className="flex-1 bg-black/60 border border-indigo-900/60 rounded p-1.5 text-emerald-300 font-mono text-[11px] resize-none focus:outline-none focus:border-indigo-400"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Test Output Drawer */}
      {testOutput && (
        <div className="glass-panel p-2.5 rounded-xl max-h-32 overflow-y-auto text-xs font-mono bg-black/70 border-emerald-500/30">
          <div className="flex items-center justify-between border-b border-emerald-900/60 pb-1 mb-1 text-[11px] text-emerald-400 font-bold">
            <span>TEST RUN RESULTS:</span>
            <button onClick={() => setTestOutput('')} className="text-gray-400 hover:text-white">✕</button>
          </div>
          <pre className="text-gray-300 whitespace-pre-wrap">{testOutput}</pre>
        </div>
      )}
    </div>
  );
};
