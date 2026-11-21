import React from 'react';
import { Save, Key } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">System Settings</h1>
        <p className="text-sm text-slate-400 mt-1">Configure AI LLM providers, notification preferences, and thresholds.</p>
      </div>

      <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-6">
        <div>
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <Key className="h-4 w-4 text-sky-400" />
            AI Provider Configuration
          </h2>
          <p className="text-xs text-slate-400 mt-1">Choose between cloud LLM providers (Gemini, OpenAI) or local Ollama.</p>
        </div>

        <div className="grid grid-cols-1 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">LLM Provider</label>
            <select className="w-full rounded-lg bg-slate-950 border border-slate-800 px-3.5 py-2 text-sm text-slate-200 focus:outline-none focus:border-sky-500">
              <option value="gemini">Google Gemini (Default)</option>
              <option value="openai">OpenAI</option>
              <option value="ollama">Ollama (Local)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Model Identifier</label>
            <input
              type="text"
              defaultValue="gemini-1.5-pro"
              className="w-full rounded-lg bg-slate-950 border border-slate-800 px-3.5 py-2 text-sm text-slate-200 focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 flex justify-end">
          <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-sm font-medium transition-colors">
            <Save className="h-4 w-4" />
            <span>Save Settings</span>
          </button>
        </div>
      </div>
    </div>
  );
};
