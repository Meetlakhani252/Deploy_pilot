import React from 'react';
import { Check, X, ShieldAlert } from 'lucide-react';

export const ApprovalsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Pending Approvals</h1>
        <p className="text-sm text-slate-400 mt-1">Human-in-the-loop gates for high-impact AI autonomous actions.</p>
      </div>

      <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20 uppercase">
              Action: Rollback
            </span>
            <h2 className="text-base font-semibold text-white mt-2">Rollback sample-target-app to previous stable release</h2>
            <p className="text-xs text-slate-400 mt-1">Requested by AI Agent via Incident INC-109</p>
          </div>
          <span className="text-xs text-slate-500 font-mono">Expires in 28m</span>
        </div>

        <div className="flex items-center justify-between pt-3 border-t border-slate-800">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <ShieldAlert className="h-4 w-4 text-amber-400" />
            <span>Target: container <span className="font-mono text-slate-300">sample-target-app:v0.9.8</span></span>
          </div>

          <div className="flex items-center gap-3">
            <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition-colors">
              <X className="h-3.5 w-3.5" /> Reject
            </button>
            <button className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium shadow-sm transition-colors">
              <Check className="h-3.5 w-3.5" /> Approve & Execute
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
