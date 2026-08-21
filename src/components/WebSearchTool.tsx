import React, { useState } from 'react';
import { Globe, Search, ExternalLink, RefreshCw } from 'lucide-react';
import { WebSearchResult } from '../types/electron';

export const WebSearchTool: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<WebSearchResult[]>([]);
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await window.skaiApi.search.web(query.trim());
      setResults(res.results || []);
      setSummary(res.summary || 'Search complete.');
    } catch (err: any) {
      setSummary(`Error searching the web: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden p-3 gap-3">
      {/* Search Input Card */}
      <form onSubmit={handleSearch} className="glass-panel p-3 rounded-xl flex flex-col gap-2 text-xs">
        <span className="font-mono font-bold text-indigo-300 flex items-center gap-1.5">
          <Globe className="w-4 h-4 text-indigo-400" />
          <span>WEB AWARENESS & SEARCH TOOL</span>
        </span>
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search online documentation, live news, or technical topics..."
            className="flex-1 bg-black/60 border border-indigo-900/60 rounded p-2.5 text-white font-sans text-xs focus:border-indigo-400 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="px-5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-bold rounded-lg flex items-center gap-1.5 transition shadow"
          >
            <Search className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Search</span>
          </button>
        </div>
      </form>

      {/* Results and Summary Panel */}
      <div className="flex-1 overflow-y-auto pr-1 space-y-3">
        {summary && (
          <div className="glass-panel p-3.5 rounded-xl space-y-2 border-indigo-500/40">
            <span className="text-[11px] font-mono font-bold text-indigo-300">SUMMARY & SYNTHESIS:</span>
            <p className="text-xs text-gray-200 leading-relaxed font-sans whitespace-pre-wrap">{summary}</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="space-y-2">
            <span className="text-[11px] font-mono font-bold text-gray-400">TOP SOURCES & ARTICLES:</span>
            {results.map((res, idx) => (
              <div
                key={idx}
                className="glass-panel p-3 rounded-xl space-y-1.5 hover:border-indigo-500/50 transition"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-indigo-300 font-sans">{res.title}</span>
                  {res.link && (
                    <a
                      href={res.link}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[11px] text-indigo-400 hover:text-indigo-200 flex items-center gap-1 font-mono"
                    >
                      <span>Visit</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
                <p className="text-xs text-gray-300 font-sans">{res.snippet}</p>
                {res.link && (
                  <span className="text-[10px] text-gray-500 font-mono block truncate">{res.link}</span>
                )}
              </div>
            ))}
          </div>
        )}

        {!summary && results.length === 0 && (
          <div className="glass-panel p-10 rounded-xl text-center text-gray-500 font-mono text-xs">
            <Globe className="w-8 h-8 text-indigo-400/40 mx-auto mb-2" />
            <p>Enter a query above to fetch online web intelligence.</p>
          </div>
        )}
      </div>
    </div>
  );
};
