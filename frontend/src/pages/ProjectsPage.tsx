import React from 'react';
import { Plus, GitBranch, ExternalLink, Server } from 'lucide-react';

export const ProjectsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Projects</h1>
          <p className="text-sm text-slate-400 mt-1">Connected repositories and monitored deployment targets.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-sm font-medium transition-colors shadow-sm">
          <Plus className="h-4 w-4" />
          <span>New Project</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all">
          <div className="flex items-start justify-between">
            <h3 className="text-base font-semibold text-white">sample-target-app</h3>
            <span className="px-2 py-0.5 text-[11px] rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
              HEALTHY
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Sample microservice for deployment & rollback verification</p>

          <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-2 text-xs text-slate-400">
            <div className="flex items-center gap-2">
              <GitBranch className="h-3.5 w-3.5 text-slate-500" />
              <span>main &bull; Meetlakhani252/sample-target-app</span>
            </div>
            <div className="flex items-center gap-2">
              <Server className="h-3.5 w-3.5 text-slate-500" />
              <span>localhost:8080</span>
            </div>
          </div>

          <div className="mt-4 flex items-center justify-end">
            <button className="text-xs text-sky-400 hover:text-sky-300 flex items-center gap-1 font-medium">
              Manage Project <ExternalLink className="h-3 w-3" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
