import React from 'react';
import { AlertOctagon, Bot, ShieldAlert } from 'lucide-react';

export const IncidentsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Incidents & AI Root Cause</h1>
        <p className="text-sm text-slate-400 mt-1">Automated log evidence aggregation, failure classification, and remediation suggestions.</p>
      </div>

      <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg bg-red-500/10 text-red-400 border border-red-500/20 flex items-center justify-center">
              <AlertOctagon className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-white">INC-109: Health check timed out after 60s</h2>
              <p className="text-xs text-slate-400">Project: sample-target-app &bull; Opened: 15m ago</p>
            </div>
          </div>
          <span className="px-2.5 py-1 text-xs rounded bg-red-500/15 text-red-400 font-medium border border-red-500/30">
            OPEN
          </span>
        </div>

        {/* AI Analysis Card */}
        <div className="p-4 rounded-lg bg-slate-950/80 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-xs text-sky-400 font-medium">
            <Bot className="h-4 w-4" />
            <span>AI Root Cause Analysis (LangGraph + Gemini)</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            The target container raised an exit code 1 during startup due to missing environment variable <code className="bg-slate-900 px-1 py-0.5 rounded text-amber-300">PORT</code>. Container failed to bind socket within the 60s health window.
          </p>

          <div className="p-3 rounded bg-amber-500/10 border border-amber-500/20 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 text-amber-300">
              <ShieldAlert className="h-4 w-4" />
              <span>Proposed Action: Rollback to image tag <span className="font-mono font-semibold">sha-e909d38</span></span>
            </div>
            <span className="text-[11px] text-slate-400">Risk Level: LOW &bull; Confidence: 96%</span>
          </div>
        </div>
      </div>
    </div>
  );
};
