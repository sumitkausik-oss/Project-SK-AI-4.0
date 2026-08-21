import React, { useState, useEffect } from 'react';
import { Brain, Plus, Trash2, Search, Tag, Sparkles } from 'lucide-react';
import { StoredMemory } from '../types/electron';

export const MemoryInspector: React.FC = () => {
  const [memories, setMemories] = useState<StoredMemory[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [newKey, setNewKey] = useState('');
  const [newContent, setNewContent] = useState('');
  const [newTags, setNewTags] = useState('');
  const [loading, setLoading] = useState(false);

  const loadMemories = async () => {
    setLoading(true);
    try {
      if (searchQuery.trim()) {
        const results = await window.skaiApi.memory.query(searchQuery);
        setMemories(results);
      } else {
        const results = await window.skaiApi.memory.list(50);
        setMemories(results);
      }
    } catch (err) {
      console.error('Failed to load memories:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMemories();
  }, [searchQuery]);

  const handleAddMemory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKey.trim() || !newContent.trim()) return;

    const tagList = newTags.split(',').map((t) => t.trim()).filter(Boolean);
    try {
      await window.skaiApi.memory.store(newKey, newContent, tagList);
      setNewKey('');
      setNewContent('');
      setNewTags('');
      loadMemories();
    } catch (err) {
      alert('Error storing memory: ' + err);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this memory fact?')) return;
    try {
      await window.skaiApi.memory.delete(id);
      loadMemories();
    } catch (err) {
      alert('Error deleting memory: ' + err);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden p-3 gap-3">
      {/* Top Search & Stats Bar */}
      <div className="glass-panel p-2.5 rounded-xl flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-1">
          <Search className="w-4 h-4 text-indigo-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search vector memories by keyword or semantic concept..."
            className="flex-1 bg-black/50 border border-indigo-900/60 rounded px-2.5 py-1.5 text-white font-sans text-xs focus:border-indigo-400 focus:outline-none"
          />
        </div>
        <div className="flex items-center gap-1.5 font-mono text-[11px] text-indigo-300">
          <Brain className="w-4 h-4 text-indigo-400" />
          <span>{memories.length} DURABLE FACTS STORED</span>
        </div>
      </div>

      {/* Add New Memory Card */}
      <form onSubmit={handleAddMemory} className="glass-panel p-3 rounded-xl flex flex-col gap-2 text-xs">
        <span className="font-mono font-bold text-indigo-300 flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>STORE DURABLE FACT (PERSISTS ACROSS SESSIONS)</span>
        </span>
        <div className="grid grid-cols-12 gap-2">
          <input
            type="text"
            value={newKey}
            onChange={(e) => setNewKey(e.target.value)}
            placeholder="Fact Key (e.g. Preferred Language)"
            className="col-span-3 bg-black/60 border border-indigo-900/60 rounded p-2 text-white font-sans text-xs focus:border-indigo-400 focus:outline-none"
          />
          <input
            type="text"
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            placeholder="Content (e.g. Sumeet Kumar prefers Python and TypeScript)"
            className="col-span-6 bg-black/60 border border-indigo-900/60 rounded p-2 text-white font-sans text-xs focus:border-indigo-400 focus:outline-none"
          />
          <input
            type="text"
            value={newTags}
            onChange={(e) => setNewTags(e.target.value)}
            placeholder="Tags (comma-separated)"
            className="col-span-2 bg-black/60 border border-indigo-900/60 rounded p-2 text-white font-sans text-xs focus:border-indigo-400 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!newKey.trim() || !newContent.trim()}
            className="col-span-1 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-bold rounded flex items-center justify-center gap-1 transition shadow"
          >
            <Plus className="w-4 h-4" />
            <span>Save</span>
          </button>
        </div>
      </form>

      {/* Memory Fact Cards Grid */}
      <div className="flex-1 overflow-y-auto pr-1 space-y-2.5">
        {memories.length === 0 ? (
          <div className="glass-panel p-8 rounded-xl text-center text-gray-500 font-mono text-xs">
            <Brain className="w-8 h-8 text-indigo-400/40 mx-auto mb-2" />
            <p>No durable facts stored yet. Add one above or tell SKAI *"remember that [fact]"* in voice chat!</p>
          </div>
        ) : (
          memories.map((mem) => (
            <div
              key={mem.id}
              className="glass-panel p-3 rounded-xl flex items-start justify-between gap-3 hover:border-indigo-500/50 transition"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-indigo-300 font-sans">{mem.key}</span>
                  <span className="text-[9px] bg-indigo-950/80 border border-indigo-800/60 text-indigo-400 px-1.5 py-0.2 rounded font-mono">
                    {mem.category || 'PREFERENCE'}
                  </span>
                </div>
                <p className="text-xs text-gray-200 leading-relaxed font-sans">{mem.content}</p>
                <div className="flex items-center gap-1.5 pt-1">
                  <Tag className="w-3 h-3 text-gray-500" />
                  {mem.tags &&
                    mem.tags.map((t, idx) => (
                      <span key={idx} className="text-[10px] bg-black/60 border border-gray-800 text-gray-400 px-1.5 py-0.2 rounded">
                        #{t}
                      </span>
                    ))}
                  <span className="text-[10px] text-gray-500 ml-auto font-mono">
                    Saved: {new Date(mem.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>

              <button
                onClick={() => handleDelete(mem.id)}
                className="p-1.5 text-gray-500 hover:text-rose-400 hover:bg-rose-950/40 rounded-lg transition"
                title="Delete Fact"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
